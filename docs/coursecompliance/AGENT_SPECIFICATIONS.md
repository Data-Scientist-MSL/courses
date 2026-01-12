# CourseCompliance - Expert Agent Specifications

## Overview

CourseCompliance uses 8 specialized expert agents, each responsible for validating a specific aspect of course quality. Each agent consists of multiple sub-agents that perform granular checks within their domain.

**Agent Result Format** (standardized across all agents):
```python
{
    "agent": "agent_name",
    "status": "pass" | "fail" | "warning" | "error",
    "issues": [
        {
            "id": "unique_issue_id",
            "severity": "critical" | "warning" | "info",
            "category": "agent_category",
            "subcategory": "sub_agent_name",
            "title": "Short issue description",
            "description": "Detailed issue description",
            "file": "path/to/file",
            "line": 123,  # optional
            "code_snippet": "...",  # optional
            "blocking": true | false,
            "auto_fixable": true | false,
            "remediation_suggestion": "How to fix this issue",
            "reference": "URL or standard reference"
        }
    ],
    "summary": {
        "total_checks": 100,
        "passed": 95,
        "failed": 5,
        "warnings": 3,
        "pass_rate": 0.95
    },
    "metadata": {
        "agent_version": "1.0.0",
        "execution_time_seconds": 45.2,
        "timestamp": "2026-01-12T10:30:00Z"
    }
}
```

---

## 1️⃣ Technical Compliance Agent

### Purpose
Validate technical correctness and functionality of all course code, links, files, and build systems.

### Sub-Agents

#### 1.1 Code Execution Checker
**Purpose**: Execute all Jupyter notebooks and Python scripts to verify they run without errors.

**Checks**:
- All `.ipynb` notebooks execute cell-by-cell without exceptions
- All `.py` scripts run without errors
- Output matches expected results (if reference outputs provided)
- Execution completes within reasonable time (timeout: 5 minutes per notebook)
- No unhandled exceptions or warnings

**Tools**: 
- `nbconvert` with `ExecutePreprocessor`
- `subprocess.run()` for Python scripts
- Custom timeout handler

**Pass Criteria**:
- 100% of notebooks execute successfully (Strict profile)
- 95% execute successfully (Standard profile)
- 80% execute successfully (Relaxed profile)

**Example Issue**:
```python
{
    "id": "TECH-CODE-001",
    "severity": "critical",
    "category": "technical",
    "subcategory": "code_execution",
    "title": "Notebook fails to execute - NameError",
    "description": "Cell 5 raises NameError: name 'pd' is not defined. Missing import statement.",
    "file": "lessons/lesson_03/analysis.ipynb",
    "line": 5,
    "code_snippet": "df = pd.read_csv('data.csv')",
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Add 'import pandas as pd' in an earlier cell",
    "reference": "https://pandas.pydata.org/docs/getting_started/install.html"
}
```

#### 1.2 Link Validator
**Purpose**: Check all URLs (internal and external) are valid and not broken.

**Checks**:
- HTTP/HTTPS links return 200 OK (or 3xx redirects)
- Internal links point to existing files/sections
- Relative paths are correct
- No 404 errors, 403 forbidden, or timeouts
- Anchor links point to existing IDs in target documents

**Tools**:
- `requests` library with retry logic
- `beautifulsoup4` for HTML link extraction
- Markdown link parser for .md files

**Pass Criteria**:
- 100% link validity (Strict)
- 90% link validity (Standard)
- 70% link validity (Relaxed)

**Example Issue**:
```python
{
    "id": "TECH-LINK-001",
    "severity": "warning",
    "category": "technical",
    "subcategory": "link_validation",
    "title": "Broken external link - 404 Not Found",
    "description": "Link to https://example.com/deprecated-api returns 404",
    "file": "lessons/lesson_02/index.md",
    "line": 45,
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Update link to current API documentation or remove",
    "reference": ""
}
```

#### 1.3 File Integrity Checker
**Purpose**: Verify all referenced files exist and directory structure is correct.

**Checks**:
- All files referenced in code/markdown exist
- No broken image/video/dataset references
- Directory structure matches expected course layout
- Required files present (README.md, requirements.txt, etc.)
- File naming conventions followed (lowercase, no spaces)

**Tools**:
- `pathlib` for path validation
- `os.path.exists()` checks
- Regex for file reference extraction

**Pass Criteria**:
- All referenced files exist
- Directory structure complete
- Naming conventions followed

**Example Issue**:
```python
{
    "id": "TECH-FILE-001",
    "severity": "critical",
    "category": "technical",
    "subcategory": "file_integrity",
    "title": "Missing dataset file",
    "description": "Referenced file 'data/train.csv' does not exist",
    "file": "lessons/lesson_04/notebook.ipynb",
    "line": 3,
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Add data/train.csv file or update reference",
    "reference": ""
}
```

#### 1.4 Dependency Checker
**Purpose**: Validate requirements.txt and check for conflicting packages or outdated versions.

**Checks**:
- `requirements.txt` exists and is parseable
- All packages installable (`pip install --dry-run`)
- No conflicting version requirements
- No known security vulnerabilities in dependencies (use Safety)
- Versions are not extremely outdated (warn if >2 years old)

**Tools**:
- `pip` with `--dry-run`
- `safety` for vulnerability checking
- `packaging` library for version parsing

**Pass Criteria**:
- All dependencies installable
- No version conflicts
- No critical vulnerabilities

**Example Issue**:
```python
{
    "id": "TECH-DEP-001",
    "severity": "warning",
    "category": "technical",
    "subcategory": "dependencies",
    "title": "Outdated package version",
    "description": "numpy==1.19.0 is outdated (current: 1.26.0, released 2023)",
    "file": "requirements.txt",
    "line": 5,
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Update to numpy>=1.24.0",
    "reference": "https://pypi.org/project/numpy/"
}
```

#### 1.5 Notebook Validator
**Purpose**: Check notebook metadata, kernel names, and output consistency.

**Checks**:
- Kernel name is valid and available (e.g., python3, ir)
- Notebook format version is current
- Cell execution order is sequential (execution_count)
- No corrupted cells or invalid JSON
- Cell outputs are present (if required) or cleared (if preferred)

**Tools**:
- `nbformat` for notebook parsing
- Custom validators for metadata

**Pass Criteria**:
- Valid notebook format
- Correct kernel specified
- Sequential execution order

**Example Issue**:
```python
{
    "id": "TECH-NB-001",
    "severity": "info",
    "category": "technical",
    "subcategory": "notebook_validation",
    "title": "Non-sequential cell execution",
    "description": "Cells executed out of order (1, 2, 5, 3, 4). May confuse learners.",
    "file": "lessons/lesson_01/intro.ipynb",
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Re-run notebook from top to bottom and save",
    "reference": ""
}
```

#### 1.6 Build Tester
**Purpose**: Test Docker builds and docker-compose startup.

**Checks**:
- Dockerfile builds without errors (if present)
- docker-compose up succeeds (if present)
- Container startup time is reasonable (<2 minutes)
- Health checks pass
- Container logs show no errors

**Tools**:
- `docker` SDK for Python
- `docker-compose` via subprocess

**Pass Criteria**:
- Docker build succeeds
- Containers start and pass health checks

**Example Issue**:
```python
{
    "id": "TECH-BUILD-001",
    "severity": "critical",
    "category": "technical",
    "subcategory": "build_testing",
    "title": "Docker build fails",
    "description": "Dockerfile line 12: package 'invalid-pkg' not found",
    "file": "Dockerfile",
    "line": 12,
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Fix package name or remove from Dockerfile",
    "reference": ""
}
```

### Inputs
- `course_path`: Absolute path to course directory
- `config`: Technical standards configuration

### Outputs
- List of technical issues with severity
- Summary statistics (pass rate, execution time)

### Dependencies
- None (runs independently)

---

## 2️⃣ Pedagogical Quality Agent

### Purpose
Ensure educational effectiveness and learning design quality.

### Sub-Agents

#### 2.1 Learning Objectives Checker
**Purpose**: Verify learning objectives are clear, measurable, achievable, and aligned with content.

**Checks**:
- Learning objectives use action verbs (Bloom's taxonomy)
- Each objective is measurable and specific
- Content covers all stated objectives
- Objectives match course difficulty level
- Objectives are written in learner-friendly language

**Tools**:
- LLM (OLLAMA) for objective quality analysis
- Bloom's taxonomy verb list validation
- Content-objective alignment scoring

**Pass Criteria**:
- All objectives use action verbs
- >90% content-objective alignment

**Example Issue**:
```python
{
    "id": "PED-OBJ-001",
    "severity": "warning",
    "category": "pedagogical",
    "subcategory": "learning_objectives",
    "title": "Vague learning objective",
    "description": "Objective 'Understand machine learning' is too vague. Use specific action verb.",
    "file": "course_info/objectives.md",
    "line": 3,
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Replace with 'Apply supervised learning algorithms to classification problems'",
    "reference": "https://tips.uark.edu/using-blooms-taxonomy/"
}
```

#### 2.2 Scaffolding Validator
**Purpose**: Check difficulty progression and logical prerequisites.

**Checks**:
- Content progresses from basic to advanced
- Each lesson builds on previous concepts
- No sudden jumps in difficulty
- Prerequisites are clearly stated
- Concepts introduced before used

**Tools**:
- LLM for difficulty analysis
- Prerequisite graph validation
- Concept dependency tracking

**Pass Criteria**:
- Smooth difficulty progression
- All prerequisites satisfied

**Example Issue**:
```python
{
    "id": "PED-SCAF-001",
    "severity": "warning",
    "category": "pedagogical",
    "subcategory": "scaffolding",
    "title": "Concept used before introduction",
    "description": "Lesson 3 uses 'gradient descent' which is introduced in Lesson 5",
    "file": "lessons/lesson_03/index.md",
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Move gradient descent introduction to Lesson 2 or reorder lessons",
    "reference": ""
}
```

#### 2.3 Assessment Quality Checker
**Purpose**: Validate quizzes cover all objectives and have appropriate difficulty.

**Checks**:
- Each learning objective covered by ≥1 assessment question
- Questions match Bloom's level of objectives
- Multiple choice questions have plausible distractors
- Answer explanations are clear
- Mix of question types (MCQ, coding, projects)

**Tools**:
- LLM for question quality analysis
- Objective-assessment mapping

**Pass Criteria**:
- 100% objective coverage
- Quality scores >80%

**Example Issue**:
```python
{
    "id": "PED-ASSESS-001",
    "severity": "warning",
    "category": "pedagogical",
    "subcategory": "assessments",
    "title": "Uncovered learning objective",
    "description": "Objective 'Evaluate model performance using cross-validation' not assessed in quizzes",
    "file": "assessments/quiz_02.md",
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Add quiz question on cross-validation techniques",
    "reference": ""
}
```

#### 2.4 Engagement Analyzer
**Purpose**: Check for variety and interactive elements.

**Checks**:
- Mix of content types (videos, text, labs, quizzes, projects)
- Interactive elements present (code exercises, simulations)
- Not too much passive reading (>80% text is warning)
- Videos are appropriately chunked (<15 minutes)
- Hands-on practice opportunities throughout

**Tools**:
- Content type detection
- Engagement score calculation

**Pass Criteria**:
- ≥3 content types per module
- <70% passive content

**Example Issue**:
```python
{
    "id": "PED-ENG-001",
    "severity": "info",
    "category": "pedagogical",
    "subcategory": "engagement",
    "title": "Excessive passive content",
    "description": "Module 2 is 85% reading with no interactive elements",
    "file": "lessons/module_02/",
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Add coding exercise or quiz to break up reading",
    "reference": ""
}
```

#### 2.5 Prerequisite Validator
**Purpose**: Verify prerequisite courses exist and are necessary.

**Checks**:
- All listed prerequisites exist in course catalog
- Prerequisites are actually needed (concepts used)
- No circular dependencies
- Prerequisite chain is reasonable (<5 courses deep)

**Tools**:
- Course catalog lookup
- Concept usage tracking

**Pass Criteria**:
- All prerequisites valid
- No circular dependencies

#### 2.6 Completion Time Estimator
**Purpose**: Estimate realistic completion time and compare with advertised duration.

**Checks**:
- Calculate time based on content (reading speed, video length, exercise time)
- Compare estimate vs. advertised time
- Warn if >30% discrepancy
- Check if time commitment is reasonable (not too dense)

**Tools**:
- Reading speed calculator (200 words/min)
- Video duration extraction
- Exercise complexity scoring

**Pass Criteria**:
- Estimate within 30% of advertised time

**Example Issue**:
```python
{
    "id": "PED-TIME-001",
    "severity": "warning",
    "category": "pedagogical",
    "subcategory": "completion_time",
    "title": "Underestimated completion time",
    "description": "Estimated time 8.5 hours, advertised as 4 hours (113% over)",
    "file": "course_info/metadata.yaml",
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Update advertised time to 8-10 hours or reduce content",
    "reference": ""
}
```

### Inputs
- `course_path`: Course directory
- `course_metadata`: Learning objectives, prerequisites
- `technical_results`: From Technical Agent (dependency)

### Outputs
- Pedagogical issues and improvement suggestions

### Dependencies
- Requires Technical Agent success (needs working code to analyze exercises)

---

## 3️⃣ Legal Compliance Agent

### Purpose
Ensure legal compliance for licensing, attribution, privacy, and copyright.

### Sub-Agents

#### 3.1 License Checker
**Purpose**: Verify all content licenses are compatible.

**Checks**:
- All third-party code has license information
- Licenses are compatible with course license (e.g., MIT + Apache OK, GPL + proprietary not OK)
- License files present where required
- Attribution requirements met for CC-BY, etc.

**Tools**:
- License compatibility matrix
- License file parsing
- SPDX license identifier recognition

**Pass Criteria**:
- All licenses compatible
- No license conflicts

**Example Issue**:
```python
{
    "id": "LEGAL-LIC-001",
    "severity": "critical",
    "category": "legal",
    "subcategory": "licensing",
    "title": "Incompatible license - GPL code in MIT course",
    "description": "File uses GPL-licensed code, incompatible with course MIT license",
    "file": "utils/helper.py",
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Replace with MIT/Apache licensed alternative or relicense course as GPL",
    "reference": "https://choosealicense.com/appendix/"
}
```

#### 3.2 Attribution Validator
**Purpose**: Check all third-party content has proper attribution.

**Checks**:
- Images have source attribution
- Code snippets cite original authors
- Datasets credit sources
- Attribution format matches license requirements
- No missing credits

**Tools**:
- Attribution pattern matching
- Image metadata extraction (EXIF)

**Pass Criteria**:
- All third-party content attributed

**Example Issue**:
```python
{
    "id": "LEGAL-ATTR-001",
    "severity": "warning",
    "category": "legal",
    "subcategory": "attribution",
    "title": "Missing image attribution",
    "description": "Image appears to be from Wikimedia Commons but lacks attribution",
    "file": "lessons/lesson_01/images/diagram.png",
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Add caption: 'Image by Author Name, CC-BY-SA 4.0, via Wikimedia Commons'",
    "reference": "https://creativecommons.org/use-remix/attribution/"
}
```

#### 3.3 Copyright Scanner
**Purpose**: Detect potentially copyrighted material without permission.

**Checks**:
- No full reproduction of copyrighted books/articles
- Fair use limits respected (short excerpts with citation OK)
- No unauthorized use of trademarked logos
- Screen captures follow fair use guidelines
- No pirated content

**Tools**:
- Copyright detection heuristics
- Image similarity search
- Text plagiarism detection

**Pass Criteria**:
- No copyright violations detected

#### 3.4 Privacy Checker
**Purpose**: Ensure GDPR/CCPA compliance and no PII in examples.

**Checks**:
- No real personal data in examples (names, emails, SSN, etc.)
- Privacy policy referenced
- Data collection consent mechanisms in place
- No tracking without disclosure
- Anonymized datasets used

**Tools**:
- PII detection patterns (regex + NER)
- GDPR compliance checklist

**Pass Criteria**:
- No PII in course content
- Privacy policy present

**Example Issue**:
```python
{
    "id": "LEGAL-PRIV-001",
    "severity": "critical",
    "category": "legal",
    "subcategory": "privacy",
    "title": "Personal data in example",
    "description": "Example CSV contains real email addresses and phone numbers",
    "file": "data/customer_data.csv",
    "blocking": true,
    "auto_fixable": true,
    "remediation_suggestion": "Replace with synthetic data using Faker library",
    "reference": "https://gdpr.eu/data-privacy/"
}
```

#### 3.5 Terms Validator
**Purpose**: Verify Terms & Conditions references are correct.

**Checks**:
- Terms of use referenced in course materials
- Links to terms are current and valid
- Terms cover course-specific usage (data downloads, API access)
- User consent mechanisms present where needed

**Tools**:
- Link validation
- Terms content checking

**Pass Criteria**:
- Valid terms references

#### 3.6 Third-Party Checker
**Purpose**: Validate licenses for datasets, libraries, and media.

**Checks**:
- Third-party datasets have license information
- Video/audio tracks are properly licensed
- Fonts used are licensed for educational use
- Icons/graphics have appropriate licenses

**Tools**:
- License metadata extraction
- Third-party asset inventory

**Pass Criteria**:
- All third-party assets licensed appropriately

### Inputs
- `course_path`: Course directory
- `course_metadata`: License information
- `third_party_assets`: Inventory of external content

### Outputs
- Legal issues, required attributions, license conflicts

### Dependencies
- None (runs independently)

---

## 4️⃣ Accessibility Agent

### Purpose
Ensure WCAG 2.1 AA compliance for inclusive learning.

### Sub-Agents

#### 4.1 WCAG Checker
**Purpose**: Run axe-core accessibility tests on HTML content.

**Checks**:
- WCAG 2.1 Level A compliance (required)
- WCAG 2.1 Level AA compliance (required)
- Semantic HTML usage (headings, landmarks)
- Form labels and ARIA attributes
- Focus indicators visible

**Tools**:
- `axe-core` via Selenium or Playwright
- HTML structure validation

**Pass Criteria**:
- 100% WCAG 2.1 AA compliance (Strict)
- 85% compliance (Standard)
- Basic compliance (Relaxed)

**Example Issue**:
```python
{
    "id": "A11Y-WCAG-001",
    "severity": "critical",
    "category": "accessibility",
    "subcategory": "wcag",
    "title": "Missing form label - WCAG 3.3.2",
    "description": "Input field lacks associated <label> element",
    "file": "interactive/quiz.html",
    "line": 45,
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Add <label for='input-id'>Label Text</label>",
    "reference": "https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions"
}
```

#### 4.2 Alt Text Validator
**Purpose**: Verify all images have descriptive alt text.

**Checks**:
- All `<img>` tags have alt attribute
- Alt text is descriptive (not "image" or "picture")
- Decorative images have alt=""
- Complex images have long descriptions
- Charts/graphs have data tables or detailed descriptions

**Tools**:
- HTML/Markdown parsing
- Alt text quality scoring (LLM)

**Pass Criteria**:
- 100% images have alt text

**Example Issue**:
```python
{
    "id": "A11Y-ALT-001",
    "severity": "critical",
    "category": "accessibility",
    "subcategory": "alt_text",
    "title": "Missing alt text",
    "description": "Image has no alt attribute",
    "file": "lessons/lesson_02/index.html",
    "line": 67,
    "blocking": true,
    "auto_fixable": true,
    "remediation_suggestion": "Add alt='Scatter plot showing positive correlation between X and Y'",
    "reference": "https://www.w3.org/WAI/tutorials/images/"
}
```

#### 4.3 Caption Checker
**Purpose**: Check all videos have captions/subtitles.

**Checks**:
- Video files have associated .vtt or .srt files
- Captions are time-synced
- Captions include speaker identification
- Non-speech sounds described [applause], [music]
- Caption quality is good (not auto-generated gibberish)

**Tools**:
- VTT/SRT file detection
- Caption quality scoring

**Pass Criteria**:
- 100% videos captioned

**Example Issue**:
```python
{
    "id": "A11Y-CAP-001",
    "severity": "critical",
    "category": "accessibility",
    "subcategory": "captions",
    "title": "Missing video captions",
    "description": "Video file has no associated caption file (.vtt or .srt)",
    "file": "videos/intro.mp4",
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Generate captions using automated tool, then manually review",
    "reference": "https://www.w3.org/WAI/media/av/captions/"
}
```

#### 4.4 Color Contrast Checker
**Purpose**: Ensure text meets 4.5:1 contrast ratio.

**Checks**:
- Text colors meet WCAG AA contrast (4.5:1 for normal, 3:1 for large)
- Important UI elements have sufficient contrast
- Color is not sole means of conveying information
- Dark mode (if present) also meets contrast requirements

**Tools**:
- Color contrast calculator
- Screenshot analysis for rendered colors

**Pass Criteria**:
- All text meets contrast ratio

**Example Issue**:
```python
{
    "id": "A11Y-CON-001",
    "severity": "warning",
    "category": "accessibility",
    "subcategory": "color_contrast",
    "title": "Insufficient color contrast",
    "description": "Text color #888 on background #FFF has contrast ratio 3.5:1 (need 4.5:1)",
    "file": "styles/main.css",
    "line": 23,
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Change text color to #757575 for 4.5:1 contrast",
    "reference": "https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum"
}
```

#### 4.5 Readability Scorer
**Purpose**: Check reading level appropriate for audience.

**Checks**:
- Flesch-Kincaid grade level appropriate (Grade 12-14 for technical content)
- Sentence length reasonable (<25 words average)
- Paragraph length reasonable (<150 words)
- Technical jargon explained
- Active voice preferred over passive

**Tools**:
- `readability-score` library
- Flesch-Kincaid calculator
- Gunning Fog index

**Pass Criteria**:
- Reading level Grade 12-16

**Example Issue**:
```python
{
    "id": "A11Y-READ-001",
    "severity": "info",
    "category": "accessibility",
    "subcategory": "readability",
    "title": "High reading level",
    "description": "Section has Flesch-Kincaid grade level 18 (college graduate), target is 14",
    "file": "lessons/lesson_05/theory.md",
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Simplify sentences, break long paragraphs, explain jargon",
    "reference": "https://readable.com/readability/flesch-reading-ease-flesch-kincaid-grade-level/"
}
```

#### 4.6 Keyboard Navigation Checker
**Purpose**: Verify all interactive elements are keyboard accessible.

**Checks**:
- All interactive elements reachable via Tab key
- Focus order is logical
- Skip links present for long pages
- No keyboard traps
- Custom controls have keyboard support

**Tools**:
- Automated keyboard navigation testing
- Tab order analysis

**Pass Criteria**:
- All interactions keyboard accessible

#### 4.7 Screen Reader Tester
**Purpose**: Test compatibility with screen readers.

**Checks**:
- ARIA labels present where needed
- Semantic HTML used (headings for structure)
- Form fields properly labeled
- Dynamic content changes announced
- Error messages programmatically associated with fields

**Tools**:
- Screen reader simulation
- ARIA attribute validation

**Pass Criteria**:
- Screen reader compatible

### Inputs
- `course_path`: HTML, Markdown, videos, slides

### Outputs
- Accessibility violations with WCAG rule references

### Dependencies
- None (runs independently)

---

## 5️⃣ Security Agent

### Purpose
Detect security vulnerabilities and sensitive data exposure.

### Sub-Agents

#### 5.1 Credential Scanner
**Purpose**: Detect hardcoded passwords, API keys, tokens.

**Checks**:
- No passwords in code or config files
- No API keys (patterns: AIza..., sk-...)
- No database connection strings with credentials
- No auth tokens hardcoded
- Credentials in .env or environment variables only

**Tools**:
- Regex patterns for common credential formats
- Entropy analysis for high-entropy strings

**Pass Criteria**:
- Zero hardcoded credentials

**Example Issue**:
```python
{
    "id": "SEC-CRED-001",
    "severity": "critical",
    "category": "security",
    "subcategory": "credentials",
    "title": "Hardcoded API key detected",
    "description": "API key found in source code: 'AIza***REDACTED***'",
    "file": "src/api_client.py",
    "line": 12,
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Move to environment variable: os.environ.get('API_KEY')",
    "reference": "https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password"
}
```

#### 5.2 Secret Detector
**Purpose**: Find AWS keys, GitHub tokens, private keys.

**Checks**:
- No AWS access keys (AKIA...)
- No GitHub personal access tokens (ghp_...)
- No private SSH/SSL keys
- No OAuth client secrets
- No JWT secrets

**Tools**:
- `truffleHog` for secret detection
- Custom secret patterns

**Pass Criteria**:
- Zero secrets exposed

#### 5.3 Code Vulnerability Scanner
**Purpose**: Check for known code vulnerabilities using Bandit.

**Checks**:
- No SQL injection vulnerabilities
- No command injection (subprocess with shell=True)
- No eval() of user input
- No pickle.loads() of untrusted data
- No weak cryptography (MD5, SHA1 for security)

**Tools**:
- `Bandit` for Python security linting
- CWE (Common Weakness Enumeration) mapping

**Pass Criteria**:
- Zero high-severity vulnerabilities

**Example Issue**:
```python
{
    "id": "SEC-VULN-001",
    "severity": "critical",
    "category": "security",
    "subcategory": "vulnerabilities",
    "title": "SQL Injection vulnerability",
    "description": "SQL query uses string formatting, vulnerable to injection",
    "file": "database/queries.py",
    "line": 34,
    "code_snippet": "query = f'SELECT * FROM users WHERE id = {user_id}'",
    "blocking": true,
    "auto_fixable": true,
    "remediation_suggestion": "Use parameterized query: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))",
    "reference": "https://cwe.mitre.org/data/definitions/89.html"
}
```

#### 5.4 Injection Checker
**Purpose**: Ensure SQL injection examples are safe, XSS examples sandboxed.

**Checks**:
- SQL injection examples use safe test databases
- XSS examples run in isolated iframes
- Code injection examples clearly marked as educational
- Dangerous examples have warnings
- No actual exploitable vulnerabilities in teaching materials

**Tools**:
- Context analysis for examples
- Warning label detection

**Pass Criteria**:
- All dangerous examples properly sandboxed/warned

#### 5.5 Dependency Security Checker
**Purpose**: Scan for vulnerable package versions using Safety.

**Checks**:
- No packages with known CVEs
- No packages with security advisories
- Dependencies reasonably up-to-date
- No abandoned packages (last update >3 years)

**Tools**:
- `safety` library
- CVE database lookup
- PyPI metadata

**Pass Criteria**:
- Zero critical vulnerabilities

**Example Issue**:
```python
{
    "id": "SEC-DEP-001",
    "severity": "critical",
    "category": "security",
    "subcategory": "dependency_security",
    "title": "Vulnerable dependency - CVE-2023-1234",
    "description": "requests==2.25.0 has known RCE vulnerability (CVE-2023-1234)",
    "file": "requirements.txt",
    "line": 3,
    "blocking": true,
    "auto_fixable": true,
    "remediation_suggestion": "Update to requests>=2.31.0",
    "reference": "https://nvd.nist.gov/vuln/detail/CVE-2023-1234"
}
```

#### 5.6 PII Scanner
**Purpose**: Detect personally identifiable information in examples.

**Checks**:
- No real SSN, credit card numbers
- No real email addresses (except generic examples)
- No real phone numbers
- No real addresses
- Use synthetic/anonymized data

**Tools**:
- NER (Named Entity Recognition)
- PII regex patterns
- Luhn algorithm for credit cards

**Pass Criteria**:
- No real PII in course content

### Inputs
- `course_path`: Code files, notebooks, configuration files

### Outputs
- Security issues with CVE references if applicable

### Dependencies
- None (runs independently)

---

## 6️⃣ Brand Consistency Agent

### Purpose
Ensure brand guidelines and style consistency.

### Sub-Agents

#### 6.1 Style Guide Checker
**Purpose**: Verify adherence to writing style guide.

**Checks**:
- Consistent capitalization (e.g., "Machine Learning" vs "machine learning")
- Punctuation style matches guide
- List formatting consistent (numbered vs. bulleted)
- Code formatting style (e.g., PEP 8)
- Markdown style consistent

**Tools**:
- Style guide rules (YAML configuration)
- Custom linters

**Pass Criteria**:
- >90% style guide compliance

**Example Issue**:
```python
{
    "id": "BRAND-STYLE-001",
    "severity": "info",
    "category": "brand",
    "subcategory": "style_guide",
    "title": "Inconsistent capitalization",
    "description": "Use 'Machine Learning' (title case) per style guide, found 'machine learning'",
    "file": "lessons/lesson_01/index.md",
    "line": 12,
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Replace with 'Machine Learning'",
    "reference": "style_guide.md#capitalization"
}
```

#### 6.2 Terminology Validator
**Purpose**: Check consistent use of technical terms.

**Checks**:
- Consistent terminology (e.g., "dataframe" vs "data frame" vs "DataFrame")
- Preferred terms used (e.g., "function" not "method" for standalone functions)
- Abbreviations defined on first use
- No conflicting definitions of same term

**Tools**:
- Terminology dictionary (YAML)
- Term usage tracking

**Pass Criteria**:
- Consistent terminology throughout

**Example Issue**:
```python
{
    "id": "BRAND-TERM-001",
    "severity": "warning",
    "category": "brand",
    "subcategory": "terminology",
    "title": "Inconsistent terminology",
    "description": "Term 'neural network' used here, 'neural net' used in Lesson 2. Be consistent.",
    "file": "lessons/lesson_03/index.md",
    "line": 45,
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Use 'neural network' consistently (preferred term)",
    "reference": "terminology.yaml"
}
```

#### 6.3 Tone Analyzer
**Purpose**: Ensure appropriate tone (educational, encouraging).

**Checks**:
- Tone is professional but friendly
- No condescending language ("Obviously...", "Clearly...")
- Encouraging language used ("You can...", "Let's...")
- Second person "you" preferred over "we" or passive voice
- No overly casual slang

**Tools**:
- LLM (OLLAMA) for tone analysis
- Tone scoring rubric

**Pass Criteria**:
- Appropriate educational tone

**Example Issue**:
```python
{
    "id": "BRAND-TONE-001",
    "severity": "info",
    "category": "brand",
    "subcategory": "tone",
    "title": "Condescending language",
    "description": "Phrase 'Obviously, you should...' may sound condescending to learners",
    "file": "lessons/lesson_04/index.md",
    "line": 23,
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Replace with 'As you can see, ...' or 'Notice that...'",
    "reference": ""
}
```

#### 6.4 Visual Identity Checker
**Purpose**: Verify brand colors, logos used correctly.

**Checks**:
- Brand colors used (hex codes match)
- Logo files are official versions
- Logo placement follows guidelines
- Font usage follows brand guidelines
- Color palette consistent

**Tools**:
- Color extraction from images/CSS
- Logo file hash comparison

**Pass Criteria**:
- Brand assets used correctly

#### 6.5 Formatting Validator
**Purpose**: Check consistent formatting (headings, code blocks, lists).

**Checks**:
- Heading hierarchy logical (H1 → H2 → H3, no skips)
- Code blocks have language specified
- Lists use consistent markers
- Emphasis (bold/italic) used appropriately
- Tables formatted consistently

**Tools**:
- Markdown linting
- HTML structure validation

**Pass Criteria**:
- Consistent formatting

**Example Issue**:
```python
{
    "id": "BRAND-FMT-001",
    "severity": "info",
    "category": "brand",
    "subcategory": "formatting",
    "title": "Skipped heading level",
    "description": "H1 followed by H3 (skips H2). Use hierarchical headings.",
    "file": "lessons/lesson_02/index.md",
    "line": 15,
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Change H3 to H2",
    "reference": ""
}
```

### Inputs
- `course_path`: All content
- `brand_guidelines`: YAML configuration

### Outputs
- Brand inconsistencies, style violations

### Dependencies
- None (runs independently)

---

## 7️⃣ Content Integrity Agent

### Purpose
Validate factual accuracy and content quality.

### Sub-Agents

#### 7.1 Fact Checker
**Purpose**: Verify technical facts against authoritative sources.

**Checks**:
- Technical claims are accurate
- Statistics/numbers have sources
- Algorithm descriptions match standard definitions
- Mathematical formulas correct
- No outdated information presented as current

**Tools**:
- RAG system with authoritative sources (documentation, textbooks, papers)
- LLM (OLLAMA) for fact verification

**Pass Criteria**:
- >95% factual accuracy

**Example Issue**:
```python
{
    "id": "CONTENT-FACT-001",
    "severity": "critical",
    "category": "content_integrity",
    "subcategory": "fact_checking",
    "title": "Factual error",
    "description": "Statement 'Python was created in 1995' is incorrect (actually 1991)",
    "file": "lessons/lesson_01/history.md",
    "line": 8,
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Correct to 'Python was created in 1991 by Guido van Rossum'",
    "reference": "https://www.python.org/doc/essays/foreword/"
}
```

#### 7.2 Accuracy Validator
**Purpose**: Check code examples follow best practices.

**Checks**:
- Code examples demonstrate recommended patterns
- No anti-patterns taught as good practice
- Performance implications mentioned where relevant
- Edge cases handled appropriately
- Modern syntax used (not deprecated)

**Tools**:
- Code quality analysis
- Best practice checklist

**Pass Criteria**:
- Code follows best practices

**Example Issue**:
```python
{
    "id": "CONTENT-ACC-001",
    "severity": "warning",
    "category": "content_integrity",
    "subcategory": "accuracy",
    "title": "Anti-pattern in example",
    "description": "Example uses mutable default argument, a known Python anti-pattern",
    "file": "lessons/lesson_03/functions.py",
    "line": 5,
    "code_snippet": "def append_to(element, to=[]):",
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Use 'def append_to(element, to=None): to = to or []'",
    "reference": "https://docs.python-guide.org/writing/gotchas/#mutable-default-arguments"
}
```

#### 7.3 Reference Checker
**Purpose**: Ensure all references/citations are up-to-date.

**Checks**:
- Citations include publication dates
- References point to current versions (not deprecated docs)
- External documentation links are current
- No references to defunct tools/libraries
- Academic citations properly formatted

**Tools**:
- Link checking
- Publication date extraction
- Citation format validation

**Pass Criteria**:
- References current and properly cited

**Example Issue**:
```python
{
    "id": "CONTENT-REF-001",
    "severity": "warning",
    "category": "content_integrity",
    "subcategory": "references",
    "title": "Outdated reference",
    "description": "Link points to Python 2.7 docs, should use Python 3.x docs",
    "file": "lessons/lesson_05/index.md",
    "line": 67,
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Update link to https://docs.python.org/3/",
    "reference": ""
}
```

#### 7.4 Consistency Checker
**Purpose**: Check internal consistency (definitions, notation).

**Checks**:
- Terms defined consistently
- Mathematical notation consistent
- Variable names consistent across examples
- Concepts explained before referenced
- No contradictory statements

**Tools**:
- Definition tracking
- Notation extraction and comparison

**Pass Criteria**:
- Internal consistency maintained

**Example Issue**:
```python
{
    "id": "CONTENT-CONS-001",
    "severity": "warning",
    "category": "content_integrity",
    "subcategory": "consistency",
    "title": "Inconsistent notation",
    "description": "Variable 'X' represents feature matrix in Lesson 2 but input vector in Lesson 3",
    "file": "lessons/lesson_03/index.md",
    "line": 12,
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Use consistent notation or clearly state when context changes",
    "reference": ""
}
```

#### 7.5 Plagiarism Detector
**Purpose**: Detect copied content without attribution.

**Checks**:
- No large blocks of text copied from other sources
- Paraphrased content is sufficiently transformed
- All quotes properly cited
- Code snippets from Stack Overflow/GitHub cited
- No unattributed course materials from competitors

**Tools**:
- Text similarity analysis
- Code similarity detection
- Web search for matching content

**Pass Criteria**:
- No plagiarism detected

**Example Issue**:
```python
{
    "id": "CONTENT-PLAG-001",
    "severity": "critical",
    "category": "content_integrity",
    "subcategory": "plagiarism",
    "title": "Potential plagiarism",
    "description": "Paragraph has 95% similarity to Wikipedia article without citation",
    "file": "lessons/lesson_02/background.md",
    "line": 34,
    "blocking": true,
    "auto_fixable": false,
    "remediation_suggestion": "Add citation or rewrite in original words",
    "reference": "https://en.wikipedia.org/wiki/Machine_learning"
}
```

### Inputs
- `course_path`: Course content
- `knowledge_base`: Authoritative sources
- `previous_version`: For comparison (optional)

### Outputs
- Factual errors, outdated references, inconsistencies

### Dependencies
- Requires Technical Agent success (needs validated content to check)

---

## 8️⃣ Performance Agent

### Purpose
Ensure optimal performance and user experience.

### Sub-Agents

#### 8.1 Load Time Checker
**Purpose**: Measure page load times for HTML content.

**Checks**:
- HTML pages load in <3 seconds
- No render-blocking resources
- Critical CSS inlined
- JavaScript loads asynchronously where possible
- No excessive DOM depth

**Tools**:
- `Lighthouse` performance audit
- Custom timing measurements

**Pass Criteria**:
- Load times <3s (95th percentile)

**Example Issue**:
```python
{
    "id": "PERF-LOAD-001",
    "severity": "warning",
    "category": "performance",
    "subcategory": "load_time",
    "title": "Slow page load",
    "description": "Page load time 5.2s, target <3s. Large image causing delay.",
    "file": "lessons/lesson_04/index.html",
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Compress image 'diagram.png' or use lazy loading",
    "reference": "https://web.dev/performance-scoring/"
}
```

#### 8.2 File Size Optimizer
**Purpose**: Check file sizes are reasonable.

**Checks**:
- Images <500KB (warn if >1MB)
- Videos appropriately compressed (not raw 4K)
- PDFs optimized (<5MB per file)
- No unnecessary large files (e.g., uncompressed datasets)
- Overall course bundle <1GB

**Tools**:
- File size analysis
- Compression ratio checking

**Pass Criteria**:
- Files reasonably sized

**Example Issue**:
```python
{
    "id": "PERF-SIZE-001",
    "severity": "warning",
    "category": "performance",
    "subcategory": "file_size",
    "title": "Large image file",
    "description": "Image is 2.4MB, recommend <500KB for web",
    "file": "images/architecture.png",
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Compress to WebP format or reduce resolution",
    "reference": ""
}
```

#### 8.3 Video Quality Checker
**Purpose**: Verify video compression is appropriate.

**Checks**:
- Video codec is efficient (H.264 or H.265)
- Bitrate appropriate for resolution (not excessive)
- Resolution matches use case (1080p for lectures, 720p acceptable)
- Audio bitrate reasonable (128-192 kbps)
- Duration/file size ratio reasonable

**Tools**:
- `ffprobe` for video analysis
- Bitrate calculation

**Pass Criteria**:
- Videos efficiently encoded

**Example Issue**:
```python
{
    "id": "PERF-VID-001",
    "severity": "info",
    "category": "performance",
    "subcategory": "video_quality",
    "title": "Inefficient video encoding",
    "description": "Video uses 10 Mbps bitrate for 720p (4 Mbps sufficient)",
    "file": "videos/lecture_01.mp4",
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Re-encode with H.264, CRF 23, 4 Mbps target bitrate",
    "reference": ""
}
```

#### 8.4 Image Optimizer
**Purpose**: Check images are compressed.

**Checks**:
- PNG images compressed (optipng/pngquant)
- Use WebP for photos (better compression than JPEG)
- SVG for diagrams/icons where possible
- No BMP or TIFF formats (inefficient for web)
- Dimensions appropriate (not serving 4K image at 800px width)

**Tools**:
- Image format detection
- Compression ratio analysis
- ImageMagick for optimization

**Pass Criteria**:
- Images optimized for web

**Example Issue**:
```python
{
    "id": "PERF-IMG-001",
    "severity": "info",
    "category": "performance",
    "subcategory": "image_optimization",
    "title": "Unoptimized PNG",
    "description": "PNG can be reduced by 60% with lossless compression",
    "file": "images/screenshot.png",
    "blocking": false,
    "auto_fixable": true,
    "remediation_suggestion": "Run: optipng -o7 screenshot.png",
    "reference": ""
}
```

#### 8.5 Bundle Size Checker
**Purpose**: Ensure total course package size is acceptable.

**Checks**:
- Total course size <1GB (strict), <2GB (standard), <5GB (relaxed)
- No huge single files (>100MB)
- Large files justified (e.g., dataset needed for exercises)
- Optional downloads separated from core content

**Tools**:
- Directory size calculation
- File manifest generation

**Pass Criteria**:
- Bundle size within limits

**Example Issue**:
```python
{
    "id": "PERF-BUNDLE-001",
    "severity": "warning",
    "category": "performance",
    "subcategory": "bundle_size",
    "title": "Large course bundle",
    "description": "Total course size 1.8GB exceeds 1GB target (strict profile)",
    "file": "",
    "blocking": false,
    "auto_fixable": false,
    "remediation_suggestion": "Move large datasets to optional downloads or compress videos",
    "reference": ""
}
```

### Inputs
- `course_path`: Course files, videos, images, HTML

### Outputs
- Performance issues, optimization suggestions

### Dependencies
- None (runs independently)

---

## Agent Execution Summary

### Independent Agents (Run in Parallel - Phase 1)
1. **Technical Compliance Agent**
2. **Security Agent**
3. **Legal Compliance Agent**
4. **Accessibility Agent**
5. **Brand Consistency Agent**
6. **Performance Agent**

### Dependent Agents (Run Sequentially - Phase 2)
7. **Pedagogical Quality Agent** (requires Technical success)
8. **Content Integrity Agent** (requires Technical success)

### Agent Versioning
- Each agent has version number (e.g., 1.0.0)
- Agents can be updated independently
- Backward compatibility for result format maintained

### Agent Configuration
- Each agent configured via YAML file
- Thresholds customizable per organization
- Rules can be enabled/disabled

### Agent Extensibility
- New sub-agents can be added without changing core
- Custom agents can be plugged in
- Community agents supported (with review)

---

## Conclusion

These 8 expert agents provide comprehensive coverage of all quality dimensions for course compliance. Each agent is specialized, focused, and produces standardized results that feed into the orchestration layer for decision-making. By combining automated checks, AI-powered analysis, and human oversight, CourseCompliance ensures every course meets high standards before launch.
