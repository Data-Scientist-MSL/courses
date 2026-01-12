# Security & Privacy Documentation

## Overview

CertificationExam implements comprehensive security and privacy measures to protect student data, maintain exam integrity, and comply with applicable regulations. This document details security controls, privacy protections, compliance requirements, and ethical AI practices.

### Security Principles
- **Defense in Depth**: Multiple layers of security
- **Least Privilege**: Minimal access rights
- **Zero Trust**: Verify every access request
- **Encryption Everywhere**: Data encrypted at rest and in transit
- **Security by Design**: Security built into architecture

### Privacy Principles
- **Data Minimization**: Collect only what's necessary
- **Purpose Limitation**: Use data only for stated purposes
- **Transparency**: Students know what data is collected and why
- **User Control**: Students can access, export, delete their data
- **Privacy by Default**: Most privacy-protective settings as default

---

## Data Security

### Encryption

#### At Rest (AES-256)

```yaml
encryption_at_rest:
  database:
    algorithm: "AES-256-GCM"
    provider: "AWS RDS encryption"
    key_management: "AWS KMS"
    key_rotation: "yearly"
  
  file_storage:
    algorithm: "AES-256"
    provider: "S3 SSE-KMS"
    objects:
      - proctoring_recordings
      - certificate_pdfs
      - student_submissions
    
  backups:
    algorithm: "AES-256"
    encryption: "mandatory"
    encrypted_before_upload: true
```

**Implementation**:
```python
from cryptography.fernet import Fernet
import boto3

# Database field-level encryption
class EncryptedField:
    def __init__(self, fernet_key: bytes):
        self.cipher = Fernet(fernet_key)
    
    def encrypt(self, plaintext: str) -> bytes:
        return self.cipher.encrypt(plaintext.encode())
    
    def decrypt(self, ciphertext: bytes) -> str:
        return self.cipher.decrypt(ciphertext).decode()

# S3 encryption
s3_client = boto3.client('s3')

def upload_encrypted(file_data: bytes, key: str):
    s3_client.put_object(
        Bucket='certificationexam-recordings',
        Key=key,
        Body=file_data,
        ServerSideEncryption='aws:kms',
        SSEKMSKeyId='arn:aws:kms:us-east-1:123456789:key/...'
    )
```

#### In Transit (TLS 1.3)

```yaml
encryption_in_transit:
  web_traffic:
    protocol: "TLS 1.3"
    minimum_version: "TLS 1.2"
    cipher_suites:
      - "TLS_AES_128_GCM_SHA256"
      - "TLS_AES_256_GCM_SHA384"
      - "TLS_CHACHA20_POLY1305_SHA256"
    
    certificates:
      provider: "Let's Encrypt"
      auto_renewal: true
      validity: "90 days"
  
  api_calls:
    protocol: "HTTPS only"
    http_redirect: true
    hsts_enabled: true
    hsts_max_age: 31536000  # 1 year
  
  database_connections:
    protocol: "TLS 1.2+"
    certificate_validation: true
```

**Nginx Configuration**:
```nginx
server {
    listen 443 ssl http2;
    server_name certificationexam.app;
    
    # TLS configuration
    ssl_certificate /etc/letsencrypt/live/certificationexam.app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/certificationexam.app/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256';
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Security headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'" always;
}
```

---

### Authentication & Authorization

#### Authentication

**Multi-Factor Authentication (MFA)**:
```yaml
authentication:
  password:
    min_length: 12
    require_uppercase: true
    require_lowercase: true
    require_number: true
    require_special_char: true
    prevent_common_passwords: true
    password_history: 5  # Can't reuse last 5 passwords
  
  mfa:
    required_for:
      - instructors
      - graders
      - administrators
    optional_for:
      - students
    methods:
      - totp  # Time-based OTP (Google Authenticator)
      - sms
      - email
      - webauthn  # Hardware keys (YubiKey)
  
  session:
    timeout: 3600  # 1 hour
    refresh_token_lifetime: 86400  # 24 hours
    concurrent_sessions: 1  # One active exam session at a time
```

**Implementation**:
```python
from passlib.hash import argon2
import pyotp

# Password hashing (Argon2)
def hash_password(password: str) -> str:
    return argon2.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return argon2.verify(password, hash)

# TOTP MFA
def generate_totp_secret() -> str:
    return pyotp.random_base32()

def verify_totp(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)
```

#### Authorization (RBAC)

**Role-Based Access Control**:
```yaml
roles:
  student:
    permissions:
      - take_exams
      - view_own_results
      - download_own_certificates
      - request_regrade
  
  grader:
    permissions:
      - view_grading_queue
      - grade_submissions
      - provide_feedback
      - view_rubrics
  
  instructor:
    permissions:
      - create_exams
      - edit_exams
      - view_all_results
      - override_grades
      - manage_rubrics
      - view_proctoring_incidents
  
  admin:
    permissions:
      - all_instructor_permissions
      - manage_users
      - view_system_logs
      - configure_proctoring
      - revoke_certificates
  
  academic_integrity_officer:
    permissions:
      - view_proctoring_recordings
      - review_flagged_submissions
      - investigate_violations
      - access_evidence_packages
```

**Implementation**:
```python
from functools import wraps
from flask import abort

def require_permission(permission: str):
    """Decorator to check user permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403, description="Insufficient permissions")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage
@app.route('/exams/<exam_id>/grade')
@require_permission('grade_submissions')
def grade_exam(exam_id):
    # Only users with 'grade_submissions' permission can access
    ...
```

---

### Exam Security

#### Question Bank Protection

```yaml
question_bank_security:
  encryption:
    - questions_encrypted_at_rest
    - answers_encrypted_separately
  
  access_control:
    - instructors_only
    - read_only_for_graders
    - no_student_access
  
  audit_logging:
    - log_all_access
    - log_modifications
    - log_exports
  
  versioning:
    - track_all_changes
    - attribution_required
    - rollback_capability
```

#### Answer Key Security

```python
# Separate encryption key for answer keys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AnswerKeyEncryption:
    def __init__(self, key: bytes):
        self.cipher = AESGCM(key)
    
    def encrypt_answer_key(self, answers: dict) -> bytes:
        """Encrypt answer key with unique nonce"""
        import json
        import os
        
        plaintext = json.dumps(answers).encode()
        nonce = os.urandom(12)
        
        ciphertext = self.cipher.encrypt(nonce, plaintext, None)
        
        # Return nonce + ciphertext
        return nonce + ciphertext
    
    def decrypt_answer_key(self, encrypted: bytes) -> dict:
        """Decrypt answer key"""
        import json
        
        nonce = encrypted[:12]
        ciphertext = encrypted[12:]
        
        plaintext = self.cipher.decrypt(nonce, ciphertext, None)
        
        return json.loads(plaintext.decode())
```

#### Session Security

```yaml
exam_session_security:
  token:
    algorithm: "HS256"
    secret_rotation: "daily"
    include_claims:
      - session_id
      - student_id
      - exam_id
      - issued_at
      - expires_at
      - ip_address
  
  validation:
    - verify_token_signature
    - check_expiration
    - verify_ip_address  # Prevent session hijacking
    - one_session_per_student
  
  termination:
    - on_timeout
    - on_submission
    - on_critical_violation
    - on_multiple_failed_auth
```

---

### Certificate Security

#### Digital Signatures

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import hashlib
import json

class CertificateSigner:
    def __init__(self, private_key):
        self.private_key = private_key
    
    def sign_certificate(self, cert_data: dict) -> str:
        """Sign certificate with RSA-2048"""
        
        # Create canonical JSON
        canonical = json.dumps(cert_data, sort_keys=True)
        
        # Hash
        cert_hash = hashlib.sha256(canonical.encode()).digest()
        
        # Sign
        signature = self.private_key.sign(
            cert_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Base64 encode
        import base64
        return base64.b64encode(signature).decode()
```

#### Blockchain Immutability

```solidity
// Smart contract prevents certificate tampering
contract CertificateRegistry {
    mapping(string => bytes32) public certificateHashes;
    mapping(string => bool) public revoked;
    
    event CertificateIssued(string certificateId, bytes32 hash);
    event CertificateRevoked(string certificateId);
    
    function issueCertificate(string memory certId, bytes32 hash) 
        public 
        onlyAuthorized 
    {
        require(certificateHashes[certId] == bytes32(0), "Already exists");
        
        certificateHashes[certId] = hash;
        emit CertificateIssued(certId, hash);
    }
    
    function verifyCertificate(string memory certId, bytes32 hash) 
        public 
        view 
        returns (bool) 
    {
        return certificateHashes[certId] == hash && !revoked[certId];
    }
}
```

---

## Privacy Protection

### Data Minimization

**What We Collect**:
```yaml
collected_data:
  required:
    - name
    - email
    - student_id
    - exam_answers
    - exam_scores
  
  proctoring_optional:
    - face_embeddings  # NOT raw images
    - webcam_recording  # Time-limited, encrypted
    - audio_snippets  # Only if incident
    - screen_activity_logs
  
  never_collected:
    - raw_biometric_data
    - social_security_numbers
    - financial_information
    - unnecessary_demographics
```

**Data Retention**:
```yaml
retention_policy:
  exam_submissions: "3 years"  # Academic record
  grades: "permanent"  # Transcript
  proctoring_recordings: "90 days"  # Or until integrity case resolved
  proctoring_logs: "1 year"
  certificates: "permanent"
  certificate_verification_logs: "1 year"
  
  auto_deletion:
    enabled: true
    schedule: "daily"
    notify_before_deletion: true
```

---

### Student Privacy Rights

#### FERPA Compliance (US)

**Family Educational Rights and Privacy Act**:
```yaml
ferpa_compliance:
  educational_records:
    - exam_submissions
    - grades
    - proctoring_incidents
    - certificates
  
  student_rights:
    - access_own_records
    - request_amendment
    - consent_to_disclosure
    - file_complaints
  
  disclosure_without_consent:
    - school_officials_with_legitimate_interest
    - other_schools_transferring_to
    - authorized_auditors
    - financial_aid_determination
    - comply_with_subpoena
  
  disclosure_prohibited:
    - marketing_companies
    - unauthorized_third_parties
    - public_without_directory_info_consent
```

#### GDPR Compliance (EU)

**General Data Protection Regulation**:
```yaml
gdpr_compliance:
  lawful_basis:
    - contract: "Necessary for exam administration"
    - consent: "Proctoring recording"
    - legitimate_interest: "Academic integrity"
  
  data_subject_rights:
    right_to_access:
      response_time: "30 days"
      format: "portable JSON"
    
    right_to_rectification:
      correct_inaccurate_data: true
      complete_incomplete_data: true
    
    right_to_erasure:
      conditions:
        - data_no_longer_necessary
        - consent_withdrawn
        - unlawfully_processed
      exceptions:
        - legal_obligation
        - public_interest
        - academic_freedom
    
    right_to_data_portability:
      format: "JSON"
      includes:
        - exam_history
        - grades
        - certificates
    
    right_to_object:
      to_processing: true
      to_automated_decision_making: true
  
  breach_notification:
    timeline: "72 hours"
    notify: ["supervisory_authority", "affected_individuals"]
```

**Implementation**:
```python
# GDPR data export
def export_student_data(student_id: str) -> dict:
    """Export all student data in portable format"""
    
    return {
        "personal_info": get_personal_info(student_id),
        "exam_history": get_exam_history(student_id),
        "grades": get_grades(student_id),
        "certificates": get_certificates(student_id),
        "proctoring_incidents": get_incidents(student_id),
        "exported_at": datetime.utcnow().isoformat(),
    }

# Right to erasure
def delete_student_data(student_id: str, reason: str):
    """Delete student data per GDPR right to erasure"""
    
    # Check if deletion allowed
    if not can_delete(student_id, reason):
        raise ValueError("Cannot delete: legal obligation to retain")
    
    # Anonymize instead of delete (for research/analytics)
    anonymize_student_data(student_id)
    
    # Delete identifiable data
    delete_personal_info(student_id)
    delete_proctoring_recordings(student_id)
    
    # Log deletion
    log_data_deletion(student_id, reason)
```

#### COPPA Compliance (US - Children)

**Children's Online Privacy Protection Act** (if under 13):
```yaml
coppa_compliance:
  age_gate:
    verify_age_before_data_collection: true
    minimum_age: 13
  
  parental_consent:
    required_for_under_13: true
    verifiable_consent_method: true
  
  data_practices:
    - collect_only_necessary
    - no_targeted_advertising
    - secure_data_storage
    - parent_can_review_and_delete
```

---

### Academic Integrity Privacy

**Proctoring Privacy Balance**:
```yaml
proctoring_privacy:
  transparency:
    - inform_before_exam
    - explain_what_monitored
    - explain_why_monitored
    - explain_how_data_used
  
  consent:
    - explicit_consent_required
    - opt_out_option: "alternative_testing"  # In-person, oral exam
  
  data_protection:
    - face_embeddings_only  # No raw images stored
    - recordings_encrypted
    - access_restricted_to_authorized_staff
    - auto_delete_after_retention_period
  
  student_access:
    - can_view_own_recordings
    - can_challenge_incidents
    - can_appeal_violations
```

---

## Compliance

### Security Compliance

#### SOC 2 Type II

```yaml
soc2_compliance:
  trust_service_criteria:
    security:
      - access_controls
      - encryption
      - vulnerability_management
      - incident_response
    
    availability:
      - system_monitoring
      - disaster_recovery
      - 99.9_percent_uptime
    
    processing_integrity:
      - data_validation
      - error_handling
      - quality_assurance
    
    confidentiality:
      - encryption
      - access_restrictions
      - nda_with_staff
    
    privacy:
      - privacy_policy
      - data_retention
      - user_rights
  
  annual_audit: true
  auditor: "independent_cpa_firm"
```

#### ISO 27001

```yaml
iso27001_compliance:
  information_security_management_system:
    - risk_assessment
    - security_policies
    - access_control
    - cryptography
    - physical_security
    - operations_security
    - communications_security
    - incident_management
    - business_continuity
  
  certification: "in_progress"
  target_date: "2026-Q3"
```

---

### Ethical AI

#### Bias Mitigation

```yaml
bias_mitigation:
  proctoring_ai:
    # Test for bias across demographics
    testing:
      - test_diverse_demographics
      - measure_false_positive_rates
      - measure_false_negative_rates
      - ensure_no_group_disparate_impact
    
    # Target: <5% FPR difference across groups
    acceptable_fpr_difference: 0.05
    
    # Regular audits
    bias_audit_frequency: "monthly"
    
    # Diverse training data
    training_data:
      - diverse_faces
      - diverse_environments
      - diverse_lighting_conditions
  
  ai_grading:
    # Ensure fair grading across student groups
    testing:
      - test_across_writing_styles
      - test_across_language_backgrounds
      - measure_grading_consistency
    
    # Human oversight
    human_review_required: true
    ai_suggestions_only: true
```

**Bias Testing**:
```python
def test_proctoring_bias():
    """Test proctoring AI for demographic bias"""
    
    # Test data from diverse demographics
    test_data = load_diverse_test_data()
    
    results_by_demographic = {}
    
    for demographic_group in test_data.groups:
        # Run proctoring AI
        predictions = proctoring_ai.predict(demographic_group.samples)
        
        # Calculate metrics
        fpr = calculate_false_positive_rate(predictions, demographic_group.labels)
        fnr = calculate_false_negative_rate(predictions, demographic_group.labels)
        
        results_by_demographic[demographic_group.name] = {
            'fpr': fpr,
            'fnr': fnr,
        }
    
    # Check for disparate impact
    max_fpr_diff = max(results.values())['fpr'] - min(results.values())['fpr']
    
    assert max_fpr_diff < 0.05, f"FPR difference too high: {max_fpr_diff}"
```

#### Explainability

```yaml
explainability:
  proctoring_incidents:
    # Students can see why they were flagged
    explanation_provided: true
    explanation_includes:
      - which_agent_flagged
      - what_behavior_detected
      - timestamp_of_incident
      - evidence_summary
  
  ai_grading:
    # Students can see AI grading rationale
    explanation_provided: true
    explanation_includes:
      - rubric_criteria_scores
      - strengths_identified
      - areas_for_improvement
      - comparison_to_rubric_levels
```

#### Human Oversight

```yaml
human_oversight:
  critical_decisions:
    # Humans required for high-stakes decisions
    exam_termination: "human_required"
    academic_integrity_violations: "human_required"
    grade_disputes: "human_required"
  
  ai_role:
    - flag_potential_issues
    - suggest_grades
    - provide_analysis
    - assist_humans
  
  human_role:
    - make_final_decisions
    - override_ai_when_appropriate
    - handle_edge_cases
    - ensure_fairness
```

---

## Incident Response

### Security Incident Response Plan

```yaml
incident_response:
  detection:
    - automated_monitoring
    - security_alerts
    - user_reports
  
  triage:
    - assess_severity
    - classify_incident_type
    - assign_response_team
  
  containment:
    - isolate_affected_systems
    - prevent_further_damage
    - preserve_evidence
  
  eradication:
    - remove_threat
    - patch_vulnerabilities
    - update_security_controls
  
  recovery:
    - restore_systems
    - verify_integrity
    - resume_operations
  
  post_incident:
    - root_cause_analysis
    - lessons_learned
    - update_procedures
    - notify_affected_parties
```

### Data Breach Response

```yaml
data_breach_response:
  immediate:
    - stop_breach
    - secure_systems
    - preserve_evidence
  
  within_24_hours:
    - assess_scope
    - identify_affected_data
    - determine_notification_requirements
  
  within_72_hours:
    - notify_supervisory_authority  # GDPR
    - notify_affected_individuals
    - notify_media_if_high_risk
  
  ongoing:
    - provide_support_to_affected
    - offer_credit_monitoring_if_appropriate
    - implement_preventive_measures
```

---

## Audit Logging

### What We Log

```yaml
audit_logging:
  authentication:
    - login_attempts
    - logout_events
    - mfa_usage
    - password_changes
  
  authorization:
    - access_denials
    - permission_changes
    - role_assignments
  
  exam_activities:
    - exam_access
    - exam_submission
    - proctoring_incidents
    - grade_changes
  
  data_access:
    - question_bank_access
    - student_record_access
    - certificate_verification
    - proctoring_recording_access
  
  administrative:
    - user_creation
    - permission_changes
    - configuration_changes
    - certificate_revocation
```

**Log Format**:
```json
{
  "timestamp": "2026-01-12T10:30:00Z",
  "event_type": "exam_access",
  "user_id": "student_123",
  "user_role": "student",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "resource_type": "exam",
  "resource_id": "exam_nlp_final",
  "action": "start_exam",
  "result": "success",
  "metadata": {
    "tier": "advanced",
    "proctoring_enabled": true
  }
}
```

### Log Retention

```yaml
log_retention:
  security_logs: "7 years"
  audit_logs: "7 years"
  access_logs: "1 year"
  application_logs: "90 days"
  
  compliance_requirement: "SOX, GDPR, FERPA"
```

---

## Conclusion

CertificationExam implements comprehensive security and privacy:
- ✅ **Data Security**: Encryption at rest (AES-256) and in transit (TLS 1.3)
- ✅ **Authentication**: MFA, strong passwords, session security
- ✅ **Authorization**: RBAC with least privilege
- ✅ **Privacy Protection**: Data minimization, short retention, user rights
- ✅ **Compliance**: FERPA, GDPR, COPPA, SOC 2, ISO 27001
- ✅ **Ethical AI**: Bias mitigation, explainability, human oversight
- ✅ **Incident Response**: Comprehensive breach response plan
- ✅ **Audit Logging**: Complete audit trail

This ensures student data is protected, exams are secure, and all regulatory requirements are met.
