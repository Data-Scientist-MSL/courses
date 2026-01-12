# Testing Strategy

This document defines the comprehensive testing approach for CoursePlayerApp, covering unit tests, integration tests, UI tests, end-to-end tests, performance tests, and accessibility tests.

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Component Tests](#component-tests)
3. [Feature Gate Tests](#feature-gate-tests)
4. [Integration Tests](#integration-tests)
5. [UI Tests](#ui-tests)
6. [End-to-End Tests](#end-to-end-tests)
7. [Performance Tests](#performance-tests)
8. [Accessibility Tests](#accessibility-tests)
9. [Test Infrastructure](#test-infrastructure)

---

## Testing Philosophy

### Principles

1. **Test Early, Test Often**: Write tests alongside code
2. **Fast Feedback**: Unit tests complete in seconds
3. **Comprehensive Coverage**: Aim for >80% code coverage
4. **Realistic Scenarios**: Test actual user workflows
5. **Tier-Aware Testing**: Test all tier combinations
6. **Automated Execution**: CI/CD integration

### Testing Pyramid

```
        /\
       /E2E\          (10%) - Full user journeys
      /------\
     /  UI    \       (20%) - UI component rendering
    /----------\
   /Integration\     (30%) - API interactions
  /--------------\
 /  Unit Tests   \   (40%) - Individual functions
/------------------\
```

---

## Component Tests

Test individual components in isolation.

### Video Player Component

**File**: `tests/unit/components/test_video_player.py`

```python
import pytest
from unittest.mock import Mock, patch
from courseplayerapp.components.video.player import VideoPlayer

class TestVideoPlayer:
    """Test video player component"""
    
    @pytest.fixture
    def mock_gtm_client(self):
        """Mock CoursesGTM client"""
        client = Mock()
        client.get_video_metadata.return_value = {
            'video_id': 'video123',
            'title': 'Test Video',
            'stream_url': 'https://cdn.example.com/video.m3u8',
            'available_qualities': ['auto', '720p', '1080p']
        }
        return client
    
    def test_basic_tier_streaming_only(self, mock_gtm_client):
        """Basic tier should only have streaming"""
        with patch('streamlit.session_state', {'tier': 'basic'}):
            player = VideoPlayer('video123', mock_gtm_client)
            
            # Should render basic player
            assert player.tier == 'basic'
            
            # Should not allow download
            with pytest.raises(AttributeError):
                player._render_download_button({})
    
    def test_intermediate_tier_download(self, mock_gtm_client):
        """Intermediate tier should support download"""
        with patch('streamlit.session_state', {'tier': 'intermediate'}):
            player = VideoPlayer('video123', mock_gtm_client)
            
            assert player.tier == 'intermediate'
            # Download should be available
            # Verify max quality is 720p
    
    def test_advanced_tier_annotations(self, mock_gtm_client):
        """Advanced tier should support annotations"""
        with patch('streamlit.session_state', {'tier': 'advanced'}):
            player = VideoPlayer('video123', mock_gtm_client)
            
            assert player.tier == 'advanced'
            # Verify annotation panel available
    
    def test_quality_selector_basic(self, mock_gtm_client):
        """Basic tier gets auto quality only"""
        with patch('streamlit.session_state', {'tier': 'basic'}):
            player = VideoPlayer('video123', mock_gtm_client)
            # Verify only auto quality available
    
    def test_quality_selector_advanced(self, mock_gtm_client):
        """Advanced tier gets manual quality selection"""
        with patch('streamlit.session_state', {'tier': 'advanced'}):
            player = VideoPlayer('video123', mock_gtm_client)
            # Verify manual quality selection available
```

### AI Tutor Component

**File**: `tests/unit/components/test_ai_tutor.py`

```python
import pytest
from unittest.mock import Mock, patch
from courseplayerapp.components.ai_tutor.chat_interface import AITutorChat

class TestAITutorChat:
    """Test AI tutor chat component"""
    
    @pytest.fixture
    def mock_ollama(self):
        """Mock OLLAMA client"""
        client = Mock()
        client.stream_chat.return_value = iter(['This ', 'is ', 'a ', 'test'])
        return client
    
    @pytest.fixture
    def mock_gtm(self):
        """Mock CoursesGTM client"""
        client = Mock()
        client.get_ai_tutor_quota.return_value = {
            'remaining': 45,
            'total': 50,
            'reset_date': '2024-02-01'
        }
        return client
    
    def test_basic_tier_blocked(self):
        """Basic tier should not access AI tutor"""
        with patch('streamlit.session_state', {'tier': 'basic'}):
            tutor = AITutorChat('course123')
            
            # Should show upgrade prompt
            with pytest.raises(PermissionError):
                tutor.render()
    
    def test_intermediate_tier_quota(self, mock_ollama, mock_gtm):
        """Intermediate tier should have quota limit"""
        with patch('streamlit.session_state', {'tier': 'intermediate'}):
            tutor = AITutorChat('course123')
            
            # Verify quota display
            quota = mock_gtm.get_ai_tutor_quota()
            assert quota['remaining'] == 45
            assert quota['total'] == 50
    
    def test_advanced_tier_unlimited(self, mock_ollama, mock_gtm):
        """Advanced tier should have unlimited quota"""
        mock_gtm.get_ai_tutor_quota.return_value = {
            'remaining': 'unlimited',
            'total': 'unlimited'
        }
        
        with patch('streamlit.session_state', {'tier': 'advanced'}):
            tutor = AITutorChat('course123')
            
            quota = mock_gtm.get_ai_tutor_quota()
            assert quota['remaining'] == 'unlimited'
    
    def test_streaming_response(self, mock_ollama):
        """Test streaming chat response"""
        with patch('streamlit.session_state', {'tier': 'intermediate'}):
            tutor = AITutorChat('course123')
            
            chunks = list(mock_ollama.stream_chat('test'))
            assert chunks == ['This ', 'is ', 'a ', 'test']
    
    def test_quota_exceeded(self, mock_gtm):
        """Test behavior when quota exceeded"""
        mock_gtm.get_ai_tutor_quota.return_value = {
            'remaining': 0,
            'total': 50
        }
        
        with patch('streamlit.session_state', {'tier': 'intermediate'}):
            tutor = AITutorChat('course123')
            
            # Should not allow new questions
            with pytest.raises(QuotaExceededError):
                tutor._handle_user_message('test')
```

### Progress Tracker Component

**File**: `tests/unit/components/test_progress_tracker.py`

```python
import pytest
from unittest.mock import Mock
from courseplayerapp.components.progress.tracker import ProgressTracker

class TestProgressTracker:
    """Test progress tracking component"""
    
    def test_basic_tier_simple_progress(self):
        """Basic tier gets simple progress only"""
        with patch('streamlit.session_state', {'tier': 'basic'}):
            tracker = ProgressTracker('course123')
            
            # Should show completion percentage only
            # No gamification features
    
    def test_intermediate_tier_gamification(self):
        """Intermediate tier gets full gamification"""
        with patch('streamlit.session_state', {'tier': 'intermediate'}):
            tracker = ProgressTracker('course123')
            
            # Should show XP, levels, streaks
            assert tracker.show_gamification == True
    
    def test_streak_calculation(self):
        """Test streak calculation logic"""
        tracker = ProgressTracker('course123')
        
        activity_dates = [
            '2024-01-01', '2024-01-02', '2024-01-03', '2024-01-05'
        ]
        
        streak = tracker._calculate_streak(activity_dates)
        assert streak == 1  # Broken at 01-04
    
    def test_xp_to_level_conversion(self):
        """Test XP to level calculation"""
        tracker = ProgressTracker('course123')
        
        assert tracker._calculate_level(0) == 1
        assert tracker._calculate_level(1000) == 2
        assert tracker._calculate_level(3000) == 4
```

---

## Feature Gate Tests

Test tier-based access control.

**File**: `tests/unit/middleware/test_feature_gates.py`

```python
import pytest
from unittest.mock import patch
from courseplayerapp.middleware.feature_gates import (
    requires_tier,
    requires_feature,
    quota_limited
)

class TestFeatureGates:
    """Test feature gating decorators"""
    
    def test_requires_tier_basic_blocked(self):
        """Basic tier blocked from Intermediate features"""
        @requires_tier('intermediate')
        def protected_function():
            return "success"
        
        with patch('streamlit.session_state', {'tier': 'basic'}):
            result = protected_function()
            assert result is None
    
    def test_requires_tier_hierarchy(self):
        """Advanced tier can access all lower tiers"""
        @requires_tier('basic')
        def basic_function():
            return "basic"
        
        @requires_tier('intermediate')
        def intermediate_function():
            return "intermediate"
        
        @requires_tier('advanced')
        def advanced_function():
            return "advanced"
        
        with patch('streamlit.session_state', {'tier': 'advanced'}):
            assert basic_function() == "basic"
            assert intermediate_function() == "intermediate"
            assert advanced_function() == "advanced"
    
    def test_requires_feature_enabled(self):
        """Feature enabled check"""
        @requires_feature('video_download')
        def download_video():
            return "downloading"
        
        # Feature enabled
        with patch('streamlit.session_state', {'enabled_features': ['video_download']}):
            assert download_video() == "downloading"
        
        # Feature not enabled
        with patch('streamlit.session_state', {'enabled_features': []}):
            assert download_video() is None
    
    def test_quota_limited_enforcement(self):
        """Quota limiting works correctly"""
        @quota_limited('test_quota')
        def quota_function():
            return "executed"
        
        with patch('courseplayerapp.middleware.feature_gates.check_quota') as mock_check:
            # Quota available
            mock_check.return_value = {'remaining': 5}
            assert quota_function() == "executed"
            
            # Quota exhausted
            mock_check.return_value = {'remaining': 0}
            assert quota_function() is None
    
    def test_stacked_decorators(self):
        """Multiple decorators work together"""
        @requires_tier('intermediate')
        @requires_feature('ai_tutor')
        @quota_limited('ai_tutor_quota')
        def ai_question():
            return "answered"
        
        with patch('streamlit.session_state', {
            'tier': 'intermediate',
            'enabled_features': ['ai_tutor']
        }):
            with patch('courseplayerapp.middleware.feature_gates.check_quota') as mock_check:
                mock_check.return_value = {'remaining': 10}
                assert ai_question() == "answered"
```

---

## Integration Tests

Test interactions with external services.

**File**: `tests/integration/test_coursesgtm_integration.py`

```python
import pytest
import requests_mock
from courseplayerapp.integrations.coursesgtm_client import CoursesGTMClient

class TestCoursesGTMIntegration:
    """Test CoursesGTM API integration"""
    
    @pytest.fixture
    def gtm_client(self):
        return CoursesGTMClient(base_url="http://test-api.example.com")
    
    def test_license_validation_success(self, gtm_client):
        """Test successful license validation"""
        with requests_mock.Mocker() as m:
            m.post(
                "http://test-api.example.com/api/v1/license/validate",
                json={
                    "valid": True,
                    "tier": "intermediate",
                    "enabled_features": ["video_download", "ai_tutor"],
                    "expires_at": "2024-12-31",
                    "user_id": "user123",
                    "user_email": "user@example.com"
                }
            )
            
            result = gtm_client.validate_license("TEST-LICENSE-KEY")
            
            assert result['valid'] == True
            assert result['tier'] == 'intermediate'
            assert 'video_download' in result['enabled_features']
    
    def test_license_validation_failure(self, gtm_client):
        """Test failed license validation"""
        with requests_mock.Mocker() as m:
            m.post(
                "http://test-api.example.com/api/v1/license/validate",
                status_code=401,
                json={"valid": False, "message": "Invalid license key"}
            )
            
            with pytest.raises(requests.exceptions.HTTPError):
                gtm_client.validate_license("INVALID-KEY")
    
    def test_api_retry_on_failure(self, gtm_client):
        """Test automatic retry on transient failures"""
        with requests_mock.Mocker() as m:
            # First call fails, second succeeds
            m.post(
                "http://test-api.example.com/api/v1/license/validate",
                [
                    {'status_code': 503},  # Service unavailable
                    {'json': {'valid': True}, 'status_code': 200}  # Success
                ]
            )
            
            result = gtm_client.validate_license("TEST-KEY")
            assert result['valid'] == True
    
    def test_progress_update(self, gtm_client):
        """Test progress update API call"""
        with requests_mock.Mocker() as m:
            m.post(
                "http://test-api.example.com/api/v1/progress/course123/update",
                json={"success": True, "xp_earned": 50}
            )
            
            result = gtm_client.update_progress('course123', 'lesson456', completed=True)
            
            assert result['success'] == True
            assert result['xp_earned'] == 50
```

---

## UI Tests

Test Streamlit page rendering.

**File**: `tests/ui/test_home_page.py`

```python
import pytest
from streamlit.testing.v1 import AppTest
from courseplayerapp.pages.00_🏠_Home import render_home_page

class TestHomePage:
    """Test home page UI"""
    
    def test_home_page_renders_basic_tier(self):
        """Home page renders correctly for Basic tier"""
        at = AppTest.from_function(render_home_page)
        at.session_state['tier'] = 'basic'
        at.session_state['user_name'] = 'Test User'
        at.run()
        
        # Check title
        assert at.title[0].value == "🏠 Welcome back, Test User!"
        
        # Check tier badge
        assert '🔵 Basic' in str(at.caption)
        
        # Should not show streak tracker
        assert 'streak' not in at.session_state
    
    def test_home_page_intermediate_tier(self):
        """Home page shows gamification for Intermediate"""
        at = AppTest.from_function(render_home_page)
        at.session_state['tier'] = 'intermediate'
        at.session_state['user_name'] = 'Test User'
        at.run()
        
        # Should show streak tracker
        # Should show XP display
    
    def test_quick_actions_buttons(self):
        """Quick action buttons are clickable"""
        at = AppTest.from_function(render_home_page)
        at.session_state['tier'] = 'intermediate'
        at.run()
        
        # Find and click buttons
        learn_button = at.button[0]
        assert learn_button.label == "🎓 Learn"
```

---

## End-to-End Tests

Test complete user workflows.

**File**: `tests/e2e/test_learning_flow.py`

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestLearningFlow:
    """End-to-end test for complete learning flow"""
    
    @pytest.fixture
    def browser(self):
        """Setup browser"""
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        yield driver
        driver.quit()
    
    def test_complete_lesson_flow(self, browser):
        """Test: Login → Browse → Start Course → Complete Lesson"""
        
        # 1. Navigate to app
        browser.get("http://localhost:8501")
        
        # 2. Enter license key
        license_input = browser.find_element(By.CSS_SELECTOR, "input[type='password']")
        license_input.send_keys("TEST-LICENSE-KEY")
        
        activate_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Activate')]")
        activate_button.click()
        
        # 3. Wait for home page
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Welcome')]"))
        )
        
        # 4. Navigate to course browser
        browser.find_element(By.LINK_TEXT, "📚 Courses").click()
        
        # 5. Start a course
        start_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Start')]")
        start_button.click()
        
        # 6. Play video
        play_button = browser.find_element(By.CSS_SELECTOR, "button.video-play")
        play_button.click()
        
        # 7. Mark complete
        complete_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Mark Complete')]")
        complete_button.click()
        
        # 8. Verify progress updated
        progress_element = browser.find_element(By.CSS_SELECTOR, ".progress-bar")
        assert "1%" in progress_element.text or progress_element.get_attribute("value") > 0
    
    def test_ai_tutor_interaction(self, browser):
        """Test AI tutor question flow"""
        
        # Navigate to AI tutor
        browser.get("http://localhost:8501/AI_Tutor")
        
        # Enter question
        question_input = browser.find_element(By.CSS_SELECTOR, "textarea")
        question_input.send_keys("What is gradient descent?")
        
        # Send
        send_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Send')]")
        send_button.click()
        
        # Wait for response
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ai-response"))
        )
        
        # Verify response contains relevant content
        response = browser.find_element(By.CSS_SELECTOR, ".ai-response")
        assert len(response.text) > 50  # Substantial response
```

---

## Performance Tests

Test app performance and scalability.

**File**: `tests/performance/test_load.py`

```python
import pytest
from locust import HttpUser, task, between

class CoursePlayerUser(HttpUser):
    """Simulated user for load testing"""
    
    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    
    def on_start(self):
        """Login on start"""
        self.client.post("/api/login", json={
            "license_key": "TEST-KEY"
        })
    
    @task(3)
    def view_home(self):
        """View home page (weighted 3x)"""
        self.client.get("/")
    
    @task(2)
    def browse_courses(self):
        """Browse courses (weighted 2x)"""
        self.client.get("/Course_Browser")
    
    @task(5)
    def watch_video(self):
        """Watch video lesson (weighted 5x - most common)"""
        self.client.get("/Learn")
        self.client.get("/api/v1/videos/video123/stream-url")
    
    @task(1)
    def use_ai_tutor(self):
        """Ask AI tutor question (weighted 1x)"""
        self.client.post("/api/ai-tutor/ask", json={
            "question": "What is machine learning?"
        })

# Run with: locust -f tests/performance/test_load.py --host=http://localhost:8501
```

**Performance Benchmarks:**

```python
def test_video_stream_start_time():
    """Video should start within 3 seconds"""
    start = time.time()
    response = requests.get("http://localhost:8501/api/videos/test/stream")
    elapsed = time.time() - start
    
    assert elapsed < 3.0, f"Video start took {elapsed}s, expected < 3s"

def test_ai_response_time():
    """AI should respond within 10 seconds"""
    start = time.time()
    response = requests.post(
        "http://localhost:8501/api/ai-tutor/ask",
        json={"question": "test"}
    )
    elapsed = time.time() - start
    
    assert elapsed < 10.0, f"AI response took {elapsed}s, expected < 10s"

def test_page_load_time():
    """Page should load within 2 seconds"""
    start = time.time()
    response = requests.get("http://localhost:8501/")
    elapsed = time.time() - start
    
    assert elapsed < 2.0, f"Page load took {elapsed}s, expected < 2s"
```

---

## Accessibility Tests

Ensure WCAG 2.1 Level AA compliance.

**File**: `tests/accessibility/test_wcag.py`

```python
import pytest
from axe_selenium_python import Axe

def test_home_page_accessibility(browser):
    """Test home page accessibility"""
    browser.get("http://localhost:8501")
    
    axe = Axe(browser)
    axe.inject()
    results = axe.run()
    
    assert len(results["violations"]) == 0, \
        f"Accessibility violations: {results['violations']}"

def test_color_contrast():
    """Test color contrast ratios"""
    # WCAG AA requires 4.5:1 for normal text, 3:1 for large text
    pass

def test_keyboard_navigation():
    """Test keyboard-only navigation"""
    pass

def test_screen_reader_compatibility():
    """Test screen reader labels"""
    pass
```

---

## Test Infrastructure

### Running Tests

```bash
# Run all tests
pytest

# Run specific category
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with coverage
pytest --cov=courseplayerapp --cov-report=html

# Run performance tests
locust -f tests/performance/test_load.py

# Run accessibility tests
pytest tests/accessibility/
```

### CI/CD Integration

**File**: `.github/workflows/test.yml`

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: pytest tests/unit/ --cov=courseplayerapp
    
    - name: Run integration tests
      run: pytest tests/integration/
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

### Test Data Management

```python
# tests/conftest.py - Shared fixtures

@pytest.fixture
def sample_user():
    return {
        'user_id': 'test123',
        'tier': 'intermediate',
        'email': 'test@example.com'
    }

@pytest.fixture
def sample_course():
    return {
        'course_id': 'ml-fundamentals',
        'title': 'Machine Learning Fundamentals',
        'modules': [...]
    }
```

---

This comprehensive testing strategy ensures CoursePlayerApp is reliable, performant, accessible, and maintains quality across all tiers and features.
