# SimulationPlayer Testing Strategy

This document defines the comprehensive testing approach for SimulationPlayer, ensuring reliability, correctness, and quality.

---

## Testing Pyramid

```
         ╱╲
        ╱  ╲       E2E Tests (10%)
       ╱────╲      - Complete scenario walkthroughs
      ╱      ╲     - Real user flows
     ╱────────╲    
    ╱          ╲   Integration Tests (30%)
   ╱────────────╲  - Agent + OLLAMA
  ╱              ╲ - Environment + Docker
 ╱────────────────╲
╱                  ╲ Unit Tests (60%)
────────────────────  - Core logic
                      - Validators
                      - Utilities
```

---

## Unit Tests

### Scope
Test individual functions and classes in isolation.

### Coverage Target
**90%** code coverage for core modules.

### Test Structure

#### Core Engine Tests
```python
# tests/unit/test_core/test_engine.py

import pytest
from simulationplayer.core import SimulationEngine
from simulationplayer.scenarios import Scenario

class TestSimulationEngine:
    @pytest.fixture
    def engine(self):
        return SimulationEngine()
    
    @pytest.fixture
    def sample_scenario(self):
        return Scenario(
            id='test-scenario',
            title='Test Scenario',
            steps=[...]
        )
    
    def test_load_scenario(self, engine, sample_scenario):
        """Test scenario loading"""
        loaded = engine.load_scenario(sample_scenario.id)
        
        assert loaded is not None
        assert loaded.id == sample_scenario.id
        assert len(loaded.steps) > 0
    
    def test_initialize_environment(self, engine, sample_scenario):
        """Test environment initialization"""
        env = engine.initialize_environment(sample_scenario.environment.type)
        
        assert env is not None
        assert env.type == sample_scenario.environment.type
    
    def test_execute_valid_action(self, engine):
        """Test executing a valid action"""
        action = Action(command='docker pull nginx')
        result = engine.execute_step('step_1', action)
        
        assert result.is_valid
        assert result.message is not None
    
    def test_execute_invalid_action(self, engine):
        """Test executing an invalid action"""
        action = Action(command='invalid command')
        result = engine.execute_step('step_1', action)
        
        assert not result.is_valid
        assert len(result.errors) > 0
```

#### Validator Tests
```python
# tests/unit/test_core/test_validator.py

import pytest
from simulationplayer.core import Validator
from simulationplayer.scenarios import ValidationRule

class TestValidator:
    @pytest.fixture
    def validator(self):
        return Validator()
    
    def test_command_exact_match(self, validator):
        """Test exact command matching"""
        rule = ValidationRule(
            type='command_exact',
            parameters={'expected': 'docker pull nginx'}
        )
        
        action = Action(command='docker pull nginx')
        result = validator.validate_action(action, [rule])
        
        assert result.is_valid
    
    def test_command_regex_match(self, validator):
        """Test regex command matching"""
        rule = ValidationRule(
            type='command_regex',
            parameters={'pattern': r'^docker (pull|image pull) nginx(:.*)?$'}
        )
        
        # Test variations
        for cmd in ['docker pull nginx', 'docker pull nginx:latest', 'docker image pull nginx']:
            action = Action(command=cmd)
            result = validator.validate_action(action, [rule])
            assert result.is_valid, f"Failed for: {cmd}"
    
    def test_output_validation(self, validator):
        """Test output content validation"""
        rule = ValidationRule(
            type='output_contains',
            parameters={'text': 'Status: Downloaded', 'location': 'stdout'}
        )
        
        action = Action(
            command='docker pull nginx',
            result=ActionResult(stdout='Status: Downloaded newer image')
        )
        
        result = validator.validate_action(action, [rule])
        assert result.is_valid
    
    def test_multi_rule_validation(self, validator):
        """Test multiple validation rules"""
        rules = [
            ValidationRule(type='command_contains', parameters={'substring': 'docker'}),
            ValidationRule(type='exit_code', parameters={'expected': 0})
        ]
        
        action = Action(
            command='docker pull nginx',
            result=ActionResult(exit_code=0)
        )
        
        result = validator.validate_action(action, rules)
        assert result.is_valid
        assert len(result.passed_rules) == 2
```

#### Environment Tests
```python
# tests/unit/test_environments/test_terminal.py

import pytest
from simulationplayer.environments import TerminalSimulator

class TestTerminalSimulator:
    @pytest.fixture
    def terminal(self):
        sim = TerminalSimulator()
        sim.initialize({})
        yield sim
        sim.cleanup()
    
    def test_initialize(self, terminal):
        """Test terminal initialization"""
        assert terminal.container is not None
        assert terminal.is_ready()
    
    def test_execute_command(self, terminal):
        """Test command execution"""
        result = terminal.execute_action(Action(command='echo "Hello"'))
        
        assert result.exit_code == 0
        assert 'Hello' in result.stdout
    
    def test_command_history(self, terminal):
        """Test command history tracking"""
        terminal.execute_action(Action(command='ls'))
        terminal.execute_action(Action(command='pwd'))
        
        history = terminal.get_command_history()
        assert len(history) == 2
        assert history[0].command == 'ls'
    
    def test_cleanup(self, terminal):
        """Test resource cleanup"""
        container_id = terminal.container.id
        terminal.cleanup()
        
        # Container should be removed
        assert not terminal.is_container_running(container_id)
```

#### Agent Tests
```python
# tests/unit/test_agents/test_step_guide.py

import pytest
from simulationplayer.agents import StepGuideAgent
from unittest.mock import Mock, patch

class TestStepGuideAgent:
    @pytest.fixture
    def agent(self):
        return StepGuideAgent()
    
    @patch('simulationplayer.agents.base.OllamaClient')
    def test_generate_guidance(self, mock_ollama, agent):
        """Test guidance generation"""
        mock_ollama.return_value.generate.return_value = {
            'response': 'Use docker pull to download images.'
        }
        
        context = {
            'step_definition': {'title': 'Pull Image', 'objective': 'Download nginx'},
            'user_context': {'tier': 'intermediate', 'attempts': 0}
        }
        
        response = agent.generate_response(context)
        
        assert response.guidance_text is not None
        assert 'docker pull' in response.guidance_text.lower()
    
    def test_guidance_adaptation(self, agent):
        """Test guidance adapts to user tier"""
        # Beginner gets more detail
        beginner_context = {'user_context': {'tier': 'basic'}}
        beginner_guidance = agent.generate_response(beginner_context)
        
        # Advanced gets concise
        advanced_context = {'user_context': {'tier': 'advanced'}}
        advanced_guidance = agent.generate_response(advanced_context)
        
        assert len(beginner_guidance.guidance_text) > len(advanced_guidance.guidance_text)
```

---

## Integration Tests

### Scope
Test interactions between components and external services.

### Coverage Target
**80%** coverage of integration points.

### Test Structure

#### Docker Integration Tests
```python
# tests/integration/test_docker_integration.py

import pytest
import docker
from simulationplayer.integrations import DockerClient

class TestDockerIntegration:
    @pytest.fixture
    def docker_client(self):
        return DockerClient()
    
    @pytest.fixture(autouse=True)
    def cleanup_containers(self, docker_client):
        """Cleanup test containers after each test"""
        yield
        docker_client.cleanup_all_test_containers()
    
    def test_create_container(self, docker_client):
        """Test container creation"""
        container = docker_client.create_simulation_container(
            scenario_id='test',
            user_id='test_user'
        )
        
        assert container is not None
        assert container.status == 'running'
    
    def test_execute_command_in_container(self, docker_client):
        """Test command execution in container"""
        container = docker_client.create_simulation_container('test', 'user')
        
        result = docker_client.execute_command(container, 'echo "test"')
        
        assert result['exit_code'] == 0
        assert 'test' in result['stdout']
    
    def test_container_resource_limits(self, docker_client):
        """Test container resource limits are enforced"""
        container = docker_client.create_simulation_container('test', 'user')
        
        # Check memory limit
        inspect = container.attrs
        assert inspect['HostConfig']['Memory'] == 512 * 1024 * 1024  # 512MB
```

#### OLLAMA Integration Tests
```python
# tests/integration/test_ollama_integration.py

import pytest
from simulationplayer.integrations import OllamaClient

@pytest.mark.integration
@pytest.mark.ollama
class TestOllamaIntegration:
    @pytest.fixture
    def ollama_client(self):
        return OllamaClient()
    
    def test_list_models(self, ollama_client):
        """Test listing available models"""
        models = ollama_client.list_models()
        
        assert len(models) > 0
        assert any('llama' in m['name'] for m in models)
    
    def test_generate_response(self, ollama_client):
        """Test text generation"""
        response = ollama_client.generate(
            model='llama3.2:3b',
            prompt='What is Docker?',
            system='You are a helpful assistant.'
        )
        
        assert response['response'] is not None
        assert len(response['response']) > 0
    
    def test_caching(self, ollama_client):
        """Test response caching"""
        prompt = 'Explain containers'
        
        # First call
        start = time.time()
        response1 = ollama_client.generate('llama3.2:3b', prompt)
        time1 = time.time() - start
        
        # Second call (should be cached)
        start = time.time()
        response2 = ollama_client.generate('llama3.2:3b', prompt)
        time2 = time.time() - start
        
        assert response1 == response2
        assert time2 < time1 / 2  # Cache should be much faster
```

#### Scenario Execution Tests
```python
# tests/integration/test_scenario_execution.py

import pytest
from simulationplayer import SimulationEngine

class TestScenarioExecution:
    @pytest.fixture
    def engine(self):
        return SimulationEngine()
    
    def test_execute_simple_scenario(self, engine):
        """Test executing a simple scenario end-to-end"""
        scenario = engine.load_scenario('test-simple-scenario')
        
        # Step 1
        result = engine.execute_step('step_1', Action(command='docker pull nginx'))
        assert result.is_valid
        
        # Step 2
        result = engine.execute_step('step_2', Action(command='docker run -d nginx'))
        assert result.is_valid
        
        # Check scenario completion
        assert engine.is_scenario_complete()
    
    def test_checkpoint_save_restore(self, engine):
        """Test checkpoint functionality"""
        scenario = engine.load_scenario('test-scenario')
        
        # Execute first step
        engine.execute_step('step_1', Action(command='docker pull nginx'))
        
        # Save checkpoint
        checkpoint = engine.save_checkpoint()
        
        # Create new engine and restore
        new_engine = SimulationEngine()
        new_engine.restore_checkpoint(checkpoint)
        
        # Should be at same point
        assert new_engine.current_step == engine.current_step
```

---

## End-to-End Tests

### Scope
Test complete user flows from start to finish.

### Coverage Target
**Key scenarios** have E2E test coverage.

### Test Structure

#### Docker Scenario E2E
```python
# tests/e2e/test_docker_scenario.py

import pytest
from simulationplayer import SimulationEngine

@pytest.mark.e2e
class TestDockerScenarioE2E:
    @pytest.fixture
    def engine(self):
        engine = SimulationEngine()
        yield engine
        engine.cleanup()
    
    def test_complete_docker_scenario(self, engine):
        """Test completing entire Docker scenario"""
        scenario = engine.load_scenario('docker-first-container')
        
        # Step 1: Pull image
        result = engine.execute_step('pull_nginx', Action(command='docker pull nginx'))
        assert result.is_valid
        assert 'success' in result.message.lower()
        
        # Step 2: Run container
        result = engine.execute_step('run_nginx', Action(command='docker run -d -p 8080:80 nginx'))
        assert result.is_valid
        
        # Step 3: Inspect
        result = engine.execute_step('inspect', Action(command='docker ps'))
        assert result.is_valid
        assert 'nginx' in result.output
        
        # Step 4: Exec
        result = engine.execute_step('exec', Action(command='docker exec $(docker ps -q) nginx -v'))
        assert result.is_valid
        
        # Step 5: Cleanup
        result = engine.execute_step('cleanup', Action(command='docker rm -f $(docker ps -q)'))
        assert result.is_valid
        
        # Check completion
        assert engine.is_scenario_complete()
        completion_data = engine.get_completion_data()
        assert completion_data['badge'] == 'Docker Novice'
        assert completion_data['points'] == 150
    
    def test_scenario_with_mistakes(self, engine):
        """Test scenario with common mistakes and recovery"""
        scenario = engine.load_scenario('docker-first-container')
        
        # Mistake: Missing -d flag
        result = engine.execute_step('run_nginx', Action(command='docker run nginx'))
        assert not result.is_valid
        assert 'detached' in result.error_message.lower()
        assert result.suggestion is not None
        
        # Correct attempt
        result = engine.execute_step('run_nginx', Action(command='docker run -d nginx'))
        assert result.is_valid
```

#### SQL Scenario E2E
```python
# tests/e2e/test_sql_scenario.py

@pytest.mark.e2e
class TestSQLScenarioE2E:
    def test_sql_joins_scenario(self):
        """Test SQL joins scenario"""
        engine = SimulationEngine()
        scenario = engine.load_scenario('sql-joins')
        
        # Step 1: Basic join
        query = "SELECT customers.name, orders.total FROM customers INNER JOIN orders ON customers.id = orders.customer_id"
        result = engine.execute_step('basic_join', Action(query=query))
        assert result.is_valid
        
        # Step 2: Join with filter
        query += " WHERE orders.total > 100"
        result = engine.execute_step('join_filter', Action(query=query))
        assert result.is_valid
        
        # Verify results
        assert all(row['total'] > 100 for row in result.data)
```

---

## Test Scenarios

### Sample Test Scenarios
Located in `tests/fixtures/sample_scenarios.yml`:

```yaml
# Minimal test scenario
test_simple:
  id: "test-simple"
  title: "Simple Test"
  difficulty: beginner
  estimated_time: 5
  
  environment:
    type: terminal
    docker_required: true
  
  steps:
    - id: "step_1"
      title: "Echo test"
      objective: "Run echo command"
      
      validation:
        rules:
          - rule_type: command_contains
            parameters:
              substring: "echo"
      
      success_message: "Success!"
```

---

## Performance Tests

### Load Testing
```python
# tests/performance/test_load.py

import pytest
from concurrent.futures import ThreadPoolExecutor
from simulationplayer import SimulationEngine

@pytest.mark.performance
class TestPerformance:
    def test_concurrent_scenarios(self):
        """Test handling multiple concurrent scenarios"""
        def run_scenario(user_id):
            engine = SimulationEngine()
            scenario = engine.load_scenario('test-simple')
            return engine.execute_all_steps(scenario)
        
        # Run 50 concurrent scenarios
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(run_scenario, i) for i in range(50)]
            results = [f.result() for f in futures]
        
        assert all(r.success for r in results)
    
    def test_ollama_response_time(self):
        """Test OLLAMA response times"""
        agent = StepGuideAgent()
        
        times = []
        for _ in range(10):
            start = time.time()
            agent.generate_response({...})
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        assert avg_time < 2.0  # Should respond in <2 seconds
```

---

## Test Utilities

### Fixtures
```python
# tests/conftest.py

import pytest
import docker
from simulationplayer import SimulationEngine

@pytest.fixture(scope='session')
def docker_client():
    """Shared Docker client"""
    return docker.from_env()

@pytest.fixture
def clean_docker_environment(docker_client):
    """Clean up Docker containers before/after tests"""
    # Cleanup before
    for container in docker_client.containers.list(filters={'label': 'test=true'}):
        container.remove(force=True)
    
    yield
    
    # Cleanup after
    for container in docker_client.containers.list(filters={'label': 'test=true'}):
        container.remove(force=True)

@pytest.fixture
def mock_ollama():
    """Mock OLLAMA responses"""
    with patch('simulationplayer.integrations.OllamaClient') as mock:
        mock.return_value.generate.return_value = {
            'response': 'Mocked AI response'
        }
        yield mock
```

### Test Helpers
```python
# tests/utils/helpers.py

def assert_validation_passes(result):
    """Assert validation result is successful"""
    assert result.is_valid, f"Validation failed: {result.errors}"

def assert_scenario_complete(engine):
    """Assert scenario is completed"""
    assert engine.is_scenario_complete()
    assert engine.get_current_state() == State.SCENARIO_COMPLETE

def create_test_action(command, exit_code=0, stdout='', stderr=''):
    """Create test action with result"""
    return Action(
        command=command,
        result=ActionResult(
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr
        )
    )
```

---

## Continuous Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/test.yml

name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements/test.txt
      
      - name: Run unit tests
        run: |
          pytest tests/unit -v --cov=simulationplayer --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  integration-tests:
    runs-on: ubuntu-latest
    
    services:
      docker:
        image: docker:dind
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
      
      - name: Install OLLAMA
        run: |
          curl -L https://ollama.ai/install.sh | sh
          ollama pull llama3.2:3b
      
      - name: Run integration tests
        run: |
          pytest tests/integration -v -m integration
  
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run E2E tests
        run: |
          pytest tests/e2e -v -m e2e
```

---

## Test Commands

```bash
# Run all tests
pytest

# Run specific test type
pytest tests/unit
pytest tests/integration
pytest tests/e2e

# Run with coverage
pytest --cov=simulationplayer --cov-report=html

# Run specific test
pytest tests/unit/test_core/test_engine.py::TestSimulationEngine::test_load_scenario

# Run with markers
pytest -m "not slow"
pytest -m integration

# Parallel execution
pytest -n auto  # Use all CPUs

# Verbose output
pytest -v -s
```

---

## Coverage Goals

- **Overall**: 85%
- **Core modules**: 90%
- **Environments**: 80%
- **Agents**: 75%
- **UI**: 60% (harder to test)

---

## Testing Best Practices

1. **Arrange-Act-Assert**: Clear test structure
2. **One assertion per test**: Focused tests
3. **Descriptive names**: `test_command_exact_match_validates_correctly`
4. **Fixtures for setup**: Reusable test data
5. **Mock external services**: Fast, reliable tests
6. **Test edge cases**: Empty inputs, null values, errors
7. **Integration tests for critical paths**: Real service interactions
8. **E2E tests for key scenarios**: Full user workflows

---

This comprehensive testing strategy ensures SimulationPlayer is reliable, correct, and maintainable.
