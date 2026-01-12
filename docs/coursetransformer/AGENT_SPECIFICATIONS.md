# CourseTransformer - Agent Specifications

This document provides detailed specifications for each of the seven core agents in the CourseTransformer system.

## Agent Architecture Overview

All agents follow a common architecture:
- Inherit from `BaseAgent` class  
- Define specific tools and capabilities
- Execute within LangGraph workflow
- Use LLM for semantic understanding
- Return structured outputs

---

## 1️⃣ Ingestion Agent

### Purpose
Parse legacy course content from multiple formats and extract structured information for downstream processing.

### Inputs
| Input | Type | Description |
|-------|------|-------------|
| `legacy_course_path` | string | Path to course directory or archive |
| `file_formats` | list[string] | Formats to process: `["R", "PDF", "MD", "video", "HTML"]` |
| `extraction_config` | dict | Configuration for extraction (depth, filters) |

### Capabilities

#### 1. R Code Parsing
- **Technology**: `rpy2`, custom R parser
- **Extracts**:
  - Function definitions and logic
  - Library dependencies (`library()`, `require()`)
  - Data transformations (dplyr chains, ggplot2 specs)
  - Statistical analyses
- **Preserves**: Comments, code structure, variable names

#### 2. PDF Text Extraction
- **Technology**: `pdfplumber` (primary), `PyPDF2` (fallback)
- **Capabilities**:
  - Text extraction with layout preservation
  - Table detection and extraction
  - Image extraction (for diagrams)
  - Metadata extraction (author, date, title)
- **Output**: Structured markdown with sections

#### 3. Markdown Processing
- **Technology**: `markdown-it-py`, `mistune`
- **Extracts**:
  - Headers (course structure)
  - Code blocks with language tags
  - Links and references
  - Embedded images
- **Output**: Parsed AST for further processing

#### 4. Video Processing
- **Technology**: `whisper` (OpenAI), `youtube-dl`
- **Capabilities**:
  - Download videos from URLs
  - Extract audio tracks
  - Transcribe with timestamps
  - Identify key frames (slide changes)
- **Output**: VTT transcripts, key frame images

#### 5. Metadata Extraction
- **LLM-Powered**: Semantic extraction from unstructured text
- **Extracts**:
  - Course title, description, author
  - Learning objectives
  - Prerequisites
  - Estimated duration
  - Topic tags
- **Output**: Standardized JSON metadata

#### 6. Course Structure Identification
- **Analysis**:
  - Directory hierarchy → Course/Module/Lesson structure
  - File naming patterns (e.g., `01_Introduction`, `02_...`)
  - Inter-file dependencies (references, imports)
- **Output**: Hierarchical course structure tree

### Outputs

#### Primary Output: Structured Course Data
```json
{
  "course_id": "01_DataScientistToolbox",
  "metadata": {
    "title": "Data Scientist's Toolbox",
    "author": "Johns Hopkins University",
    "date": "2015",
    "topics": ["R", "RStudio", "Git", "GitHub"],
    "duration_hours": 4
  },
  "structure": {
    "modules": [
      {
        "module_id": "02_installingR",
        "title": "Installing R",
        "lessons": [
          {
            "lesson_id": "02_01_installingR",
            "title": "Installing R",
            "type": "lecture",
            "content_path": "01_DataScientistToolbox/02_01_installingR/index.md",
            "assets": ["slides.pdf", "install-script.R"]
          }
        ]
      }
    ]
  },
  "extracted_concepts": [
    {
      "concept": "version_control",
      "mentions": 15,
      "contexts": ["Git basics", "GitHub workflow"],
      "code_examples": ["git add .", "git commit -m"]
    },
    {
      "concept": "reproducible_research",
      "mentions": 8,
      "contexts": ["RMarkdown", "knitr"]
    }
  ],
  "code_inventory": {
    "R": {
      "files": 12,
      "lines": 453,
      "libraries": ["ggplot2", "dplyr", "tidyr", "knitr"]
    }
  }
}
```

#### Secondary Output: Raw Content Index
- File manifest with checksums
- Raw text for full-text search
- Binary asset registry (videos, images)

### Tools

#### Code Parsing Tools
```python
tools = [
    Tool(
        name="parse_r_code",
        func=parse_r_file,
        description="Parse R file and extract functions, libraries, logic"
    ),
    Tool(
        name="extract_imports",
        func=extract_r_imports,
        description="Extract all library() and require() calls"
    )
]
```

#### Document Processing Tools
```python
tools = [
    Tool(
        name="extract_pdf_text",
        func=extract_from_pdf,
        description="Extract text from PDF preserving structure"
    ),
    Tool(
        name="parse_markdown",
        func=parse_markdown_file,
        description="Parse Markdown into structured AST"
    )
]
```

### LLM Usage

#### Concept Extraction Prompt
```
Given the following course content:
{content}

Extract the core educational concepts being taught. For each concept, provide:
1. Concept name (e.g., "linear_regression", "version_control")
2. Brief definition
3. Context in which it's taught

Output as JSON array.
```

#### Metadata Extraction Prompt
```
Analyze this course material and extract:
- Title
- Learning objectives (3-5 bullet points)
- Prerequisites (if any)
- Estimated duration for a beginner learner

Content:
{content}
```

### Error Handling

| Error Condition | Recovery Strategy |
|----------------|-------------------|
| Corrupt PDF | Try OCR with `pytesseract` |
| R syntax error | Log error, extract what's parseable, continue |
| Missing video | Skip video, process other content |
| Encoding issues | Try multiple encodings (UTF-8, Latin-1, ASCII) |

### Performance Considerations

- **Parallel processing**: Process files concurrently (ThreadPoolExecutor)
- **Streaming**: Stream large PDFs page-by-page
- **Caching**: Cache parsed content by file hash
- **Rate limiting**: Respect API limits for external video services

---

## 2️⃣ Analysis Agent

### Purpose
Assess the relevance of legacy content in 2026 and identify gaps where modern topics should be added.

### Inputs
| Input | Type | Description |
|-------|------|-------------|
| `parsed_content` | dict | Output from Ingestion Agent |
| `extracted_concepts` | list[dict] | Concepts from legacy course |
| `target_year` | int | Target year for modernization (default: 2026) |
| `guiding_principles` | dict | Modernization guidelines |

### Capabilities

#### 1. Relevance Checker
- **Methodology**: Semantic analysis against current best practices
- **Checks**:
  - Is concept still taught in modern courses?
  - Are techniques still industry-standard?
  - Are libraries/tools still maintained?
- **Scoring**: 0-100% relevance score per concept
- **Categories**:
  - **Timeless (90-100%)**: Foundational concepts (statistics, algorithms)
  - **Relevant (70-89%)**: Still valid but may need updates
  - **Outdated (40-69%)**: Needs significant modernization
  - **Obsolete (0-39%)**: Should be replaced or removed

#### 2. Gap Analyzer
- **Compares**: Legacy concepts vs. modern AI/ML curriculum
- **Identifies missing topics**:
  - **Modern AI**: Transformers, LLMs, RAG, Prompt Engineering
  - **MLOps**: Model deployment, monitoring, versioning (MLflow, DVC)
  - **Privacy-Preserving ML**: Federated learning, differential privacy
  - **Modern Tools**: Docker, Kubernetes, GitHub Actions, pre-commit
- **Output**: Prioritized list of gaps (critical, important, nice-to-have)

#### 3. Technology Stack Analyzer
- **Compares**:
  - Legacy: R, RStudio, specific package versions
  - Modern: Python 3.10+, VS Code, current libraries
- **Analyzes**:
  - Library deprecation status
  - Migration paths (ggplot2 → plotly, dplyr → pandas)
  - Breaking changes in newer versions
- **Recommendations**: Keep, migrate, or replace each technology

#### 4. Difficulty Assessor
- **Maps content** to CoursesGTM tiers:
  - **Basic**: Introductory, no prerequisites
  - **Intermediate**: Requires basic knowledge
  - **Advanced**: Requires intermediate + specialized skills
- **Criteria**:
  - Mathematical complexity
  - Coding skill required
  - Domain knowledge assumed
- **Uses**: Bloom's Taxonomy levels

### Outputs

#### Relevance Report
```json
{
  "overall_relevance": 67,
  "concept_analysis": [
    {
      "concept": "linear_regression",
      "relevance_score": 95,
      "status": "timeless",
      "reasoning": "Foundational statistical concept, still widely used",
      "recommendation": "keep",
      "suggested_updates": ["Add regularization (Ridge, Lasso)", "Include scikit-learn implementation"]
    },
    {
      "concept": "r_data_frames",
      "relevance_score": 45,
      "status": "outdated",
      "reasoning": "Concept is valid, but R syntax is legacy",
      "recommendation": "migrate",
      "modern_equivalent": "pandas.DataFrame"
    },
    {
      "concept": "manual_cross_validation",
      "relevance_score": 30,
      "status": "obsolete",
      "reasoning": "Modern libraries automate this (scikit-learn)",
      "recommendation": "replace",
      "modern_equivalent": "sklearn.model_selection.cross_val_score"
    }
  ],
  "library_analysis": {
    "ggplot2": {
      "status": "active",
      "last_update": "2024-11",
      "recommendation": "migrate",
      "python_equivalent": "plotly / matplotlib + seaborn"
    },
    "dplyr": {
      "status": "active",
      "recommendation": "migrate",
      "python_equivalent": "pandas"
    }
  }
}
```

For brevity, see full specification in repository.


#### Gap Analysis
```json
{
  "missing_topics": [
    {
      "topic": "transformers_architecture",
      "priority": "critical",
      "reasoning": "Essential for modern NLP and AI",
      "suggested_placement": "Advanced tier, after neural networks",
      "estimated_hours": 8
    },
    {
      "topic": "large_language_models",
      "priority": "critical",
      "reasoning": "Foundational to AI/ML in 2026",
      "dependencies": ["transformers_architecture"],
      "estimated_hours": 12
    },
    {
      "topic": "mlops_basics",
      "priority": "important",
      "reasoning": "Industry standard for deployment",
      "suggested_placement": "Intermediate tier",
      "estimated_hours": 6
    },
    {
      "topic": "docker_containerization",
      "priority": "important",
      "reasoning": "Standard for reproducible environments",
      "suggested_placement": "Basic tier, early in curriculum",
      "estimated_hours": 4
    }
  ],
  "technology_gaps": {
    "development_tools": ["VS Code", "GitHub Copilot", "Jupyter Lab"],
    "ml_frameworks": ["PyTorch", "Hugging Face Transformers"],
    "deployment": ["FastAPI", "Docker", "GitHub Actions"]
  }
}
```

#### Modernization Suggestions
```json
{
  "structural_changes": [
    {
      "suggestion": "Split 'Data Scientist Toolbox' into 'Modern Dev Environment' and 'Scientific Python Basics'",
      "reasoning": "Original course mixes setup and programming concepts"
    },
    {
      "suggestion": "Create new track: 'Modern AI/ML with LLMs'",
      "reasoning": "Missing entire category of modern AI"
    }
  ],
  "content_enhancements": [
    {
      "module": "Regression Models",
      "enhancement": "Add section on neural network-based regression",
      "priority": "important"
    }
  ]
}
```

### Tools

```python
tools = [
    Tool(
        name="check_library_status",
        func=check_pypi_library_status,
        description="Check if library is maintained, deprecated, or has security issues"
    ),
    Tool(
        name="query_knowledge_base",
        func=query_rag_system,
        description="Query knowledge base for modern best practices"
    ),
    Tool(
        name="assess_difficulty",
        func=calculate_bloom_taxonomy_level,
        description="Assess cognitive difficulty using Bloom's Taxonomy"
    )
]
```

### LLM Usage

#### Relevance Assessment Prompt
```
You are an expert data science educator in 2026. Assess the relevance of this concept:

Concept: {concept_name}
Description: {concept_description}
Original context (2015): {original_context}

Evaluate:
1. Is this concept still taught in modern data science courses?
2. Are there better/newer alternatives?
3. What updates would make it current for 2026?

Provide relevance score (0-100) and reasoning.
```

#### Gap Identification Prompt
```
Compare these course topics from 2015 to modern AI/ML curriculum in 2026:

Legacy topics: {legacy_topics}

Modern curriculum areas:
- Large Language Models & Transformers
- MLOps and Model Deployment
- Privacy-Preserving ML
- Modern Python Data Science Stack

Identify:
1. Critical gaps (must add)
2. Important gaps (should add)
3. Nice-to-have additions

For each gap, suggest where it fits in the curriculum.
```

### Knowledge Base Integration

- **Query**: "What are industry standard ML practices in 2026?"
- **Retrieval**: Top-k relevant documents from vector store
- **Context**: Use retrieved info to ground relevance assessments
- **Fact-checking**: Verify claims against authoritative sources

---

## 3️⃣ Planning Agent

### Purpose
Design the new curriculum structure and create a detailed transformation plan based on analysis results.

### Inputs
| Input | Type | Description |
|-------|------|-------------|
| `relevance_report` | dict | Output from Analysis Agent |
| `gap_analysis` | dict | Identified missing topics |
| `guiding_principles` | dict | Pedagogical and modernization guidelines |
| `tier_structure` | dict | CoursesGTM tier definitions |

### Capabilities

#### 1. Curriculum Planner
- **Designs**: Complete course track structure
- **Organizes**:
  - Tracks (e.g., "Foundational Python", "Modern AI/ML")
  - Courses within tracks
  - Modules within courses
  - Lessons within modules
- **Applies**: Pedagogical scaffolding (simple → complex)
- **Balances**: Theory vs. practice (per guiding principles)

#### 2. Dependency Mapper
- **Identifies**: Prerequisite relationships between courses
- **Creates**: Dependency graph (DAG)
- **Validates**: No circular dependencies
- **Suggests**: Optimal learning paths
- **Considers**: Flexible paths for different learner goals

#### 3. Scope Definer
- **Categorizes each piece of legacy content**:
  - **Keep**: Minimal changes (timeless content)
  - **Modernize**: Update (relevant but needs refresh)
  - **Create**: New content (fill gaps)
  - **Remove**: Discard (obsolete content)
- **Estimates**: Hours of work per category
- **Prioritizes**: Critical path items first

#### 4. Tier Distributor
- **Assigns courses** to CoursesGTM tiers:
  - **Basic**: Foundational, broad access
  - **Intermediate**: Specialized, mid-tier
  - **Advanced**: Expert-level, premium
- **Criteria**:
  - Difficulty level
  - Prerequisites
  - Market positioning
  - Content depth

### Outputs

See complete specification including curriculum structure JSON, transformation plan, tools, and LLM usage in repository.

---

## 4️⃣ Modernization Agent

### Purpose
Transform legacy code and concepts to modern equivalents while preserving semantic intent.

### Inputs
| Input | Type | Description |
|-------|------|-------------|
| `legacy_code` | dict | R code files and snippets |
| `legacy_concepts` | list[dict] | Concepts to modernize |
| `transformation_plan` | dict | Tasks from Planning Agent |
| `target_language` | string | Target language (default: "Python") |

### Capabilities

#### 1. Code Translator (R → Python)
- **Not just syntax**: Semantic translation preserving intent
- **Handles**:
  - Data frames: R `data.frame` → `pandas.DataFrame`
  - Pipelines: `%>%` → method chaining or `pipe()`
  - Plotting: `ggplot2` → `plotly` or `matplotlib + seaborn`
  - Statistics: R stats → `scipy.stats`, `statsmodels`
  - Functional programming: `apply`, `map` → list comprehensions, `map()`, `pandas.apply()`

**Example**:
```r
# Legacy R
library(dplyr)
library(ggplot2)

mtcars %>%
  filter(mpg > 20) %>%
  group_by(cyl) %>%
  summarize(avg_hp = mean(hp)) %>%
  ggplot(aes(x = cyl, y = avg_hp)) +
  geom_bar(stat = "identity")
```

```python
# Modern Python
import pandas as pd
import plotly.express as px

(mtcars
 .query("mpg > 20")
 .groupby("cyl")
 .agg(avg_hp=("hp", "mean"))
 .reset_index()
 .pipe(lambda df: px.bar(df, x="cyl", y="avg_hp"))
)
```

See complete modernization agent specification in repository.

---

## 5️⃣ Generation Agent

### Purpose
Create new course content from scratch using templates and LLM generation.

### Capabilities

#### 1. Slide Generator (Marp Markdown)
- Creates lecture slides in Marp format
- Structure: Title → Learning objectives → Content → Takeaways → Practice

#### 2. Lab Generator (Jupyter Notebooks)
- Creates interactive coding exercises
- Fill-in-the-blank with automatic grading

#### 3. Quiz Generator
- Multiple choice, coding challenges, conceptual questions
- Adaptive difficulty with plausible distractors

#### 4. Diagram Generator (Mermaid)
- Flowcharts, sequence diagrams, architectures
- LLM-powered generation from descriptions

#### 5. Dataset Curator
- Finds relevant, modern datasets from Kaggle, UCI, Hugging Face

#### 6. Project Designer
- Creates capstone projects with rubrics

See complete generation agent specification in repository.

---

## 6️⃣ Quality Assurance Agent

### Purpose
Verify accuracy, consistency, and completeness of generated content before human review.

### Capabilities

#### 1. Accuracy Checker
- Fact-checking against knowledge base
- Code execution verification
- Math and formula validation

#### 2. Code Verifier
- Execute all code snippets
- Run notebooks with nbconvert
- Linting (pylint, black)
- Security checks (bandit)

#### 3. Consistency Validator
- Terminology, notation, style consistency
- Cross-reference validation

#### 4. Completeness Checker
- All learning objectives addressed
- Sufficient examples and exercises

#### 5. Readability Scorer
- Flesch-Kincaid grade level
- Target: Grade 12-14 (college)

### Outputs

#### Quality Report
```json
{
  "overall_score": 87,
  "pass": true,
  "threshold": 75,
  "checks": {
    "accuracy": {"score": 96, "status": "pass"},
    "code_execution": {"score": 100, "status": "pass"},
    "code_quality": {"score": 85, "status": "pass"},
    "consistency": {"score": 90, "status": "pass"},
    "completeness": {"score": 75, "status": "pass"},
    "readability": {"score": 82, "status": "pass"}
  },
  "summary": {
    "critical_issues": 0,
    "warnings": 3,
    "info": 1
  }
}
```

See complete QA agent specification in repository.

---

## 7️⃣ Export Agent

### Purpose
Format and package approved content for deployment to CoursesGTM and CoursePlayerApp.

### Capabilities

#### 1. CoursesGTM Formatter
- Generates `curriculum.json`, `tiers.json`
- Maps courses to tiers
- Validates against schema

#### 2. CoursePlayerApp Packager
- Organizes files into expected directory structure
- Creates content manifests
- Bundles all assets

#### 3. Metadata Generator
- Course descriptions, tags, durations
- SEO-friendly content

#### 4. Docker Packager (Optional)
- Creates reproducible learning environment
- Includes all dependencies

### Outputs

**Directory Structure**:
```
courses-v2/
├── 00_Philosophy/
│   ├── manifest.json
│   ├── 01_Augmented_Human/
│   │   ├── slides/
│   │   ├── labs/
│   │   └── quizzes/
│   └── assets/
└── curriculum.json
```

See complete export agent specification in repository.

---

## Agent Interaction Patterns

### Sequential Flow
```
Ingestion → Analysis → Planning → Modernization → Generation → QA → Export
```

### Parallel Execution
```
Generation Agent spawns parallel tasks:
├── Generate Slides
├── Generate Labs
└── Generate Quizzes
```

### Retry with Feedback
```
QA Agent detects issues → Generation Agent regenerates → QA re-checks
```

### Human-Guided Loop
```
Planning Agent creates plan → Human reviews → Agent revises (if needed) → Approved → Proceed
```

---

## Agent Communication Protocol

All agents communicate via shared state object:

```python
state = {
    "ingestion_output": {...},
    "analysis_output": {...},
    "planning_output": {...},
    # ... etc
}

def execute(self, state: dict) -> dict:
    input_data = state['previous_agent_output']
    result = self.process(input_data)
    return {
        **state,
        'current_agent_output': result
    }
```

---

## Error Handling Matrix

| Agent | Common Errors | Recovery Strategy |
|-------|---------------|-------------------|
| Ingestion | Corrupt file | Skip file, log warning |
| Analysis | LLM timeout | Use cached results, fallback |
| Planning | Invalid structure | Return with error for human |
| Modernization | Translation failure | Flag for human review |
| Generation | Template missing | Use default template |
| QA | Code execution error | Mark failed, provide details |
| Export | Schema validation failure | Block export until fixed |

---

## Performance Benchmarks (Estimated)

| Agent | Avg Duration | LLM Calls | Tokens Used |
|-------|--------------|-----------|-------------|
| Ingestion | 2-5 min | 5-10 | 5K-15K |
| Analysis | 3-7 min | 10-20 | 15K-30K |
| Planning | 5-10 min | 15-25 | 25K-50K |
| Modernization | 10-20 min | 20-40 | 30K-60K |
| Generation | 15-30 min | 50-100 | 80K-150K |
| QA | 5-10 min | 10-20 | 10K-25K |
| Export | 1-3 min | 0-2 | 0-2K |

**Total per course**: ~40-85 minutes

---

## Future Agent Extensions

Potential new agents:
- **Translation Agent**: Internationalization
- **Accessibility Agent**: WCAG compliance
- **Video Generation Agent**: Text-to-video lectures
- **Interactive Diagram Agent**: Interactive visualizations
- **Personalization Agent**: Adaptive content
- **Assessment Agent**: Comprehensive exams

These integrate into the existing LangGraph workflow seamlessly.
