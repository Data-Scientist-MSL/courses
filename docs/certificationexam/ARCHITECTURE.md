# CertificationExam System Architecture

## System Overview

### Purpose
CertificationExam is an intelligent, fair, and secure remote examination system that combines AI-powered proctoring, flexible rubric-based grading, and blockchain-verified digital certificates to enable trusted remote assessment and credentialing.

### Goals
- **Academic Integrity**: Ensure fair exams through multi-agent AI proctoring while respecting student privacy
- **Flexible Assessment**: Support diverse question types with automated, semi-automated, and manual grading
- **Professional Credentialing**: Issue verifiable, blockchain-backed certificates recognized by employers
- **Accessibility First**: WCAG 2.1 AA compliance with comprehensive accommodations
- **Privacy & Ethics**: Minimal data collection, transparent monitoring, human oversight for critical decisions
- **Seamless Integration**: Work cohesively with CoursesGTM, CoursePlayerApp, and external platforms

### Ethical Considerations
**Privacy First**:
- Face embeddings only (no raw images stored after verification)
- Time-limited recordings (auto-delete after 90 days)
- Encryption at rest and in transit
- Explicit student consent for monitoring

**Fairness & Bias Mitigation**:
- Regular audits for discriminatory patterns in AI proctoring
- Comprehensive accommodations for disabilities
- Human review required for critical violations
- Explainable AI (students can see why they were flagged)

**Proportionality**:
- Monitoring intensity matches exam stakes
- Low-stakes exams: minimal proctoring
- High-stakes exams: comprehensive monitoring with human oversight

---

## High-Level Architecture

### System Components Overview

```mermaid
graph TB
    subgraph "Student Interface"
        UI[Web UI - Streamlit/React]
        Camera[Webcam]
        Mic[Microphone]
        Screen[Screen Capture]
    end
    
    subgraph "Exam Engine"
        ExamOrch[Exam Orchestrator]
        Timer[Timer Service]
        QuestionBank[Question Bank]
        SubmissionHandler[Submission Handler]
    end
    
    subgraph "AI Proctoring System"
        ProcCoord[Proctoring Coordinator - LangGraph]
        Agent1[Identity Verification]
        Agent2[Attention Monitoring]
        Agent3[Environment Scanning]
        Agent4[Audio Analysis]
        Agent5[Screen Activity]
        Agent6[Behavior Pattern]
        Agent7[Integrity Verification]
        Agent8[Recording & Evidence]
    end
    
    subgraph "Assessment System"
        AutoGrader[Auto Grader]
        AIGrader[AI-Assisted Grader - OLLAMA]
        ManualQueue[Manual Grading Queue]
        RubricEngine[Rubric Engine]
    end
    
    subgraph "Certificate System"
        CertGen[Certificate Generator]
        TemplateEngine[Template Engine - ReportLab]
        Signer[Digital Signature Service]
        Blockchain[Blockchain Service - Web3.py]
        QRGen[QR Code Generator]
    end
    
    subgraph "Verification System"
        VerifyPortal[Public Verification Portal]
        VerifyAPI[Verification API]
        RevocationList[Revocation List]
    end
    
    subgraph "Data Layer"
        PostgreSQL[(PostgreSQL)]
        Redis[(Redis Cache)]
        S3[(S3 Storage)]
    end
    
    UI --> ExamOrch
    Camera --> ProcCoord
    Mic --> ProcCoord
    Screen --> ProcCoord
    
    ExamOrch --> QuestionBank
    ExamOrch --> Timer
    ExamOrch --> ProcCoord
    ExamOrch --> SubmissionHandler
    
    ProcCoord --> Agent1
    ProcCoord --> Agent2
    ProcCoord --> Agent3
    ProcCoord --> Agent4
    ProcCoord --> Agent5
    ProcCoord --> Agent6
    ProcCoord --> Agent7
    ProcCoord --> Agent8
    
    SubmissionHandler --> AutoGrader
    SubmissionHandler --> AIGrader
    SubmissionHandler --> ManualQueue
    AutoGrader --> RubricEngine
    AIGrader --> RubricEngine
    ManualQueue --> RubricEngine
    
    RubricEngine --> CertGen
    CertGen --> TemplateEngine
    CertGen --> Signer
    CertGen --> Blockchain
    CertGen --> QRGen
    
    CertGen --> VerifyPortal
    VerifyPortal --> VerifyAPI
    VerifyAPI --> RevocationList
    
    ExamOrch --> PostgreSQL
    ProcCoord --> Redis
    Agent8 --> S3
    RubricEngine --> PostgreSQL
    CertGen --> PostgreSQL
    VerifyPortal --> PostgreSQL
```

---

## Component Breakdown

### 1. Exam Engine

**Purpose**: Orchestrate exam delivery, timing, and submission

**Components**:
- **Exam Orchestrator**: Main controller coordinating all exam activities
  - Launch pre-exam checks (identity, environment)
  - Start/stop timer
  - Handle student navigation (previous/next question)
  - Trigger auto-save every 30 seconds
  - Process submission

- **Timer Service**: Manage time limits and warnings
  - Track total exam time
  - Per-question time limits (optional)
  - Grace period after expiration (e.g., 2 minutes)
  - Warnings at 10 min, 5 min, 1 min remaining
  - Auto-submit on hard deadline

- **Question Bank**: Store and retrieve questions
  - CRUD operations for questions
  - Question randomization (different order per student)
  - Question pools (random selection)
  - Question versioning
  - Media support (images, audio, video)

- **Submission Handler**: Process exam submissions
  - Validate answers
  - Timestamp submission
  - Route to appropriate grading pipeline
  - Generate submission receipt

**Technology Stack**:
- Python 3.10+ (FastAPI backend)
- PostgreSQL (persistent storage)
- Redis (session state, real-time data)

---

### 2. AI Proctoring System

**Purpose**: Monitor exam sessions for academic integrity violations

**Architecture**: 8 specialist agents coordinated by LangGraph

**Proctoring Coordinator (LangGraph)**:
- Orchestrates all 8 agents running in parallel
- Aggregates signals every 2-5 seconds
- Maintains shared state (student attention, risk score, incidents)
- Makes decisions (continue, warn, flag, terminate)
- Implements human-in-the-loop for critical violations

**State Management**:
```python
ProctoringState = {
    "session_id": str,
    "student_id": str,
    "exam_id": str,
    "start_time": datetime,
    "current_risk_score": float,  # 0-100
    "incidents": List[Incident],
    "warnings_issued": int,
    "face_verified": bool,
    "environment_verified": bool,
    "attention_level": str,  # "focused", "distracted", "absent"
    "agent_signals": Dict[str, AgentSignal],
}
```

**8 Specialist Agents**: See [PROCTORING_AGENTS.md](./PROCTORING_AGENTS.md) for detailed specifications.

**Technology Stack**:
- LangGraph (agent orchestration)
- MediaPipe, OpenCV (computer vision)
- face_recognition, DeepFace (face verification)
- Whisper, pyannote.audio (audio analysis)
- YOLO (object detection)
- scikit-learn (anomaly detection)
- Redis (real-time state)

---

### 3. Assessment System

**Purpose**: Grade exams using auto-grading, AI-assisted grading, and manual review

**Grading Pipeline**:

```mermaid
graph LR
    Submission[Submission Received] --> AutoGrade{Auto-gradable?}
    AutoGrade -->|MCQ, Coding| Instant[Instant Grading]
    AutoGrade -->|Essay, Project| AIAssist[AI-Assisted Grading]
    AutoGrade -->|Complex| Manual[Manual Queue]
    
    Instant --> Rubric[Rubric Engine]
    AIAssist --> HumanReview{Needs Review?}
    HumanReview -->|Yes| Manual
    HumanReview -->|No| Rubric
    Manual --> Grader[Human Grader]
    Grader --> Rubric
    
    Rubric --> FinalScore[Final Score]
    FinalScore --> Publish[Publish Results]
    Publish --> CertCheck{Passed?}
    CertCheck -->|Yes| Certificate[Generate Certificate]
    CertCheck -->|No| End[End]
```

**Auto Grader**:
- **MCQ**: Exact match against answer key
- **Coding**: Run unit tests, check output, performance analysis
- **Fill-in-blank**: Exact or fuzzy match
- **Short answer**: Pattern matching, keyword detection

**AI-Assisted Grader (OLLAMA)**:
- Essay evaluation against rubric criteria
- Suggests scores with explanations
- Plagiarism detection
- Human grader reviews and approves/adjusts

**Manual Grading Queue**:
- Projects, complex essays, subjective assessments
- Blind grading option (hide student identity)
- Multiple graders for high-stakes exams
- Grader calibration system

**Rubric Engine**:
- Parse YAML rubric definitions
- Calculate weighted scores
- Aggregate across multiple criteria
- Generate detailed feedback

**Technology Stack**:
- OLLAMA (AI grading)
- pytest, unittest (code execution sandboxes)
- pylint, flake8 (code quality)
- PostgreSQL (grading data)

---

### 4. Certificate Generator

**Purpose**: Create professional, verifiable digital certificates

**Components**:

**Template Engine**:
- Parse JSON template definitions
- Render certificates as PDFs (ReportLab)
- Support custom fonts, images, backgrounds
- Dynamic field substitution

**Digital Signature Service**:
- RSA-2048 or Ed25519 cryptographic signing
- Sign certificate hash
- Embed signature in PDF metadata
- Visual signature placement
- Multi-signer support (instructor, dean, CEO)

**QR Code Generator**:
- Generate QR with verification URL
- Embed certificate ID + checksum
- Configurable size and error correction

**Blockchain Service** (optional):
- Store certificate hash on Ethereum/Polygon
- Smart contract integration
- Return transaction hash
- Optional NFT minting

**Delivery**:
- Email with PDF attachment (SendGrid/SES)
- Student dashboard download
- LinkedIn integration
- Digital wallet (Apple/Google)

**Technology Stack**:
- ReportLab, Pillow (PDF/image generation)
- cryptography (digital signatures)
- qrcode (QR generation)
- Web3.py (blockchain)
- AWS S3/Cloudflare R2 (storage)

---

### 5. Verification Portal

**Purpose**: Public verification of certificate authenticity

**Features**:
- **Web Portal**: `https://gai-observe.online/verify`
  - Certificate ID lookup
  - QR code scan (camera or upload)
  - PDF upload (extract ID from metadata)

- **Verification API**: REST API for employers
  - API key authentication
  - Rate limiting (100 requests/hour)
  - Audit logging

- **Revocation System**:
  - Revoke certificates (academic dishonesty)
  - Public revocation list
  - Verification checks revocation status

**Technology Stack**:
- FastAPI (web portal and API)
- PostgreSQL (certificate registry)
- Redis (rate limiting, caching)

---

## Technology Stack Summary

### Backend
- **Python 3.10+**: Primary language
- **FastAPI**: Web framework
- **LangGraph**: Agent orchestration
- **OLLAMA**: AI grading

### Computer Vision & Audio
- **MediaPipe**: Face mesh, pose estimation
- **OpenCV**: Video processing
- **face_recognition**: Face verification
- **DeepFace**: Liveness detection
- **YOLO**: Object detection
- **Whisper**: Audio transcription
- **pyannote.audio**: Speaker diarization

### Document Generation
- **ReportLab**: PDF generation
- **Pillow**: Image processing
- **qrcode**: QR code generation

### Blockchain
- **Web3.py**: Ethereum/Polygon integration
- **ethers.js**: Frontend blockchain interaction

### Data Storage
- **PostgreSQL**: Primary database
  - Exam definitions
  - Student submissions
  - Grades
  - Certificates
- **Redis**: Real-time state
  - Proctoring state
  - Session data
  - Rate limiting
- **AWS S3 / Cloudflare R2**: Object storage
  - Proctoring recordings
  - Certificate PDFs
  - Media files

### Frontend
- **Streamlit**: Rapid prototyping UI
- **React**: Production UI (optional)
- **TailwindCSS**: Styling

### DevOps
- **Docker**: Containerization
- **Kubernetes**: Orchestration (for scale)
- **GitHub Actions**: CI/CD

---

## Data Flow Diagrams

### Student Exam Journey

```mermaid
sequenceDiagram
    participant S as Student
    participant UI as Exam UI
    participant EO as Exam Orchestrator
    participant PC as Proctoring Coordinator
    participant AG as Auto Grader
    participant MG as Manual Grader
    participant CG as Certificate Generator
    
    S->>UI: Launch Exam
    UI->>EO: Initialize Exam Session
    EO->>PC: Start Pre-Exam Checks
    PC->>S: Request Face Verification
    S->>PC: Provide Face + ID
    PC->>PC: Verify Identity
    PC->>S: Request Room Scan
    S->>PC: Show Environment (360°)
    PC->>PC: Scan Environment
    PC->>EO: Environment OK
    EO->>S: Start Exam (Timer Begins)
    
    loop During Exam
        S->>UI: Answer Questions
        UI->>EO: Auto-save Progress
        PC->>PC: Monitor (8 agents)
        PC->>S: Warning (if needed)
    end
    
    S->>UI: Submit Exam
    UI->>EO: Process Submission
    EO->>AG: Auto-grade (MCQ, Coding)
    AG->>EO: Instant Results
    EO->>MG: Queue (Essays, Projects)
    MG->>MG: Human Review
    MG->>EO: Manual Scores
    EO->>S: Publish Results
    
    alt Passed
        EO->>CG: Generate Certificate
        CG->>CG: Create PDF, Sign, Blockchain
        CG->>S: Deliver Certificate (Email, Portal)
    end
```

### Proctoring Workflow

```mermaid
graph TD
    Start[Exam Session Active] --> Monitor[Every 2-5 seconds]
    Monitor --> Parallel{Run 8 Agents in Parallel}
    
    Parallel --> A1[Identity Agent: Face Match?]
    Parallel --> A2[Attention Agent: Gaze OK?]
    Parallel --> A3[Environment Agent: Objects OK?]
    Parallel --> A4[Audio Agent: Voices?]
    Parallel --> A5[Screen Agent: Tab Switch?]
    Parallel --> A6[Behavior Agent: Anomalies?]
    Parallel --> A7[Integrity Agent: Calculate Risk]
    Parallel --> A8[Recording Agent: Log Events]
    
    A1 --> Aggregate[Aggregate Signals]
    A2 --> Aggregate
    A3 --> Aggregate
    A4 --> Aggregate
    A5 --> Aggregate
    A6 --> Aggregate
    A7 --> Aggregate
    A8 --> Aggregate
    
    Aggregate --> Risk{Risk Score?}
    Risk -->|0-30: Low| Continue[Continue Exam]
    Risk -->|30-60: Medium| Warn[Issue Warning]
    Risk -->|60-80: High| Flag[Flag for Review]
    Risk -->|80-100: Critical| Human{Human Review}
    
    Human -->|False Positive| Continue
    Human -->|Violation| Terminate[Terminate Exam]
    
    Continue --> Monitor
    Warn --> Monitor
    Flag --> Monitor
    Terminate --> End[Exam Ended]
```

### Grading Workflow

```mermaid
graph TD
    Submit[Submission Received] --> Parse[Parse Answers]
    Parse --> Route{Question Type?}
    
    Route -->|MCQ| MCQGrade[Exact Match]
    Route -->|Coding| CodeGrade[Run Tests]
    Route -->|Essay| EssayRoute{AI-Gradable?}
    Route -->|Short Answer| Pattern[Pattern Match]
    Route -->|File Upload| ManualQ[Manual Queue]
    
    MCQGrade --> Rubric[Apply Rubric]
    CodeGrade --> Rubric
    Pattern --> Rubric
    
    EssayRoute -->|Yes| OLLAMA[OLLAMA Evaluation]
    EssayRoute -->|No| ManualQ
    
    OLLAMA --> Confidence{Confidence?}
    Confidence -->|High| Rubric
    Confidence -->|Low| ManualQ
    
    ManualQ --> HumanGrader[Human Grader]
    HumanGrader --> Rubric
    
    Rubric --> Aggregate[Aggregate Scores]
    Aggregate --> Final[Final Score]
    Final --> Publish[Publish Results]
```

---

## Privacy & Ethics

### FERPA Compliance
- **Educational Records**: Exam submissions are educational records
- **Access Control**: Only authorized staff can access grades
- **Student Rights**: Students can view/export their data
- **Consent**: Students consent to proctoring before exam

### GDPR Considerations
- **Lawful Basis**: Contract (exam requirement) and consent (proctoring)
- **Data Minimization**: Collect only necessary data
- **Right to Erasure**: Delete data on request (after retention period)
- **Data Portability**: Export student data in standard format
- **Breach Notification**: Notify within 72 hours

### Data Retention Policies
- **Exam Submissions**: 3 years (academic record)
- **Proctoring Recordings**: 90 days (or until academic integrity case resolved)
- **Grades**: Permanent (transcript record)
- **Certificates**: Permanent (verification)
- **Audit Logs**: 1 year (compliance)

### Student Privacy Protections
- **Face Embeddings Only**: No raw face images stored after verification
- **Encrypted Storage**: AES-256 at rest, TLS 1.3 in transit
- **Access Logging**: All data access logged
- **No Permanent Surveillance**: Recordings deleted after retention period
- **Transparency**: Students know what's monitored and why

### Bias Mitigation in AI Proctoring
- **Diverse Training Data**: Face recognition trained on diverse datasets
- **Regular Audits**: Monthly bias testing (false positive rates by demographics)
- **Human Oversight**: Critical decisions require human review
- **Explainability**: Students can see why they were flagged
- **Appeals Process**: Students can appeal integrity violations
- **Accommodations**: Relaxed rules for disabilities

---

## Scalability & Performance

### System Capacity
- **Concurrent Exams**: 100+ simultaneous exam sessions
- **Students per Exam**: Up to 1,000 students per exam instance
- **Proctoring Latency**: < 5 seconds (signal to decision)
- **Grading Throughput**: 
  - MCQ: Instant (< 1 second)
  - Coding: < 30 seconds
  - Essays: 2-5 minutes (AI-assisted)
  - Manual: Dependent on grader availability

### Infrastructure
- **Load Balancing**: Distribute across multiple servers
- **Horizontal Scaling**: Add more workers for proctoring/grading
- **CDN**: Serve static assets (exam media) from CDN
- **Database Optimization**: Indexing, query optimization, read replicas
- **Caching**: Redis for frequently accessed data

### Monitoring & Alerting
- **Application Monitoring**: Prometheus, Grafana
- **Error Tracking**: Sentry
- **Performance Monitoring**: New Relic, DataDog
- **Uptime Monitoring**: PingDom, StatusCake
- **Alerts**: PagerDuty for critical issues

---

## Security Considerations

### Authentication & Authorization
- **Student Authentication**: OAuth 2.0, SSO integration
- **Role-Based Access Control (RBAC)**:
  - Student: Take exams, view own results
  - Grader: Access grading queue
  - Instructor: Create exams, view results
  - Admin: Full access

### Data Encryption
- **At Rest**: AES-256 (database, file storage)
- **In Transit**: TLS 1.3 (all network communication)
- **Key Management**: AWS KMS, Azure Key Vault

### Exam Security
- **Question Bank Protection**: Encrypted, access-logged
- **Answer Key Protection**: Encrypted, grader-only access
- **Session Tokens**: Short-lived, cryptographically secure
- **Browser Lockdown**: Optional (disable DevTools, right-click)

### Certificate Security
- **Digital Signatures**: RSA-2048 or Ed25519
- **Blockchain Immutability**: Certificate hashes on-chain
- **Revocation**: Public revocation list

---

## Future Enhancements

### Phase 2 Features
- **Adaptive Exams**: Questions adjust based on student performance
- **Live Proctoring**: Human proctors via video call (high-stakes exams)
- **Peer Review**: Students review each other's work
- **Exam Analytics**: Detailed analytics for instructors (question difficulty, discrimination index)
- **Mobile App**: Take exams on mobile devices

### Phase 3 Features
- **VR Exams**: Immersive exam environments (Meta Quest, Vision Pro)
- **Biometric Authentication**: Fingerprint, iris scan
- **Advanced AI Grading**: GPT-4/Claude for complex essays
- **Global Exam Centers**: Partner with physical test centers

---

## Conclusion

CertificationExam provides a comprehensive solution for remote examination and credentialing:
- ✅ **Secure**: AI proctoring + human oversight
- ✅ **Fair**: Bias mitigation + accommodations
- ✅ **Flexible**: Multiple question types + grading methods
- ✅ **Verifiable**: Blockchain-backed certificates
- ✅ **Compliant**: FERPA, GDPR, WCAG 2.1 AA
- ✅ **Integrated**: Works with CoursesGTM, CoursePlayerApp

This architecture enables trusted remote assessment at scale while respecting student privacy and maintaining academic integrity.
