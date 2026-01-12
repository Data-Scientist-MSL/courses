# CourseTransformer - Example Transformation Workflows

This document provides detailed examples of transformation workflows.

## Example 1: Transform "01_DataScientistToolbox" (R) → Modern Foundations (Python)

### Input

**Legacy Course**: Johns Hopkins "Data Scientist's Toolbox"
- **Language**: R
- **Topics**: R, RStudio, Git, GitHub
- **Year**: 2015
- **Format**: Markdown lectures, R scripts

**Guiding Principles**:
```yaml
target_year: 2026
primary_language: Python
modern_topics: [Docker, VS Code, GitHub Copilot, OLLAMA]
hands_on_ratio: 0.8
```

### Workflow Execution

#### Stage 1: Ingestion (2 minutes)

**Input**: `/legacy_courses/01_DataScientistToolbox/`

**Process**:
- Parse 35 markdown files
- Extract 12 R scripts
- Identify 4 modules: R Setup, RStudio, Git Basics, GitHub

**Output**:
```json
{
  "extracted_concepts": [
    {"concept": "version_control", "mentions": 15},
    {"concept": "reproducible_research", "mentions": 8},
    {"concept": "r_programming", "mentions": 25}
  ],
  "code_inventory": {
    "R": {"files": 12, "lines": 453, "libraries": ["ggplot2", "dplyr"]}
  }
}
```

#### Stage 2: Analysis (4 minutes)

**Process**:
- Check relevance of each concept
- Identify gaps in modern tools

**Output**:
```json
{
  "overall_relevance": 65,
  "concept_analysis": [
    {
      "concept": "version_control",
      "relevance_score": 98,
      "status": "timeless",
      "recommendation": "keep"
    },
    {
      "concept": "r_programming",
      "relevance_score": 45,
      "status": "outdated",
      "recommendation": "migrate",
      "modern_equivalent": "Python"
    },
    {
      "concept": "rstudio",
      "relevance_score": 40,
      "status": "outdated",
      "recommendation": "replace",
      "modern_equivalent": "VS Code"
    }
  ],
  "missing_topics": [
    {"topic": "docker", "priority": "critical"},
    {"topic": "github_copilot", "priority": "important"},
    {"topic": "ollama", "priority": "important"}
  ]
}
```

#### Stage 3: Planning (7 minutes)

**Process**:
- Generate new curriculum structure
- Create transformation plan

**Output**:
```json
{
  "curriculum_structure": {
    "track_name": "Modern Data Science Foundations",
    "courses": [
      {
        "course_id": "00_philosophy",
        "course_name": "Data Science Philosophy & Ethics",
        "tier": "basic",
        "transformation_type": "create"
      },
      {
        "course_id": "01_modern_dev_environment",
        "course_name": "Modern Development Environment",
        "tier": "basic",
        "modules": [
          {
            "module_id": "01_01_python_setup",
            "transformation_type": "create",
            "replaces": ["02_01_installingR"]
          },
          {
            "module_id": "01_02_git_github",
            "transformation_type": "keep",
            "source": ["02_04_git", "02_05_github"]
          },
          {
            "module_id": "01_03_docker_basics",
            "transformation_type": "create"
          }
        ]
      }
    ]
  }
}
```

**Human Review**: ✅ Approved with comment: "Add more emphasis on OLLAMA for local AI development"

#### Stage 4: Modernization (15 minutes)

**Process**:
- Translate R code to Python
- Update library references

**Example Translation**:
```r
# Original R
library(ggplot2)
data <- read.csv("data.csv")
ggplot(data, aes(x=year, y=value)) + geom_line()
```

```python
# Modernized Python
import pandas as pd
import plotly.express as px

data = pd.read_csv("data.csv")
px.line(data, x="year", y="value")
```

#### Stage 5: Generation (25 minutes)

**Process**:
- Generate slides for Python setup
- Create Docker lab
- Generate quizzes

**Generated Content**:
- 45 slides (Marp markdown)
- 8 Jupyter notebook labs
- 30 quiz questions
- 12 Mermaid diagrams

#### Stage 6: Quality Assurance (8 minutes)

**QA Report**:
```json
{
  "overall_score": 92,
  "checks": {
    "code_execution": {"score": 100, "all_code_runs": true},
    "accuracy": {"score": 96, "facts_verified": 48/50},
    "consistency": {"score": 88, "minor_terminology_issues": 2},
    "completeness": {"score": 95}
  },
  "issues": [
    {
      "severity": "warning",
      "description": "Docker lab complexity may be high for beginners",
      "recommendation": "Add introductory section"
    }
  ]
}
```

**Decision**: Pass with minor issues → Proceed to human review

#### Stage 7: Human Content Review (20 minutes)

**Human Actions**:
- Review Docker lab → Approved with edit (added beginner intro)
- Review Python setup slides → Regenerate with more OLLAMA content
- Review quizzes → Approved all

**Decision**: ✅ Approved

#### Stage 8: Export (2 minutes)

**Output Structure**:
```
export/
├── coursesgtm/
│   └── curriculum.json
├── courseplayerapp/
│   ├── 00_Philosophy/
│   ├── 01_Modern_Dev_Environment/
│   │   ├── 01_Python_Setup/
│   │   │   ├── slides/
│   │   │   ├── labs/
│   │   │   └── quizzes/
│   │   ├── 02_Git_GitHub/
│   │   └── 03_Docker_Basics/
│   └── assets/
└── docker/
    └── Dockerfile
```

### Results

**Total Time**: ~83 minutes (1.4 hours)
- **Legacy Course**: 4 hours of R-based content
- **Modern Course**: 6 hours of Python-based content
- **New Topics Added**: Docker, OLLAMA, Modern Python practices
- **Quality Score**: 92%

---

## Example 2: Create New Course "10_Transformers_LLMs" (From Scratch)

### Input

**Topic Specification**: "Create comprehensive course on Transformers and Large Language Models"
- **No legacy content** (pure generation)
- **Target Tier**: Advanced
- **Duration**: 12 hours

**Guiding Principles**:
```yaml
target_year: 2026
primary_language: Python
pedagogical:
  hands_on_ratio: 0.85
  project_based: true
```

### Workflow Execution (Abbreviated)

#### Stage 1 & 2: Ingestion & Analysis (Skipped)
No legacy content to ingest or analyze.

#### Stage 3: Planning (12 minutes)

**Human-Provided Outline**:
1. Attention Mechanism
2. Transformer Architecture
3. BERT & Encoder Models
4. GPT & Decoder Models
5. Fine-Tuning Techniques
6. Prompt Engineering
7. RAG Systems
8. Capstone: Build a QA System

**Generated Plan**:
```json
{
  "course_id": "10_transformers_llms",
  "modules": [
    {"module_id": "01_attention", "lessons": 4},
    {"module_id": "02_transformer_arch", "lessons": 5},
    {"module_id": "03_bert", "lessons": 4},
    {"module_id": "04_gpt", "lessons": 4},
    {"module_id": "05_fine_tuning", "lessons": 5},
    {"module_id": "06_prompt_engineering", "lessons": 4},
    {"module_id": "07_rag", "lessons": 5},
    {"module_id": "08_capstone", "lessons": 1}
  ],
  "total_lessons": 32,
  "estimated_hours": 12
}
```

**Human Review**: ✅ Approved

#### Stage 4: Modernization (Skipped)
No legacy code to modernize.

#### Stage 5: Generation (60 minutes)

**Generated**:
- 120 slides explaining Transformers
- 15 hands-on labs (implementing attention, fine-tuning BERT, etc.)
- 40 quiz questions
- 25 diagrams (architecture diagrams, attention visualizations)
- 1 capstone project with starter code

**Example Generated Lab**:
```python
# Lab: Implement Multi-Head Attention
import torch
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        # TODO: Implement multi-head attention
        # Instructions: ...
        pass
    
    def forward(self, query, key, value, mask=None):
        # TODO: Complete forward pass
        pass

# Test your implementation
# ...
```

#### Stage 6: QA (15 minutes)

**QA Report**: Overall score 89%
- All code executes ✅
- Minor accuracy issue: One slide claims "BERT always outperforms GPT" (too absolute)
- Fix: Softened claim to "BERT often performs better on classification tasks"

#### Stage 7: Human Review (30 minutes)

**Actions**:
- Approved most content
- Regenerated 2 labs with more detailed instructions
- Approved

#### Stage 8: Export (2 minutes)

**Output**: Complete 12-hour course on Transformers & LLMs

### Results

**Total Time**: ~119 minutes (2 hours)
- **Course Created**: 12 hours of content
- **From Scratch**: No legacy content used
- **Quality**: 89% (excellent for generated content)

---

## Key Takeaways

1. **Legacy Transformation**: Faster than creating from scratch (1.4 hours vs 2 hours) because less content generation needed
2. **Human Review Critical**: Humans improved quality by 5-10% in both examples
3. **Quality Metrics**: Both courses met >85% quality threshold
4. **Efficiency**: ~10x faster than manual course creation (manual would take 20-40 hours per course)
