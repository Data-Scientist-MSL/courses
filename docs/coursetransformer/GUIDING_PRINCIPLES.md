# CourseTransformer - Guiding Principles Framework

This document defines the configurable principles that guide course transformation decisions.

## Overview

Guiding Principles are the philosophical and practical guidelines that shape how CourseTransformer transforms legacy content into modern courses. They are:
- **Configurable**: Adjust per transformation
- **Declarative**: Defined in YAML
- **Actionable**: Directly influence agent behavior
- **Human-Centric**: Reflect educational values and goals

## Principle Categories

### 1. Augmented Human Philosophy

**Core Tenets**:
- **AI Assists, Humans Decide**: AI handles mechanical tasks (parsing, translation, generation), but humans make creative and pedagogical decisions
- **Transparency**: All AI suggestions are explainable; humans can see reasoning
- **Human Final Authority**: Humans have veto power over all AI outputs
- **Collaborative**: AI and human strengths complement each other
- **Ethical**: AI serves learner needs, not efficiency alone

**Implications for Transformation**:
- Mandatory human review checkpoints (planning, content)
- AI provides multiple options, human chooses
- Clear attribution of AI-generated vs human-created content
- Humans can override any AI decision

**Agent Behavior**:
- Planning Agent: Generate 2-3 curriculum options, let human select
- Generation Agent: Mark AI-generated content clearly
- QA Agent: Flag issues but don't auto-fix without approval

---

### 2. Pedagogical Principles

#### Active Learning
- **Hands-On Practice**: Prioritize labs, projects, exercises over passive reading
- **Learning by Doing**: 80% practice, 20% theory (configurable)
- **Immediate Feedback**: Quizzes with explanations, auto-graded exercises
- **Real-World Application**: Use current datasets and industry scenarios

**Implementation**:
```yaml
pedagogical_preferences:
  hands_on_ratio: 0.8
  active_learning: true
  immediate_feedback: true
```

#### Scaffolded Difficulty
- **Progressive Complexity**: Basic → Intermediate → Advanced
- **Prerequisites Enforced**: Can't skip foundational courses
- **Mastery-Based**: Complete one tier before advancing
- **Bloom's Taxonomy**: Align content to cognitive levels

**Course Tiers**:
- **Basic**: Remember, Understand (Bloom's levels 1-2)
- **Intermediate**: Apply, Analyze (Bloom's levels 3-4)
- **Advanced**: Evaluate, Create (Bloom's levels 5-6)

#### Spaced Repetition
- **Concept Reinforcement**: Revisit key concepts across multiple modules
- **Incremental Complexity**: Same concept at increasing depth
- **Interleaved Practice**: Mix related topics to strengthen connections

#### Project-Based Learning
- **Capstone Projects**: End each course with synthesis project
- **Portfolio Building**: Projects suitable for showcasing to employers
- **Authentic Assessment**: Evaluate through work product, not just tests

**Example**:
```yaml
project_based: true
capstone_required: true
project_types:
  - end_to_end_ml_pipeline
  - research_paper_implementation
  - open_source_contribution
```

---

### 3. Modernization Guidelines

#### What Makes Content "Modern" (2026)?

**Technology**:
- **Current Libraries**: Latest stable versions (not bleeding edge)
- **Modern Practices**: Type hints, linting, testing, CI/CD
- **Cloud & Local**: Options for both cloud (AWS, Azure) and local (Docker, OLLAMA)
- **Privacy-First**: Emphasize local models, data sovereignty

**Topics**:
- **AI/ML 2026**: Transformers, LLMs, RAG, prompt engineering, MLOps
- **Tools**: VS Code, GitHub Copilot, Docker, Jupyter Lab, DVC
- **Deployment**: FastAPI, Streamlit, Docker, Kubernetes basics
- **Ethics**: AI bias, fairness, interpretability, privacy

**Code Style**:
- Python 3.10+ features (pattern matching, type hints, dataclasses)
- Functional + OOP hybrid
- Emphasis on readability (PEP 8, black formatting)

#### When to Keep Legacy Content

**Keep If**:
- **Timeless Concepts**: Statistics fundamentals, algorithm theory
- **Well-Explained**: Original explanation is clearer than AI-generated
- **Historical Value**: Context on how field evolved
- **No Modern Equivalent**: Concept hasn't fundamentally changed

**Examples to Keep**:
- Basic probability and statistics
- Foundational ML algorithms (linear regression, k-means)
- Data manipulation concepts (even if syntax changes)
- Scientific method and experimental design

#### When to Modernize

**Modernize If**:
- **Same Concept, New Tools**: Concept valid, but tools/libraries changed
- **Syntax Update**: R → Python translation
- **API Changes**: Library APIs evolved (sklearn v0.x → v1.x)
- **Enhancement Opportunity**: Can add regularization, validation, etc.

**Examples**:
- R `ggplot2` → Python `plotly` (interactive visualization)
- Manual cross-validation → `sklearn.model_selection`
- Basic regression → Add regularization (Ridge, Lasso)

#### When to Create New Content

**Create If**:
- **Gap Identified**: Topic missing from legacy curriculum
- **Modern Requirement**: Industry now expects this knowledge
- **Pedagogical Need**: Better scaffolding requires intermediate step

**Critical New Topics (2026)**:
- Transformer architecture and attention mechanism
- Large Language Models (GPT, BERT, LLaMA)
- Retrieval Augmented Generation (RAG)
- MLOps (experiment tracking, model deployment, monitoring)
- Privacy-preserving ML (federated learning, differential privacy)
- Docker and containerization for reproducibility

#### When to Remove

**Remove If**:
- **Obsolete**: No longer used in industry
- **Deprecated**: Library/tool no longer maintained
- **Superseded**: Better approach has replaced it
- **Misleading**: Teaches anti-patterns or outdated practices

**Examples to Remove**:
- Deprecated Python 2.x code
- Unmaintained libraries with no migration path
- Manual techniques now automated (e.g., feature scaling without sklearn)
- Platform-specific solutions (e.g., Windows-only tools)

---

### 4. Quality Standards

#### Code Quality
```yaml
code_quality:
  execution_pass_rate: 1.0  # 100% of code must run
  linting_score: 8.0        # pylint score ≥ 8.0/10
  security_issues: 0         # No security vulnerabilities
  complexity_threshold: 10   # Max cyclomatic complexity
  test_coverage: 0.8         # 80% test coverage for complex code
```

**Requirements**:
- All code snippets execute successfully
- No syntax errors, no runtime errors
- Follows PEP 8 style guide
- Security scan (bandit) passes
- Readable variable names, adequate comments

#### Content Accuracy
```yaml
accuracy:
  fact_check_threshold: 0.95  # 95% accuracy
  citation_required: true      # External claims need sources
  rag_verification: true       # Cross-check against knowledge base
```

**Requirements**:
- Factual claims verified against authoritative sources
- Mathematical formulas correct
- Code output matches expected results
- No outdated information

#### Completeness
```yaml
completeness:
  learning_objectives_coverage: 1.0  # 100% of objectives addressed
  exercise_ratio: 0.6                # 60% of concepts have exercises
  example_ratio: 0.8                 # 80% of concepts have code examples
```

**Requirements**:
- All stated learning objectives are taught
- Every major concept has code example
- Sufficient practice exercises (3-5 per module)
- No unexplained jargon

#### Consistency
```yaml
consistency:
  terminology_standard: true   # Use consistent terms
  notation_standard: true      # Math notation consistent
  code_style_standard: true    # Follow style guide
```

**Requirements**:
- Same concept called by same name throughout
- Mathematical notation consistent (e.g., always use bold for vectors)
- Code style uniform (black formatted)
- Template structure consistent across modules

#### Readability
```yaml
readability:
  flesch_kincaid_grade: [12, 14]  # College reading level
  avg_sentence_length: [15, 25]    # 15-25 words per sentence
  jargon_density: 0.15             # Max 15% technical jargon
```

**Requirements**:
- Appropriate for college-level learners
- Technical terms defined on first use
- Clear, concise explanations
- Good use of examples and analogies

---

### 5. Technology Preferences

#### Primary Stack (2026)

**Languages**:
```yaml
languages:
  primary: Python
  version: "3.10+"
  secondary: [R, Julia]  # For specific use cases
```

**ML/AI Frameworks**:
```yaml
ml_frameworks:
  traditional_ml: scikit-learn
  deep_learning: PyTorch
  transformers: Hugging Face Transformers
  llm_frameworks: [LangChain, LlamaIndex]
  experiment_tracking: [MLflow, Weights & Biases]
```

**Data Processing**:
```yaml
data:
  dataframes: pandas
  high_performance: polars
  sql: DuckDB
  big_data: PySpark  # Advanced tier only
```

**Visualization**:
```yaml
visualization:
  interactive: plotly
  static: [matplotlib, seaborn]
  dashboards: Streamlit
```

**Development Tools**:
```yaml
tools:
  ide: VS Code
  ai_assistant: GitHub Copilot
  notebook: Jupyter Lab
  version_control: Git
  containerization: Docker
  ci_cd: GitHub Actions
```

**LLM Integration**:
```yaml
llm:
  primary: OLLAMA  # Local, privacy-first
  models: [llama2, mistral, codellama]
  fallback: [OpenAI, Anthropic]  # Optional, with consent
  use_cases:
    - code_generation
    - documentation
    - tutoring
```

**Deployment**:
```yaml
deployment:
  api: FastAPI
  frontend: Streamlit
  containerization: Docker
  orchestration: docker-compose  # Basic; Kubernetes in Advanced
```

---

### 6. Configurable Principles (YAML Schema)

**Complete Configuration Example**:
```yaml
# principles_config.yaml

# Metadata
transformation_id: "jhu_ds_to_modern_2026"
created_by: "Jane Educator"
created_at: "2026-01-12T10:00:00Z"

# Philosophy
philosophy: augmented_human
transparency: true
human_final_authority: true

# Modernization
target_year: 2026
primary_language: Python
python_version: "3.10+"
secondary_languages:
  - R  # For statistical concepts
  - Julia  # For high-performance computing

# LLM Integration
llm_integration:
  provider: OLLAMA
  models:
    analysis: llama2:7b
    generation: mixtral:8x7b
    code: codellama:13b
  privacy_first: true
  api_fallback:
    enabled: false  # Set to true to allow OpenAI as fallback

# Modern Topics to Add
modern_topics:
  critical:
    - transformers_architecture
    - large_language_models
    - retrieval_augmented_generation
    - mlops_fundamentals
  important:
    - docker_containerization
    - github_actions_ci_cd
    - fastapi_deployment
    - privacy_preserving_ml
  nice_to_have:
    - federated_learning
    - model_interpretability
    - gpu_optimization

# Quality Standards
quality_thresholds:
  code:
    pass_rate: 1.0
    pylint_score: 8.0
    security_issues: 0
    complexity_max: 10
  accuracy: 0.95
  completeness: 0.90
  readability:
    flesch_kincaid_grade: [12, 14]
    jargon_density_max: 0.15

# Pedagogical Preferences
pedagogical:
  learning_approach: active_learning
  hands_on_ratio: 0.8
  theory_ratio: 0.2
  quiz_frequency: per_module
  quizzes_per_module: [5, 10]
  project_based: true
  capstone_required: true
  immediate_feedback: true
  spaced_repetition: true

# Course Structure
course_structure:
  tiers:
    - basic
    - intermediate
    - advanced
  tier_distribution:
    basic: 0.40      # 40% of courses
    intermediate: 0.35  # 35% of courses
    advanced: 0.25   # 25% of courses
  
  module_size:
    lessons_per_module: [3, 5]
    hours_per_module: [2, 4]

# Technology Stack
technology_stack:
  languages:
    primary: Python
    version: "3.10+"
  
  ml_frameworks:
    traditional: scikit-learn
    deep_learning: PyTorch
    transformers: transformers  # Hugging Face
    llm: [LangChain, LlamaIndex]
  
  data:
    dataframes: pandas
    sql: DuckDB
    visualization: [plotly, matplotlib, seaborn]
  
  tools:
    ide: VS Code
    notebook: Jupyter Lab
    containerization: Docker
    version_control: Git
    ci_cd: GitHub Actions
  
  deployment:
    api: FastAPI
    frontend: Streamlit
    container: Docker

# Content Preferences
content_preferences:
  code_style:
    formatter: black
    linter: pylint
    type_hints: required
    docstrings: google_style
  
  documentation:
    format: markdown
    include_examples: true
    include_diagrams: true
  
  datasets:
    prefer_modern: true
    max_size_mb: 100
    sources: [kaggle, uci, huggingface]
  
  licensing:
    code: MIT
    content: CC-BY-SA-4.0
    respect_original: true

# Export Configuration
export:
  formats:
    - coursesgtm
    - courseplayerapp
    - docker
  
  coursesgtm:
    generate_tiers: true
    generate_pricing: true
    include_metadata: true
  
  courseplayerapp:
    convert_slides: html
    bundle_assets: true
    create_manifest: true
  
  docker:
    base_image: "python:3.10-slim"
    include_jupyter: true
    include_ollama: false  # Set true for full AI environment
```

---

## Loading and Using Principles

### Python Interface

```python
from pathlib import Path
import yaml
from typing import Dict, Any

class GuidingPrinciples:
    """Load and manage guiding principles"""
    
    def __init__(self, config_path: str = None):
        if config_path:
            self.config = self.load_from_file(config_path)
        else:
            self.config = self.get_defaults()
    
    @staticmethod
    def load_from_file(path: str) -> Dict[str, Any]:
        """Load principles from YAML file"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    @staticmethod
    def get_defaults() -> Dict[str, Any]:
        """Get default principles for 2026"""
        return {
            "philosophy": "augmented_human",
            "target_year": 2026,
            "primary_language": "Python",
            "llm_integration": {"provider": "OLLAMA"},
            "quality_thresholds": {
                "code": {"pass_rate": 1.0},
                "accuracy": 0.95,
                "completeness": 0.90
            },
            # ... full defaults
        }
    
    def get(self, key: str, default=None):
        """Get principle value by dotted key path"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def should_include_topic(self, topic: str) -> bool:
        """Check if a modern topic should be included"""
        critical = self.config['modern_topics'].get('critical', [])
        important = self.config['modern_topics'].get('important', [])
        return topic in (critical + important)
    
    def get_quality_threshold(self, metric: str) -> float:
        """Get quality threshold for specific metric"""
        return self.get(f'quality_thresholds.{metric}')
```

### Agent Usage

```python
# In an agent
class AnalysisAgent(BaseAgent):
    def __init__(self, llm_client, principles: GuidingPrinciples):
        self.llm = llm_client
        self.principles = principles
    
    def should_modernize_concept(self, concept: str) -> bool:
        """Decide if concept should be modernized based on principles"""
        target_year = self.principles.get('target_year')
        # ... analysis logic
        return decision
    
    def get_modern_topics(self) -> List[str]:
        """Get list of modern topics to add"""
        critical = self.principles.config['modern_topics']['critical']
        important = self.principles.config['modern_topics']['important']
        return critical + important
```

---

## Principle Presets

### Preset: "Default 2026"
**Use Case**: General purpose modernization

```yaml
name: "Default 2026"
description: "Balanced modernization for 2026"
philosophy: augmented_human
target_year: 2026
hands_on_ratio: 0.8
llm_integration: OLLAMA
modern_topics:
  - transformers
  - llms
  - mlops
  - docker
```

### Preset: "R to Python Migration"
**Use Case**: Statistical R courses → Python

```yaml
name: "R to Python Migration"
description: "Focused on R→Python translation"
philosophy: augmented_human
primary_language: Python
secondary_languages: [R]  # Keep R examples for comparison
translation_strategy: semantic  # Not just syntax
preserve_statistical_rigor: true
modern_topics:
  - docker  # For reproducibility
  - jupyter  # Modern notebooks
```

### Preset: "Bootcamp Style"
**Use Case**: Fast-paced, intensive learning

```yaml
name: "Bootcamp Style"
description: "Intensive, project-heavy curriculum"
philosophy: project_based
hands_on_ratio: 0.95  # Almost all hands-on
theory_ratio: 0.05
project_based: true
capstone_required: true
pace: intensive
skip_deep_theory: true  # Focus on practical application
```

### Preset: "Academic Rigor"
**Use Case**: University-level theoretical depth

```yaml
name: "Academic Rigor"
description: "Theoretical depth with mathematical foundations"
philosophy: augmented_human
hands_on_ratio: 0.5  # 50/50 theory/practice
theory_ratio: 0.5
mathematical_rigor: high
include_proofs: true
include_derivations: true
modern_topics:
  - theoretical_foundations
  - mathematical_ml
```

---

## Validating Principles

```python
from jsonschema import validate

PRINCIPLES_SCHEMA = {
    "type": "object",
    "required": ["philosophy", "target_year", "primary_language"],
    "properties": {
        "philosophy": {
            "type": "string",
            "enum": ["augmented_human", "self_paced", "project_based", "bootcamp"]
        },
        "target_year": {
            "type": "integer",
            "minimum": 2024,
            "maximum": 2030
        },
        "quality_thresholds": {
            "type": "object",
            "properties": {
                "accuracy": {"type": "number", "minimum": 0, "maximum": 1},
                "completeness": {"type": "number", "minimum": 0, "maximum": 1}
            }
        }
    }
}

def validate_principles(config: dict) -> bool:
    """Validate principles configuration"""
    try:
        validate(instance=config, schema=PRINCIPLES_SCHEMA)
        return True
    except Exception as e:
        print(f"Validation error: {e}")
        return False
```

---

This guiding principles framework ensures that all transformations are consistent, high-quality, and aligned with modern educational best practices.
