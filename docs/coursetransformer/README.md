# CourseTransformer Documentation

## Overview

CourseTransformer is an AI-powered, human-guided workflow system that transforms legacy educational content into modern, interactive courses compatible with CoursesGTM and CoursePlayerApp.

## Vision

An intelligent multi-agent system that:
- Ingests legacy courses (like the Johns Hopkins R-based Data Science Specialization)
- Analyzes content for relevance and gaps
- Plans modernization with human oversight
- Transforms code and concepts to modern equivalents
- Generates new interactive content
- Ensures quality through automated checks
- Exports to modern course delivery platforms

## Key Features

- **Multi-Agent Architecture**: 7 specialized agents working in concert
- **LangGraph Orchestration**: Stateful workflow with human-in-the-loop checkpoints
- **OLLAMA Integration**: Privacy-first local LLM processing
- **Human-Guided**: Humans make final decisions on all creative and pedagogical choices
- **Quality Assured**: Automated fact-checking, code execution, and consistency validation
- **Flexible Export**: Compatible with CoursesGTM and CoursePlayerApp

## Documentation Index

### 1. [ARCHITECTURE.md](./ARCHITECTURE.md)
**System design, components, and data flow**

Key sections:
- System Overview
- High-Level Architecture (Mermaid diagram)
- Component Breakdown (7 agents, orchestrator, human interface, knowledge base)
- Technology Stack
- Data Flow (sequence diagram)
- State Management
- Scalability Considerations

### 2. [AGENT_SPECIFICATIONS.md](./AGENT_SPECIFICATIONS.md)
**Detailed specifications for all 7 core agents**

Agents covered:
1. **Ingestion Agent**: Parse legacy content (R, PDF, MD, video)
2. **Analysis Agent**: Assess relevance and identify gaps
3. **Planning Agent**: Design curriculum structure
4. **Modernization Agent**: Transform code R → Python
5. **Generation Agent**: Create slides, labs, quizzes, diagrams
6. **Quality Assurance Agent**: Verify accuracy and completeness
7. **Export Agent**: Package for CoursesGTM/CoursePlayerApp

Each agent includes:
- Purpose and responsibilities
- Inputs and outputs
- Capabilities and tools
- LLM usage patterns
- Error handling

### 3. [WORKFLOW_ORCHESTRATION.md](./WORKFLOW_ORCHESTRATION.md)
**LangGraph workflow implementation**

Key sections:
- State Schema (TypedDict)
- Workflow Graph (Mermaid)
- Conditional Edge Functions
- Human Review Nodes
- Parallel Processing
- State Persistence
- Error Handling & Retry Logic

### 4. [HUMAN_LOOP_INTERFACE.md](./HUMAN_LOOP_INTERFACE.md)
**Streamlit UI specification**

Pages covered:
1. Home Dashboard
2. Guiding Principles Editor
3. Ingestion Tab
4. Analysis Tab
5. **Planning Tab** ⭐ (Human Review Required)
6. Progress Tab
7. **Content Review Tab** ⭐ (Human Review Required)
8. Quality Report Tab
9. Export Tab

Includes:
- UI mockups and layouts
- WebSocket integration for real-time updates
- State management across pages

### 5. [GUIDING_PRINCIPLES.md](./GUIDING_PRINCIPLES.md)
**Configurable principles framework**

Categories:
- **Augmented Human Philosophy**: AI assists, humans decide
- **Pedagogical Principles**: Active learning, scaffolded difficulty
- **Modernization Guidelines**: When to keep/modernize/create/remove
- **Quality Standards**: Code quality, accuracy, completeness thresholds
- **Technology Preferences**: Python 3.10+, PyTorch, OLLAMA
- **Configurable YAML Schema**: Complete configuration example

Includes:
- 4 preset configurations
- Python interface for loading principles
- Validation schema

### 6. [AGENT_TEMPLATES.md](./AGENT_TEMPLATES.md)
**Code templates for implementation**

Includes:
- BaseAgent class (abstract)
- Example: IngestionAgent (complete implementation)
- Example: AnalysisAgent (complete implementation)
- AgentFactory pattern
- Unit test examples

### 7. [INTEGRATION.md](./INTEGRATION.md)
**External system integrations**

Integrations covered:
- **CoursesGTM**: Schema mapping, curriculum.json, tiers.json
- **CoursePlayerApp**: Directory structure, manifest format
- **OLLAMA**: Model selection, context window management, caching
- **Knowledge Base (RAG)**: ChromaDB, embeddings, fact-checking

### 8. [EXAMPLES.md](./EXAMPLES.md)
**Detailed transformation examples**

Examples:
1. **Example 1**: Transform "01_DataScientistToolbox" (R) → Modern Foundations (Python)
   - Complete workflow walkthrough
   - Stage-by-stage outputs
   - Human review decisions
   - Total time: 83 minutes
   
2. **Example 2**: Create "10_Transformers_LLMs" from scratch
   - No legacy content
   - Pure AI generation
   - Total time: 119 minutes

### 9. [MODULE_STRUCTURE.md](./MODULE_STRUCTURE.md)
**Codebase organization**

Defines:
- Project root structure
- Package structure (`coursetransformer/`)
- Entry points (CLI, Streamlit)
- Installation & setup
- Dependencies (pyproject.toml)

### 10. [TESTING.md](./TESTING.md)
**Testing strategy**

Covers:
- Test pyramid (unit, integration, E2E)
- Test structure
- Agent unit tests
- Integration tests
- E2E tests with mocked human reviews
- Coverage targets (>80%)
- CI/CD integration

## Quick Start

### For Implementers

1. Start with [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the system
2. Review [AGENT_SPECIFICATIONS.md](./AGENT_SPECIFICATIONS.md) for agent details
3. Study [WORKFLOW_ORCHESTRATION.md](./WORKFLOW_ORCHESTRATION.md) for LangGraph implementation
4. Use [AGENT_TEMPLATES.md](./AGENT_TEMPLATES.md) as coding reference
5. Follow [MODULE_STRUCTURE.md](./MODULE_STRUCTURE.md) for project organization
6. Implement tests per [TESTING.md](./TESTING.md)

### For Users

1. Read [ARCHITECTURE.md](./ARCHITECTURE.md) - System Overview section
2. Review [HUMAN_LOOP_INTERFACE.md](./HUMAN_LOOP_INTERFACE.md) to understand the UI
3. Configure principles using [GUIDING_PRINCIPLES.md](./GUIDING_PRINCIPLES.md)
4. See [EXAMPLES.md](./EXAMPLES.md) for real-world transformation workflows

### For Integrators

1. Review [INTEGRATION.md](./INTEGRATION.md) for system integration points
2. Study CoursesGTM schema in [INTEGRATION.md](./INTEGRATION.md)
3. Understand CoursePlayerApp format in [INTEGRATION.md](./INTEGRATION.md)

## Technology Stack

- **Language**: Python 3.10+
- **Workflow**: LangGraph
- **Agent Framework**: LangChain
- **LLM**: OLLAMA (local) with fallback to OpenAI/Anthropic
- **UI**: Streamlit
- **Vector DB**: ChromaDB
- **State**: SQLite + JSON
- **Export**: CoursesGTM JSON schema, CoursePlayerApp directory structure

## Design Philosophy

### Augmented Human
- **AI assists, humans decide**: AI handles mechanical tasks, humans make creative decisions
- **Transparency**: All AI suggestions are explainable
- **Human authority**: Humans have veto power over all AI outputs

### Privacy-First
- **Local LLM**: OLLAMA runs locally (no external API calls by default)
- **Data sovereignty**: All processing can happen on-premises
- **Optional cloud**: OpenAI/Anthropic available only with explicit consent

### Quality-Driven
- **Automated QA**: Code execution, fact-checking, consistency validation
- **Human review**: Mandatory checkpoints for planning and content
- **Measurable standards**: >95% accuracy, 100% code pass rate, >90% completeness

## Acceptance Criteria

✅ All 10 documentation files created with comprehensive content
✅ Architecture includes Mermaid diagrams (workflow, state machine, data flow)
✅ All 7 agent types fully specified with inputs, outputs, capabilities, tools
✅ LangGraph workflow with conditional edges, error handling, parallel processing
✅ Streamlit UI mockups/wireframes for all 9 tabs
✅ Guiding principles framework with YAML configuration
✅ Agent code templates (base class + 2 example agents)
✅ Integration specifications for CoursesGTM, CoursePlayerApp, OLLAMA, RAG
✅ 2 detailed example transformations (legacy→modern, new creation)
✅ Testing strategy with coverage targets (>80%)

## Next Steps

The actual CourseTransformer implementation will be developed based on these specifications in future pull requests.

This documentation provides:
- Complete system design
- Implementation guidelines
- Integration specifications
- Quality standards
- Testing requirements

It enables implementation without further clarification while maintaining flexibility for iterative improvement.

## License

This documentation is part of the CourseTransformer project.
Content follows CC-BY-SA-4.0 license.
Code examples follow MIT license.

---

**Last Updated**: 2026-01-12  
**Version**: 1.0.0  
**Status**: Complete - Ready for Implementation
