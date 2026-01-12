# CoursePlayerApp - Testing Strategy

## Overview

Comprehensive testing ensures CoursePlayerApp delivers a reliable, secure, and high-quality learning experience. This document defines the testing strategy, including unit tests, integration tests, UI tests, accessibility tests, and performance tests.

---

## Testing Pyramid

```
        /\
       /  \      E2E Tests (5%)
      /____\     - User journeys
     /      \    - Critical flows
    /  UI    \   
   /__________\  Integration Tests (20%)
  /            \ - API integrations
 /    Unit      \- Feature gating
/______________\ Unit Tests (75%)
                 - Core logic
                 - Utilities
```

**Strategy**: Heavy emphasis on unit tests for fast feedback, selective integration and E2E tests for critical paths.

---

## Test Environment Setup

### Test Stack

**Framework**: `pytest`
**Coverage**: `pytest-cov`
**Mocking**: `unittest.mock`
**API Mocking**: `responses`
**UI Testing**: `playwright`
**Load Testing**: `locust`

### Installation

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock responses playwright locust

# Install Playwright browsers
playwright install
```

### Project Structure

```
CoursePlayerApp/
├── tests/
│   ├── unit/
│   │   ├── test_feature_flags.py
│   │   ├── test_auth.py
│   │   ├── test_progress_tracker.py
│   │   └── test_ai_tutor.py
│   ├── integration/
│   │   ├── test_coursesgtm_integration.py
│   │   ├── test_simulationplayer_integration.py
│   │   └── test_ollama_integration.py
│   ├── ui/
│   │   ├── test_login_flow.py
│   │   ├── test_course_player.py
│   │   └── test_navigation.py
│   ├── accessibility/
│   │   ├── test_wcag_compliance.py
│   │   └── test_screen_reader.py
│   ├── performance/
│   │   ├── test_load.py
│   │   └── test_response_times.py
│   ├── conftest.py
│   └── fixtures/
│       ├── mock_data.py
│       └── mock_api_responses.py
└── pytest.ini
```

### Configuration

**pytest.ini**:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=utils
    --cov=components
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    ui: UI tests
    slow: Slow-running tests
    accessibility: Accessibility tests
```

---

## Unit Tests (75%)

### Test Coverage Goals
- **Core logic**: 90%+
- **Utilities**: 85%+
- **Components**: 70%+

### 1. Feature Gating Tests

**File**: `tests/unit/test_feature_flags.py`

```python
import pytest
from utils.feature_flags import FeatureFlags

def test_basic_tier_video_download():
    """Basic tier should not have video download enabled"""
    flags = FeatureFlags.get_flags("basic")
    assert flags["video_download"] == False
    assert flags["video_quality"] == "480p"


def test_intermediate_tier_ai_tutor():
    """Intermediate tier should have AI Tutor with 50 question quota"""
    flags = FeatureFlags.get_flags("intermediate")
    assert flags["ai_tutor_enabled"] == True
    assert flags["ai_tutor_quota"] == 50


def test_advanced_tier_unlimited_ai():
    """Advanced tier should have unlimited AI Tutor"""
    flags = FeatureFlags.get_flags("advanced")
    assert flags["ai_tutor_quota"] == -1  # unlimited


def test_course_access_basic():
    """Basic tier should have access to 5 courses"""
    courses = FeatureFlags.get_course_access("basic")
    assert len(courses) == 5
    assert "ai-01" in courses
    assert "ai-04" not in courses  # Advanced course not accessible


def test_course_access_advanced():
    """Advanced tier should have access to all courses"""
    courses = FeatureFlags.get_course_access("advanced")
    assert len(courses) == 9
    assert "ai-04" in courses


def test_invalid_tier():
    """Should raise error for invalid tier"""
    with pytest.raises(ValueError, match="Invalid tier"):
        FeatureFlags.get_flags("premium")


@pytest.mark.parametrize("tier,expected_download", [
    ("basic", False),
    ("intermediate", True),
    ("advanced", True)
])
def test_video_download_by_tier(tier, expected_download):
    """Test video download permission for each tier"""
    flags = FeatureFlags.get_flags(tier)
    assert flags["video_download"] == expected_download
```

---

### 2. Authentication Tests

**File**: `tests/unit/test_auth.py`

```python
import pytest
from unittest.mock import patch, MagicMock
from utils.auth import authenticate, validate_jwt_token, logout
import streamlit as st

@pytest.fixture
def mock_api_response():
    """Mock successful API response"""
    return {
        "success": True,
        "user_id": "test-user-123",
        "email": "test@example.com",
        "tier": "intermediate",
        "token": "mock-jwt-token",
        "expires_at": "2026-01-13T00:00:00Z"
    }


def test_authenticate_success(mock_api_response):
    """Test successful authentication"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_api_response
        
        with patch.object(st, 'session_state', {}):
            result = authenticate("TEST-VALID-KEY")
            
            assert result == True
            assert st.session_state["authenticated"] == True
            assert st.session_state["tier"] == "intermediate"


def test_authenticate_invalid_key():
    """Test authentication with invalid key"""
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 401
        mock_post.return_value.json.return_value = {
            "success": False,
            "error": "Invalid license key"
        }
        
        with patch.object(st, 'session_state', {}):
            result = authenticate("INVALID-KEY")
            
            assert result == False
            assert st.session_state.get("authenticated") != True


def test_authenticate_network_error():
    """Test authentication with network error"""
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        
        with patch.object(st, 'session_state', {}):
            result = authenticate("TEST-KEY")
            
            assert result == False


def test_jwt_token_validation():
    """Test JWT token validation"""
    valid_token = generate_test_jwt()
    payload = validate_jwt_token(valid_token)
    
    assert payload["user_id"] == "test-user-123"
    assert payload["tier"] == "intermediate"


def test_jwt_token_expired():
    """Test expired JWT token"""
    expired_token = generate_expired_jwt()
    
    with pytest.raises(Exception, match="Token expired"):
        validate_jwt_token(expired_token)


def test_logout():
    """Test logout clears session state"""
    with patch.object(st, 'session_state', {
        "authenticated": True,
        "user_id": "test-user",
        "tier": "intermediate"
    }):
        logout()
        
        assert "authenticated" not in st.session_state
        assert "user_id" not in st.session_state
```

---

### 3. Progress Tracker Tests

**File**: `tests/unit/test_progress_tracker.py`

```python
import pytest
from unittest.mock import patch, MagicMock
from utils.progress_tracker import ProgressTracker

@pytest.fixture
def tracker():
    """Create progress tracker instance"""
    return ProgressTracker("test-user-123")


def test_update_video_progress(tracker):
    """Test updating video watch progress"""
    with patch('database.db.query') as mock_query, \
         patch('database.db.execute') as mock_execute:
        
        mock_query.return_value = None  # No existing record
        
        tracker.update_video_progress(
            video_id="video-123",
            position_seconds=600,
            duration_seconds=1200
        )
        
        # Verify database insert was called
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args[0]
        
        # Check completion percentage (600/1200 = 50%)
        assert 50 in call_args[1]


def test_calculate_module_completion(tracker):
    """Test module completion calculation"""
    with patch.object(tracker, '_calculate_module_completion', return_value=67):
        completion = tracker._calculate_module_completion("ai-03", "module-01")
        
        assert completion == 67
        assert 0 <= completion <= 100


def test_update_lab_progress_completion(tracker):
    """Test marking lab as completed"""
    with patch('database.db.query') as mock_query, \
         patch('database.db.execute') as mock_execute:
        
        mock_query.return_value = None
        
        tracker.update_lab_progress(
            lab_id="lab-123",
            completed=True,
            score=95,
            time_spent=3600
        )
        
        # Verify completion was set to True
        call_args = mock_execute.call_args[0]
        assert True in call_args[1]  # completed = True


def test_quiz_score_calculation(tracker):
    """Test quiz score percentage calculation"""
    with patch('database.db.query') as mock_query, \
         patch('database.db.execute') as mock_execute:
        
        mock_query.return_value = None
        
        tracker.update_quiz_progress(
            quiz_id="quiz-123",
            score=8,
            max_score=10,
            time_taken=600
        )
        
        # Verify percentage (8/10 = 80%)
        call_args = mock_execute.call_args[0]
        assert 80 in call_args[1]
```

---

### 4. AI Tutor Tests

**File**: `tests/unit/test_ai_tutor.py`

```python
import pytest
from unittest.mock import patch, MagicMock
from ai_tutor.tutor import AITutor
from utils.quota_tracker import QuotaTracker

@pytest.fixture
def intermediate_tutor():
    """Create AI Tutor for intermediate tier"""
    with patch.object(st, 'session_state', {
        "current_course": "ai-03",
        "course_title": "NLP with Transformers"
    }):
        return AITutor("test-user", "intermediate")


def test_basic_tier_disabled(intermediate_tutor):
    """Basic tier should not have AI Tutor access"""
    tutor = AITutor("test-user", "basic")
    result = tutor.ask_question("What is NLP?")
    
    assert result["success"] == False
    assert "Intermediate tier" in result["answer"]


def test_intermediate_quota_enforcement(intermediate_tutor):
    """Intermediate tier should enforce 50 question quota"""
    with patch.object(intermediate_tutor.quota_tracker, 'usage', 50):
        result = intermediate_tutor.ask_question("What is a transformer?")
        
        assert result["success"] == False
        assert "quota" in result["answer"].lower()


def test_advanced_unlimited(intermediate_tutor):
    """Advanced tier should have unlimited questions"""
    tutor = AITutor("test-user", "advanced")
    
    with patch('ollama.chat') as mock_ollama:
        mock_ollama.return_value = {
            "message": {"content": "A transformer is a neural network architecture..."},
            "eval_count": 150
        }
        
        result = tutor.ask_question("What is a transformer?")
        
        assert result["success"] == True
        assert "transformer" in result["answer"].lower()


def test_quota_increment(intermediate_tutor):
    """Quota should increment after successful question"""
    initial_usage = intermediate_tutor.quota_tracker.usage
    
    with patch('ollama.chat') as mock_ollama, \
         patch.object(intermediate_tutor.quota_tracker, 'increment_usage') as mock_increment:
        
        mock_ollama.return_value = {
            "message": {"content": "Answer here"},
            "eval_count": 100
        }
        
        intermediate_tutor.ask_question("Test question")
        
        mock_increment.assert_called_once()


def test_hint_mode(intermediate_tutor):
    """Hint mode should provide guidance without full solution"""
    with patch('ollama.chat') as mock_ollama:
        mock_ollama.return_value = {
            "message": {"content": "Think about the attention mechanism..."},
            "eval_count": 50
        }
        
        result = intermediate_tutor.get_hint_mode("I'm stuck on Lab 3")
        
        assert result["success"] == True
        # Verify hint instruction was added to prompt
        mock_ollama.assert_called_once()
```

---

## Integration Tests (20%)

### 1. CoursesGTM API Integration

**File**: `tests/integration/test_coursesgtm_integration.py`

```python
import pytest
import responses
from utils.api_client import CoursesGTMClient

@pytest.fixture
def gtm_client():
    """Create CoursesGTM client instance"""
    return CoursesGTMClient(base_url="http://localhost:8000")


@responses.activate
def test_validate_license_success(gtm_client):
    """Test successful license validation"""
    responses.add(
        responses.POST,
        "http://localhost:8000/api/v1/licenses/validate",
        json={
            "success": True,
            "user_id": "test-user",
            "tier": "intermediate",
            "token": "mock-token"
        },
        status=200
    )
    
    result = gtm_client.validate_license("TEST-KEY")
    
    assert result["success"] == True
    assert result["tier"] == "intermediate"


@responses.activate
def test_get_courses(gtm_client):
    """Test fetching course catalog"""
    responses.add(
        responses.GET,
        "http://localhost:8000/api/v1/courses",
        json={
            "courses": [
                {"id": "ai-01", "title": "Intro to AI"},
                {"id": "ai-02", "title": "ML Fundamentals"}
            ],
            "total": 2
        },
        status=200
    )
    
    courses = gtm_client.get_courses("mock-token")
    
    assert len(courses["courses"]) == 2
    assert courses["total"] == 2


@responses.activate
def test_api_rate_limit(gtm_client):
    """Test handling of rate limit errors"""
    responses.add(
        responses.GET,
        "http://localhost:8000/api/v1/courses",
        json={"error": "Rate limit exceeded"},
        status=429
    )
    
    with pytest.raises(Exception, match="Rate limit"):
        gtm_client.get_courses("mock-token")
```

---

### 2. SimulationPlayer Integration

**File**: `tests/integration/test_simulationplayer_integration.py`

```python
import pytest
from utils.lab_launcher import generate_lab_launch_url

def test_launch_url_generation():
    """Test SimulationPlayer launch URL generation"""
    url = generate_lab_launch_url(
        course_id="ai-03",
        lab_id="lab1",
        user_id="test-user",
        tier="intermediate",
        token="mock-token"
    )
    
    assert "simulationplayer.com/launch" in url
    assert "course_id=ai-03" in url
    assert "lab_id=lab1" in url
    assert "tier=intermediate" in url


def test_lab_completion_webhook():
    """Test lab completion webhook handling"""
    from api.webhooks import lab_complete_webhook
    
    with app.test_client() as client:
        response = client.post('/api/webhook/lab-complete', json={
            "user_id": "test-user",
            "lab_id": "lab1",
            "completed": True,
            "score": 95,
            "signature": "valid-signature"
        })
        
        assert response.status_code == 200
        assert response.json["success"] == True
```

---

### 3. OLLAMA Integration

**File**: `tests/integration/test_ollama_integration.py`

```python
import pytest
import ollama

@pytest.mark.slow
def test_ollama_connection():
    """Test OLLAMA service is accessible"""
    try:
        models = ollama.list()
        assert "llama3.1:8b" in [m['name'] for m in models['models']]
    except Exception as e:
        pytest.skip(f"OLLAMA not available: {e}")


@pytest.mark.slow
def test_ollama_chat_response():
    """Test OLLAMA generates response"""
    try:
        response = ollama.chat(
            model="llama3.1:8b",
            messages=[{"role": "user", "content": "What is 2+2?"}]
        )
        
        assert "4" in response['message']['content']
    except Exception as e:
        pytest.skip(f"OLLAMA not available: {e}")
```

---

## UI Tests (5%)

### Using Playwright

**File**: `tests/ui/test_login_flow.py`

```python
import pytest
from playwright.sync_api import Page, expect

def test_login_page_loads(page: Page):
    """Test login page loads correctly"""
    page.goto("http://localhost:8501")
    
    expect(page.locator("h1")).to_have_text("GAI-Observe Academy")
    expect(page.locator('input[type="password"]')).to_be_visible()


def test_login_with_valid_key(page: Page):
    """Test login with valid license key"""
    page.goto("http://localhost:8501")
    
    # Enter license key
    page.fill('input[type="password"]', "TEST-VALID-KEY")
    page.click('text="Login"')
    
    # Wait for redirect to dashboard
    page.wait_for_url("**/Dashboard")
    expect(page.locator("text=Welcome back")).to_be_visible()


def test_login_with_invalid_key(page: Page):
    """Test login with invalid license key"""
    page.goto("http://localhost:8501")
    
    page.fill('input[type="password"]', "INVALID-KEY")
    page.click('text="Login"')
    
    # Should show error message
    expect(page.locator("text=Invalid license")).to_be_visible()


def test_course_navigation(page: Page):
    """Test navigating to course player"""
    # Assume already logged in
    page.goto("http://localhost:8501/My_Courses")
    
    # Click on first course
    page.click('button:has-text("Continue Learning"):first')
    
    # Should navigate to course player
    page.wait_for_url("**/Course_Player")
    expect(page.locator("video")).to_be_visible()
```

---

## Accessibility Tests

**File**: `tests/accessibility/test_wcag_compliance.py`

```python
import pytest
from playwright.sync_api import Page
from axe_playwright_python.sync_playwright import Axe

def test_homepage_accessibility(page: Page):
    """Test homepage WCAG compliance"""
    page.goto("http://localhost:8501")
    
    axe = Axe()
    results = axe.run(page)
    
    assert len(results.violations) == 0, f"Violations: {results.violations}"


def test_dashboard_accessibility(page: Page):
    """Test dashboard WCAG compliance"""
    # Login first
    login(page)
    page.goto("http://localhost:8501/Dashboard")
    
    axe = Axe()
    results = axe.run(page)
    
    assert len(results.violations) == 0


def test_keyboard_navigation(page: Page):
    """Test all interactive elements are keyboard accessible"""
    page.goto("http://localhost:8501")
    
    # Tab through elements
    page.keyboard.press("Tab")
    focused = page.evaluate("document.activeElement.tagName")
    assert focused in ["INPUT", "BUTTON", "A"]


def test_color_contrast(page: Page):
    """Test color contrast ratios"""
    page.goto("http://localhost:8501")
    
    # Check primary button contrast
    button = page.locator("button").first
    bg_color = button.evaluate("window.getComputedStyle(this).backgroundColor")
    text_color = button.evaluate("window.getComputedStyle(this).color")
    
    contrast_ratio = calculate_contrast_ratio(bg_color, text_color)
    assert contrast_ratio >= 4.5  # WCAG AA standard
```

---

## Performance Tests

### Load Testing with Locust

**File**: `tests/performance/test_load.py`

```python
from locust import HttpUser, task, between

class CoursePlayerUser(HttpUser):
    wait_time = between(1, 5)
    
    def on_start(self):
        """Login before running tasks"""
        self.client.post("/api/v1/licenses/validate", json={
            "license_key": "TEST-KEY"
        })
    
    @task(3)
    def view_dashboard(self):
        """Simulate viewing dashboard"""
        self.client.get("/Dashboard")
    
    @task(2)
    def browse_courses(self):
        """Simulate browsing courses"""
        self.client.get("/My_Courses")
    
    @task(1)
    def watch_video(self):
        """Simulate watching video"""
        self.client.get("/Course_Player")
        self.client.post("/api/progress/video", json={
            "video_id": "video-123",
            "position": 600
        })


# Run: locust -f tests/performance/test_load.py --host=http://localhost:8501
```

### Response Time Tests

**File**: `tests/performance/test_response_times.py`

```python
import pytest
import time
from utils.api_client import CoursesGTMClient

def test_course_catalog_response_time():
    """Course catalog should load within 2 seconds"""
    client = CoursesGTMClient()
    
    start = time.time()
    courses = client.get_courses("mock-token")
    end = time.time()
    
    assert (end - start) < 2.0, "Course catalog took too long to load"


def test_video_streaming_startup():
    """Video should start playing within 3 seconds"""
    # Measure time from request to first frame
    start = time.time()
    url = get_video_streaming_url("video-123", "intermediate")
    # ... simulate video load
    end = time.time()
    
    assert (end - start) < 3.0
```

---

## Continuous Integration (CI)

### GitHub Actions Workflow

**File**: `.github/workflows/test.yml`

```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

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
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: pytest tests/unit -v --cov --cov-report=xml
    
    - name: Run integration tests
      run: pytest tests/integration -v -m "not slow"
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Install Playwright
      run: playwright install
    
    - name: Run UI tests
      run: pytest tests/ui -v
    
    - name: Run accessibility tests
      run: pytest tests/accessibility -v
```

---

## Test Data Management

### Fixtures

**File**: `tests/fixtures/mock_data.py`

```python
import pytest

@pytest.fixture
def mock_user():
    """Mock user data"""
    return {
        "user_id": "test-user-123",
        "email": "test@example.com",
        "tier": "intermediate",
        "license_key": "TEST-KEY"
    }


@pytest.fixture
def mock_course():
    """Mock course data"""
    return {
        "id": "ai-03-nlp-transformers",
        "title": "NLP with Transformers",
        "modules": [
            {
                "id": "module-01",
                "title": "Introduction",
                "videos": [{"id": "v1", "title": "What is NLP?"}]
            }
        ]
    }


@pytest.fixture
def mock_progress():
    """Mock progress data"""
    return {
        "course_id": "ai-03",
        "overall_progress": 67,
        "modules_completed": 2
    }
```

---

## Test Execution

### Run All Tests
```bash
pytest
```

### Run Specific Test Types
```bash
# Unit tests only
pytest tests/unit

# Integration tests only
pytest tests/integration

# UI tests only
pytest tests/ui

# Accessibility tests
pytest tests/accessibility

# Slow tests (integration + load)
pytest -m slow

# Fast tests only (exclude slow)
pytest -m "not slow"
```

### Coverage Report
```bash
pytest --cov=utils --cov=components --cov-report=html
open htmlcov/index.html
```

---

## Test Metrics & KPIs

### Coverage Goals
- **Overall coverage**: ≥80%
- **Critical paths** (auth, feature gating): ≥95%
- **UI components**: ≥70%

### Performance Benchmarks
- **API response time**: <500ms (p95)
- **Page load time**: <2s (p95)
- **Video startup**: <3s

### Accessibility Goals
- **Zero critical violations**: axe/WAVE
- **Lighthouse accessibility score**: ≥90

---

## Testing Best Practices

### 1. Test Naming Convention
```python
# Good
def test_intermediate_tier_has_50_ai_tutor_quota():
    ...

# Bad
def test_quota():
    ...
```

### 2. Arrange-Act-Assert Pattern
```python
def test_video_progress_update():
    # Arrange
    tracker = ProgressTracker("user-123")
    
    # Act
    tracker.update_video_progress("video-123", position=600, duration=1200)
    
    # Assert
    progress = tracker.get_video_progress("video-123")
    assert progress['completion_percentage'] == 50
```

### 3. Use Fixtures for Common Setup
```python
@pytest.fixture
def authenticated_user():
    """Setup authenticated user session"""
    with patch.object(st, 'session_state', {
        "authenticated": True,
        "tier": "intermediate"
    }):
        yield


def test_course_access(authenticated_user):
    # Test uses authenticated session
    ...
```

### 4. Mock External Dependencies
```python
# Mock CoursesGTM API
with patch('requests.post') as mock_post:
    mock_post.return_value.json.return_value = {"tier": "intermediate"}
    ...

# Mock OLLAMA
with patch('ollama.chat') as mock_ollama:
    mock_ollama.return_value = {"message": {"content": "Answer"}}
    ...
```

---

## Conclusion

This comprehensive testing strategy ensures:
- **Reliability**: Catch bugs before production
- **Quality**: Maintain high code quality standards
- **Performance**: Meet response time SLAs
- **Accessibility**: WCAG compliance validated
- **Confidence**: Safe to deploy frequently

Testing is not optional—it's essential for delivering a world-class learning platform.
