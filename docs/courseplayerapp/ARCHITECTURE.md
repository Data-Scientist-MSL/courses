# CoursePlayerApp - System Architecture

## System Overview

### Purpose
CoursePlayerApp is a modern, adaptive learning experience platform that delivers personalized educational content based on user subscription tiers. Built with Streamlit, it provides an intuitive interface for accessing courses, watching videos, completing labs, and interacting with an AI tutor.

### User Experience Philosophy
- **Tier-Adaptive**: Content and features dynamically adjust based on user's subscription level (Basic/Intermediate/Advanced)
- **Progressive Disclosure**: Show available features prominently, preview locked features to encourage upgrades
- **Seamless Integration**: Smooth handoffs to SimulationPlayer (labs) and CertificationExam (assessments)
- **Learning-First**: Minimize friction in the learning journey, maximize engagement

---

## High-Level Architecture

### System Context Diagram

```mermaid
graph TB
    User[Student User]
    CPA[CoursePlayerApp<br/>Streamlit Web App]
    GTM[CoursesGTM API<br/>License & Content Management]
    SP[SimulationPlayer<br/>Interactive Labs]
    CE[CertificationExam<br/>Assessments & Certificates]
    LS[LemonSqueezy<br/>Payment Provider]
    OLLAMA[OLLAMA<br/>Local AI Service]
    Storage[Cloud Storage<br/>Cloudflare R2/AWS S3]
    
    User -->|Access via browser| CPA
    CPA -->|Validate license<br/>Fetch courses| GTM
    CPA -->|Launch labs| SP
    CPA -->|Launch exams| CE
    CPA -->|AI assistance| OLLAMA
    CPA -->|Stream/download videos<br/>Fetch slides| Storage
    GTM -->|Verify payment| LS
    SP -->|Report completion| CPA
    CE -->|Issue certificate| CPA
```

### Authentication & License Validation Flow

```mermaid
sequenceDiagram
    participant U as User
    participant CPA as CoursePlayerApp
    participant GTM as CoursesGTM API
    participant LS as LemonSqueezy
    
    U->>CPA: Enter license key
    CPA->>GTM: POST /api/v1/licenses/validate
    GTM->>LS: Verify license status
    LS-->>GTM: Active/Expired/Invalid
    GTM->>GTM: Determine tier from product_id
    GTM-->>CPA: JWT token + tier + user_id
    CPA->>CPA: Store session (token, tier, user_id)
    CPA-->>U: Redirect to Dashboard
    
    Note over CPA: All subsequent requests include JWT
    
    U->>CPA: Access course
    CPA->>GTM: GET /api/v1/courses/{course_id}/access
    GTM-->>CPA: Allowed/Denied + tier_requirements
    CPA->>CPA: Check feature_flags[tier]
    CPA-->>U: Show content or upgrade prompt
```

### Content Delivery Pipeline

```mermaid
flowchart LR
    subgraph "Content Sources"
        GTM_API[CoursesGTM API]
        R2[Cloudflare R2<br/>Video Storage]
    end
    
    subgraph "CoursePlayerApp"
        Auth[Authentication Layer]
        FG[Feature Gating Engine]
        VP[Video Player]
        SV[Slides Viewer]
        PT[Progress Tracker]
    end
    
    subgraph "User Experience"
        UI[Streamlit UI]
    end
    
    GTM_API -->|Course metadata| Auth
    Auth -->|Validated session| FG
    FG -->|Tier config| VP
    FG -->|Tier config| SV
    R2 -->|Video stream/download| VP
    GTM_API -->|Slides PDFs/PPTX| SV
    VP --> PT
    SV --> PT
    PT --> UI
    VP --> UI
    SV --> UI
```

### Feature Gating System

```mermaid
flowchart TD
    Request[User Action Request]
    Session{Session<br/>Valid?}
    GetTier[Retrieve Tier from Session]
    LoadFlags[Load feature_flags.json]
    CheckFeature{Feature<br/>Allowed?}
    Execute[Execute Action]
    ShowUpgrade[Show Upgrade Prompt]
    
    Request --> Session
    Session -->|No| Redirect[Redirect to Login]
    Session -->|Yes| GetTier
    GetTier --> LoadFlags
    LoadFlags --> CheckFeature
    CheckFeature -->|Yes| Execute
    CheckFeature -->|No| ShowUpgrade
    ShowUpgrade --> Display[Display with disabled UI]
```

### Integration Points

```mermaid
graph LR
    CPA[CoursePlayerApp]
    
    subgraph "External Systems"
        GTM[CoursesGTM<br/>:8000]
        SP[SimulationPlayer<br/>:8080]
        CE[CertificationExam<br/>:8090]
        OLLAMA[OLLAMA<br/>:11434]
    end
    
    CPA -->|REST API| GTM
    CPA -->|URL redirect + params| SP
    CPA -->|URL redirect + params| CE
    CPA -->|Python SDK| OLLAMA
    
    SP -.->|Webhook: lab completion| CPA
    CE -.->|Webhook: certificate issued| CPA
```

---

## Component Breakdown

### 1. Authentication System
**Responsibility**: Validate license keys and manage user sessions

**Components**:
- `auth.py`: License validation logic
- `session_manager.py`: JWT token handling
- Login page: Streamlit form for license entry

**Flow**:
1. User enters license key (format: `XXXX-XXXX-XXXX-XXXX`)
2. App sends to CoursesGTM `/api/v1/licenses/validate`
3. Receives JWT with claims: `user_id`, `tier`, `email`, `expiry`
4. Stores in `st.session_state` (secure, server-side)
5. All pages check `st.session_state["authenticated"]` before rendering

**Security**:
- JWT tokens signed with HS256
- 24-hour token expiry
- No password storage (license key validated per session)

### 2. Course Navigation
**Responsibility**: Display available courses and navigate to course content

**Components**:
- `course_catalog.py`: Fetch and filter courses from CoursesGTM
- `course_card.py`: Reusable course display component
- My Courses page: Grid/list view with search and filters

**Features**:
- Filter by category (AI, Data Science, Machine Learning)
- Filter by difficulty (Beginner, Intermediate, Advanced)
- Search by title/description
- Sort by: Recently accessed, Progress, Alphabetical
- Display progress bars and tier badges

### 3. Video Player (Adaptive)
**Responsibility**: Stream or download videos based on user tier

**Components**:
- `video_player.py`: Streamlit video component wrapper
- `video_downloader.py`: Generate signed download URLs
- Quality selector (for Advanced tier)

**Tier-Based Behavior**:

| Tier | Quality | Streaming | Download | Speed Control |
|------|---------|-----------|----------|---------------|
| Basic | 480p | ✅ | ❌ | ✅ |
| Intermediate | 720p | ✅ | ✅ | ✅ |
| Advanced | 1080p | ✅ | ✅ (+ quality selection) | ✅ |

**Additional Features**:
- Resume from last position (stored in progress DB)
- Playback speed: 0.5x, 1x, 1.25x, 1.5x, 2x
- Captions/subtitles (VTT format)
- Fullscreen mode
- Picture-in-picture (browser-dependent)

### 4. Slides Viewer/Exporter
**Responsibility**: Display course slides and enable export

**Components**:
- `slides_viewer.py`: PDF viewer using `streamlit-pdf-viewer`
- `slides_exporter.py`: Generate download links for slides

**Tier-Based Behavior**:

| Tier | View Slides | Export PDF | Export PPTX |
|------|-------------|------------|-------------|
| Basic | ✅ | ❌ | ❌ |
| Intermediate | ✅ | ✅ | ❌ |
| Advanced | ✅ | ✅ | ✅ |

**Features**:
- Navigate between slides (prev/next)
- Thumbnail view
- Search within slides
- Annotations (Advanced tier only)

### 5. Lab Launcher
**Responsibility**: Integrate with SimulationPlayer for hands-on practice

**Components**:
- `lab_launcher.py`: Generate SimulationPlayer URLs with params
- Lab listing page: Show available labs with completion status

**Integration Flow**:
```python
# Example: Launch lab
def launch_lab(course_id: str, lab_id: str, user_id: str, tier: str):
    # Check tier permissions
    if tier == "basic":
        return show_lab_preview()  # Read-only view
    
    # Generate launch URL
    callback_url = f"https://courseplayerapp.com/api/lab-complete"
    launch_url = f"https://simulationplayer.com/launch?course_id={course_id}&lab_id={lab_id}&user_id={user_id}&callback={callback_url}"
    
    # Open in new tab
    st.markdown(f'<a href="{launch_url}" target="_blank">🚀 Start Lab</a>', unsafe_allow_html=True)
```

**Tier-Based Behavior**:

| Tier | Lab Access | Code Execution | Save Progress |
|------|------------|----------------|---------------|
| Basic | Read-only (view code) | ❌ | ❌ |
| Intermediate | Interactive | ✅ | ✅ |
| Advanced | Full access | ✅ | ✅ |

### 6. AI Tutor (OLLAMA-powered)
**Responsibility**: Provide context-aware learning assistance

**Components**:
- `ai_tutor.py`: OLLAMA integration with quota management
- Chat interface: Streamlit chat UI in sidebar/dedicated tab
- `quota_tracker.py`: Track monthly usage per user

**Architecture**:
```python
class AITutor:
    def __init__(self, tier: str, user_id: str, course_context: dict):
        self.tier = tier
        self.user_id = user_id
        self.context = course_context  # {course_id, module_id, topic}
        self.quota = TIER_QUOTAS[tier]
        self.usage = db.get_monthly_usage(user_id)
    
    def ask(self, question: str) -> str:
        # Check quota
        if self.tier == "basic":
            return UPGRADE_MESSAGE_INTERMEDIATE
        
        if self.tier == "intermediate" and self.usage >= self.quota:
            return QUOTA_EXCEEDED_MESSAGE
        
        # Build context-aware prompt
        prompt = self._build_prompt(question)
        
        # Call OLLAMA (llama3.1:8b model)
        response = ollama.chat(model="llama3.1:8b", messages=[
            {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        
        # Increment usage
        if self.tier == "intermediate":
            db.increment_usage(self.user_id)
        
        return response['message']['content']
```

**Quota Limits**:
- Basic: 0 questions (feature disabled)
- Intermediate: 50 questions/month (resets 1st of each month)
- Advanced: Unlimited

### 7. Progress Tracker
**Responsibility**: Track and visualize learning progress

**Components**:
- `progress_tracker.py`: Update progress metrics
- `progress_visualizer.py`: Generate Plotly charts
- My Progress page: Dashboard with stats and charts

**Tracked Metrics**:
- Video completion percentage per module
- Slides viewed (yes/no per deck)
- Labs completed (score + completion status)
- Quiz scores (score/max_score, attempts)
- Time spent per course (total minutes)
- Overall course completion (0-100%)

**Storage Schema**:
```json
{
  "user_id": "uuid-v4",
  "course_id": "ai-03-nlp-transformers",
  "overall_progress": 67,
  "time_spent_minutes": 420,
  "last_accessed": "2026-01-15T14:30:00Z",
  "modules": [
    {
      "module_id": "module-01",
      "title": "Introduction to NLP",
      "progress": 100,
      "videos": [
        {
          "video_id": "v1-intro",
          "watched": true,
          "completion_percentage": 100,
          "last_position_seconds": 0,
          "time_spent_seconds": 1200
        }
      ],
      "slides": [
        {"slide_deck_id": "s1", "viewed": true, "viewed_at": "2026-01-10T10:00:00Z"}
      ],
      "labs": [
        {"lab_id": "lab1-tokenization", "completed": true, "score": 95, "completed_at": "2026-01-12T15:00:00Z"}
      ],
      "quiz": {
        "quiz_id": "q1",
        "score": 8,
        "max_score": 10,
        "attempts": 2,
        "last_attempt": "2026-01-13T09:00:00Z"
      }
    }
  ]
}
```

**Visualizations**:
- Progress bars (per course, per module)
- Time spent line chart (daily)
- Completion heatmap (calendar view)
- Quiz performance bar chart
- Achievement badges (unlocked at milestones)

### 8. Certificate Viewer
**Responsibility**: Display earned certificates and enable sharing

**Components**:
- `certificate_viewer.py`: Fetch and display certificates
- Certificate grid: Visual gallery of earned certificates
- Share functionality: LinkedIn, Twitter, copy verification link

**Certificate Data**:
```json
{
  "certificate_id": "cert-ai-03-nlp-2026-01-15",
  "user_id": "uuid-v4",
  "course_id": "ai-03-nlp-transformers",
  "course_title": "Natural Language Processing with Transformers",
  "issue_date": "2026-01-15",
  "verification_url": "https://certifications.gai-observe.com/verify/cert-ai-03-nlp-2026-01-15",
  "blockchain_hash": "0x1a2b3c..." // Advanced tier only
}
```

**Tier-Based Features**:

| Tier | Certificate Type | Blockchain Verification | Design |
|------|------------------|-------------------------|---------|
| Basic | Standard | ❌ | Basic template |
| Intermediate | Standard | ❌ | Standard template |
| Advanced | Premium | ✅ | Premium template |

---

## Technology Stack

### Frontend
- **Streamlit 1.30+**: Web framework for Python
  - Rapid prototyping
  - Built-in components (video, file upload, charts)
  - Session state management
  - Custom components via `streamlit-component-lib`

### Backend
- **Python 3.10+**: Core language
- **Requests**: HTTP client for CoursesGTM API
- **PyJWT**: JWT token validation
- **Pandas**: Data manipulation for progress analytics
- **Plotly**: Interactive visualizations
- **OLLAMA Python SDK**: AI tutor integration

### AI/ML
- **OLLAMA**: Local LLM inference
  - Model: `llama3.1:8b` (8 billion parameters)
  - Runs on CPU or GPU
  - No external API calls (privacy-preserving)

### Storage
- **Cloudflare R2 or AWS S3**: Video and slide storage
  - HLS streaming for videos
  - Signed URLs for downloads (expiry: 1 hour)

### Database (via CoursesGTM)
- **PostgreSQL**: User data, progress, licenses
- **Redis**: Session caching, quota tracking

### Deployment
- **Docker**: Containerized deployment
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Reverse proxy (SSL termination)

---

## Feature Gating Matrix

### Basic Tier ($97)
**Target Audience**: Casual learners, budget-conscious students

| Feature | Access | Notes |
|---------|--------|-------|
| Courses | 5 foundational | `ai-01`, `ai-02`, `ds-01`, `ds-02`, `ml-01` |
| Video | Stream only (480p) | No download |
| Slides | View only | No export |
| Labs | Read-only | View code, no execution |
| AI Tutor | ❌ Disabled | Upgrade prompt shown |
| Progress Tracking | Basic | Videos watched, course completion |
| Certificates | Standard | If earned |

### Intermediate Tier ($247)
**Target Audience**: Serious learners, professionals upskilling

| Feature | Access | Notes |
|---------|--------|-------|
| Courses | 8 courses | + `ai-03`, `ds-03`, `ml-02` |
| Video | Stream + download (720p) | MP4 download |
| Slides | View + export (PDF) | PDF download |
| Labs | Interactive | Full execution in SimulationPlayer |
| AI Tutor | ✅ Enabled (50 Q/month) | Quota resets monthly |
| Progress Tracking | Advanced | + time spent, quiz scores |
| Certificates | Standard | If earned |

### Advanced Tier ($497)
**Target Audience**: Power users, career-focused professionals

| Feature | Access | Notes |
|---------|--------|-------|
| Courses | All 9 courses | + `ai-04` (advanced topics) |
| Video | Stream + download (1080p) | Quality selector |
| Slides | View + export (PDF + PPTX) | Both formats |
| Labs | Full access | All simulations |
| AI Tutor | ✅ Unlimited | No quota |
| Progress Tracking | Detailed | + heatmaps, analytics |
| Certificates | Premium | Blockchain-verified |
| Support | Priority | 24-hour response SLA |

---

## Data Flow Diagrams

### Student Login → License Validation → Course Access

```mermaid
sequenceDiagram
    participant S as Student
    participant CPA as CoursePlayerApp
    participant GTM as CoursesGTM
    participant DB as Database
    
    S->>CPA: Navigate to app URL
    CPA->>CPA: Check session_state
    
    alt Not Authenticated
        CPA->>S: Show login page
        S->>CPA: Enter license key
        CPA->>GTM: POST /api/v1/licenses/validate
        GTM->>DB: Query license status
        DB-->>GTM: License data + tier
        GTM-->>CPA: JWT + user profile
        CPA->>CPA: Store in session_state
        CPA-->>S: Redirect to Dashboard
    else Already Authenticated
        CPA-->>S: Show Dashboard
    end
    
    S->>CPA: Click on course
    CPA->>CPA: Load feature_flags[tier]
    CPA->>GTM: GET /api/v1/courses/{course_id}/access
    GTM-->>CPA: Access granted/denied
    
    alt Access Granted
        CPA->>GTM: GET /api/v1/courses/{course_id}
        GTM-->>CPA: Course content metadata
        CPA-->>S: Show course player
    else Access Denied
        CPA-->>S: Show upgrade prompt
    end
```

### Video Playback Flow (Stream vs Download)

```mermaid
flowchart TD
    Start[User clicks video]
    CheckTier{Check Tier}
    Basic[Basic Tier]
    Inter[Intermediate Tier]
    Adv[Advanced Tier]
    
    Stream480[Stream 480p]
    Stream720[Stream 720p]
    Stream1080[Stream 1080p]
    
    DownloadOpt{Download Option?}
    Download720[Download 720p MP4]
    QualitySelect{Quality Selection}
    Download1080[Download 1080p MP4]
    Download720_2[Download 720p MP4]
    
    Start --> CheckTier
    CheckTier -->|basic| Basic
    CheckTier -->|intermediate| Inter
    CheckTier -->|advanced| Adv
    
    Basic --> Stream480
    
    Inter --> Stream720
    Stream720 --> DownloadOpt
    DownloadOpt -->|Yes| Download720
    DownloadOpt -->|No| Continue[Continue Streaming]
    
    Adv --> Stream1080
    Stream1080 --> QualitySelect
    QualitySelect -->|1080p| Download1080
    QualitySelect -->|720p| Download720_2
    QualitySelect -->|Stream only| Continue
```

### AI Tutor Interaction Flow

```mermaid
sequenceDiagram
    participant U as User
    participant CPA as CoursePlayerApp
    participant QT as Quota Tracker
    participant OLLAMA as OLLAMA Service
    participant DB as Database
    
    U->>CPA: Ask question in AI Tutor
    CPA->>CPA: Get tier from session
    
    alt Basic Tier
        CPA-->>U: "AI Tutor available in Intermediate tier ($247)"
    else Intermediate Tier
        CPA->>QT: Check monthly usage
        QT->>DB: SELECT usage WHERE user_id AND month
        DB-->>QT: Usage count (e.g., 45/50)
        QT-->>CPA: Remaining quota: 5
        
        alt Quota Remaining
            CPA->>OLLAMA: Send prompt with context
            OLLAMA-->>CPA: AI response
            CPA->>QT: Increment usage
            QT->>DB: UPDATE usage SET count = count + 1
            CPA-->>U: Display AI response (4 remaining)
        else Quota Exceeded
            CPA-->>U: "Monthly quota reached. Upgrade to Advanced for unlimited!"
        end
    else Advanced Tier
        CPA->>OLLAMA: Send prompt with context
        OLLAMA-->>CPA: AI response
        CPA-->>U: Display AI response (unlimited)
    end
```

### Lab Launch Flow

```mermaid
sequenceDiagram
    participant U as User
    participant CPA as CoursePlayerApp
    participant SP as SimulationPlayer
    participant DB as Progress Database
    
    U->>CPA: Click "Start Lab" button
    CPA->>CPA: Check tier permissions
    
    alt Basic Tier
        CPA-->>U: Show read-only lab preview (code view)
    else Intermediate/Advanced Tier
        CPA->>CPA: Generate launch URL with params
        Note over CPA: URL includes: course_id, lab_id, user_id, callback_url
        CPA->>SP: Open in new tab (redirect)
        SP->>SP: Load lab scenario
        SP-->>U: Interactive lab environment
        
        U->>SP: Complete lab exercises
        SP->>SP: Validate solutions
        SP->>CPA: POST /api/webhook/lab-complete
        Note over SP,CPA: Payload: {user_id, lab_id, score, completion_time}
        CPA->>DB: UPDATE progress SET lab_completed = true
        CPA-->>U: Show success notification
    end
```

---

## Security Considerations

### Authentication
- License keys are single-use tokens (validated on each session start)
- JWT tokens include `exp` claim (24-hour expiry)
- Tokens stored in `st.session_state` (server-side, not browser)
- No sensitive data in URL parameters

### Authorization
- Feature flags checked on every protected action
- Tier validation performed server-side (not just UI hiding)
- API calls to CoursesGTM include JWT in `Authorization` header

### Data Privacy
- OLLAMA runs locally (no data sent to external AI APIs)
- Video downloads use signed URLs (1-hour expiry)
- User progress encrypted at rest (in CoursesGTM database)

### Rate Limiting
- AI Tutor quota enforced at application layer
- API rate limits inherited from CoursesGTM (100 req/min per user)

---

## Scalability Considerations

### Horizontal Scaling
- Streamlit apps are stateless (session stored in database/Redis)
- Can run multiple CoursePlayerApp instances behind load balancer
- OLLAMA can be deployed as separate service (GPU instances)

### Caching Strategy
- Course metadata cached (TTL: 1 hour)
- Feature flags cached (TTL: 5 minutes)
- Video URLs pre-signed and cached (TTL: 50 minutes)

### Performance Optimization
- Lazy loading for course lists (pagination)
- Video streaming via CDN (Cloudflare R2)
- Plotly charts rendered client-side (reduce server load)

---

## Monitoring & Observability

### Metrics to Track
- User authentication success/failure rate
- Video playback errors (per quality level)
- AI Tutor response time
- Page load times
- Feature gate violations (attempted access to locked features)

### Logging
- Structured JSON logs (using Python `logging` module)
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Log aggregation via ELK stack or similar

### Alerting
- Alert on authentication failures >10% in 5 minutes
- Alert on AI Tutor errors >5% in 10 minutes
- Alert on video playback errors >5% in 5 minutes

---

## Future Enhancements

### Phase 2 Features
- Mobile app (React Native or Flutter)
- Offline mode (download courses for offline viewing)
- Peer discussion forums
- Live cohort-based learning

### Phase 3 Features
- Gamification (points, leaderboards, badges)
- AI-generated personalized learning paths
- Integration with corporate LMS (SCORM export)
- Multi-language support (i18n)

---

## Conclusion

This architecture provides a solid foundation for CoursePlayerApp, balancing:
- **User Experience**: Smooth, adaptive interface
- **Business Model**: Clear tier differentiation to drive upgrades
- **Technical Excellence**: Modern stack, scalable design
- **Security**: License-based authentication, feature gating
- **Extensibility**: Easy to add new features and integrations

The modular design allows for incremental development and testing, with clear integration points for external systems (CoursesGTM, SimulationPlayer, CertificationExam, OLLAMA).
