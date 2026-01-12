# CourseCompliance - Compliance Profiles

## Overview

Compliance Profiles define different levels of quality requirements and validation strictness for different use cases. CourseCompliance supports three predefined profiles and allows custom profile creation.

**Purpose**:
- **Flexibility**: Different courses need different validation levels
- **Context-Aware**: MVP courses vs. enterprise deployments have different needs
- **Configurability**: Organizations can customize thresholds
- **Consistency**: Standardized profiles across teams

---

## Profile Architecture

```yaml
# Profile YAML structure
profile_name: "standard"
description: "Balanced quality and speed for general course launches"
use_cases:
  - "General public courses"
  - "E-learning platforms"
  - "Academic institutions"

# Threshold configuration
thresholds:
  # Issue limits
  critical_issues_max: 3
  warning_issues_max: 15
  info_issues_unlimited: true
  
  # Category-specific pass rates
  code_pass_rate_min: 0.95        # 95% of code must execute
  link_validity_min: 0.90          # 90% of links valid
  wcag_compliance_min: 0.85        # 85% WCAG 2.1 AA compliance
  security_critical_max: 0         # No critical security issues
  readability_grade_max: 16        # Max Flesch-Kincaid grade level
  
  # Performance thresholds
  max_load_time_seconds: 3.0
  max_bundle_size_gb: 2.0
  max_image_size_kb: 500
  max_video_bitrate_mbps: 5.0

# Behavior configuration
behavior:
  auto_approve: true                # Auto-approve if thresholds met
  require_sign_off: false           # Human sign-off required?
  early_termination: false          # Stop on first critical issue?
  incremental_checks: true          # Support incremental validation?
  
# Audit configuration
audit:
  level: "standard"                 # minimal, standard, full
  retain_days: 90                   # Audit log retention
  include_auto_fixes: true          # Log auto-remediation?
  
# Agent configuration (can disable non-critical agents)
agents:
  technical: {enabled: true, required: true}
  pedagogical: {enabled: true, required: false}
  legal: {enabled: true, required: true}
  accessibility: {enabled: true, required: true}
  security: {enabled: true, required: true}
  brand: {enabled: true, required: false}
  content_integrity: {enabled: true, required: false}
  performance: {enabled: true, required: false}

# Remediation configuration
remediation:
  auto_fix_enabled: true
  max_auto_fix_attempts: 3
  require_approval_for_high_risk: true
  
# Reporting
reporting:
  executive_summary: true
  detailed_findings: true
  audit_trail: true
  export_formats: ["html", "pdf", "json"]
```

---

## Predefined Profiles

### 1. Strict Profile (Enterprise)

**File**: `profiles/strict.yaml`

**Use Case**: Enterprise deployment, regulated industries, maximum quality

**Philosophy**: Zero tolerance for critical issues, comprehensive validation, human oversight required

```yaml
profile_name: "strict"
description: "Maximum quality standards for enterprise and regulated deployments"

use_cases:
  - "Enterprise learning management systems"
  - "Regulated industries (healthcare, finance, government)"
  - "Certification and accreditation programs"
  - "High-stakes training (safety, compliance)"

thresholds:
  # Issues
  critical_issues_max: 0            # ZERO critical issues
  warning_issues_max: 5             # Very few warnings
  blocking_issues_max: 0            # No blocking issues
  
  # Technical
  code_pass_rate_min: 1.0           # 100% code execution
  link_validity_min: 1.0            # 100% links valid
  file_integrity_min: 1.0           # All files present
  dependency_security_max: 0        # No vulnerable dependencies
  
  # Accessibility
  wcag_compliance_min: 1.0          # 100% WCAG 2.1 AA
  alt_text_coverage_min: 1.0        # All images
  caption_coverage_min: 1.0         # All videos
  contrast_ratio_min: 4.5           # WCAG AA
  
  # Security
  security_critical_max: 0          # No security issues
  security_warning_max: 0           # Even warnings not allowed
  pii_exposure_max: 0               # No PII
  credentials_exposed_max: 0        # No hardcoded credentials
  
  # Legal
  license_conflicts_max: 0          # All licenses compatible
  missing_attribution_max: 0        # All attributed
  copyright_violations_max: 0       # No violations
  
  # Content
  fact_accuracy_min: 0.98           # 98% factual accuracy
  plagiarism_max: 0                 # No plagiarism
  reference_recency_days: 365       # References <1 year old
  
  # Performance
  max_load_time_seconds: 2.0        # Fast loading
  max_bundle_size_gb: 1.0           # Compact bundle
  max_image_size_kb: 300            # Optimized images
  lighthouse_performance_min: 95    # Lighthouse score

behavior:
  auto_approve: false               # ALWAYS require human sign-off
  require_sign_off: true            # Explicit approval needed
  approver_role: "compliance_officer"
  early_termination: true           # Stop on critical issues
  incremental_checks: false         # Always full validation

audit:
  level: "full"                     # Maximum audit detail
  retain_days: 2555                 # 7 years (regulatory compliance)
  include_auto_fixes: true
  include_screenshots: true
  include_code_snapshots: true
  cryptographic_hash: true          # For integrity verification

agents:
  technical: {enabled: true, required: true, timeout_minutes: 30}
  pedagogical: {enabled: true, required: true, timeout_minutes: 20}
  legal: {enabled: true, required: true, timeout_minutes: 15}
  accessibility: {enabled: true, required: true, timeout_minutes: 20}
  security: {enabled: true, required: true, timeout_minutes: 15}
  brand: {enabled: true, required: true, timeout_minutes: 10}
  content_integrity: {enabled: true, required: true, timeout_minutes: 25}
  performance: {enabled: true, required: true, timeout_minutes: 15}

remediation:
  auto_fix_enabled: true
  max_auto_fix_attempts: 3
  require_approval_for_high_risk: true
  require_approval_for_medium_risk: true  # Even medium risk needs approval
  rollback_on_validation_failure: true

reporting:
  executive_summary: true
  detailed_findings: true
  audit_trail: true
  compliance_certificate: true      # Generate certificate on approval
  export_formats: ["html", "pdf", "json", "csv"]
  sign_reports: true                # Digital signature

notifications:
  on_completion: ["compliance_team", "course_owner", "legal_team"]
  on_failure: ["compliance_team", "course_owner", "engineering_lead"]
  on_critical_issue: ["compliance_officer"]  # Immediate notification
```

**Launch Gate Logic**:
```python
def strict_launch_gate(state: ComplianceState) -> bool:
    """Strict profile launch decision"""
    
    # ANY critical issue = FAIL
    if len(state.critical_issues) > 0:
        return False
    
    # ANY blocking issue = FAIL
    if len(state.blocking_issues) > 0:
        return False
    
    # Too many warnings = FAIL
    if len(state.warning_issues) > 5:
        return False
    
    # ANY category below threshold = FAIL
    for category, threshold in state.thresholds.items():
        if not meets_threshold(state, category, threshold):
            return False
    
    # Human sign-off REQUIRED
    if not state.human_approved:
        return False
    
    return True
```

---

### 2. Standard Profile (Default)

**File**: `profiles/standard.yaml`

**Use Case**: General course launches, balanced quality/speed

**Philosophy**: High quality with pragmatic thresholds, auto-approve when criteria met

```yaml
profile_name: "standard"
description: "Balanced quality and speed for general course launches"

use_cases:
  - "Public online courses"
  - "E-learning platforms"
  - "Corporate training (non-critical)"
  - "Academic courses"

thresholds:
  # Issues
  critical_issues_max: 3            # Up to 3 critical (with justification)
  warning_issues_max: 15
  
  # Technical
  code_pass_rate_min: 0.95          # 95% of code executes
  link_validity_min: 0.90           # 90% links valid
  file_integrity_min: 0.98          # 98% files present
  dependency_security_max: 0        # No critical vulnerabilities
  
  # Accessibility
  wcag_compliance_min: 0.85         # 85% WCAG 2.1 AA
  alt_text_coverage_min: 0.90       # 90% of images
  caption_coverage_min: 0.85        # 85% of videos
  contrast_ratio_min: 4.5           # WCAG AA
  
  # Security
  security_critical_max: 0          # No critical security issues
  security_warning_max: 5           # Up to 5 warnings OK
  pii_exposure_max: 0               # No PII
  credentials_exposed_max: 0        # No hardcoded credentials
  
  # Legal
  license_conflicts_max: 0          # All licenses compatible
  missing_attribution_max: 2        # Up to 2 minor attribution issues
  
  # Content
  fact_accuracy_min: 0.95           # 95% factual accuracy
  plagiarism_max: 0                 # No plagiarism
  reference_recency_days: 730       # References <2 years old
  
  # Performance
  max_load_time_seconds: 3.0
  max_bundle_size_gb: 2.0
  max_image_size_kb: 500
  lighthouse_performance_min: 80

behavior:
  auto_approve: true                # Auto-approve if thresholds met
  require_sign_off: false           # No sign-off if auto-approved
  early_termination: false
  incremental_checks: true

audit:
  level: "standard"
  retain_days: 90                   # 3 months
  include_auto_fixes: true

agents:
  technical: {enabled: true, required: true, timeout_minutes: 20}
  pedagogical: {enabled: true, required: false, timeout_minutes: 15}
  legal: {enabled: true, required: true, timeout_minutes: 10}
  accessibility: {enabled: true, required: true, timeout_minutes: 15}
  security: {enabled: true, required: true, timeout_minutes: 10}
  brand: {enabled: true, required: false, timeout_minutes: 5}
  content_integrity: {enabled: true, required: false, timeout_minutes: 15}
  performance: {enabled: true, required: false, timeout_minutes: 10}

remediation:
  auto_fix_enabled: true
  max_auto_fix_attempts: 3
  require_approval_for_high_risk: true
  rollback_on_validation_failure: true

reporting:
  executive_summary: true
  detailed_findings: true
  audit_trail: true
  export_formats: ["html", "pdf", "json"]

notifications:
  on_completion: ["course_owner"]
  on_failure: ["course_owner", "qa_team"]
```

**Launch Gate Logic**:
```python
def standard_launch_gate(state: ComplianceState) -> bool:
    """Standard profile launch decision"""
    
    # Unresolved blocking issues = FAIL
    if has_unresolved_blocking_issues(state):
        return False
    
    # Too many critical issues = FAIL
    unresolved_critical = count_unresolved_critical(state)
    if unresolved_critical > 3:
        return False
    
    # If critical issues exist, require justification
    if unresolved_critical > 0:
        if not has_risk_acceptance(state):
            return False
    
    # Check category thresholds
    if not meets_category_thresholds(state):
        return False
    
    return True
```

---

### 3. Relaxed Profile (MVP/Beta)

**File**: `profiles/relaxed.yaml`

**Use Case**: MVPs, beta courses, rapid iteration

**Philosophy**: Minimum viable quality, catch critical issues only, iterate quickly

```yaml
profile_name: "relaxed"
description: "Minimum viable quality for MVP, beta, and rapid iteration"

use_cases:
  - "MVP courses"
  - "Beta testing"
  - "Internal prototypes"
  - "Rapid iteration environments"
  - "Proof of concepts"

thresholds:
  # Issues
  critical_issues_max: 10           # Up to 10 critical issues
  warning_issues_unlimited: true    # Unlimited warnings
  
  # Technical
  code_pass_rate_min: 0.80          # 80% code execution
  link_validity_min: 0.70           # 70% links valid
  file_integrity_min: 0.90          # 90% files present
  dependency_security_max: 5        # Up to 5 low-severity vulnerabilities
  
  # Accessibility
  wcag_compliance_min: 0.50         # Basic accessibility (50%)
  alt_text_coverage_min: 0.60       # 60% of images
  caption_coverage_min: 0.50        # 50% of videos
  # Color contrast not required
  
  # Security
  security_critical_max: 0          # No critical security (still important!)
  security_warning_unlimited: true  # Warnings OK
  pii_exposure_max: 0               # No PII (still important!)
  credentials_exposed_max: 0        # No credentials (still important!)
  
  # Legal
  license_conflicts_max: 2          # Some conflicts OK (to fix later)
  missing_attribution_max: 10       # Many attributions can wait
  
  # Content
  fact_accuracy_min: 0.85           # 85% factual accuracy
  plagiarism_max: 0                 # No plagiarism (still important!)
  reference_recency_days: 1825      # References <5 years OK
  
  # Performance
  max_load_time_seconds: 5.0        # Slower OK
  max_bundle_size_gb: 5.0           # Larger OK
  max_image_size_kb: 1000           # Unoptimized OK
  lighthouse_performance_min: 50    # Lower performance OK

behavior:
  auto_approve: true                # Auto-approve with warnings
  require_sign_off: false
  early_termination: false
  incremental_checks: true
  skip_non_critical_agents: true    # Skip brand, performance if time-constrained

audit:
  level: "minimal"                  # Basic logging only
  retain_days: 30                   # 1 month
  include_auto_fixes: false         # Don't log auto-fixes

agents:
  technical: {enabled: true, required: true, timeout_minutes: 15}
  pedagogical: {enabled: false, required: false}  # Skip for speed
  legal: {enabled: true, required: true, timeout_minutes: 5}
  accessibility: {enabled: true, required: false, timeout_minutes: 10}
  security: {enabled: true, required: true, timeout_minutes: 10}
  brand: {enabled: false, required: false}        # Skip for speed
  content_integrity: {enabled: false, required: false}  # Skip for speed
  performance: {enabled: false, required: false}  # Skip for speed

remediation:
  auto_fix_enabled: true
  max_auto_fix_attempts: 1          # One attempt only
  require_approval_for_high_risk: false  # Apply all auto-fixes
  rollback_on_validation_failure: false  # Keep moving forward

reporting:
  executive_summary: true
  detailed_findings: false          # Summary only
  audit_trail: false                # No detailed audit
  export_formats: ["json"]          # JSON only

notifications:
  on_completion: ["course_owner"]
  on_critical_issue: ["course_owner"]  # Only critical issues
```

**Launch Gate Logic**:
```python
def relaxed_launch_gate(state: ComplianceState) -> bool:
    """Relaxed profile launch decision"""
    
    # Only block on:
    # 1. Hardcoded credentials/secrets
    # 2. PII exposure
    # 3. Critical security vulnerabilities
    # 4. Too many critical issues
    
    blocking_categories = ["credentials", "pii", "security_critical"]
    
    for issue in state.critical_issues:
        if issue["subcategory"] in blocking_categories:
            return False
    
    # Too many critical issues overall
    if len(state.critical_issues) > 10:
        return False
    
    # Everything else is acceptable
    return True
```

---

## Profile Comparison Table

| Aspect | Strict | Standard | Relaxed |
|--------|--------|----------|---------|
| **Use Case** | Enterprise, Regulated | General Courses | MVP, Beta |
| **Critical Issues** | 0 | ≤3 (justified) | ≤10 |
| **Warnings** | ≤5 | ≤15 | Unlimited |
| **Code Pass Rate** | 100% | 95% | 80% |
| **Link Validity** | 100% | 90% | 70% |
| **WCAG Compliance** | 100% AA | 85% AA | 50% (basic) |
| **Security** | 0 issues | 0 critical | 0 credentials/PII |
| **Auto-Approve** | No (sign-off) | Yes (if thresholds met) | Yes (with warnings) |
| **Audit Retention** | 7 years | 3 months | 1 month |
| **All Agents Run** | Yes | Yes | No (skip 3) |
| **Launch Time** | Slowest | Medium | Fastest |
| **Quality Level** | Maximum | High | Minimum Viable |

---

## Custom Profiles

Organizations can create custom profiles:

### Example: Custom Profile for Healthcare Training

```yaml
profile_name: "healthcare_training"
description: "High quality for healthcare industry training with HIPAA compliance"

parent_profile: "strict"  # Inherit from strict and override

# Override thresholds
thresholds:
  # Stricter on privacy
  pii_exposure_max: 0
  phi_exposure_max: 0               # Protected Health Information
  
  # Stricter on accuracy
  fact_accuracy_min: 0.99           # 99% for medical facts
  
  # Stricter on accessibility (ADA compliance)
  wcag_compliance_min: 1.0
  screen_reader_compatible: true

# Additional checks
additional_checks:
  - hipaa_compliance
  - medical_terminology_accuracy
  - clinical_guideline_adherence

# Custom agent
custom_agents:
  - name: "hipaa_compliance_agent"
    enabled: true
    required: true
```

### Example: Custom Profile for Internal Engineering Docs

```yaml
profile_name: "internal_engineering"
description: "Technical documentation for internal engineering teams"

parent_profile: "relaxed"

# Override: stricter on code quality, relaxed on accessibility
thresholds:
  code_pass_rate_min: 1.0           # 100% for engineers
  wcag_compliance_min: 0.30         # Internal use, lower accessibility OK
  
# Disable some agents
agents:
  pedagogical: {enabled: false}     # Not a course, just docs
  brand: {enabled: false}           # Internal, brand doesn't matter
  
# Enable code-specific checks
additional_checks:
  - code_coverage_min: 0.80         # 80% test coverage
  - api_documentation_complete: true
```

---

## Profile Selection

### Automatic Profile Selection

```python
def recommend_profile(course_metadata: Dict) -> str:
    """Recommend compliance profile based on course metadata"""
    
    # Enterprise course?
    if course_metadata.get("enterprise", False):
        return "strict"
    
    # Regulated industry?
    if course_metadata.get("industry") in ["healthcare", "finance", "government"]:
        return "strict"
    
    # Beta/MVP?
    if course_metadata.get("status") in ["beta", "mvp", "prototype"]:
        return "relaxed"
    
    # Default
    return "standard"
```

### Manual Override

```python
# Command line
python -m coursecompliance \
    --course-path /path/to/course \
    --profile strict

# Programmatic
from coursecompliance import run_compliance_check

result = run_compliance_check(
    course_path="/path/to/course",
    compliance_profile="strict"
)
```

### Profile in Course Metadata

```yaml
# course_metadata.yaml
course:
  name: "Advanced Machine Learning"
  status: "production"
  
compliance:
  profile: "standard"  # Specify profile in course metadata
  custom_thresholds:   # Override specific thresholds
    code_pass_rate_min: 0.98
    wcag_compliance_min: 0.90
```

---

## Profile Validation

Validate profile configuration before use:

```python
class ProfileValidator:
    """Validate compliance profile configuration"""
    
    def validate(self, profile: Dict) -> List[str]:
        """Validate profile, return list of errors"""
        errors = []
        
        # Check required fields
        required = ["profile_name", "thresholds", "behavior", "agents"]
        for field in required:
            if field not in profile:
                errors.append(f"Missing required field: {field}")
        
        # Validate thresholds are numeric and in valid range
        for key, value in profile.get("thresholds", {}).items():
            if key.endswith("_min") or key.endswith("_max"):
                if not isinstance(value, (int, float)):
                    errors.append(f"Threshold {key} must be numeric")
                if key.endswith("_min") and value < 0:
                    errors.append(f"Minimum threshold {key} cannot be negative")
        
        # Validate agents configuration
        for agent, config in profile.get("agents", {}).items():
            if "enabled" not in config:
                errors.append(f"Agent {agent} missing 'enabled' field")
            if config.get("required") and not config.get("enabled"):
                errors.append(f"Agent {agent} is required but disabled")
        
        return errors
```

---

## Profile Inheritance

Support profile inheritance to avoid duplication:

```yaml
# custom_profile.yaml
profile_name: "my_custom_profile"
parent_profile: "standard"  # Inherit from standard

# Only specify overrides
thresholds:
  code_pass_rate_min: 0.98  # Override: stricter than standard
  
agents:
  brand: {enabled: false}   # Override: disable brand checks
  
# Everything else inherited from standard profile
```

```python
def load_profile_with_inheritance(profile_name: str) -> Dict:
    """Load profile with inheritance support"""
    
    profile = load_profile_yaml(profile_name)
    
    if "parent_profile" in profile:
        parent = load_profile_with_inheritance(profile["parent_profile"])
        # Merge: child overrides parent
        merged = deep_merge(parent, profile)
        return merged
    
    return profile
```

---

## Conclusion

Compliance Profiles provide:

1. **Flexibility**: Different validation levels for different contexts
2. **Clarity**: Clear thresholds and expectations
3. **Consistency**: Standardized profiles across organization
4. **Customization**: Easy to create custom profiles
5. **Inheritance**: Reuse common configurations
6. **Validation**: Ensure profiles are correctly configured

By choosing the right profile (Strict, Standard, or Relaxed) or creating a custom one, organizations can balance quality requirements with development velocity, ensuring courses meet appropriate standards for their intended use case.
