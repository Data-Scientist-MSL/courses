# CourseTransformer - Workflow Orchestration

This document specifies the LangGraph-based workflow orchestration for the CourseTransformer system.

## Overview

The CourseTransformer workflow is implemented using **LangGraph**, a framework for building stateful, multi-agent workflows. The workflow coordinates the execution of 7 core agents with human-in-the-loop checkpoints.

## State Schema

The workflow state is a typed dictionary that persists data across all agent transitions:

```python
from typing import TypedDict, Optional, List, Dict, Any
from datetime import datetime

class TransformationState(TypedDict):
    """Complete state for a course transformation workflow"""
    
    # Workflow metadata
    transformation_id: str
    status: str  # "initialized" | "in_progress" | "paused" | "completed" | "failed"
    current_stage: str
    created_at: str
    updated_at: str
    
    # Input configuration
    legacy_course_path: str
    guiding_principles: Dict[str, Any]
    export_config: Dict[str, Any]
    
    # Stage outputs
    ingestion_output: Optional[Dict[str, Any]]
    analysis_output: Optional[Dict[str, Any]]
    planning_output: Optional[Dict[str, Any]]
    modernization_output: Optional[Dict[str, Any]]
    generation_output: Optional[Dict[str, Any]]
    qa_output: Optional[Dict[str, Any]]
    export_output: Optional[Dict[str, Any]]
    
    # Human interactions
    human_reviews: List[Dict[str, Any]]
    awaiting_human_review: bool
    current_review_stage: Optional[str]
    
    # Error tracking
    errors: List[Dict[str, Any]]
    retry_count: int
    
    # Performance metrics
    stage_durations: Dict[str, float]
    llm_token_usage: Dict[str, int]
```

### State Initialization

```python
def initialize_state(
    legacy_course_path: str,
    guiding_principles: dict,
    export_config: dict = None
) -> TransformationState:
    """Initialize workflow state"""
    return {
        "transformation_id": str(uuid.uuid4()),
        "status": "initialized",
        "current_stage": "ingestion",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        
        "legacy_course_path": legacy_course_path,
        "guiding_principles": guiding_principles,
        "export_config": export_config or {},
        
        "ingestion_output": None,
        "analysis_output": None,
        "planning_output": None,
        "modernization_output": None,
        "generation_output": None,
        "qa_output": None,
        "export_output": None,
        
        "human_reviews": [],
        "awaiting_human_review": False,
        "current_review_stage": None,
        
        "errors": [],
        "retry_count": 0,
        
        "stage_durations": {},
        "llm_token_usage": {},
    }
```

## Workflow Graph

The workflow is defined as a directed graph with conditional edges:

```mermaid
graph TD
    START([Start]) --> INIT[Initialize State]
    INIT --> INGEST[Ingestion Agent]
    INGEST --> ANALYZE[Analysis Agent]
    ANALYZE --> PLAN[Planning Agent]
    PLAN --> REVIEW_PLAN{Human Review Plan}
    
    REVIEW_PLAN -->|Approved| MODERNIZE[Modernization Agent]
    REVIEW_PLAN -->|Needs Adjustment| PLAN
    REVIEW_PLAN -->|Rejected| ABORT([Abort])
    
    MODERNIZE --> GENERATE[Generation Agent]
    GENERATE --> QA[Quality Agent]
    
    QA --> QA_DECISION{Quality Check}
    QA_DECISION -->|Passed| REVIEW_CONTENT{Human Review Content}
    QA_DECISION -->|Minor Issues| REVIEW_CONTENT
    QA_DECISION -->|Critical Issues| GENERATE
    QA_DECISION -->|Code Failures| MODERNIZE
    
    REVIEW_CONTENT -->|Approved| EXPORT[Export Agent]
    REVIEW_CONTENT -->|Edit Required| GENERATE
    REVIEW_CONTENT -->|Regenerate| GENERATE
    REVIEW_CONTENT -->|Rejected| ABORT
    
    EXPORT --> COMPLETE([Complete])
    
    INGEST -->|Error| ERROR_HANDLER[Error Handler]
    ANALYZE -->|Error| ERROR_HANDLER
    PLAN -->|Error| ERROR_HANDLER
    MODERNIZE -->|Error| ERROR_HANDLER
    GENERATE -->|Error| ERROR_HANDLER
    QA -->|Error| ERROR_HANDLER
    EXPORT -->|Error| ERROR_HANDLER
    
    ERROR_HANDLER -->|Retry| INGEST
    ERROR_HANDLER -->|Fatal| ABORT
    
    style REVIEW_PLAN fill:#ffe1e1
    style REVIEW_CONTENT fill:#ffe1e1
    style QA_DECISION fill:#e1f5ff
    style ERROR_HANDLER fill:#fff4e1
```

## LangGraph Implementation

### Graph Definition

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# Initialize graph with state schema
workflow = StateGraph(TransformationState)

# Add agent nodes
workflow.add_node("ingestion", ingestion_agent.execute)
workflow.add_node("analysis", analysis_agent.execute)
workflow.add_node("planning", planning_agent.execute)
workflow.add_node("modernization", modernization_agent.execute)
workflow.add_node("generation", generation_agent.execute)
workflow.add_node("qa", qa_agent.execute)
workflow.add_node("export", export_agent.execute)

# Add human review nodes
workflow.add_node("review_plan", human_review_plan)
workflow.add_node("review_content", human_review_content)

# Add error handler
workflow.add_node("error_handler", handle_error)

# Set entry point
workflow.set_entry_point("ingestion")

# Add sequential edges
workflow.add_edge("ingestion", "analysis")
workflow.add_edge("analysis", "planning")
workflow.add_edge("planning", "review_plan")

# Add conditional edges
workflow.add_conditional_edges(
    "review_plan",
    route_plan_review,
    {
        "approved": "modernization",
        "needs_adjustment": "planning",
        "rejected": END
    }
)

workflow.add_edge("modernization", "generation")
workflow.add_edge("generation", "qa")

workflow.add_conditional_edges(
    "qa",
    route_qa_results,
    {
        "passed": "review_content",
        "minor_issues": "review_content",
        "regenerate": "generation",
        "remodernize": "modernization"
    }
)

workflow.add_conditional_edges(
    "review_content",
    route_content_review,
    {
        "approved": "export",
        "regenerate": "generation",
        "rejected": END
    }
)

workflow.add_edge("export", END)

# Error handling edges
for node in ["ingestion", "analysis", "planning", "modernization", "generation", "qa", "export"]:
    workflow.add_conditional_edges(
        node,
        check_for_errors,
        {
            "success": node,  # Continue to next node via existing edges
            "error": "error_handler"
        }
    )

# Compile with checkpointing
memory = SqliteSaver.from_conn_string(":memory:")
app = workflow.compile(checkpointer=memory)
```

## Conditional Edge Functions

### Plan Review Router

```python
def route_plan_review(state: TransformationState) -> str:
    """Route based on human plan review decision"""
    if not state["human_reviews"]:
        # No review yet, wait for human
        return "needs_review"
    
    latest_review = state["human_reviews"][-1]
    decision = latest_review["decision"]
    
    if decision == "approved":
        return "approved"
    elif decision == "needs_adjustment":
        return "needs_adjustment"
    else:  # rejected
        return "rejected"
```

### QA Results Router

```python
def route_qa_results(state: TransformationState) -> str:
    """Route based on QA check results"""
    qa_output = state["qa_output"]
    
    if not qa_output:
        return "error"
    
    overall_score = qa_output["overall_score"]
    critical_issues = qa_output["summary"]["critical_issues"]
    
    if critical_issues > 0:
        # Check if issues are in code execution vs generation
        code_execution_failed = qa_output["checks"]["code_execution"]["score"] < 50
        if code_execution_failed:
            return "remodernize"  # Modernization produced bad code
        else:
            return "regenerate"  # Generation issues
    elif overall_score >= 75:
        return "passed"
    else:
        return "minor_issues"  # Can proceed to human review with warnings
```

### Content Review Router

```python
def route_content_review(state: TransformationState) -> str:
    """Route based on human content review decision"""
    if not state["human_reviews"]:
        return "needs_review"
    
    latest_review = state["human_reviews"][-1]
    decision = latest_review["decision"]
    
    if decision == "approved":
        return "approved"
    elif decision in ["edit", "regenerate"]:
        return "regenerate"
    else:  # rejected
        return "rejected"
```

### Error Check

```python
def check_for_errors(state: TransformationState) -> str:
    """Check if current stage has errors"""
    if state["errors"] and state["errors"][-1]["stage"] == state["current_stage"]:
        return "error"
    return "success"
```

## Human Review Nodes

### Plan Review

```python
async def human_review_plan(state: TransformationState) -> TransformationState:
    """Pause workflow for human plan review"""
    state["awaiting_human_review"] = True
    state["current_review_stage"] = "planning"
    state["status"] = "awaiting_plan_review"
    
    # Persist state
    save_state(state)
    
    # Emit event for UI
    emit_event("plan_ready_for_review", {
        "transformation_id": state["transformation_id"],
        "plan": state["planning_output"]
    })
    
    # Block until human provides feedback
    # (In practice, workflow is paused and resumed when human submits review)
    return state
```

### Content Review

```python
async def human_review_content(state: TransformationState) -> TransformationState:
    """Pause workflow for human content review"""
    state["awaiting_human_review"] = True
    state["current_review_stage"] = "content"
    state["status"] = "awaiting_content_review"
    
    save_state(state)
    
    emit_event("content_ready_for_review", {
        "transformation_id": state["transformation_id"],
        "content": state["generation_output"],
        "quality_report": state["qa_output"]
    })
    
    return state
```

## Parallel Processing

### Parallel Content Generation

The Generation Agent can parallelize independent tasks:

```python
async def generation_agent_execute(state: TransformationState) -> TransformationState:
    """Execute generation with parallel tasks"""
    concepts = state["modernization_output"]["concepts"]
    
    # Spawn parallel generation tasks
    tasks = [
        generate_slides_async(concepts),
        generate_labs_async(concepts),
        generate_quizzes_async(concepts),
        generate_diagrams_async(concepts)
    ]
    
    # Wait for all to complete
    results = await asyncio.gather(*tasks)
    
    state["generation_output"] = {
        "slides": results[0],
        "labs": results[1],
        "quizzes": results[2],
        "diagrams": results[3]
    }
    
    return state
```

### Parallel Course Processing

Multiple courses can be transformed in parallel:

```python
async def transform_multiple_courses(course_paths: List[str]) -> List[str]:
    """Transform multiple courses in parallel"""
    tasks = [
        transform_single_course(path)
        for path in course_paths
    ]
    
    results = await asyncio.gather(*tasks)
    return results
```

## State Persistence

### Checkpoint System

LangGraph automatically checkpoints state after each node execution:

```python
# State is saved after each agent completes
# Can resume from any checkpoint

# Resume from checkpoint
config = {"configurable": {"thread_id": transformation_id}}
result = await app.ainvoke(state, config=config)
```

### Manual Pause/Resume

```python
def pause_transformation(transformation_id: str):
    """Pause a running transformation"""
    state = load_state(transformation_id)
    state["status"] = "paused"
    save_state(state)

def resume_transformation(transformation_id: str):
    """Resume a paused transformation"""
    state = load_state(transformation_id)
    state["status"] = "in_progress"
    config = {"configurable": {"thread_id": transformation_id}}
    
    # Resume from last checkpoint
    result = app.invoke(state, config=config)
    return result
```

## Error Handling

### Retry Logic

```python
def handle_error(state: TransformationState) -> TransformationState:
    """Handle agent failures with retry logic"""
    current_error = state["errors"][-1]
    stage = current_error["stage"]
    
    # Check retry count
    if state["retry_count"] >= 3:
        # Max retries exceeded
        state["status"] = "failed"
        state["current_stage"] = "error"
        
        # Escalate to human
        emit_event("escalation_required", {
            "transformation_id": state["transformation_id"],
            "error": current_error,
            "retry_count": state["retry_count"]
        })
        
        return state
    
    # Increment retry counter
    state["retry_count"] += 1
    
    # Retry with exponential backoff
    sleep_time = 2 ** state["retry_count"]
    time.sleep(sleep_time)
    
    # Reset to failed stage
    state["current_stage"] = stage
    state["status"] = "retrying"
    
    return state
```

### Error Categories

```python
class ErrorSeverity(Enum):
    RECOVERABLE = "recoverable"  # Retry automatically
    ESCALATION = "escalation"    # Notify human, await decision
    FATAL = "fatal"              # Abort transformation

def categorize_error(error: Exception) -> ErrorSeverity:
    """Categorize error severity"""
    if isinstance(error, (TimeoutError, ConnectionError)):
        return ErrorSeverity.RECOVERABLE
    elif isinstance(error, (ValidationError, SchemaError)):
        return ErrorSeverity.ESCALATION
    else:
        return ErrorSeverity.FATAL
```

## Workflow Execution

### Start Transformation

```python
async def start_transformation(
    legacy_course_path: str,
    guiding_principles: dict
) -> str:
    """Start a new transformation workflow"""
    
    # Initialize state
    state = initialize_state(legacy_course_path, guiding_principles)
    transformation_id = state["transformation_id"]
    
    # Save initial state
    save_state(state)
    
    # Start workflow (async)
    config = {"configurable": {"thread_id": transformation_id}}
    asyncio.create_task(app.ainvoke(state, config=config))
    
    return transformation_id
```

### Monitor Progress

```python
def get_transformation_status(transformation_id: str) -> dict:
    """Get current status of transformation"""
    state = load_state(transformation_id)
    
    return {
        "transformation_id": transformation_id,
        "status": state["status"],
        "current_stage": state["current_stage"],
        "progress_percentage": calculate_progress(state),
        "awaiting_human_review": state["awaiting_human_review"],
        "errors": state["errors"],
        "estimated_completion": estimate_completion(state)
    }
```

### Submit Human Review

```python
def submit_human_review(
    transformation_id: str,
    decision: str,  # "approved", "needs_adjustment", "rejected"
    feedback: str = ""
) -> dict:
    """Submit human review and resume workflow"""
    
    state = load_state(transformation_id)
    
    # Record review
    review = {
        "stage": state["current_review_stage"],
        "timestamp": datetime.utcnow().isoformat(),
        "decision": decision,
        "feedback": feedback
    }
    state["human_reviews"].append(review)
    
    # Clear review flag
    state["awaiting_human_review"] = False
    state["current_review_stage"] = None
    state["status"] = "in_progress"
    
    # Save state
    save_state(state)
    
    # Resume workflow
    config = {"configurable": {"thread_id": transformation_id}}
    result = app.invoke(state, config=config)
    
    return result
```

## Streaming Updates

### Real-Time Events

```python
async def stream_transformation_events(transformation_id: str):
    """Stream real-time events from transformation"""
    config = {"configurable": {"thread_id": transformation_id}}
    
    async for event in app.astream_events(config=config):
        yield {
            "type": event["type"],
            "timestamp": datetime.utcnow().isoformat(),
            "data": event["data"]
        }
```

### Event Types

- `agent_started`: Agent begins execution
- `agent_completed`: Agent finishes successfully
- `agent_failed`: Agent encounters error
- `human_review_required`: Workflow paused for review
- `quality_check_completed`: QA results available
- `transformation_completed`: Full workflow done
- `transformation_failed`: Workflow aborted

## Workflow Visualization

### Current State Diagram

```python
def visualize_workflow_state(transformation_id: str) -> str:
    """Generate Mermaid diagram of current workflow state"""
    state = load_state(transformation_id)
    
    # Generate diagram showing:
    # - Completed stages (green)
    # - Current stage (blue)
    # - Pending stages (gray)
    # - Failed stages (red)
    
    return mermaid_diagram
```

## Performance Optimization

### Caching

```python
# Cache LLM responses
@cache_llm_response(ttl=3600)
def call_llm(prompt: str, model: str) -> str:
    return llm_client.generate(prompt, model)

# Cache knowledge base queries
@cache_rag_query(ttl=1800)
def query_knowledge_base(query: str) -> List[str]:
    return rag_system.query(query)
```

### Resource Management

```python
# Limit concurrent LLM calls
semaphore = asyncio.Semaphore(5)

async def call_llm_with_limit(prompt: str) -> str:
    async with semaphore:
        return await llm_client.generate_async(prompt)
```

## Testing the Workflow

### Unit Tests

```python
def test_route_plan_review_approved():
    state = create_mock_state()
    state["human_reviews"] = [{"decision": "approved"}]
    
    result = route_plan_review(state)
    assert result == "approved"

def test_route_qa_results_critical_issues():
    state = create_mock_state()
    state["qa_output"] = {
        "overall_score": 60,
        "summary": {"critical_issues": 2}
    }
    
    result = route_qa_results(state)
    assert result in ["regenerate", "remodernize"]
```

### Integration Tests

```python
async def test_full_workflow():
    """Test complete workflow with mocked human reviews"""
    
    # Mock human review responses
    mock_reviews = {
        "planning": {"decision": "approved"},
        "content": {"decision": "approved"}
    }
    
    # Start transformation
    transformation_id = await start_transformation(
        "/test/legacy_course",
        {"target_year": 2026}
    )
    
    # Simulate workflow with auto-approvals
    result = await run_workflow_with_mocked_reviews(
        transformation_id,
        mock_reviews
    )
    
    assert result["status"] == "completed"
    assert result["export_output"] is not None
```

## Configuration

### Workflow Configuration

```yaml
# workflow_config.yaml
workflow:
  max_retries: 3
  timeout_seconds: 3600
  checkpoint_interval: 60
  
  parallel_processing:
    enabled: true
    max_concurrent_tasks: 5
  
  human_review:
    timeout_hours: 24  # Auto-escalate if no review after 24h
    notification_channels: ["email", "slack"]
  
  error_handling:
    retry_backoff_multiplier: 2
    escalation_threshold: 3
```

## Deployment

### Production Setup

```python
# Use persistent checkpointing
from langgraph.checkpoint.postgres import PostgresSaver

# Production database
memory = PostgresSaver.from_conn_string(
    "postgresql://user:pass@host:5432/coursetransformer"
)

app = workflow.compile(checkpointer=memory)
```

### Monitoring

```python
# Add observability
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("transformation_workflow")
async def start_transformation_with_tracing(...):
    # Workflow execution with tracing
    pass
```

---

This workflow orchestration specification provides a complete foundation for implementing the CourseTransformer multi-agent system with LangGraph.
