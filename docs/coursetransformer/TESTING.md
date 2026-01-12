# CourseTransformer - Testing Strategy

This document defines the testing approach for the CourseTransformer system.

## Testing Philosophy

- **Comprehensive Coverage**: Target >80% code coverage
- **Test Pyramid**: More unit tests, fewer integration tests, minimal E2E tests
- **Fast Feedback**: Unit tests run in <5 seconds
- **Isolated Tests**: No dependencies between tests
- **Mocked External Services**: Don't call actual OLLAMA/APIs in tests

## Test Structure

```
tests/
├── unit/                      # Unit tests
│   ├── agents/
│   │   ├── test_ingestion_agent.py
│   │   ├── test_analysis_agent.py
│   │   ├── test_planning_agent.py
│   │   ├── test_modernization_agent.py
│   │   ├── test_generation_agent.py
│   │   ├── test_qa_agent.py
│   │   └── test_export_agent.py
│   ├── orchestrator/
│   │   ├── test_workflow.py
│   │   ├── test_state.py
│   │   └── test_routes.py
│   ├── knowledge/
│   │   ├── test_rag.py
│   │   └── test_fact_checker.py
│   └── llm/
│       ├── test_client.py
│       └── test_cache.py
├── integration/               # Integration tests
│   ├── test_agent_chaining.py
│   ├── test_llm_integration.py
│   ├── test_kb_integration.py
│   └── test_export_integration.py
├── e2e/                       # End-to-end tests
│   ├── test_full_transformation.py
│   └── test_new_course_creation.py
├── fixtures/                  # Test data
│   ├── sample_legacy_course/
│   ├── expected_outputs/
│   └── mock_responses.json
└── conftest.py               # Pytest configuration
```

## Unit Tests

### Agent Tests

Test each agent's core logic in isolation.

```python
# tests/unit/agents/test_ingestion_agent.py
import pytest
from unittest.mock import Mock, patch
from coursetransformer.agents import IngestionAgent

@pytest.fixture
def mock_llm():
    """Mock LLM client"""
    llm = Mock()
    llm.generate.return_value = '{"concepts": []}'
    return llm

@pytest.fixture
def sample_principles():
    """Sample guiding principles"""
    return {
        "target_year": 2026,
        "primary_language": "Python"
    }

def test_ingestion_agent_initialization(mock_llm, sample_principles):
    """Test agent initializes correctly"""
    agent = IngestionAgent(mock_llm, sample_principles)
    assert agent.llm == mock_llm
    assert agent.principles == sample_principles
    assert len(agent.tools) > 0

def test_parse_r_file(mock_llm, sample_principles, tmp_path):
    """Test R file parsing"""
    agent = IngestionAgent(mock_llm, sample_principles)
    
    # Create test R file
    r_file = tmp_path / "test.R"
    r_file.write_text("""
    library(ggplot2)
    library(dplyr)
    
    my_function <- function(x) {
        return(x + 1)
    }
    """)
    
    result = agent._parse_r_file(str(r_file))
    
    assert result["language"] == "R"
    assert "ggplot2" in result["libraries"]
    assert "dplyr" in result["libraries"]
    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "my_function"

def test_execute_success(mock_llm, sample_principles, tmp_path):
    """Test successful execution"""
    agent = IngestionAgent(mock_llm, sample_principles)
    
    # Create test course directory
    course_dir = tmp_path / "test_course"
    course_dir.mkdir()
    (course_dir / "test.R").write_text("library(ggplot2)")
    
    state = {
        "legacy_course_path": str(course_dir),
        "file_formats": ["R"],
        "errors": []
    }
    
    result = agent.execute(state)
    
    assert "ingestion_output" in result
    assert "parsed_content" in result["ingestion_output"]
    assert "extracted_concepts" in result["ingestion_output"]
    assert len(result["errors"]) == 0

def test_execute_handles_error(mock_llm, sample_principles):
    """Test error handling"""
    agent = IngestionAgent(mock_llm, sample_principles)
    
    state = {
        "legacy_course_path": "/nonexistent/path",
        "file_formats": ["R"],
        "errors": []
    }
    
    result = agent.execute(state)
    
    assert len(result["errors"]) > 0
    assert "IngestionAgent" in result["errors"][0]["agent"]
```

### Orchestrator Tests

Test workflow routing and state transitions.

```python
# tests/unit/orchestrator/test_routes.py
import pytest
from coursetransformer.orchestrator.routes import (
    route_plan_review,
    route_qa_results,
    route_content_review
)

def test_route_plan_review_approved():
    """Test plan review routing when approved"""
    state = {
        "human_reviews": [
            {"stage": "planning", "decision": "approved"}
        ]
    }
    
    result = route_plan_review(state)
    assert result == "approved"

def test_route_plan_review_rejected():
    """Test plan review routing when rejected"""
    state = {
        "human_reviews": [
            {"stage": "planning", "decision": "rejected"}
        ]
    }
    
    result = route_plan_review(state)
    assert result == "rejected"

def test_route_qa_critical_issues():
    """Test QA routing with critical issues"""
    state = {
        "qa_output": {
            "overall_score": 60,
            "summary": {"critical_issues": 3},
            "checks": {
                "code_execution": {"score": 30}  # Very low
            }
        }
    }
    
    result = route_qa_results(state)
    assert result == "remodernize"  # Code issues → remodernize

def test_route_qa_passed():
    """Test QA routing when passed"""
    state = {
        "qa_output": {
            "overall_score": 90,
            "summary": {"critical_issues": 0}
        }
    }
    
    result = route_qa_results(state)
    assert result == "passed"
```

### Knowledge Base Tests

```python
# tests/unit/knowledge/test_rag.py
import pytest
from coursetransformer.knowledge import KnowledgeBase

@pytest.fixture
def kb():
    """In-memory knowledge base for testing"""
    return KnowledgeBase(persist_directory=":memory:")

def test_add_documents(kb):
    """Test adding documents"""
    docs = ["Test document 1", "Test document 2"]
    metadata = [{"source": "test"}, {"source": "test"}]
    
    kb.add_documents(docs, metadata)
    
    # Verify documents were added
    results = kb.query("Test", n_results=2)
    assert len(results) == 2

def test_query(kb):
    """Test querying"""
    kb.add_documents(
        ["Python is a programming language"],
        [{"topic": "python"}]
    )
    
    results = kb.query("programming language", n_results=1)
    
    assert len(results) > 0
    assert "Python" in results[0]["document"]

def test_fact_check(kb, mocker):
    """Test fact-checking"""
    kb.add_documents(
        ["Transformers were introduced in 2017"],
        [{"topic": "transformers"}]
    )
    
    # Mock LLM response
    mock_llm = mocker.patch("coursetransformer.knowledge.rag.ollama_client")
    mock_llm.generate.return_value = "The claim is accurate."
    
    result = kb.fact_check("Transformers were introduced in 2017")
    
    assert "verification" in result
    assert len(result["sources"]) > 0
```

## Integration Tests

Test interaction between components.

```python
# tests/integration/test_agent_chaining.py
import pytest
from coursetransformer.agents import AgentFactory

@pytest.fixture
def mock_llm(mocker):
    """Mock LLM with reasonable responses"""
    llm = mocker.Mock()
    llm.generate.side_effect = lambda prompt, agent_type: '{"result": "success"}'
    return llm

def test_ingestion_to_analysis_flow(mock_llm, tmp_path):
    """Test data flow from Ingestion to Analysis"""
    principles = {"target_year": 2026}
    
    # Create test course
    course_dir = tmp_path / "course"
    course_dir.mkdir()
    (course_dir / "test.R").write_text("library(ggplot2)")
    
    # Ingestion
    ingestion_agent = AgentFactory.create_agent("ingestion", mock_llm, principles)
    state = {
        "legacy_course_path": str(course_dir),
        "file_formats": ["R"],
        "errors": []
    }
    state = ingestion_agent.execute(state)
    
    # Analysis
    analysis_agent = AgentFactory.create_agent("analysis", mock_llm, principles)
    state = analysis_agent.execute(state)
    
    assert "ingestion_output" in state
    assert "analysis_output" in state
    assert "concept_analysis" in state["analysis_output"]

def test_llm_integration(mocker):
    """Test actual OLLAMA integration (requires OLLAMA running)"""
    # This test is skipped in CI but can run locally
    pytest.skip("Requires OLLAMA running locally")
    
    from coursetransformer.llm import OLLAMAClient
    
    client = OLLAMAClient()
    response = client.generate("Say 'test successful'", "analysis")
    
    assert "test successful" in response.lower()
```

## End-to-End Tests

Test complete workflows with mocked human interactions.

```python
# tests/e2e/test_full_transformation.py
import pytest
import asyncio
from coursetransformer.orchestrator import workflow

@pytest.fixture
def sample_course(tmp_path):
    """Create sample legacy course"""
    course_dir = tmp_path / "sample_course"
    course_dir.mkdir()
    
    # Add some R files
    (course_dir / "lesson1.R").write_text("""
    library(ggplot2)
    data <- read.csv("data.csv")
    ggplot(data, aes(x=x, y=y)) + geom_point()
    """)
    
    return course_dir

@pytest.fixture
def mock_human_reviews():
    """Mock human review responses"""
    return {
        "planning": {"decision": "approved", "feedback": ""},
        "content": {"decision": "approved", "feedback": ""}
    }

@pytest.mark.asyncio
async def test_full_transformation_workflow(sample_course, mock_human_reviews, mocker):
    """Test complete transformation from start to finish"""
    # Mock LLM
    mock_llm = mocker.patch("coursetransformer.agents.base.llm_client")
    mock_llm.generate.return_value = '{"result": "success"}'
    
    # Mock human reviews
    mocker.patch(
        "coursetransformer.orchestrator.workflow.get_human_review",
        side_effect=lambda stage: mock_human_reviews[stage]
    )
    
    # Start transformation
    principles = {
        "target_year": 2026,
        "primary_language": "Python",
        "quality_thresholds": {
            "code": {"pass_rate": 0.9},
            "accuracy": 0.9
        }
    }
    
    result = await workflow.start_transformation(
        str(sample_course),
        principles
    )
    
    # Wait for completion
    transformation_id = result["transformation_id"]
    final_state = await workflow.wait_for_completion(transformation_id, timeout=300)
    
    # Verify workflow completed successfully
    assert final_state["status"] == "completed"
    assert "export_output" in final_state
    assert "coursesgtm_path" in final_state["export_output"]
    
    # Verify all stages executed
    assert final_state["ingestion_output"] is not None
    assert final_state["analysis_output"] is not None
    assert final_state["planning_output"] is not None
    assert final_state["modernization_output"] is not None
    assert final_state["generation_output"] is not None
    assert final_state["qa_output"] is not None
    assert final_state["export_output"] is not None
```

## Test Data

### Sample Legacy Course

```
tests/fixtures/sample_legacy_course/
├── 01_Introduction/
│   ├── index.md
│   └── intro.R
├── 02_DataManipulation/
│   ├── index.md
│   ├── dplyr_examples.R
│   └── slides.pdf
└── README.md
```

### Expected Outputs

```python
# tests/fixtures/expected_outputs.py
EXPECTED_INGESTION_OUTPUT = {
    "extracted_concepts": [
        {"concept": "data_frames", "mentions": 10},
        {"concept": "data_visualization", "mentions": 8}
    ],
    "code_inventory": {
        "R": {"files": 2, "libraries": ["dplyr", "ggplot2"]}
    }
}

EXPECTED_ANALYSIS_OUTPUT = {
    "overall_relevance": 70,
    "missing_topics": [
        {"topic": "docker", "priority": "critical"}
    ]
}
```

## Running Tests

### All Tests

```bash
pytest
```

### Unit Tests Only

```bash
pytest tests/unit/
```

### With Coverage

```bash
pytest --cov=coursetransformer --cov-report=html
```

### Specific Test

```bash
pytest tests/unit/agents/test_ingestion_agent.py::test_parse_r_file
```

### Fast Tests (Skip E2E)

```bash
pytest -m "not e2e"
```

## Coverage Targets

| Component | Target Coverage |
|-----------|----------------|
| Agents | >85% |
| Orchestrator | >90% |
| Knowledge Base | >80% |
| LLM Client | >75% |
| Utils | >85% |
| **Overall** | **>80%** |

## Continuous Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        pytest --cov=coursetransformer --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

This comprehensive testing strategy ensures CourseTransformer is robust, reliable, and maintainable.
