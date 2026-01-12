# SimulationPlayer Documentation

Comprehensive requirements and design documentation for the SimulationPlayer AI-powered interactive simulation system.

## Overview

SimulationPlayer is an extension for CoursePlayerApp that provides hands-on, AI-guided interactive simulations for technical learning. It combines:
- **7 Environment Types** for diverse technical domains
- **5 AI Agents** for intelligent guidance and support
- **OLLAMA Integration** for zero-budget local LLM inference
- **Tier-Based Access** via CoursesGTM integration

## Documentation Files

### Core Architecture & Design

1. **[ARCHITECTURE.md](ARCHITECTURE.md)** (690 lines)
   - System overview and goals
   - High-level architecture with Mermaid diagrams
   - Component breakdown (Core, Environments, Agents, UI)
   - Technology stack (Python, Streamlit, OLLAMA, Docker)
   - Data flow diagrams
   - State management
   - Tier integration with CoursesGTM

2. **[MODULE_STRUCTURE.md](MODULE_STRUCTURE.md)** (536 lines)
   - Complete directory structure
   - Module organization
   - Package structure
   - Configuration files
   - Import structure
   - Development workflow

### Environment & Agents

3. **[ENVIRONMENT_TYPES.md](ENVIRONMENT_TYPES.md)** (1,759 lines)
   - Terminal Simulator - Bash/shell commands
   - Code Editor - Monaco-based editing with execution
   - Infrastructure Builder - Drag-drop cloud architecture
   - Database Query - SQL with sample databases
   - API Interaction - REST/GraphQL testing
   - ML Pipeline Builder - Visual ML workflow designer
   - Docker Compose Designer - Interactive YAML builder

4. **[AGENT_SYSTEM.md](AGENT_SYSTEM.md)** (1,505 lines)
   - Step Guide Agent - Contextual explanations
   - Validation Agent - Rule-based validation
   - Error Recovery Agent - Mistake diagnosis
   - Hint Agent - Progressive 3-level hints
   - Context Agent - RAG-powered Q&A
   - OLLAMA integration details

### Scenario Creation

5. **[SCENARIO_AUTHORING.md](SCENARIO_AUTHORING.md)** (1,129 lines)
   - Complete YAML schema
   - Step-by-step authoring workflow
   - Best practices and guidelines
   - JSON Schema for validation
   - Template scenarios
   - Common patterns

6. **[EXAMPLE_SCENARIOS.md](EXAMPLE_SCENARIOS.md)** (494 lines)
   - 5 complete example scenarios:
     1. Docker First Container (Terminal)
     2. Git Basic Workflow (Terminal)
     3. Python Bug Fix (Code Editor)
     4. SQL Joins (Database)
     5. ML Pipeline (ML Pipeline Builder)

### User Interface & Integration

7. **[UI_DESIGN.md](UI_DESIGN.md)** (787 lines)
   - Streamlit component specifications
   - Layout wireframes
   - Environment-specific UIs
   - Completion modal
   - Responsive design
   - Color palette and typography

8. **[INTEGRATIONS.md](INTEGRATIONS.md)** (835 lines)
   - CoursePlayerApp plugin integration
   - CoursesGTM tier-based access
   - Docker for sandboxed execution
   - JupyterLab for code execution
   - OLLAMA for AI agents
   - Database integrations (SQLite, DuckDB, PostgreSQL)
   - Optional cloud sandbox (AWS, GCP, Azure)

### Analytics & Testing

9. **[ANALYTICS.md](ANALYTICS.md)** (661 lines)
   - Tracked metrics (completion, performance, engagement, learning)
   - Analytics dashboard for creators
   - Personal progress dashboard for learners
   - Adaptive difficulty system
   - Analytics API
   - Privacy & ethics considerations

10. **[TESTING.md](TESTING.md)** (764 lines)
    - Testing pyramid (Unit 60%, Integration 30%, E2E 10%)
    - Unit test examples
    - Integration test examples
    - E2E test examples
    - Performance testing
    - CI/CD workflow
    - Coverage goals (85% overall)

## Key Features

### 🎮 Interactive Environments
- **Terminal**: Sandboxed command-line practice
- **Code Editor**: Monaco editor with execution
- **Visual Builders**: Drag-drop for infrastructure and ML
- **Database**: SQL practice with sample data

### 🤖 AI-Powered Assistance
- **Step Guidance**: Contextual explanations without spoiling
- **Error Recovery**: Intelligent mistake diagnosis
- **Progressive Hints**: 3-level hint system
- **Q&A Support**: RAG-powered context agent

### 📊 Analytics & Adaptation
- Track completion, performance, and learning metrics
- Adaptive difficulty based on user performance
- Insights dashboard for course creators
- Personal progress tracking for learners

### 🔐 Security & Tier Access
- Docker sandboxing for all code execution
- No network access from containers
- Tier-based feature gating (Basic, Intermediate, Advanced)
- Resource limits and timeouts

## Technical Stack

- **Language**: Python 3.10+
- **UI Framework**: Streamlit
- **AI/LLM**: OLLAMA (llama3.2:3b, llama3.1:8b)
- **Containerization**: Docker
- **Code Editor**: Monaco Editor (streamlit-monaco)
- **Databases**: SQLite, DuckDB
- **Data Format**: YAML for scenarios
- **Validation**: JSON Schema

## Getting Started

### For Scenario Authors
1. Read [SCENARIO_AUTHORING.md](SCENARIO_AUTHORING.md) for authoring guide
2. Review [EXAMPLE_SCENARIOS.md](EXAMPLE_SCENARIOS.md) for templates
3. Use templates in `templates/` directory
4. Validate with JSON Schema

### For Developers
1. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Check [MODULE_STRUCTURE.md](MODULE_STRUCTURE.md) for codebase layout
3. Read [TESTING.md](TESTING.md) for testing strategy
4. See [INTEGRATIONS.md](INTEGRATIONS.md) for external dependencies

### For Course Creators
1. Understand [ANALYTICS.md](ANALYTICS.md) for tracking capabilities
2. Review [UI_DESIGN.md](UI_DESIGN.md) for learner experience
3. Check tier access in [INTEGRATIONS.md](INTEGRATIONS.md)

## Documentation Stats

- **Total Files**: 10
- **Total Lines**: 9,160
- **Total Size**: 268 KB
- **Diagrams**: Mermaid architecture and flow diagrams
- **Code Examples**: Python, YAML, SQL, Shell
- **Complete Scenarios**: 5 production-ready examples

## Next Steps

This is **documentation-only**. The actual implementation will be in a future PR.

The documentation enables:
- ✅ Scenario authoring by non-developers
- ✅ Clear integration path with CoursePlayerApp
- ✅ Agent system for helpful, non-spoiling guidance
- ✅ Flexible validation for multiple valid solutions
- ✅ Error recovery to help users learn from mistakes

## License

Part of the Data Science Specialization course materials.
Creative Commons Attribution NonCommercial ShareAlike (CC-NC-SA)
