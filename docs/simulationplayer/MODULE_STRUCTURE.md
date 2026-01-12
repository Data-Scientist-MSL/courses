# SimulationPlayer Module Structure

This document defines the complete directory structure and module organization for SimulationPlayer.

---

## Directory Structure

```
SimulationPlayer/
├── simulationplayer/                 # Main package
│   ├── __init__.py
│   ├── __version__.py
│   │
│   ├── core/                         # Core engine components
│   │   ├── __init__.py
│   │   ├── engine.py                 # SimulationEngine
│   │   ├── state_machine.py          # State management
│   │   ├── validator.py              # ValidationAgent
│   │   └── checkpoint.py             # CheckpointManager
│   │
│   ├── environments/                 # Environment types
│   │   ├── __init__.py
│   │   ├── base.py                   # Environment base class
│   │   ├── terminal.py               # TerminalSimulator
│   │   ├── code_editor.py            # CodeEditorSimulator
│   │   ├── infrastructure.py         # InfrastructureBuilder
│   │   ├── database.py               # DatabaseQuerySimulator
│   │   ├── api.py                    # APIInteractionSimulator
│   │   ├── ml_pipeline.py            # MLPipelineBuilder
│   │   └── docker_compose.py         # DockerComposeDesigner
│   │
│   ├── agents/                       # AI guidance agents
│   │   ├── __init__.py
│   │   ├── base.py                   # BaseAgent
│   │   ├── step_guide.py             # StepGuideAgent
│   │   ├── error_recovery.py         # ErrorRecoveryAgent
│   │   ├── hint.py                   # HintAgent
│   │   ├── context.py                # ContextAgent
│   │   └── orchestrator.py           # AgentOrchestrator
│   │
│   ├── ui/                           # Streamlit UI components
│   │   ├── __init__.py
│   │   ├── main.py                   # Main simulation viewer
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── header.py             # Header bar
│   │   │   ├── progress.py           # Progress indicator
│   │   │   ├── step_panel.py         # Step panel
│   │   │   ├── sidebar.py            # Sidebar panels
│   │   │   ├── feedback.py           # Feedback display
│   │   │   └── completion_modal.py   # Completion modal
│   │   └── themes/
│   │       └── default.css           # UI styling
│   │
│   ├── scenarios/                    # Scenario management
│   │   ├── __init__.py
│   │   ├── loader.py                 # ScenarioLoader
│   │   ├── schema.py                 # Scenario data models
│   │   └── validator.py              # YAML schema validator
│   │
│   ├── integrations/                 # External integrations
│   │   ├── __init__.py
│   │   ├── docker_client.py          # Docker integration
│   │   ├── jupyter_client.py         # Jupyter integration
│   │   ├── ollama_client.py          # OLLAMA LLM client
│   │   ├── database_client.py        # Database integration
│   │   ├── courseplayer.py           # CoursePlayerApp plugin
│   │   └── coursesgtm.py             # CoursesGTM API client
│   │
│   ├── analytics/                    # Analytics & tracking
│   │   ├── __init__.py
│   │   ├── tracker.py                # Event tracking
│   │   ├── metrics.py                # Metrics calculation
│   │   ├── insights.py               # Insight generation
│   │   └── dashboard.py              # Analytics dashboard
│   │
│   └── utils/                        # Utilities
│       ├── __init__.py
│       ├── config.py                 # Configuration management
│       ├── logging.py                # Logging setup
│       ├── cache.py                  # Caching utilities
│       └── helpers.py                # Helper functions
│
├── scenarios/                        # Scenario YAML files
│   ├── docker/
│   │   ├── first-container.yml
│   │   ├── volumes-networks.yml
│   │   └── multi-container.yml
│   ├── git/
│   │   ├── basic-workflow.yml
│   │   ├── branching.yml
│   │   └── conflict-resolution.yml
│   ├── python/
│   │   ├── bug-fix-sum.yml
│   │   ├── type-hints.yml
│   │   └── refactoring.yml
│   ├── sql/
│   │   ├── select-basics.yml
│   │   ├── joins.yml
│   │   └── window-functions.yml
│   ├── ml/
│   │   ├── pipeline-basics.yml
│   │   ├── feature-engineering.yml
│   │   └── model-evaluation.yml
│   └── databases/                    # Sample databases
│       ├── ecommerce/
│       │   ├── schema.sql
│       │   └── data.sql
│       └── social/
│           ├── schema.sql
│           └── data.sql
│
├── templates/                        # Scenario templates
│   ├── terminal-template.yml
│   ├── code-editor-template.yml
│   ├── database-template.yml
│   └── ml-pipeline-template.yml
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures
│   │
│   ├── unit/                         # Unit tests
│   │   ├── test_core/
│   │   │   ├── test_engine.py
│   │   │   ├── test_state_machine.py
│   │   │   └── test_validator.py
│   │   ├── test_environments/
│   │   │   ├── test_terminal.py
│   │   │   ├── test_code_editor.py
│   │   │   └── test_database.py
│   │   └── test_agents/
│   │       ├── test_step_guide.py
│   │       ├── test_error_recovery.py
│   │       └── test_hint.py
│   │
│   ├── integration/                  # Integration tests
│   │   ├── test_docker_integration.py
│   │   ├── test_ollama_integration.py
│   │   └── test_scenario_execution.py
│   │
│   ├── e2e/                          # End-to-end tests
│   │   ├── test_docker_scenario.py
│   │   ├── test_git_scenario.py
│   │   └── test_sql_scenario.py
│   │
│   └── fixtures/                     # Test data
│       ├── sample_scenarios.yml
│       ├── mock_responses.json
│       └── test_databases/
│
├── docs/                             # Documentation
│   └── simulationplayer/
│       ├── ARCHITECTURE.md
│       ├── ENVIRONMENT_TYPES.md
│       ├── AGENT_SYSTEM.md
│       ├── SCENARIO_AUTHORING.md
│       ├── UI_DESIGN.md
│       ├── INTEGRATIONS.md
│       ├── EXAMPLE_SCENARIOS.md
│       ├── ANALYTICS.md
│       ├── MODULE_STRUCTURE.md
│       └── TESTING.md
│
├── scripts/                          # Utility scripts
│   ├── setup_ollama.sh               # Pull OLLAMA models
│   ├── validate_scenarios.py         # Validate all scenarios
│   ├── generate_scenario.py          # Scenario generator
│   └── seed_analytics.py             # Seed test analytics data
│
├── docker/                           # Docker configurations
│   ├── Dockerfile                    # Main Dockerfile
│   ├── Dockerfile.runtime            # Simulation runtime image
│   └── docker-compose.yml            # Development setup
│
├── .github/                          # GitHub configuration
│   └── workflows/
│       ├── test.yml                  # CI tests
│       ├── lint.yml                  # Code linting
│       └── deploy.yml                # Deployment
│
├── requirements/                     # Python dependencies
│   ├── base.txt                      # Core dependencies
│   ├── dev.txt                       # Development dependencies
│   └── test.txt                      # Testing dependencies
│
├── .gitignore
├── .env.example                      # Environment variables template
├── setup.py                          # Package setup
├── pyproject.toml                    # Project configuration
├── README.md
└── LICENSE
```

---

## Module Descriptions

### Core (`simulationplayer/core/`)

#### `engine.py`
```python
class SimulationEngine:
    """
    Main orchestrator for simulations.
    
    Responsibilities:
    - Load scenarios
    - Initialize environments
    - Manage step progression
    - Coordinate agents
    - Handle checkpoints
    """
    
    def load_scenario(scenario_id: str) -> Scenario
    def execute_step(step_id: str, action: Action) -> StepResult
    def save_checkpoint() -> CheckpointData
```

#### `state_machine.py`
```python
class StateMachine:
    """
    Manages simulation state transitions.
    
    States: NOT_STARTED, IN_PROGRESS, STEP_COMPLETE, 
            SCENARIO_COMPLETE, PAUSED, FAILED
    """
    
    def transition(from_state: State, to_state: State) -> bool
    def get_current_state() -> State
```

#### `validator.py`
```python
class Validator:
    """
    Validates user actions against step requirements.
    
    Supports: command validation, output validation,
              state validation, multi-criteria validation
    """
    
    def validate(action: Action, rules: list[ValidationRule]) -> ValidationResult
```

### Environments (`simulationplayer/environments/`)

Each environment module implements the `Environment` base class:

```python
class Environment(ABC):
    @abstractmethod
    def initialize(initial_state: dict) -> None
    
    @abstractmethod
    def execute_action(action: Action) -> ActionResult
    
    @abstractmethod
    def get_state() -> dict
    
    @abstractmethod
    def reset() -> None
    
    @abstractmethod
    def cleanup() -> None
    
    @abstractmethod
    def render_ui() -> StreamlitComponent
```

### Agents (`simulationplayer/agents/`)

All agents extend `BaseAgent`:

```python
class BaseAgent(ABC):
    def __init__(model: str, ollama_endpoint: str)
    
    @abstractmethod
    def generate_response(context: dict) -> AgentResponse
```

### UI (`simulationplayer/ui/`)

Streamlit-based user interface:

- **main.py**: Entry point, overall layout
- **components/**: Reusable UI components
- **themes/**: CSS styling

### Integrations (`simulationplayer/integrations/`)

External service clients:

- **docker_client.py**: Container management
- **ollama_client.py**: LLM inference
- **coursesgtm.py**: Progress tracking API

---

## Configuration Files

### `pyproject.toml`
```toml
[tool.poetry]
name = "simulationplayer"
version = "0.1.0"
description = "AI-powered interactive simulation platform"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
streamlit = "^1.28.0"
docker = "^6.1.0"
pyyaml = "^6.0"
pydantic = "^2.0"
ollama = "^0.1.0"
duckdb = "^0.9.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
black = "^23.7.0"
mypy = "^1.5.0"
flake8 = "^6.1.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### `.env.example`
```bash
# OLLAMA Configuration
OLLAMA_ENDPOINT=http://localhost:11434

# CoursesGTM Integration
COURSESGTM_API_KEY=your_api_key_here
COURSESGTM_BASE_URL=https://api.coursesgtm.com/v1

# Docker Configuration
DOCKER_HOST=unix:///var/run/docker.sock

# Database Configuration (optional)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=simulationplayer
POSTGRES_USER=simuser
POSTGRES_PASSWORD=simpass

# Analytics Configuration
ENABLE_ANALYTICS=true
ANALYTICS_DB=analytics.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=simulationplayer.log

# Security
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Entry Points

### CLI Tool
```bash
# Start simulation UI
simulationplayer run --scenario docker-first-container

# Validate scenarios
simulationplayer validate scenarios/

# Generate new scenario from template
simulationplayer new --type terminal --name my-scenario

# Analytics dashboard
simulationplayer analytics --scenario docker-first-container
```

### Python API
```python
from simulationplayer import SimulationEngine

# Load and run scenario
engine = SimulationEngine()
scenario = engine.load_scenario('docker-first-container')
result = engine.run(scenario)
```

### Streamlit App
```bash
# Launch as standalone app
streamlit run simulationplayer/ui/main.py

# Or as CoursePlayerApp plugin
# Integrated automatically when installed
```

---

## Package Installation

### Development Installation
```bash
# Clone repository
git clone https://github.com/your-org/simulationplayer.git
cd simulationplayer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Set up OLLAMA
scripts/setup_ollama.sh

# Run tests
pytest
```

### Production Installation
```bash
pip install simulationplayer

# Or with specific extras
pip install simulationplayer[cloud]  # For cloud sandbox
pip install simulationplayer[analytics]  # For advanced analytics
```

---

## Import Structure

```python
# Core components
from simulationplayer import SimulationEngine, ScenarioLoader
from simulationplayer.core import StateMachine, Validator

# Environments
from simulationplayer.environments import (
    TerminalSimulator,
    CodeEditorSimulator,
    DatabaseQuerySimulator
)

# Agents
from simulationplayer.agents import (
    StepGuideAgent,
    ErrorRecoveryAgent,
    HintAgent,
    ContextAgent
)

# Integrations
from simulationplayer.integrations import (
    DockerClient,
    OllamaClient,
    CoursesGTMClient
)

# Analytics
from simulationplayer.analytics import AnalyticsEngine, MetricsCalculator
```

---

## Development Workflow

### 1. Create New Environment Type
```bash
# Create environment module
touch simulationplayer/environments/custom_env.py

# Implement Environment interface
# Add tests
touch tests/unit/test_environments/test_custom_env.py

# Add documentation
# Update ENVIRONMENT_TYPES.md
```

### 2. Create New Scenario
```bash
# Generate from template
python scripts/generate_scenario.py --type terminal --name my-scenario

# Edit scenario YAML
vim scenarios/my-category/my-scenario.yml

# Validate
python scripts/validate_scenarios.py scenarios/my-category/my-scenario.yml

# Test
pytest tests/e2e/test_my_scenario.py
```

### 3. Add New Agent
```bash
# Create agent module
touch simulationplayer/agents/custom_agent.py

# Implement BaseAgent
# Add to AgentOrchestrator
# Add tests
```

---

## File Naming Conventions

- **Python modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Scenario files**: `kebab-case.yml`
- **Test files**: `test_*.py`

---

## Code Organization Principles

1. **Separation of Concerns**: Each module has one clear responsibility
2. **Dependency Injection**: Components receive dependencies, don't create them
3. **Interface-Based**: Use abstract base classes for extensibility
4. **Configuration over Code**: Settings in config files, not hardcoded
5. **Testability**: All components easily testable in isolation

---

This modular structure enables easy extension, maintenance, and testing of SimulationPlayer while keeping the codebase organized and scalable.
