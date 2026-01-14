# Testing Strategy

## Overview

Comprehensive testing ensures CoursePlayerApp delivers a reliable, secure, and high-quality learning experience. This specification defines the testing approach across unit, integration, UI, accessibility, and security testing.

---

## Testing Pyramid

```
           /\
          /  \
         / UI \
        / Tests \
       /----------\
      /            \
     / Integration  \
    /     Tests      \
   /------------------\
  /                    \
 /     Unit Tests       \
/-----------------------

\

- **Unit Tests** (70%): Fast, isolated component testing
- **Integration Tests** (20%): API and system integration
- **UI/E2E Tests** (10%): User workflow validation
```

---

## 1. Unit Testing

### Test Framework
- **pytest**: Primary testing framework
- **pytest-cov**: Code coverage reporting
- **pytest-mock**: Mocking dependencies

### Setup

**File**: `requirements-dev.txt`
```txt
pytest==7.4.0
pytest-cov==4.1.0
pytest-mock==3.11.1
pytest-streamlit==0.1.0
```

**File**: `pytest.ini`
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

### Unit Test Examples

#### Testing Feature Gating Logic

**File**: `tests/test_feature_gating.py`
```python
import pytest
from utils.feature_flags import get_tier_config, has_feature_access

class TestFeatureGating:
    """Test feature gating logic"""
    
    def test_basic_tier_video_download_disabled(self):
        """Basic tier should not have video download"""
        config = get_tier_config('basic')
        assert config['video_download'] == False
        assert config['video_quality'] == '480p'
    
    def test_intermediate_tier_video_download_enabled(self):
        """Intermediate tier should have video download"""
        config = get_tier_config('intermediate')
        assert config['video_download'] == True
        assert config['video_quality'] == '720p'
    
    def test_advanced_tier_unlimited_ai_tutor(self):
        """Advanced tier should have unlimited AI tutor"""
        config = get_tier_config('advanced')
        assert config['ai_tutor_enabled'] == True
        assert config['ai_tutor_quota'] == -1  # Unlimited
    
    def test_invalid_tier_raises_error(self):
        """Invalid tier should raise ValueError"""
        with pytest.raises(ValueError):
            get_tier_config('invalid_tier')
    
    def test_course_access_basic_tier(self, mocker):
        """Basic tier should only access basic courses"""
        mocker.patch('streamlit.session_state', {'tier': 'basic'})
        
        assert has_feature_access('ai-01') == True
        assert has_feature_access('ai-04') == False  # Advanced course
    
    def test_course_access_advanced_tier(self, mocker):
        """Advanced tier should access all courses"""
        mocker.patch('streamlit.session_state', {'tier': 'advanced'})
        
        assert has_feature_access('ai-01') == True
        assert has_feature_access('ai-04') == True
```

#### Testing AI Tutor Quota

**File**: `tests/test_ai_tutor.py`
```python
import pytest
from components.ai_tutor import AITutor
from datetime import datetime

class TestAITutor:
    """Test AI Tutor quota management"""
    
    @pytest.fixture
    def basic_tutor(self, mocker):
        """Basic tier AI tutor"""
        mocker.patch('streamlit.session_state', {
            'tier': 'basic',
            'user_id': 'test_user'
        })
        return AITutor()
    
    @pytest.fixture
    def intermediate_tutor(self, mocker):
        """Intermediate tier AI tutor"""
        mocker.patch('streamlit.session_state', {
            'tier': 'intermediate',
            'user_id': 'test_user'
        })
        mocker.patch('components.ai_tutor.get_ai_usage', return_value=0)
        return AITutor()
    
    @pytest.fixture
    def advanced_tutor(self, mocker):
        """Advanced tier AI tutor"""
        mocker.patch('streamlit.session_state', {
            'tier': 'advanced',
            'user_id': 'test_user'
        })
        return AITutor()
    
    def test_basic_tier_cannot_ask(self, basic_tutor):
        """Basic tier should not be able to ask questions"""
        can_ask, message = basic_tutor.can_ask_question()
        assert can_ask == False
        assert "Intermediate tier" in message
    
    def test_intermediate_tier_quota_enforcement(self, intermediate_tutor, mocker):
        """Intermediate tier should enforce 50 question quota"""
        # Simulate 50 questions used
        mocker.patch('components.ai_tutor.get_ai_usage', return_value=50)
        intermediate_tutor.usage = 50
        
        can_ask, message = intermediate_tutor.can_ask_question()
        assert can_ask == False
        assert "used all 50" in message
    
    def test_advanced_tier_unlimited(self, advanced_tutor):
        """Advanced tier should have unlimited questions"""
        can_ask, message = advanced_tutor.can_ask_question()
        assert can_ask == True
        assert "Unlimited" in message
    
    def test_question_increments_usage(self, intermediate_tutor, mocker):
        """Asking question should increment usage"""
        mock_increment = mocker.patch('components.ai_tutor.increment_ai_usage')
        mocker.patch('components.ai_tutor.ollama_chat', return_value="Answer")
        
        intermediate_tutor.ask_question("What is AI?")
        
        mock_increment.assert_called_once()
```

#### Testing Progress Calculation

**File**: `tests/test_progress.py`
```python
import pytest
from utils.progress import (
    calculate_course_progress,
    calculate_video_completion,
    calculate_quiz_completion
)

class TestProgressCalculation:
    """Test progress calculation logic"""
    
    def test_video_completion_all_watched(self):
        """All videos watched should be 100%"""
        modules = [
            {
                'videos': [
                    {'completion_percentage': 100},
                    {'completion_percentage': 100}
                ]
            }
        ]
        
        assert calculate_video_completion(modules) == 100
    
    def test_video_completion_partial(self):
        """Half videos watched should be 50%"""
        modules = [
            {
                'videos': [
                    {'completion_percentage': 100},
                    {'completion_percentage': 0}
                ]
            }
        ]
        
        assert calculate_video_completion(modules) == 50
    
    def test_quiz_completion_all_passed(self):
        """All quizzes passed should be 100%"""
        modules = [
            {'quiz': {'status': 'completed', 'passed': True}},
            {'quiz': {'status': 'completed', 'passed': True}}
        ]
        
        assert calculate_quiz_completion(modules) == 100
    
    def test_course_progress_weighted(self):
        """Course progress should use weighted average"""
        course_data = {
            'modules': [
                {
                    'videos': [
                        {'completion_percentage': 100},
                        {'completion_percentage': 100}
                    ],
                    'quiz': {'status': 'completed', 'passed': True},
                    'labs': [{'status': 'completed'}],
                    'slides': [{'slides_count': 10, 'slides_viewed': 10}]
                }
            ]
        }
        
        progress = calculate_course_progress(course_data)
        assert progress == 100
```

#### Testing Video Player

**File**: `tests/test_video_player.py`
```python
import pytest
from components.video_player import build_video_url, render_download_button

class TestVideoPlayer:
    """Test video player functionality"""
    
    def test_build_video_url_basic_tier(self):
        """Basic tier should get 480p URL"""
        config = {'video_quality': '480p'}
        url = build_video_url('video-123', 'basic', config)
        assert '480p' in url
    
    def test_build_video_url_intermediate_tier(self):
        """Intermediate tier should get 720p URL"""
        config = {'video_quality': '720p'}
        url = build_video_url('video-123', 'intermediate', config)
        assert '720p' in url
    
    def test_build_video_url_advanced_tier(self):
        """Advanced tier should get master playlist"""
        config = {'video_quality': '1080p'}
        url = build_video_url('video-123', 'advanced', config)
        assert 'master' in url or '1080p' in url
    
    def test_download_button_disabled_basic(self, mocker):
        """Download button should be disabled for basic tier"""
        mocker.patch('streamlit.session_state', {'tier': 'basic'})
        config = {'video_download': False}
        
        # Should show upgrade message instead of button
        # (Test would check Streamlit output)
        pass
```

---

## 2. Integration Testing

### API Integration Tests

**File**: `tests/integration/test_coursesgtm_api.py`
```python
import pytest
import requests
from utils.api import validate_license, get_courses, save_progress

class TestCoursesGTMIntegration:
    """Test integration with CoursesGTM API"""
    
    @pytest.fixture
    def api_url(self):
        """API base URL"""
        return "https://staging-api.coursesgtm.com"
    
    def test_license_validation_success(self, api_url):
        """Valid license should return success"""
        response = validate_license("TEST-VALID-KEY-1234-5678")
        
        assert response['success'] == True
        assert 'user_id' in response
        assert 'tier' in response
        assert 'token' in response
    
    def test_license_validation_invalid_key(self, api_url):
        """Invalid license should return 401"""
        with pytest.raises(Exception) as exc:
            validate_license("INVALID-KEY")
        
        assert "Invalid" in str(exc.value)
    
    def test_get_courses_by_tier(self, api_url, mocker):
        """Get courses should filter by tier"""
        mocker.patch('streamlit.session_state', {
            'tier': 'intermediate',
            'token': 'test_token'
        })
        
        courses = get_courses()
        
        assert isinstance(courses, list)
        assert len(courses) > 0
        # Should include intermediate courses, exclude advanced
    
    def test_save_progress_video(self, api_url, mocker):
        """Save video progress should succeed"""
        mocker.patch('streamlit.session_state', {
            'user_id': 'test_user',
            'token': 'test_token'
        })
        
        result = save_progress(
            progress_type='video',
            item_id='v01',
            data={'position_seconds': 540, 'completion_percentage': 45}
        )
        
        assert result == True
```

### SimulationPlayer Integration

**File**: `tests/integration/test_simulation_player.py`
```python
import pytest
from components.lab_launcher import launch_lab
from utils.webhooks import handle_lab_completion

class TestSimulationPlayerIntegration:
    """Test integration with SimulationPlayer"""
    
    def test_lab_launch_generates_session(self, mocker):
        """Launching lab should generate session token"""
        mocker.patch('streamlit.session_state', {
            'user_id': 'test_user',
            'tier': 'intermediate',
            'token': 'test_token'
        })
        
        mock_api = mocker.patch('requests.post')
        mock_api.return_value.status_code = 200
        mock_api.return_value.json.return_value = {
            'session_token': 'session_abc',
            'lab_url': 'https://sim.example.com/lab-01'
        }
        
        launch_lab('ai-01', 'lab-01')
        
        mock_api.assert_called_once()
    
    def test_lab_completion_webhook(self, mocker):
        """Lab completion webhook should update progress"""
        webhook_payload = {
            'session_token': 'session_abc',
            'user_id': 'test_user',
            'course_id': 'ai-01',
            'lab_id': 'lab-01',
            'score': 95,
            'time_spent_seconds': 3600
        }
        
        mock_save = mocker.patch('utils.progress.sync_lab_completion')
        mock_save.return_value = True
        
        result = handle_lab_completion(webhook_payload)
        
        assert result['success'] == True
        mock_save.assert_called_once()
```

---

## 3. UI/E2E Testing

### Streamlit App Testing

**File**: `tests/ui/test_app_flow.py`
```python
import pytest
from streamlit.testing.v1 import AppTest

class TestAppFlow:
    """Test end-to-end user flows"""
    
    def test_login_flow(self):
        """Test complete login flow"""
        at = AppTest.from_file("Home.py")
        at.run()
        
        # Enter license key
        at.text_input[0].input("TEST-VALID-KEY-1234-5678").run()
        
        # Click login
        at.button[0].click().run()
        
        # Should redirect to dashboard
        assert at.session_state['authenticated'] == True
        assert at.session_state['tier'] in ['basic', 'intermediate', 'advanced']
    
    def test_course_selection_flow(self):
        """Test selecting and starting a course"""
        at = AppTest.from_file("pages/2_📚_My_Courses.py")
        
        # Mock authenticated session
        at.session_state['authenticated'] = True
        at.session_state['tier'] = 'intermediate'
        
        at.run()
        
        # Should display courses
        assert len(at.button) > 0
        
        # Click on a course
        at.button[0].click().run()
        
        # Should navigate to course player
        assert 'current_course_id' in at.session_state
    
    def test_video_playback(self):
        """Test video player rendering"""
        at = AppTest.from_file("pages/3_🎓_Course_Player.py")
        
        at.session_state['authenticated'] = True
        at.session_state['tier'] = 'intermediate'
        at.session_state['current_course_id'] = 'ai-01'
        at.session_state['current_video_id'] = 'v01'
        
        at.run()
        
        # Should render video player
        # (Check for video element in output)
        pass
```

### Selenium E2E Tests (Optional)

**File**: `tests/e2e/test_selenium.py`
```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSeleniumE2E:
    """End-to-end tests with Selenium"""
    
    @pytest.fixture
    def driver(self):
        """Setup Chrome driver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()
    
    def test_login_and_navigate(self, driver):
        """Test login and navigation"""
        driver.get("http://localhost:8501")
        
        # Enter license key
        license_input = driver.find_element(By.ID, "license_input")
        license_input.send_keys("TEST-VALID-KEY-1234-5678")
        
        # Click login
        login_button = driver.find_element(By.TEXT, "Login")
        login_button.click()
        
        # Wait for dashboard
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TEXT, "Dashboard"))
        )
        
        assert "Dashboard" in driver.page_source
```

---

## 4. Accessibility Testing

### Automated Accessibility Tests

**File**: `tests/accessibility/test_wcag.py`
```python
import pytest
from axe_selenium_python import Axe

class TestAccessibility:
    """Test WCAG 2.1 AA compliance"""
    
    def test_login_page_accessibility(self, driver):
        """Login page should be accessible"""
        driver.get("http://localhost:8501")
        
        axe = Axe(driver)
        axe.inject()
        
        results = axe.run()
        
        # Should have no violations
        assert len(results["violations"]) == 0
    
    def test_dashboard_accessibility(self, driver):
        """Dashboard should be accessible"""
        # Login first
        login(driver)
        
        driver.get("http://localhost:8501/Dashboard")
        
        axe = Axe(driver)
        axe.inject()
        
        results = axe.run()
        
        # Check for critical violations
        critical = [v for v in results["violations"] if v["impact"] == "critical"]
        assert len(critical) == 0
```

### Manual Accessibility Checklist

**File**: `tests/accessibility/manual_checklist.md`
```markdown
# Manual Accessibility Testing Checklist

## Keyboard Navigation
- [ ] Can navigate entire app with Tab key
- [ ] Focus indicators are visible
- [ ] No keyboard traps
- [ ] Skip navigation links work
- [ ] All buttons/links accessible via keyboard

## Screen Reader (NVDA/VoiceOver)
- [ ] Page titles announced correctly
- [ ] Headings announced in correct order
- [ ] Form labels associated with inputs
- [ ] Error messages announced
- [ ] Dynamic content changes announced

## Visual
- [ ] Color contrast ≥ 4.5:1 for text
- [ ] Text resizable to 200% without breaking
- [ ] High contrast mode works
- [ ] Information not conveyed by color alone

## Video
- [ ] All videos have captions
- [ ] Captions are accurate and synchronized
- [ ] Caption settings work
- [ ] Audio descriptions available (if applicable)

## Forms
- [ ] All inputs have labels
- [ ] Error messages are clear
- [ ] Required fields indicated
- [ ] Validation messages accessible
```

---

## 5. Security Testing

### Authentication Security Tests

**File**: `tests/security/test_auth_security.py`
```python
import pytest
from utils.auth import validate_token, is_token_expired

class TestAuthSecurity:
    """Test authentication security"""
    
    def test_expired_token_rejected(self):
        """Expired tokens should be rejected"""
        expired_token = generate_expired_token()
        assert is_token_expired(expired_token) == True
    
    def test_invalid_token_rejected(self):
        """Invalid tokens should be rejected"""
        invalid_token = "invalid.token.here"
        assert validate_token(invalid_token) == False
    
    def test_sql_injection_prevention(self, mocker):
        """SQL injection attempts should be sanitized"""
        malicious_input = "'; DROP TABLE users; --"
        
        # Should not execute SQL
        with pytest.raises(Exception):
            save_user_data(malicious_input)
    
    def test_xss_prevention(self):
        """XSS attempts should be escaped"""
        malicious_input = "<script>alert('XSS')</script>"
        
        escaped = escape_html(malicious_input)
        assert "<script>" not in escaped
```

### Rate Limiting Tests

**File**: `tests/security/test_rate_limiting.py`
```python
import pytest
from utils.rate_limiter import check_rate_limit

class TestRateLimiting:
    """Test rate limiting"""
    
    def test_login_rate_limit(self):
        """Login should be rate limited"""
        user_ip = "192.168.1.1"
        
        # First 5 attempts should succeed
        for i in range(5):
            assert check_rate_limit('login', user_ip) == True
        
        # 6th attempt should be blocked
        assert check_rate_limit('login', user_ip) == False
```

---

## 6. Performance Testing

### Load Testing

**File**: `tests/performance/locustfile.py`
```python
from locust import HttpUser, task, between

class CoursePlayerUser(HttpUser):
    """Simulate user behavior"""
    wait_time = between(1, 5)
    
    def on_start(self):
        """Login before testing"""
        self.client.post("/api/v1/licenses/validate", json={
            "license_key": "TEST-KEY-1234-5678"
        })
    
    @task(3)
    def view_dashboard(self):
        """View dashboard (common action)"""
        self.client.get("/Dashboard")
    
    @task(2)
    def browse_courses(self):
        """Browse courses"""
        self.client.get("/My_Courses")
    
    @task(1)
    def watch_video(self):
        """Watch video"""
        self.client.get("/Course_Player")
```

**Run Load Test**:
```bash
locust -f tests/performance/locustfile.py --host=http://localhost:8501
```

---

## 7. CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/test.yml`
```yaml
name: Test Suite

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
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: |
        pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Run accessibility tests
      run: |
        npm install -g pa11y-ci
        pa11y-ci --sitemap http://localhost:8501/sitemap.xml
```

---

## 8. Test Coverage Goals

### Coverage Targets

| Component | Target | Current |
|-----------|--------|---------|
| **Feature Gating** | 100% | - |
| **Authentication** | 95% | - |
| **Video Player** | 90% | - |
| **Progress Tracking** | 90% | - |
| **AI Tutor** | 85% | - |
| **Overall** | 80% | - |

### Viewing Coverage Report

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html

# Open report
open htmlcov/index.html
```

---

## 9. Test Data Management

### Test Fixtures

**File**: `tests/conftest.py`
```python
import pytest

@pytest.fixture
def mock_user_basic():
    """Mock basic tier user"""
    return {
        'user_id': 'test_basic_user',
        'email': 'basic@test.com',
        'tier': 'basic',
        'token': 'test_token_basic'
    }

@pytest.fixture
def mock_user_intermediate():
    """Mock intermediate tier user"""
    return {
        'user_id': 'test_int_user',
        'email': 'intermediate@test.com',
        'tier': 'intermediate',
        'token': 'test_token_int'
    }

@pytest.fixture
def mock_user_advanced():
    """Mock advanced tier user"""
    return {
        'user_id': 'test_adv_user',
        'email': 'advanced@test.com',
        'tier': 'advanced',
        'token': 'test_token_adv'
    }

@pytest.fixture
def mock_course_data():
    """Mock course data"""
    return {
        'course_id': 'ai-01',
        'title': 'Introduction to AI',
        'modules': [
            {
                'module_id': 'module-01',
                'videos': [
                    {'video_id': 'v01', 'completion_percentage': 100}
                ],
                'quiz': {'status': 'completed', 'passed': True}
            }
        ]
    }
```

---

## 10. Testing Best Practices

### Dos

✅ Write tests before/during feature development (TDD)
✅ Keep tests isolated and independent
✅ Use descriptive test names
✅ Mock external dependencies (APIs, databases)
✅ Test edge cases and error conditions
✅ Maintain high test coverage (>80%)
✅ Run tests in CI/CD pipeline
✅ Review test failures immediately

### Don'ts

❌ Don't skip writing tests ("I'll add them later")
❌ Don't test implementation details
❌ Don't write flaky tests
❌ Don't ignore failing tests
❌ Don't commit code with failing tests
❌ Don't test third-party libraries
❌ Don't hardcode test data

---

## Conclusion

A comprehensive testing strategy ensures CoursePlayerApp is reliable, accessible, and secure. Continuous testing throughout development and deployment maintains quality and user trust.

**Testing Command Summary**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_feature_gating.py

# Run accessibility tests
pa11y-ci

# Run load tests
locust -f tests/performance/locustfile.py
```

