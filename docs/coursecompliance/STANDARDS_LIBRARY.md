# CourseCompliance - Standards Library

## Overview

The Standards Library is a comprehensive collection of YAML-based standards that define the compliance requirements for each of the 8 expert agent categories. These standards are:

- **Version-Controlled**: Tracked in git for change history
- **Human-Editable**: YAML format for easy customization
- **Machine-Readable**: Programmatically loaded by agents
- **Hierarchical**: Organized by category and subcategory
- **Extensible**: New standards can be added without code changes

**Directory Structure**:
```
docs/coursecompliance/standards/
├── technical/
│   ├── code_execution.yaml
│   ├── link_validity.yaml
│   ├── file_integrity.yaml
│   ├── dependency_management.yaml
│   ├── notebook_validation.yaml
│   └── build_testing.yaml
├── pedagogical/
│   ├── learning_objectives.yaml
│   ├── scaffolding.yaml
│   ├── assessments.yaml
│   ├── engagement.yaml
│   ├── prerequisites.yaml
│   └── completion_time.yaml
├── legal/
│   ├── licenses.yaml
│   ├── attribution.yaml
│   ├── copyright.yaml
│   └── privacy.yaml
├── accessibility/
│   ├── wcag_2_1.yaml
│   ├── readability.yaml
│   └── media_accessibility.yaml
├── security/
│   ├── credentials.yaml
│   ├── vulnerabilities.yaml
│   ├── pii.yaml
│   └── safe_examples.yaml
├── brand/
│   ├── style_guide.yaml
│   ├── terminology.yaml
│   └── formatting.yaml
├── content_integrity/
│   ├── fact_checking.yaml
│   ├── accuracy.yaml
│   ├── references.yaml
│   └── consistency.yaml
└── performance/
    ├── load_time.yaml
    ├── file_size.yaml
    ├── video_quality.yaml
    └── image_optimization.yaml
```

---

## Standard Format

Each standard YAML file follows this structure:

```yaml
# Standard metadata
standard:
  id: "TECH-CODE-EXEC"
  name: "Code Execution Standard"
  version: "1.0.0"
  category: "technical"
  subcategory: "code_execution"
  description: "Standards for ensuring all course code executes without errors"
  last_updated: "2026-01-12"

# Compliance profiles (thresholds vary by profile)
profiles:
  strict:
    enabled: true
    pass_threshold: 1.0  # 100%
    blocking_on_failure: true
  standard:
    enabled: true
    pass_threshold: 0.95  # 95%
    blocking_on_failure: true
  relaxed:
    enabled: true
    pass_threshold: 0.80  # 80%
    blocking_on_failure: false

# Individual requirements
requirements:
  - id: "CODE-EXEC-001"
    name: "Jupyter notebooks execute without errors"
    description: "All .ipynb files must execute cell-by-cell without raising exceptions"
    severity: "critical"  # critical, warning, info
    blocking: true  # Blocks launch if failed
    auto_fixable: false
    check_type: "automated"  # automated, manual, ai_assisted
    
    # How to check
    validation:
      method: "execute_notebook"
      timeout_seconds: 300
      parameters:
        kernel: "python3"
        allow_errors: false
    
    # What to look for
    pass_criteria:
      - "All cells execute successfully"
      - "No exceptions raised"
      - "Execution completes within timeout"
    
    fail_criteria:
      - "Any cell raises exception"
      - "Execution times out"
      - "Kernel crash"
    
    # How to fix
    remediation:
      auto_fix: false
      suggestion: "Review stack trace, fix code error, ensure all dependencies installed"
      documentation_url: "https://jupyter-notebook.readthedocs.io/"
    
    # Examples
    examples:
      passing:
        - "All cells in notebook execute and produce expected output"
      failing:
        - "Cell 5 raises NameError: name 'pd' is not defined"
        - "Cell 10 times out after 5 minutes"

  - id: "CODE-EXEC-002"
    name: "Python scripts execute without errors"
    description: "All .py files must run without raising exceptions"
    severity: "critical"
    blocking: true
    auto_fixable: false
    check_type: "automated"
    
    validation:
      method: "execute_script"
      timeout_seconds: 120
      parameters:
        python_version: "3.10"
    
    pass_criteria:
      - "Script exits with code 0"
      - "No exceptions raised"
    
    fail_criteria:
      - "Non-zero exit code"
      - "Unhandled exception"
    
    remediation:
      auto_fix: false
      suggestion: "Fix syntax or runtime errors, add try-except for expected errors"
      documentation_url: ""

# Related standards
related_standards:
  - "TECH-DEP-001"  # Dependency management (must install deps first)
  - "TECH-FILE-001"  # File integrity (files must exist to execute)

# Changelog
changelog:
  - version: "1.0.0"
    date: "2026-01-12"
    changes: "Initial standard definition"
```

---

## Technical Standards

### 1. Code Execution Standard (`technical/code_execution.yaml`)

**Purpose**: Ensure all course code executes without errors

**Requirements**:
- `CODE-EXEC-001`: Jupyter notebooks execute without errors
- `CODE-EXEC-002`: Python scripts execute without errors
- `CODE-EXEC-003`: Output matches expected results (if reference provided)
- `CODE-EXEC-004`: Execution completes within reasonable time

**Profiles**:
- **Strict**: 100% pass rate, all code must execute
- **Standard**: 95% pass rate
- **Relaxed**: 80% pass rate

---

### 2. Link Validity Standard (`technical/link_validity.yaml`)

**Purpose**: Ensure all links are valid and not broken

**Requirements**:
- `LINK-001`: HTTP/HTTPS links return 200 OK
- `LINK-002`: Internal links point to existing files
- `LINK-003`: Anchor links point to existing IDs
- `LINK-004`: No 404, 403, or timeout errors

**Validation Method**: `requests` library with retry logic

**Auto-Fix**: Update broken links to current versions (if known)

---

### 3. File Integrity Standard (`technical/file_integrity.yaml`)

**Purpose**: Verify all referenced files exist

**Requirements**:
- `FILE-001`: All files referenced in code exist
- `FILE-002`: All images/videos/datasets exist
- `FILE-003`: Directory structure matches expected layout
- `FILE-004`: Required files present (README, requirements.txt)
- `FILE-005`: File naming conventions followed

**File Naming Convention**:
```yaml
naming_rules:
  - pattern: "^[a-z0-9_-]+$"
    description: "Lowercase, numbers, underscores, hyphens only"
  - no_spaces: true
  - no_special_chars: true
  - extensions:
      python: [".py"]
      jupyter: [".ipynb"]
      markdown: [".md"]
      data: [".csv", ".json", ".parquet"]
```

---

### 4. Dependency Management Standard (`technical/dependency_management.yaml`)

**Purpose**: Validate dependencies and check for conflicts

**Requirements**:
- `DEP-001`: requirements.txt exists and is parseable
- `DEP-002`: All packages are installable
- `DEP-003`: No version conflicts
- `DEP-004`: No critical security vulnerabilities (checked by Security Agent)
- `DEP-005`: No extremely outdated packages (>2 years old gets warning)

**Version Policy**:
```yaml
version_policy:
  max_age_years: 2
  warn_on_outdated: true
  suggest_updates: true
  pin_exact_versions: false  # Use >= instead of ==
```

---

### 5. Notebook Validation Standard (`technical/notebook_validation.yaml`)

**Purpose**: Check notebook metadata and structure

**Requirements**:
- `NB-001`: Valid notebook format (nbformat v4+)
- `NB-002`: Kernel name is valid
- `NB-003`: Cell execution order is sequential
- `NB-004`: No corrupted cells
- `NB-005`: Cell outputs present or cleared (configurable)

**Metadata Requirements**:
```yaml
required_metadata:
  kernel_name: true
  language_info: true
  kernelspec: true

recommended_metadata:
  author: true
  course_name: true
  lesson_number: true
```

---

### 6. Build Testing Standard (`technical/build_testing.yaml`)

**Purpose**: Test Docker builds and docker-compose startup

**Requirements**:
- `BUILD-001`: Dockerfile builds without errors (if present)
- `BUILD-002`: docker-compose up succeeds (if present)
- `BUILD-003`: Container startup time <2 minutes
- `BUILD-004`: Health checks pass
- `BUILD-005`: No error messages in container logs

---

## Pedagogical Standards

### 1. Learning Objectives Standard (`pedagogical/learning_objectives.yaml`)

**Purpose**: Ensure learning objectives are clear and measurable

**Requirements**:
- `OBJ-001`: Objectives use action verbs from Bloom's taxonomy
- `OBJ-002`: Each objective is specific and measurable
- `OBJ-003`: Content coverage aligns with objectives (>90%)
- `OBJ-004`: Objectives match course difficulty level
- `OBJ-005`: Written in learner-friendly language

**Bloom's Taxonomy Verbs**:
```yaml
blooms_taxonomy:
  remember: [define, list, recall, recognize, state]
  understand: [classify, describe, explain, identify, summarize]
  apply: [apply, demonstrate, execute, implement, use]
  analyze: [analyze, compare, contrast, differentiate, examine]
  evaluate: [assess, critique, evaluate, judge, test]
  create: [create, design, develop, formulate, plan]

minimum_level: "understand"  # Course should target at least this level
```

**AI Check**: Use LLM to assess objective quality

---

### 2. Scaffolding Standard (`pedagogical/scaffolding.yaml`)

**Purpose**: Check difficulty progression is logical

**Requirements**:
- `SCAF-001`: Content progresses basic → intermediate → advanced
- `SCAF-002`: Each lesson builds on previous concepts
- `SCAF-003`: No sudden jumps in difficulty
- `SCAF-004`: Prerequisites clearly stated
- `SCAF-005`: Concepts introduced before used

**Difficulty Levels**:
```yaml
difficulty_levels:
  - level: 1
    name: "Basic"
    description: "Fundamentals, no prior knowledge assumed"
  - level: 2
    name: "Intermediate"
    description: "Builds on basics, some experience helpful"
  - level: 3
    name: "Advanced"
    description: "Complex topics, requires solid foundation"

max_jump: 1  # Can't skip from Basic to Advanced
```

---

### 3. Assessment Standard (`pedagogical/assessments.yaml`)

**Purpose**: Validate quiz and assessment quality

**Requirements**:
- `ASSESS-001`: Each learning objective covered by ≥1 assessment
- `ASSESS-002`: Questions match Bloom's level of objectives
- `ASSESS-003`: Multiple choice has 3-5 plausible distractors
- `ASSESS-004`: Answer explanations are clear
- `ASSESS-005`: Mix of question types (MCQ, coding, projects)

**Question Quality Rubric**:
```yaml
mcq_quality:
  num_options: [3, 5]  # 3-5 answer choices
  distractor_quality: "plausible"  # Not obviously wrong
  explanation_required: true
  difficulty_appropriate: true

coding_exercise:
  starter_code_provided: true
  test_cases_included: true
  solution_provided: true
  hints_available: true
```

---

### 4. Engagement Standard (`pedagogical/engagement.yaml`)

**Purpose**: Ensure variety and interactivity

**Requirements**:
- `ENG-001`: ≥3 content types per module (video, text, lab, quiz)
- `ENG-002`: Interactive elements present
- `ENG-003`: <70% passive reading
- `ENG-004`: Videos chunked appropriately (<15 min)
- `ENG-005`: Hands-on practice opportunities throughout

**Content Mix**:
```yaml
content_types:
  - type: "video"
    min_percentage: 0.15
    max_percentage: 0.40
  - type: "reading"
    min_percentage: 0.20
    max_percentage: 0.70
  - type: "lab"
    min_percentage: 0.10
    max_percentage: 0.50
  - type: "quiz"
    min_percentage: 0.05
    max_percentage: 0.20
  - type: "project"
    min_percentage: 0.05
    max_percentage: 0.30
```

---

### 5. Prerequisite Standard (`pedagogical/prerequisites.yaml`)

**Purpose**: Validate prerequisite relationships

**Requirements**:
- `PREREQ-001`: All listed prerequisites exist in catalog
- `PREREQ-002`: Prerequisites are actually used
- `PREREQ-003`: No circular dependencies
- `PREREQ-004`: Prerequisite chain ≤5 courses deep

---

### 6. Completion Time Standard (`pedagogical/completion_time.yaml`)

**Purpose**: Ensure realistic time estimates

**Requirements**:
- `TIME-001`: Estimate within 30% of advertised time
- `TIME-002`: Time commitment is reasonable (<40 hours/week)
- `TIME-003`: Consistent pacing across modules

**Time Estimation**:
```yaml
time_estimates:
  reading_wpm: 200  # Words per minute
  video_multiplier: 1.2  # Account for pausing/rewinding
  coding_exercise_minutes: 30  # Average per exercise
  quiz_minutes_per_question: 2
  project_hours: 4  # Average small project
```

---

## Legal Standards

### 1. License Standard (`legal/licenses.yaml`)

**Purpose**: Ensure license compatibility

**Requirements**:
- `LIC-001`: All third-party code has license information
- `LIC-002`: Licenses are compatible
- `LIC-003`: License files present where required
- `LIC-004`: Attribution requirements met

**License Compatibility Matrix**:
```yaml
compatible_licenses:
  MIT:
    - MIT
    - Apache-2.0
    - BSD-3-Clause
    - CC-BY-4.0
  Apache-2.0:
    - MIT
    - Apache-2.0
    - BSD-3-Clause
  GPL-3.0:
    - GPL-3.0
    - AGPL-3.0
  # GPL not compatible with MIT for distribution

incompatible_combinations:
  - [GPL-3.0, MIT]
  - [AGPL-3.0, Apache-2.0]
  - [proprietary, copyleft]
```

---

### 2. Attribution Standard (`legal/attribution.yaml`)

**Purpose**: Check proper attribution

**Requirements**:
- `ATTR-001`: Images have source attribution
- `ATTR-002`: Code snippets cite original authors
- `ATTR-003`: Datasets credit sources
- `ATTR-004`: Attribution format matches license

**Attribution Formats**:
```yaml
attribution_templates:
  cc_by:
    format: "{title} by {author}, {license}, via {source}"
    example: "Neural Network Diagram by Jane Doe, CC-BY-4.0, via Wikimedia Commons"
  
  code_snippet:
    format: "# Source: {author}, {url}\n# License: {license}"
    example: "# Source: Stack Overflow user johndoe, https://stackoverflow.com/...\n# License: CC-BY-SA"
```

---

### 3. Copyright Standard (`legal/copyright.yaml`)

**Purpose**: Detect copyright violations

**Requirements**:
- `COPYRIGHT-001`: No full reproduction of copyrighted works
- `COPYRIGHT-002`: Fair use limits respected
- `COPYRIGHT-003`: No unauthorized trademarked logos
- `COPYRIGHT-004`: Screen captures follow fair use

**Fair Use Guidelines**:
```yaml
fair_use:
  text_excerpt_max_words: 500
  text_excerpt_percentage: 0.10  # Max 10% of original
  requires_citation: true
  educational_purpose: true
  transformative: true
```

---

### 4. Privacy Standard (`legal/privacy.yaml`)

**Purpose**: Ensure GDPR/CCPA compliance

**Requirements**:
- `PRIV-001`: No real PII in examples
- `PRIV-002`: Privacy policy referenced
- `PRIV-003`: Data collection consent mechanisms
- `PRIV-004`: Anonymized datasets used

**PII Patterns**:
```yaml
pii_patterns:
  email: '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
  ssn: '\b\d{3}-\d{2}-\d{4}\b'
  phone: '\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
  credit_card: '\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b'

exceptions:
  - "example@example.com"  # Generic examples OK
  - "555-555-5555"  # Fake phone numbers OK
```

---

## Accessibility Standards

### 1. WCAG 2.1 Standard (`accessibility/wcag_2_1.yaml`)

**Purpose**: Ensure WCAG 2.1 AA compliance

**Requirements**: Complete WCAG 2.1 Level AA requirements

```yaml
wcag_2_1_aa:
  # Perceivable
  - guideline: "1.1"
    name: "Text Alternatives"
    criteria:
      - id: "1.1.1"
        name: "Non-text Content"
        level: "A"
        requirement: "All images have alt text"
  
  - guideline: "1.2"
    name: "Time-based Media"
    criteria:
      - id: "1.2.1"
        name: "Audio-only and Video-only (Prerecorded)"
        level: "A"
      - id: "1.2.2"
        name: "Captions (Prerecorded)"
        level: "A"
        requirement: "All videos have captions"
      - id: "1.2.4"
        name: "Captions (Live)"
        level: "AA"
  
  # Operable
  - guideline: "2.1"
    name: "Keyboard Accessible"
    criteria:
      - id: "2.1.1"
        name: "Keyboard"
        level: "A"
        requirement: "All functionality keyboard accessible"
  
  # Understandable
  - guideline: "3.1"
    name: "Readable"
    criteria:
      - id: "3.1.1"
        name: "Language of Page"
        level: "A"
      - id: "3.1.2"
        name: "Language of Parts"
        level: "AA"
  
  # Robust
  - guideline: "4.1"
    name: "Compatible"
    criteria:
      - id: "4.1.1"
        name: "Parsing"
        level: "A"
      - id: "4.1.2"
        name: "Name, Role, Value"
        level: "A"

# Full WCAG 2.1 AA requirements (109 success criteria)
# See: https://www.w3.org/WAI/WCAG21/quickref/?versions=2.1&levels=aa
```

---

### 2. Readability Standard (`accessibility/readability.yaml`)

**Purpose**: Ensure appropriate reading level

**Requirements**:
- `READ-001`: Flesch-Kincaid grade level 12-16
- `READ-002`: Average sentence length <25 words
- `READ-003`: Average paragraph length <150 words
- `READ-004`: Technical jargon explained

**Readability Metrics**:
```yaml
readability_metrics:
  flesch_kincaid_grade:
    min: 10
    max: 16
    target: 14
  
  flesch_reading_ease:
    min: 40  # Difficult
    max: 70  # Standard
    target: 60
  
  gunning_fog:
    max: 15

  sentence_length:
    avg_max: 25
    absolute_max: 40

  paragraph_length:
    avg_max: 150
    absolute_max: 250
```

---

### 3. Media Accessibility Standard (`accessibility/media_accessibility.yaml`)

**Purpose**: Ensure accessible media

**Requirements**:
- `MEDIA-001`: All images have descriptive alt text
- `MEDIA-002`: All videos have captions (.vtt or .srt)
- `MEDIA-003`: Captions are time-synced
- `MEDIA-004`: Transcripts available for audio
- `MEDIA-005`: Color is not sole means of conveying info

---

## Security Standards

### 1. Credentials Standard (`security/credentials.yaml`)

**Purpose**: Detect hardcoded credentials

**Requirements**:
- `CRED-001`: No hardcoded passwords
- `CRED-002`: No API keys in code
- `CRED-003`: No database credentials
- `CRED-004`: No auth tokens

**Detection Patterns**:
```yaml
credential_patterns:
  - pattern: 'password\s*=\s*["\'][^"\']+["\']'
    severity: "critical"
    description: "Hardcoded password"
  
  - pattern: 'api[_-]?key\s*=\s*["\'][^"\']+["\']'
    severity: "critical"
    description: "Hardcoded API key"
  
  - pattern: 'AIza[0-9A-Za-z_-]{35}'
    severity: "critical"
    description: "Google API key"
  
  - pattern: 'sk-[a-zA-Z0-9]{48}'
    severity: "critical"
    description: "OpenAI API key"
```

---

### 2. Vulnerabilities Standard (`security/vulnerabilities.yaml`)

**Purpose**: Detect code vulnerabilities

**Requirements**:
- `VULN-001`: No SQL injection vulnerabilities
- `VULN-002`: No command injection
- `VULN-003`: No eval() of user input
- `VULN-004`: No pickle.loads() of untrusted data
- `VULN-005`: No weak cryptography (MD5, SHA1 for security)

**Bandit Rules**: Uses all Bandit security checks

---

### 3. PII Standard (`security/pii.yaml`)

**Purpose**: Detect personally identifiable information

**Requirements**:
- `PII-001`: No real email addresses
- `PII-002`: No real phone numbers
- `PII-003`: No SSN or credit cards
- `PII-004`: Use synthetic data

---

### 4. Safe Examples Standard (`security/safe_examples.yaml`)

**Purpose**: Ensure security examples are safe

**Requirements**:
- `SAFE-001`: SQL injection examples use test DBs
- `SAFE-002`: XSS examples run in iframes
- `SAFE-003`: Dangerous code clearly marked
- `SAFE-004`: Examples include warnings

---

## Brand Standards

### 1. Style Guide Standard (`brand/style_guide.yaml`)

**Purpose**: Enforce writing style

```yaml
style_rules:
  capitalization:
    - term: "Machine Learning"
      rule: "Title case"
    - term: "Python"
      rule: "Capitalize"
  
  punctuation:
    oxford_comma: true
    quote_style: "double"
  
  lists:
    numbered_when: "sequence matters"
    bulleted_when: "no specific order"
```

---

### 2. Terminology Standard (`brand/terminology.yaml`)

**Purpose**: Ensure consistent terminology

```yaml
preferred_terms:
  - term: "DataFrame"
    not: ["dataframe", "data frame", "data-frame"]
    context: "When referring to pandas DataFrame objects"
  
  - term: "machine learning"
    not: ["ML", "Machine Learning"]
    context: "General use (lowercase)"
  
  - term: "Jupyter Notebook"
    not: ["jupyter notebook", "Jupyter notebook"]
```

---

### 3. Formatting Standard (`brand/formatting.yaml`)

**Purpose**: Ensure consistent formatting

```yaml
formatting_rules:
  headings:
    hierarchy: [H1, H2, H3]  # Don't skip levels
    style: "Title Case"
  
  code_blocks:
    language_required: true
    style: "python"  # For Python code
  
  lists:
    marker: "-"  # Consistent bullet marker
```

---

## Content Integrity Standards

### 1. Fact Checking Standard (`content_integrity/fact_checking.yaml`)

**Purpose**: Verify factual accuracy

**Requirements**:
- `FACT-001`: Technical claims are accurate
- `FACT-002`: Statistics have sources
- `FACT-003`: Algorithm descriptions match standards
- `FACT-004`: No outdated info presented as current

---

### 2. Accuracy Standard (`content_integrity/accuracy.yaml`)

**Purpose**: Code follows best practices

**Requirements**:
- `ACC-001`: Code demonstrates recommended patterns
- `ACC-002`: No anti-patterns
- `ACC-003`: Modern syntax used

---

### 3. References Standard (`content_integrity/references.yaml`)

**Purpose**: Ensure current references

**Requirements**:
- `REF-001`: Citations include dates
- `REF-002`: Links point to current versions
- `REF-003`: No defunct tools
- `REF-004`: Academic citations properly formatted

---

### 4. Consistency Standard (`content_integrity/consistency.yaml`)

**Purpose**: Internal consistency

**Requirements**:
- `CONS-001`: Terms defined consistently
- `CONS-002`: Notation consistent
- `CONS-003`: Variable names consistent

---

## Performance Standards

### 1. Load Time Standard (`performance/load_time.yaml`)

**Purpose**: Ensure fast page loads

```yaml
thresholds:
  strict:
    max_load_time_seconds: 2.0
  standard:
    max_load_time_seconds: 3.0
  relaxed:
    max_load_time_seconds: 5.0

lighthouse_scores:
  performance_min: 90  # Lighthouse performance score
```

---

### 2. File Size Standard (`performance/file_size.yaml`)

**Purpose**: Reasonable file sizes

```yaml
file_size_limits:
  images:
    warning_kb: 500
    critical_kb: 1000
  videos:
    warning_mb: 50
    critical_mb: 100
  pdfs:
    warning_mb: 5
    critical_mb: 10
  total_course:
    strict_gb: 1
    standard_gb: 2
    relaxed_gb: 5
```

---

### 3. Video Quality Standard (`performance/video_quality.yaml`)

**Purpose**: Efficient video encoding

```yaml
video_encoding:
  codec: ["h264", "h265"]
  resolution:
    lecture: "1080p"
    demo: "720p"
  bitrate_mbps:
    1080p: 4
    720p: 2.5
  audio_bitrate_kbps: 128
```

---

### 4. Image Optimization Standard (`performance/image_optimization.yaml`)

**Purpose**: Compressed images

```yaml
image_formats:
  preferred: ["webp", "svg"]
  acceptable: ["png", "jpg"]
  discouraged: ["bmp", "tiff"]

compression:
  png_quality: 90
  jpg_quality: 85
  webp_quality: 80
```

---

## Loading Standards in Code

```python
import yaml
from pathlib import Path

class StandardsLoader:
    def __init__(self, standards_dir: str = "standards"):
        self.standards_dir = Path(standards_dir)
        self._cache = {}
    
    def load_standard(self, category: str, filename: str):
        """Load a specific standard YAML file"""
        cache_key = f"{category}/{filename}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        path = self.standards_dir / category / f"{filename}.yaml"
        with open(path) as f:
            standard = yaml.safe_load(f)
        
        self._cache[cache_key] = standard
        return standard
    
    def load_category(self, category: str):
        """Load all standards for a category"""
        category_dir = self.standards_dir / category
        standards = {}
        
        for yaml_file in category_dir.glob("*.yaml"):
            standard = self.load_standard(category, yaml_file.stem)
            standards[yaml_file.stem] = standard
        
        return standards
    
    def get_requirements(self, category: str, profile: str = "standard"):
        """Get requirements for a category filtered by compliance profile"""
        standards = self.load_category(category)
        requirements = []
        
        for standard in standards.values():
            if standard["profiles"][profile]["enabled"]:
                requirements.extend(standard["requirements"])
        
        return requirements
```

---

## Conclusion

The Standards Library provides a comprehensive, maintainable, and extensible foundation for CourseCompliance. By defining standards in YAML, we enable:

- **Version Control**: Track changes over time
- **Customization**: Organizations can modify standards to fit their needs
- **Transparency**: Clear documentation of what's being checked
- **Consistency**: Standardized format across all categories
- **Extensibility**: Easy to add new standards without code changes

All agents reference these standards when performing compliance checks, ensuring consistent and comprehensive validation across the entire course production pipeline.
