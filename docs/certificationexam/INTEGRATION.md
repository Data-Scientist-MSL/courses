# Integration Documentation

## Overview

CertificationExam integrates with the broader learning ecosystem and external services to provide a seamless end-to-end experience. This document details integration points with internal systems (CoursesGTM, CoursePlayerApp, etc.) and external platforms (LinkedIn, blockchain, payment processors, etc.).

---

## Internal Integrations

### Integration with CoursesGTM

**Purpose**: Manage course catalog, user tiers, licensing, and access control

#### Tier-Based Exam Access

```yaml
tier_integration:
  basic_tier:
    exam_access: "limited"
    features:
      proctoring: false
      auto_grading_only: true
      certificates: "basic_pdf"
      attempts: 3
  
  intermediate_tier:
    exam_access: "standard"
    features:
      proctoring: "standard"
      ai_assisted_grading: true
      certificates: "professional_pdf"
      blockchain_verification: false
      attempts: 2
  
  advanced_tier:
    exam_access: "full"
    features:
      proctoring: "strict"
      ai_assisted_grading: true
      manual_review: true
      certificates: "blockchain_verified"
      blockchain_verification: true
      priority_grading: true
      attempts: 1
  
  enterprise_tier:
    exam_access: "custom"
    features:
      proctoring: "configurable"
      custom_rubrics: true
      dedicated_grader: true
      certificates: "fully_customized"
      blockchain_verification: true
      api_access: true
      white_label: true
      attempts: "unlimited"
```

#### API Integration

```python
# Check student tier before allowing exam access
from coursesgtm import CoursesGTMClient

def check_exam_eligibility(student_id: str, exam_id: str) -> dict:
    """Check if student can access exam based on tier"""
    
    gtm_client = CoursesGTMClient(api_key=GTM_API_KEY)
    
    # Get student enrollment and tier
    enrollment = gtm_client.get_enrollment(student_id)
    
    if not enrollment:
        return {
            'eligible': False,
            'reason': 'Not enrolled in course'
        }
    
    # Get tier requirements for exam
    exam = db.query(Exam).filter_by(id=exam_id).first()
    required_tier = exam.minimum_tier
    
    student_tier = enrollment.tier
    tier_hierarchy = ['basic', 'intermediate', 'advanced', 'enterprise']
    
    if tier_hierarchy.index(student_tier) < tier_hierarchy.index(required_tier):
        return {
            'eligible': False,
            'reason': f'Requires {required_tier} tier. You have {student_tier}.',
            'upgrade_url': 'https://coursesgtm.com/upgrade'
        }
    
    return {
        'eligible': True,
        'tier': student_tier,
        'features': TIER_FEATURES[student_tier]
    }
```

#### Course Completion Tracking

```python
def sync_exam_completion_to_gtm(student_id: str, exam_id: str, result: dict):
    """Sync exam completion back to CoursesGTM"""
    
    gtm_client = CoursesGTMClient(api_key=GTM_API_KEY)
    
    gtm_client.update_progress(
        student_id=student_id,
        course_id=exam.course_id,
        activity_type='exam',
        activity_id=exam_id,
        status='completed',
        score=result['score'],
        passed=result['passed'],
        completed_at=datetime.utcnow()
    )
```

---

### Integration with CoursePlayerApp

**Purpose**: Launch exams from course interface, track progress, display achievements

#### Exam Launch from Course Page

```javascript
// CoursePlayerApp embeds exam launcher
<div class="course-section">
    <h3>📝 Final Exam</h3>
    <p>Complete the final exam to earn your certificate.</p>
    
    <button onclick="launchExam('exam_nlp_final_2026')">
        Start Final Exam
    </button>
</div>

<script>
async function launchExam(examId) {
    // Check eligibility via CertificationExam API
    const response = await fetch(
        `https://certificationexam.api/v1/exams/${examId}/check-eligibility`,
        {
            headers: {
                'Authorization': `Bearer ${userToken}`
            }
        }
    );
    
    const result = await response.json();
    
    if (result.eligible) {
        // Redirect to exam page
        window.location.href = `https://certificationexam.app/exams/${examId}`;
    } else {
        // Show error
        alert(result.reason);
    }
}
</script>
```

#### Progress Dashboard Integration

```yaml
progress_dashboard:
  # Display in CoursePlayerApp dashboard
  exam_status:
    - exam_id: "exam_nlp_midterm"
      status: "completed"
      score: 85
      passed: true
      completed_at: "2026-01-10"
    
    - exam_id: "exam_nlp_final"
      status: "available"
      available_from: "2026-01-15"
      attempts_remaining: 1
    
    - exam_id: "exam_nlp_project"
      status: "in_progress"
      started_at: "2026-01-12"
      time_remaining: "45 minutes"
```

#### Certificate Display in Achievements

```javascript
// Show certificates in CoursePlayerApp "Achievements" section
<div class="achievements">
    <h2>🏆 Your Certificates</h2>
    
    <div class="certificate-card">
        <img src="certificate-thumbnail.png" alt="Certificate preview">
        <h3>NLP, Transformers & LLMs</h3>
        <p>Completed: January 15, 2026</p>
        <p>Grade: A (95%)</p>
        <div class="actions">
            <button onclick="downloadCertificate('CERT-2026-NLP-12345')">
                📥 Download PDF
            </button>
            <button onclick="addToLinkedIn('CERT-2026-NLP-12345')">
                💼 Add to LinkedIn
            </button>
            <button onclick="verifyCertificate('CERT-2026-NLP-12345')">
                ✅ Verify
            </button>
        </div>
    </div>
</div>
```

---

### Integration with CourseTransformer

**Purpose**: Auto-generate quiz questions from course materials

#### Question Generation API

```python
from coursetransformer import CourseTransformerClient

def generate_quiz_from_module(module_id: str, question_count: int = 10):
    """Generate quiz questions from course module using AI"""
    
    transformer = CourseTransformerClient(api_key=TRANSFORMER_API_KEY)
    
    # Get module content
    module = transformer.get_module(module_id)
    
    # Generate questions
    questions = transformer.generate_questions(
        content=module.content,
        question_types=['mcq', 'short_answer'],
        count=question_count,
        difficulty_distribution={
            'easy': 0.3,
            'medium': 0.5,
            'hard': 0.2
        }
    )
    
    # Import into question bank
    for question in questions:
        import_question_to_bank(question)
    
    return questions
```

**Generated Question Example**:
```yaml
# Auto-generated from module content
question:
  id: "q_auto_gen_001"
  title: "Transformer Positional Encoding"
  type: "mcq"
  prompt: "Why is positional encoding necessary in Transformer models?"
  
  options:
    - text: "To encode the position of words in the sequence"
      correct: true
    - text: "To reduce model size"
      correct: false
    - text: "To speed up training"
      correct: false
  
  metadata:
    generated_by: "CourseTransformer"
    source_module: "module_transformers_architecture"
    confidence: 0.89
```

---

### Integration with CourseCompliance

**Purpose**: Validate exam quality, accessibility, fairness

#### Pre-Publish Compliance Check

```python
from coursecompliance import ComplianceChecker

def run_compliance_check(exam_id: str) -> dict:
    """Check exam compliance before publishing"""
    
    checker = ComplianceChecker(api_key=COMPLIANCE_API_KEY)
    
    exam = db.query(Exam).filter_by(id=exam_id).first()
    
    # Run checks
    results = {
        'accessibility': checker.check_accessibility(exam),
        'bias': checker.check_bias(exam),
        'question_quality': checker.check_question_quality(exam),
        'rubric_fairness': checker.check_rubric_fairness(exam),
        'legal_compliance': checker.check_legal_compliance(exam),
    }
    
    # Overall pass/fail
    results['compliant'] = all([
        results['accessibility']['pass'],
        results['bias']['pass'],
        results['question_quality']['pass'],
        results['rubric_fairness']['pass'],
        results['legal_compliance']['pass'],
    ])
    
    return results
```

**Compliance Report**:
```yaml
compliance_report:
  exam_id: "exam_nlp_final_2026"
  checked_at: "2026-01-10T10:00:00Z"
  
  accessibility:
    pass: true
    wcag_level: "AA"
    issues: []
  
  bias:
    pass: true
    checked_for:
      - gender_bias
      - cultural_bias
      - language_complexity
    issues:
      - type: "cultural_bias"
        severity: "low"
        question_id: "q_05"
        description: "Reference to US-specific holiday. Consider international audience."
        recommendation: "Use generic example or provide context."
  
  question_quality:
    pass: true
    readability_score: 65  # Flesch-Kincaid (college level)
    issues: []
  
  rubric_fairness:
    pass: true
    inter_rater_reliability: 0.87
    issues: []
  
  legal_compliance:
    pass: true
    ferpa_compliant: true
    coppa_compliant: true
    gdpr_compliant: true
```

---

## External Integrations

### LinkedIn Integration

**Add Certificate to Profile**:

```python
def generate_linkedin_add_url(certificate_id: str) -> str:
    """Generate LinkedIn 'Add to Profile' URL"""
    
    cert = db.query(Certificate).filter_by(id=certificate_id).first()
    
    params = {
        'startTask': 'CERTIFICATION_NAME',
        'name': cert.course_title,
        'organizationId': LINKEDIN_ORG_ID,
        'issueYear': cert.issue_date.year,
        'issueMonth': cert.issue_date.month,
        'certUrl': f"https://gai-observe.online/verify/{certificate_id}",
        'certId': certificate_id,
    }
    
    return f"https://www.linkedin.com/profile/add?{urlencode(params)}"
```

**LinkedIn Learning Integration** (optional):
```yaml
linkedin_learning:
  # Sync course to LinkedIn Learning
  course_sync:
    enabled: false  # Requires LinkedIn partnership
    
  # Certificate verification
  verification_webhook:
    url: "https://api.linkedin.com/v2/certifications/verify"
    enabled: true
```

---

### Blockchain Integration

**Ethereum/Polygon**:

```python
from web3 import Web3

class BlockchainCertificateService:
    def __init__(self, network='polygon'):
        self.w3 = Web3(Web3.HTTPProvider(NETWORK_URLS[network]))
        self.contract = self.w3.eth.contract(
            address=CONTRACT_ADDRESSES[network],
            abi=CONTRACT_ABI
        )
    
    def issue_on_chain(self, certificate_id: str, certificate_hash: str):
        """Issue certificate on blockchain"""
        
        # Build transaction
        txn = self.contract.functions.issueCertificate(
            certificate_id,
            self.w3.keccak(text=certificate_hash)
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price,
        })
        
        # Sign and send
        signed = self.w3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        
        # Wait for confirmation
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return tx_hash.hex()
```

**NFT Minting** (optional):

```solidity
// ERC-721 Certificate NFT
contract CertificateNFT is ERC721 {
    struct CertificateMetadata {
        string certificateId;
        string studentName;
        string courseTitle;
        uint256 issueDate;
        string metadataURI;
    }
    
    mapping(uint256 => CertificateMetadata) public certificates;
    
    function mintCertificate(
        address student,
        string memory certificateId,
        string memory metadataURI
    ) public onlyAuthorized returns (uint256) {
        uint256 tokenId = totalSupply() + 1;
        _mint(student, tokenId);
        
        certificates[tokenId] = CertificateMetadata({
            certificateId: certificateId,
            studentName: getStudentName(student),
            courseTitle: getCourseTitle(certificateId),
            issueDate: block.timestamp,
            metadataURI: metadataURI
        });
        
        return tokenId;
    }
}
```

---

### Payment Integration

**Exam Fees** (via LemonSqueezy):

```python
import lemonsqueezy

def create_exam_payment(student_id: str, exam_id: str) -> dict:
    """Create payment for exam fee"""
    
    exam = db.query(Exam).filter_by(id=exam_id).first()
    
    if exam.fee == 0:
        # Free exam
        return {'payment_required': False}
    
    # Create checkout
    checkout = lemonsqueezy.Checkout.create(
        product_id=exam.product_id,
        customer_email=get_student_email(student_id),
        custom_data={
            'student_id': student_id,
            'exam_id': exam_id,
        },
        redirect_url=f"https://certificationexam.app/exams/{exam_id}",
    )
    
    return {
        'payment_required': True,
        'amount': exam.fee,
        'currency': 'USD',
        'checkout_url': checkout.url,
    }

# Webhook handler
@app.post('/webhooks/lemonsqueezy')
def handle_payment_webhook(request: Request):
    """Handle payment confirmation"""
    
    payload = request.json()
    
    if payload['event'] == 'order_created':
        # Payment successful
        student_id = payload['custom_data']['student_id']
        exam_id = payload['custom_data']['exam_id']
        
        # Grant exam access
        grant_exam_access(student_id, exam_id)
        
        # Send confirmation email
        send_exam_access_email(student_id, exam_id)
    
    return {'status': 'success'}
```

---

### Email Integration

**SendGrid / AWS SES**:

```python
import sendgrid
from sendgrid.helpers.mail import Mail

def send_exam_reminder(student_id: str, exam_id: str):
    """Send exam reminder email"""
    
    student = get_student(student_id)
    exam = db.query(Exam).filter_by(id=exam_id).first()
    
    message = Mail(
        from_email='exams@gai-observe.online',
        to_emails=student.email,
        subject=f'Reminder: {exam.title} - Starting Soon',
        html_content=f"""
        <h2>Exam Reminder</h2>
        <p>Hi {student.first_name},</p>
        <p>This is a reminder that your exam <strong>{exam.title}</strong> is starting soon.</p>
        <p><strong>Exam Window:</strong> {exam.availability_start} - {exam.availability_end}</p>
        <p><strong>Duration:</strong> {exam.duration} minutes</p>
        <p><strong>Proctoring:</strong> {'Enabled' if exam.proctoring_enabled else 'Disabled'}</p>
        <p>Make sure you have:</p>
        <ul>
            <li>Working webcam and microphone</li>
            <li>Stable internet connection</li>
            <li>Quiet environment</li>
        </ul>
        <p><a href="https://certificationexam.app/exams/{exam_id}">Start Exam</a></p>
        <p>Good luck!</p>
        """
    )
    
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    response = sg.send(message)
```

**Email Templates**:
```yaml
email_templates:
  exam_reminder:
    trigger: "24_hours_before_exam_window_closes"
    subject: "Reminder: {{exam_title}} - Due Soon"
  
  exam_available:
    trigger: "exam_window_opens"
    subject: "{{exam_title}} is Now Available"
  
  results_available:
    trigger: "grading_complete"
    subject: "Your {{exam_title}} Results are Ready"
  
  certificate_issued:
    trigger: "certificate_generated"
    subject: "Your Certificate for {{course_title}}"
    attachments: ["certificate.pdf"]
```

---

### Storage Integration

**AWS S3 / Cloudflare R2**:

```python
import boto3

s3_client = boto3.client('s3')

# Upload proctoring recording
def upload_recording(session_id: str, video_file: bytes):
    """Upload proctoring recording to S3"""
    
    key = f"recordings/{session_id}/webcam.mp4"
    
    s3_client.put_object(
        Bucket='certificationexam-recordings',
        Key=key,
        Body=video_file,
        ServerSideEncryption='AES256',
        Metadata={
            'session_id': session_id,
            'recorded_at': datetime.utcnow().isoformat(),
        }
    )
    
    return f"s3://certificationexam-recordings/{key}"

# Upload certificate PDF
def upload_certificate(certificate_id: str, pdf_file: bytes):
    """Upload certificate PDF to S3"""
    
    key = f"certificates/{certificate_id}.pdf"
    
    s3_client.put_object(
        Bucket='certificationexam-certificates',
        Key=key,
        Body=pdf_file,
        ServerSideEncryption='AES256',
        ContentType='application/pdf',
        ACL='private',  # Not publicly accessible
    )
    
    # Generate presigned URL (expires in 1 hour)
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'certificationexam-certificates', 'Key': key},
        ExpiresIn=3600
    )
    
    return url
```

---

### Single Sign-On (SSO)

**OAuth 2.0 / SAML**:

```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)

# Google OAuth
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('auth_callback_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def auth_callback_google():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    
    # Find or create user
    user = find_or_create_user(user_info['email'])
    
    # Log in user
    login_user(user)
    
    return redirect('/dashboard')
```

**Enterprise SAML**:
```yaml
saml_integration:
  # For enterprise customers
  identity_providers:
    - name: "Okta"
      entity_id: "https://company.okta.com"
      sso_url: "https://company.okta.com/app/saml/sso"
      certificate: "..."
    
    - name: "Azure AD"
      entity_id: "https://sts.windows.net/tenant-id/"
      sso_url: "https://login.microsoftonline.com/tenant-id/saml2"
      certificate: "..."
```

---

## API Integration Patterns

### Webhook Integration

```yaml
webhooks:
  # Send events to external systems
  events:
    exam_completed:
      url: "https://customer.com/webhooks/exam-completed"
      payload:
        student_id: "{{student_id}}"
        exam_id: "{{exam_id}}"
        score: "{{score}}"
        passed: "{{passed}}"
        completed_at: "{{completed_at}}"
    
    certificate_issued:
      url: "https://customer.com/webhooks/certificate-issued"
      payload:
        student_id: "{{student_id}}"
        certificate_id: "{{certificate_id}}"
        course_title: "{{course_title}}"
        issued_at: "{{issued_at}}"
  
  security:
    signature_header: "X-CertificationExam-Signature"
    signature_algorithm: "HMAC-SHA256"
    secret_key: "shared_secret"
```

### REST API

```yaml
rest_api:
  base_url: "https://api.certificationexam.com/v1"
  
  authentication:
    type: "Bearer"
    header: "Authorization: Bearer {api_key}"
  
  endpoints:
    # Exams
    - GET /exams
    - GET /exams/{exam_id}
    - POST /exams
    - PUT /exams/{exam_id}
    - DELETE /exams/{exam_id}
    
    # Exam instances
    - POST /exams/{exam_id}/instances
    - GET /instances/{instance_id}
    - POST /instances/{instance_id}/submit
    
    # Results
    - GET /results/{instance_id}
    
    # Certificates
    - GET /certificates/{certificate_id}
    - POST /certificates/{certificate_id}/verify
```

---

## Integration Testing

```python
# Integration tests
import pytest

def test_coursesgtm_integration():
    """Test CoursesGTM tier-based access"""
    
    # Mock student with basic tier
    student = create_test_student(tier='basic')
    
    # Try to access advanced exam
    response = client.get(f'/exams/{advanced_exam_id}/check-eligibility')
    
    assert response.status_code == 403
    assert 'requires advanced tier' in response.json()['reason']

def test_blockchain_integration():
    """Test blockchain certificate issuance"""
    
    # Issue certificate
    cert_id = issue_certificate(student_id, exam_id)
    
    # Verify on blockchain
    blockchain = BlockchainCertificateService(network='polygon_testnet')
    verified = blockchain.verify_on_chain(cert_id, cert_hash)
    
    assert verified is True

def test_linkedin_integration():
    """Test LinkedIn add to profile URL generation"""
    
    url = generate_linkedin_add_url(certificate_id)
    
    assert 'linkedin.com/profile/add' in url
    assert certificate_id in url
```

---

## Conclusion

CertificationExam integrates seamlessly with:
- ✅ **Internal Systems**: CoursesGTM, CoursePlayerApp, CourseTransformer, CourseCompliance
- ✅ **Professional Networks**: LinkedIn certification display
- ✅ **Blockchain**: Ethereum/Polygon for immutable verification
- ✅ **Payments**: LemonSqueezy for exam fees
- ✅ **Email**: SendGrid/SES for notifications
- ✅ **Storage**: S3/R2 for recordings and certificates
- ✅ **SSO**: OAuth, SAML for enterprise authentication

These integrations create a cohesive ecosystem for end-to-end learning, assessment, and credentialing.
