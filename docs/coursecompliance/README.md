# CourseCompliance - Documentation

## Overview

**CourseCompliance** is an orchestrated multi-expert agent system that validates courses against comprehensive standards for technical correctness, pedagogical quality, legal compliance, accessibility, security, brand consistency, content integrity, and performance before launch.

This directory contains complete requirements and design documentation for the CourseCompliance system.

---

## Documentation Structure

### Core Documentation

| Document | Description | Lines |
|----------|-------------|-------|
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | System overview, components, technology stack, data flow diagrams | 499 |
| **[AGENT_SPECIFICATIONS.md](./AGENT_SPECIFICATIONS.md)** | Detailed specifications for all 8 expert agents | 1,676 |
| **[WORKFLOW_ORCHESTRATION.md](./WORKFLOW_ORCHESTRATION.md)** | LangGraph workflow with phases, state schema, error handling | 1,207 |
| **[STANDARDS_LIBRARY.md](./STANDARDS_LIBRARY.md)** | YAML-based standards definitions for all validation categories | 1,006 |
| **[REMEDIATION_SYSTEM.md](./REMEDIATION_SYSTEM.md)** | Auto-fix capabilities and remediation suggestion generation | 911 |
| **[COMPLIANCE_PROFILES.md](./COMPLIANCE_PROFILES.md)** | Three compliance profiles: Strict, Standard, Relaxed | 694 |
| **[HUMAN_REVIEW_DASHBOARD.md](./HUMAN_REVIEW_DASHBOARD.md)** | Streamlit UI specifications with 7 key views | 948 |
| **[INTEGRATION.md](./INTEGRATION.md)** | External system and tool integrations | 813 |
| **[REPORTING_SYSTEM.md](./REPORTING_SYSTEM.md)** | Five report types in multiple formats | 770 |
| **[TESTING.md](./TESTING.md)** | Comprehensive testing strategy with fixtures | 950 |

**Total Documentation**: 9,474 lines

### Standards Library

Example YAML standards files:

```
docs/coursecompliance/standards/
├── technical/
│   └── code_execution.yaml          # Code execution standards
├── accessibility/
│   └── wcag_2_1.yaml                # WCAG 2.1 AA compliance
└── security/
    └── credentials.yaml             # Credential security standards
```

---

## Quick Start

### 1. Understand the Architecture

Start with **[ARCHITECTURE.md](./ARCHITECTURE.md)** to understand:
- System purpose and goals
- High-level architecture
- 8 expert agent types
- Technology stack
- Data flow

### 2. Learn About the Agents

Read **[AGENT_SPECIFICATIONS.md](./AGENT_SPECIFICATIONS.md)** for:
- Detailed specifications for each of 8 agents
- Sub-agents and their responsibilities
- Tools and validation methods
- Pass/fail criteria
- Example issues

### 3. Understand the Workflow

See **[WORKFLOW_ORCHESTRATION.md](./WORKFLOW_ORCHESTRATION.md)** for:
- LangGraph state machine
- 7 workflow phases
- Parallel and sequential execution
- Error handling and retry logic
- Pause/resume for human review

### 4. Explore Compliance Standards

Check **[STANDARDS_LIBRARY.md](./STANDARDS_LIBRARY.md)** and `standards/` directory for:
- YAML format for standards
- Standards for all 8 categories
- Compliance thresholds
- Example standards files

### 5. Review Remediation

Learn from **[REMEDIATION_SYSTEM.md](./REMEDIATION_SYSTEM.md)** about:
- Auto-fixable issue categories
- Suggestion generation
- Re-validation workflow
- Audit trail

---

## Key Features

### 🤖 8 Expert Agents

1. **Technical Compliance**: Code execution, links, files, dependencies, notebooks, builds
2. **Pedagogical Quality**: Learning objectives, scaffolding, assessments, engagement
3. **Legal Compliance**: Licenses, attribution, copyright, privacy (GDPR/CCPA)
4. **Accessibility**: WCAG 2.1 AA, alt text, captions, contrast, readability
5. **Security**: Credentials, secrets, vulnerabilities, PII, safe examples
6. **Brand Consistency**: Style guide, terminology, tone, visual identity
7. **Content Integrity**: Fact checking, accuracy, references, consistency, plagiarism
8. **Performance**: Load times, file sizes, video quality, image optimization

### 🔄 Workflow Orchestration

- **LangGraph** state machine
- **Parallel execution** of independent agents
- **Sequential execution** of dependent agents
- **Auto-remediation** for ~30% of issues
- **Human-in-the-loop** for complex decisions
- **Pause/resume** capability

### 📊 Compliance Profiles

| Profile | Use Case | Critical Issues | Code Pass Rate | WCAG Compliance |
|---------|----------|----------------|----------------|-----------------|
| **Strict** | Enterprise, Regulated | 0 | 100% | 100% AA |
| **Standard** | General Courses | ≤3 | 95% | 85% AA |
| **Relaxed** | MVP, Beta | ≤10 | 80% | 50% Basic |

### 🛠️ Auto-Remediation

- Missing alt text → Generate with AI
- Code formatting → Apply black/prettier
- Outdated packages → Update requirements.txt
- Image compression → Optimize with tools
- Color contrast → Adjust colors for WCAG

### 👥 Human Review Dashboard

Streamlit-based UI with:
- Compliance overview
- Issue browser (filter, sort, search)
- Issue detail view
- Remediation workspace
- Approval workflow
- Audit trail viewer
- Trends & analytics

### 📄 Comprehensive Reporting

- **Compliance Report** (HTML + PDF)
- **Executive Summary** (1-page Markdown + PDF)
- **Detailed Findings** (HTML with collapsible sections)
- **Audit Log** (JSON + CSV)
- **Trend Report** (Interactive Plotly dashboard)

### 🔌 Integrations

**Course Production Ecosystem**:
- CourseTransformer (feedback loop)
- CoursesGTM (pre-export validation)
- CoursePlayerApp (compatibility checks)
- SimulationPlayer (scenario validation)

**External Tools**:
- axe-core (accessibility)
- Lighthouse (performance)
- Bandit (Python security)
- Safety (dependency vulnerabilities)
- OLLAMA (AI-powered analysis)

---

## Implementation Readiness

This documentation provides:

✅ **Complete specifications** for all components  
✅ **Detailed architecture** with diagrams  
✅ **API contracts** and data schemas  
✅ **Code examples** and templates  
✅ **Testing strategy** with fixtures  
✅ **Integration points** clearly defined  
✅ **Standards library** format and examples  

Implementation can proceed directly from this documentation without further clarification.

---

## Success Metrics

- **Auto-Fix Rate**: >30% of common issues
- **Time to Compliance**: <30 minutes for standard course
- **Approval Rate**: >80% of courses passing Standard profile
- **Human Review Time**: <15 minutes per course
- **Coverage**: >80% test coverage

---

## Technology Stack

- **Python 3.10+**: Primary language
- **LangGraph**: Workflow orchestration
- **OLLAMA**: AI-powered analysis
- **Streamlit**: Human review UI
- **axe-core, Lighthouse, Bandit, Safety**: External tools
- **SQLite**: State persistence
- **Jinja2**: Report templates
- **Plotly**: Trend visualizations

---

## Augmented Human Philosophy

CourseCompliance embodies "AI assists, humans decide":

**AI Responsibilities**:
- Detect issues comprehensively
- Classify severity and priority
- Generate remediation suggestions
- Apply safe, deterministic fixes

**Human Responsibilities**:
- Final judgment on ambiguous cases
- Risk acceptance with justification
- Creative solutions beyond AI suggestions
- Launch approval sign-off

---

## Next Steps

1. **Review**: Read through all documentation files
2. **Implement**: Build agents, workflow, dashboard
3. **Test**: Create test fixtures and run comprehensive tests
4. **Deploy**: Integrate with course production pipeline
5. **Iterate**: Gather feedback and improve

---

## Questions?

For questions or clarifications about this documentation, please refer to:
- The specific documentation file for the topic
- Code examples provided in the documentation
- YAML standards files in the `standards/` directory

---

## Version

**Documentation Version**: 1.0.0  
**Last Updated**: January 12, 2026  
**Status**: Complete and ready for implementation

---

## License

This documentation is part of the Johns Hopkins Data Science Specialization course materials and follows the same licensing terms as the parent repository.
