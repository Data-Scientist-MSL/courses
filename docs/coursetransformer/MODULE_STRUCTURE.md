# CourseTransformer - Module Structure

This document defines the directory structure and organization for the CourseTransformer codebase.

## Project Root Structure

```
CourseTransformer/
├── coursetransformer/          # Main package
│   ├── __init__.py
│   ├── agents/                 # Agent implementations
│   ├── orchestrator/           # LangGraph workflow
│   ├── human_loop/            # Streamlit UI
│   ├── knowledge/             # RAG system
│   ├── llm/                   # LLM integrations
│   ├── principles/            # Principle loaders
│   └── utils/                 # Utilities
├── workflows/                  # Workflow definitions
├── templates/                  # Content templates
├── examples/                   # Usage examples
├── tests/                      # Test suite
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── config/                     # Configuration files
├── pyproject.toml             # Project configuration
├── requirements.txt           # Dependencies
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Multi-container setup
└── README.md                  # Project README
```

## Core Package Structure

### agents/

```
coursetransformer/agents/
├── __init__.py
├── base.py                    # BaseAgent class
├── ingestion.py              # IngestionAgent
├── analysis.py               # AnalysisAgent
├── planning.py               # PlanningAgent
├── modernization.py          # ModernizationAgent
├── generation.py             # GenerationAgent
├── qa.py                     # QualityAgent
├── export.py                 # ExportAgent
└── factory.py                # AgentFactory
```

**Key Files**:
- `base.py`: Base class with common functionality
- Each agent in separate file for modularity
- `factory.py`: Factory pattern for agent creation

### orchestrator/

```
coursetransformer/orchestrator/
├── __init__.py
├── workflow.py               # LangGraph workflow definition
├── state.py                  # State schema
├── routes.py                 # Conditional edge functions
├── checkpoints.py            # Checkpoint management
└── events.py                 # Event emitters
```

**Responsibilities**:
- LangGraph workflow graph definition
- State management
- Routing logic
- Checkpoint/resume functionality

### human_loop/

```
coursetransformer/human_loop/
├── __init__.py
├── app.py                    # Main Streamlit app
├── pages/
│   ├── 1_Guiding_Principles.py
│   ├── 2_Ingestion.py
│   ├── 3_Analysis.py
│   ├── 4_Planning.py
│   ├── 5_Progress.py
│   ├── 6_Content_Review.py
│   ├── 7_Quality_Report.py
│   └── 8_Export.py
├── components/
│   ├── state_manager.py      # Session state management
│   ├── ui_components.py      # Reusable UI components
│   └── websocket_client.py   # WebSocket for real-time updates
└── utils/
    ├── formatting.py         # Data formatting utilities
    └── validation.py         # Input validation
```

### knowledge/

```
coursetransformer/knowledge/
├── __init__.py
├── rag.py                    # RAG system interface
├── vector_store.py           # ChromaDB wrapper
├── embeddings.py             # Embedding generation
├── fact_checker.py           # Fact-checking logic
└── seed_data/                # Initial knowledge base data
    ├── modern_practices.txt
    ├── best_practices.txt
    └── reference_docs.txt
```

### llm/

```
coursetransformer/llm/
├── __init__.py
├── client.py                 # Unified LLM client interface
├── ollama.py                 # OLLAMA integration
├── openai.py                 # OpenAI integration (optional)
├── anthropic.py              # Anthropic integration (optional)
├── prompts/                  # Prompt templates
│   ├── ingestion_prompts.py
│   ├── analysis_prompts.py
│   ├── planning_prompts.py
│   ├── modernization_prompts.py
│   ├── generation_prompts.py
│   └── qa_prompts.py
└── cache.py                  # Response caching
```

### principles/

```
coursetransformer/principles/
├── __init__.py
├── loader.py                 # YAML principle loader
├── validator.py              # Principle validation
├── defaults.py               # Default configurations
└── presets/                  # Pre-defined presets
    ├── default_2026.yaml
    ├── r_to_python.yaml
    ├── bootcamp_style.yaml
    └── academic_rigor.yaml
```

### utils/

```
coursetransformer/utils/
├── __init__.py
├── file_utils.py             # File I/O operations
├── parser_utils.py           # Code parsing utilities
├── validation.py             # Schema validation
├── formatting.py             # Data formatting
├── logging_config.py         # Logging setup
└── constants.py              # Constants and enums
```

## Templates Directory

```
templates/
├── slides/
│   ├── base_template.md      # Base Marp slide template
│   └── theme.css             # Custom Marp theme
├── labs/
│   ├── notebook_template.ipynb
│   └── lab_structure.json
├── quizzes/
│   └── quiz_template.json
├── diagrams/
│   └── diagram_patterns.md   # Common Mermaid patterns
└── exports/
    ├── coursesgtm_template.json
    └── manifest_template.json
```

## Workflows Directory

```
workflows/
├── full_transformation.yaml  # Complete workflow config
├── incremental_update.yaml   # Partial update workflow
├── new_course_creation.yaml  # From-scratch workflow
└── schemas/
    └── workflow_schema.json  # Workflow config schema
```

## Configuration Directory

```
config/
├── default_config.yaml       # Default application config
├── development.yaml          # Development overrides
├── production.yaml           # Production overrides
├── logging.yaml              # Logging configuration
└── models.yaml               # LLM model configurations
```

## Entry Points

### CLI Entry Point

```python
# coursetransformer/__main__.py
import click
from .orchestrator import workflow

@click.group()
def cli():
    """CourseTransformer CLI"""
    pass

@cli.command()
@click.option('--course-path', required=True)
@click.option('--principles', required=True)
def transform(course_path, principles):
    """Transform a legacy course"""
    result = workflow.start_transformation(course_path, principles)
    click.echo(f"Transformation started: {result['transformation_id']}")

@cli.command()
def ui():
    """Launch Streamlit UI"""
    import subprocess
    subprocess.run(["streamlit", "run", "coursetransformer/human_loop/app.py"])

if __name__ == '__main__':
    cli()
```

### Streamlit Entry Point

```python
# coursetransformer/human_loop/app.py
import streamlit as st

st.set_page_config(
    page_title="CourseTransformer",
    page_icon="🎓",
    layout="wide"
)

st.title("CourseTransformer Dashboard")
# ... dashboard implementation
```

## Installation & Setup

### Development Setup

```bash
# Clone repository
git clone https://github.com/org/CourseTransformer.git
cd CourseTransformer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -e ".[dev]"

# Install OLLAMA (if not already installed)
# See https://ollama.ai/download

# Pull required models
ollama pull llama2:7b
ollama pull llama2:13b
ollama pull mixtral:8x7b
ollama pull codellama:13b

# Seed knowledge base
python -m coursetransformer.knowledge.seed

# Run tests
pytest

# Start UI
streamlit run coursetransformer/human_loop/app.py
```

### Docker Setup

```bash
# Build image
docker-compose build

# Start services
docker-compose up

# UI available at http://localhost:8501
```

## Dependencies (pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "coursetransformer"
version = "0.1.0"
description = "AI-powered course transformation system"
requires-python = ">=3.10"

dependencies = [
    "langchain>=0.1.0",
    "langgraph>=0.1.0",
    "streamlit>=1.30.0",
    "chromadb>=0.4.0",
    "PyPDF2>=3.0.0",
    "pdfplumber>=0.10.0",
    "pyyaml>=6.0",
    "click>=8.1.0",
    "pandas>=2.0.0",
    "requests>=2.31.0",
    "aiohttp>=3.9.0",
    "jsonschema>=4.20.0",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "pylint>=3.0.0",
    "mypy>=1.7.0",
]

[project.scripts]
coursetransformer = "coursetransformer.__main__:cli"
```

---

This modular structure ensures maintainability, testability, and extensibility of the CourseTransformer system.
