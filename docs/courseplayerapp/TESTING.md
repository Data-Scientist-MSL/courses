# CoursePlayerApp - Testing Strategy

## Overview

This document outlines the comprehensive testing strategy for CoursePlayerApp, covering unit tests, integration tests, end-to-end tests, visual regression tests, and performance tests.

## Testing Philosophy

CoursePlayerApp follows a **test pyramid** approach:

```
        /\
       /E2E\          <- Fewer, high-value
      /______\
     /Visual  \       <- Critical UI paths
    /__________\
   /Integration\      <- External services
  /______________\
 /   Unit Tests   \   <- Most tests here
/__________________\
```

**Principles**:
- **Fast Feedback**: Unit tests run in < 1 second
- **Isolation**: Tests don't depend on each other
- **Deterministic**: Same input = same output
- **Comprehensive**: >80% code coverage target
- **Maintainable**: Clear, readable test code

## Test Coverage Target

| Layer | Coverage Target | Test Count Estimate |
|-------|----------------|---------------------|
| Unit Tests | >85% | ~500 tests |
| Integration Tests | >70% | ~100 tests |
| E2E Tests | Critical paths | ~50 tests |
| Visual Regression | All components | ~30 snapshots |
| Performance Tests | Key endpoints | ~20 tests |

## Unit Tests

### Framework

**Tools**:
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking support
- `pytest-asyncio` - Async test support

**Configuration**: `pytest.ini`

```ini
[pytest]
testpaths = tests/unit
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=courseplayerapp
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    -v
    -s
asyncio_mode = auto
```

### Component Unit Tests

**File**: `tests/unit/test_video_player.py`

```python
import pytest
from unittest.mock import Mock, patch
from courseplayerapp.components import VideoPlayer

class TestVideoPlayer:
    """Unit tests for VideoPlayer component"""
    
    @pytest.fixture
    def mock_gtm_client(self):
        """Mock CoursesGTM client"""
        with patch('courseplayerapp.components.CoursesGTMClient') as mock:
            mock_instance = Mock()
            mock.get_instance.return_value = mock_instance
            yield mock_instance
    
    def test_basic_tier_no_download(self, mock_gtm_client):
        """Basic tier should not have download button"""
        mock_gtm_client.get_user_tier.return_value = 'basic'
        mock_gtm_client.can_use_feature.return_value = False
        
        player = VideoPlayer('course-1', 'video-1')
        
        # Verify download feature is not available
        assert not player._has_feature('video_download')
    
    def test_intermediate_tier_has_download(self, mock_gtm_client):
        """Intermediate tier should have download button"""
        mock_gtm_client.get_user_tier.return_value = 'intermediate'
        mock_gtm_client.can_use_feature.return_value = True
        
        player = VideoPlayer('course-1', 'video-1')
        
        # Verify download feature is available
        assert player._has_feature('video_download')
    
    def test_get_max_quality_by_tier(self, mock_gtm_client):
        """Test max quality based on tier"""
        player = VideoPlayer('course-1', 'video-1')
        
        assert player._get_max_quality('basic') == '720p'
        assert player._get_max_quality('intermediate') == '1080p'
        assert player._get_max_quality('advanced') == '4k'
    
    @pytest.mark.asyncio
    async def test_stream_url_generation(self, mock_gtm_client):
        """Test HLS stream URL generation"""
        mock_gtm_client.get_user_tier.return_value = 'intermediate'
        
        player = VideoPlayer('course-1', 'video-1')
        url = player._get_stream_url()
        
        assert 'video-1' in url
        assert '1080p' in url
        assert url.endswith('.m3u8')
```

**File**: `tests/unit/test_ai_tutor.py`

```python
import pytest
from unittest.mock import Mock, patch, AsyncMock
from courseplayerapp.components import AITutorChat

class TestAITutor:
    """Unit tests for AI Tutor component"""
    
    @pytest.fixture
    def mock_gtm_client(self):
        with patch('courseplayerapp.components.CoursesGTMClient') as mock:
            mock_instance = Mock()
            mock.get_instance.return_value = mock_instance
            yield mock_instance
    
    @pytest.fixture
    def mock_ollama_client(self):
        with patch('courseplayerapp.components.OLLAMAClient') as mock:
            yield mock
    
    def test_basic_tier_no_access(self, mock_gtm_client):
        """Basic tier should not have AI tutor access"""
        mock_gtm_client.get_user_tier.return_value = 'basic'
        mock_gtm_client.can_use_feature.return_value = False
        
        tutor = AITutorChat('course-1')
        
        assert not tutor._has_feature('ai_tutor')
    
    def test_intermediate_quota_check(self, mock_gtm_client):
        """Intermediate tier should enforce 50 question quota"""
        mock_gtm_client.get_user_tier.return_value = 'intermediate'
        mock_gtm_client.get_feature_usage.return_value = 45
        
        tutor = AITutorChat('course-1')
        
        assert tutor._check_quota() == True
        assert tutor._get_remaining_quota() == 5
    
    def test_intermediate_quota_exceeded(self, mock_gtm_client):
        """Test quota exceeded for intermediate tier"""
        mock_gtm_client.get_user_tier.return_value = 'intermediate'
        mock_gtm_client.get_feature_usage.return_value = 50
        
        tutor = AITutorChat('course-1')
        
        assert tutor._check_quota() == False
    
    def test_advanced_unlimited_quota(self, mock_gtm_client):
        """Advanced tier should have unlimited quota"""
        mock_gtm_client.get_user_tier.return_value = 'advanced'
        
        tutor = AITutorChat('course-1')
        
        assert tutor._check_quota() == True
        assert tutor._get_remaining_quota() == 'unlimited'
    
    @pytest.mark.asyncio
    async def test_query_tracks_usage(self, mock_gtm_client, mock_ollama_client):
        """Test that queries track usage"""
        mock_gtm_client.get_user_tier.return_value = 'intermediate'
        mock_gtm_client.get_feature_usage.return_value = 25
        mock_ollama_client.query.return_value = AsyncMock(return_value="Answer")
        
        tutor = AITutorChat('course-1')
        await tutor._handle_message("What is pandas?")
        
        # Verify usage was tracked
        mock_gtm_client.increment_feature_usage.assert_called_once_with('ai_tutor_quota')
```

### Feature Gate Unit Tests

**File**: `tests/unit/test_feature_gates.py`

```python
import pytest
from unittest.mock import Mock, patch
from courseplayerapp.feature_gates import (
    FeatureGate,
    requires_feature,
    requires_tier,
    quota_limited,
    FeatureNotAvailableError,
    QuotaExceededError
)

class TestFeatureGate:
    """Unit tests for feature gating system"""
    
    @pytest.fixture
    def feature_gate(self):
        return FeatureGate()
    
    @pytest.fixture
    def mock_gtm(self):
        with patch('courseplayerapp.feature_gates.CoursesGTMClient') as mock:
            yield mock.get_instance.return_value
    
    def test_can_use_feature_basic_tier(self, feature_gate, mock_gtm):
        """Test basic tier feature access"""
        mock_gtm.get_user_tier.return_value = 'basic'
        
        # Basic tier can stream videos
        assert feature_gate.can_use_feature('video_streaming') == True
        
        # Basic tier cannot download videos
        assert feature_gate.can_use_feature('video_download') == False
    
    def test_can_use_feature_intermediate_tier(self, feature_gate, mock_gtm):
        """Test intermediate tier feature access"""
        mock_gtm.get_user_tier.return_value = 'intermediate'
        
        # Can download videos
        assert feature_gate.can_use_feature('video_download') == True
        
        # Can use AI tutor
        assert feature_gate.can_use_feature('ai_tutor') == True
        
        # Cannot use GPU notebooks
        assert feature_gate.can_use_feature('notebook_gpu') == False
    
    def test_requires_feature_decorator(self, mock_gtm):
        """Test @requires_feature decorator"""
        mock_gtm.can_use_feature.return_value = False
        
        @requires_feature('video_download')
        def download_video():
            return "downloaded"
        
        with pytest.raises(FeatureNotAvailableError) as exc_info:
            download_video()
        
        assert 'video_download' in str(exc_info.value)
    
    def test_requires_tier_decorator(self, mock_gtm):
        """Test @requires_tier decorator"""
        mock_gtm.get_user_tier.return_value = 'basic'
        
        @requires_tier('intermediate')
        def advanced_feature():
            return "success"
        
        with pytest.raises(InsufficientTierError):
            advanced_feature()
    
    def test_quota_limited_decorator(self, mock_gtm):
        """Test @quota_limited decorator"""
        mock_gtm.get_user_tier.return_value = 'intermediate'
        mock_gtm.get_feature_usage.return_value = 50  # Quota exceeded
        
        @quota_limited('ai_tutor_quota')
        def ask_question():
            return "answer"
        
        with pytest.raises(QuotaExceededError) as exc_info:
            ask_question()
        
        assert exc_info.value.limit == 50
```

### Running Unit Tests

```bash
# Run all unit tests
pytest tests/unit/

# Run specific test file
pytest tests/unit/test_video_player.py

# Run with coverage
pytest tests/unit/ --cov=courseplayerapp --cov-report=html

# Run tests matching pattern
pytest tests/unit/ -k "test_quota"

# Run in parallel
pytest tests/unit/ -n auto
```

## Integration Tests

### Framework

**Tools**:
- `pytest` - Test framework
- `pytest-docker` - Docker container management
- `httpx` - HTTP client for API testing
- `testcontainers` - Ephemeral test containers

### CoursesGTM Integration Tests

**File**: `tests/integration/test_coursesgtm_integration.py`

```python
import pytest
import os
from courseplayerapp.integrations import CoursesGTMClient

@pytest.mark.integration
class TestCoursesGTMIntegration:
    """Integration tests with CoursesGTM API"""
    
    @pytest.fixture(scope='class')
    def gtm_client(self):
        """Initialize GTM client with test credentials"""
        client = CoursesGTMClient.initialize(
            api_key=os.getenv('TEST_COURSESGTM_API_KEY'),
            api_endpoint=os.getenv('TEST_COURSESGTM_ENDPOINT')
        )
        yield client
        client.close()
    
    def test_validate_license(self, gtm_client):
        """Test license validation"""
        result = gtm_client.validate_license('TEST-LICENSE-KEY')
        
        assert result['valid'] == True
        assert 'tier' in result
        assert 'expires_at' in result
    
    def test_get_user_tier(self, gtm_client):
        """Test fetching user tier"""
        tier = gtm_client.get_user_tier('test-user-id')
        
        assert tier in ['basic', 'intermediate', 'advanced', 'enterprise']
    
    def test_can_access_course(self, gtm_client):
        """Test course access check"""
        result = gtm_client.can_access_course(
            course_id='data-science-101',
            user_id='test-user-id'
        )
        
        assert 'allowed' in result
        assert isinstance(result['allowed'], bool)
    
    def test_track_progress(self, gtm_client):
        """Test progress tracking"""
        response = gtm_client.track_progress(
            user_id='test-user-id',
            course_id='data-science-101',
            lesson_id='intro',
            status='completed'
        )
        
        assert response['status'] == 'success'
```

### OLLAMA Integration Tests

**File**: `tests/integration/test_ollama_integration.py`

```python
import pytest
from testcontainers.core.container import DockerContainer
from courseplayerapp.integrations import OLLAMAClient

@pytest.mark.integration
class TestOLLAMAIntegration:
    """Integration tests with OLLAMA service"""
    
    @pytest.fixture(scope='class')
    def ollama_container(self):
        """Start OLLAMA container for testing"""
        container = DockerContainer('ollama/ollama:latest')
        container.with_exposed_ports(11434)
        container.start()
        
        yield container
        
        container.stop()
    
    @pytest.fixture
    def ollama_client(self, ollama_container):
        """Initialize OLLAMA client"""
        port = ollama_container.get_exposed_port(11434)
        return OLLAMAClient(base_url=f"http://localhost:{port}")
    
    def test_query_model(self, ollama_client):
        """Test querying OLLAMA model"""
        response = ollama_client.query(
            prompt="What is 2+2?",
            model="llama3.2:3b"
        )
        
        assert response is not None
        assert len(response) > 0
    
    def test_streaming_response(self, ollama_client):
        """Test streaming response"""
        chunks = []
        for chunk in ollama_client.query(
            prompt="Count to 5",
            model="llama3.2:3b",
            stream=True
        ):
            chunks.append(chunk)
        
        assert len(chunks) > 0
```

### Running Integration Tests

```bash
# Run integration tests (requires test services)
pytest tests/integration/ -m integration

# Run with Docker containers
docker-compose -f docker-compose.test.yml up -d
pytest tests/integration/
docker-compose -f docker-compose.test.yml down
```

## End-to-End Tests

### Framework

**Tools**:
- `playwright` - Browser automation
- `pytest-playwright` - Pytest integration

**Configuration**: `pytest.ini`

```ini
[pytest]
markers =
    e2e: End-to-end tests (run with --e2e)
```

### E2E Test Examples

**File**: `tests/e2e/test_user_flows.py`

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.e2e
class TestUserFlows:
    """End-to-end user flow tests"""
    
    def test_basic_tier_user_flow(self, page: Page):
        """Test complete flow for Basic tier user"""
        # Navigate to app
        page.goto("http://localhost:8501")
        
        # Enter license key
        page.fill('input[type="password"]', 'BASIC-TEST-LICENSE')
        page.click('button:has-text("Validate License")')
        
        # Verify tier badge
        expect(page.locator('text=Foundation Builder')).to_be_visible()
        
        # Navigate to course
        page.click('text=Data Science 101')
        
        # Start video
        page.click('text=Watch Video')
        
        # Verify download button is disabled
        download_btn = page.locator('button:has-text("Download")')
        expect(download_btn).to_be_disabled()
        
        # Verify upgrade prompt
        expect(page.locator('text=Upgrade to Intermediate')).to_be_visible()
    
    def test_intermediate_tier_ai_tutor(self, page: Page):
        """Test AI Tutor for Intermediate tier"""
        # Login as intermediate user
        login_as_tier(page, 'intermediate')
        
        # Navigate to AI Tutor
        page.click('text=AI Tutor')
        
        # Verify quota display
        expect(page.locator('text=Questions remaining:')).to_be_visible()
        
        # Ask question
        page.fill('input[placeholder="Ask a question..."]', 'What is pandas?')
        page.click('button:has-text("Send")')
        
        # Verify response appears
        expect(page.locator('.ai-response')).to_be_visible(timeout=10000)
        
        # Verify quota decremented
        expect(page.locator('text=49/50')).to_be_visible()
    
    def test_upgrade_flow(self, page: Page):
        """Test upgrade from Basic to Intermediate"""
        # Login as basic user
        login_as_tier(page, 'basic')
        
        # Click upgrade on locked feature
        page.click('button:has-text("Upgrade to Intermediate")')
        
        # Verify pricing page
        expect(page.locator('text=$247/year')).to_be_visible()
        
        # Click upgrade button
        page.click('button:has-text("Upgrade Now")')
        
        # Verify redirect to payment (or mock)
        expect(page.url).to_contain('checkout')

def login_as_tier(page: Page, tier: str):
    """Helper to login as specific tier"""
    licenses = {
        'basic': 'BASIC-TEST-KEY',
        'intermediate': 'INT-TEST-KEY',
        'advanced': 'ADV-TEST-KEY'
    }
    
    page.goto("http://localhost:8501")
    page.fill('input[type="password"]', licenses[tier])
    page.click('button:has-text("Validate License")')
    page.wait_for_load_state('networkidle')
```

### Running E2E Tests

```bash
# Install Playwright browsers
playwright install

# Run E2E tests
pytest tests/e2e/ --e2e

# Run with headed browser (see what's happening)
pytest tests/e2e/ --e2e --headed

# Run specific browser
pytest tests/e2e/ --e2e --browser chromium

# Record test
playwright codegen http://localhost:8501
```

## Visual Regression Tests

### Framework

**Tools**:
- `playwright` - Screenshots
- `pytest-playwright` - Integration
- `pixelmatch` - Image comparison

### Visual Test Examples

**File**: `tests/visual/test_component_snapshots.py`

```python
import pytest
from playwright.sync_api import Page

@pytest.mark.visual
class TestComponentSnapshots:
    """Visual regression tests for components"""
    
    def test_video_player_basic_tier(self, page: Page):
        """Snapshot video player for basic tier"""
        login_as_tier(page, 'basic')
        page.goto("http://localhost:8501/Learn")
        
        # Take screenshot
        page.screenshot(path='tests/visual/snapshots/video-player-basic.png')
        
        # Compare with baseline
        assert_screenshot_matches(
            'tests/visual/snapshots/video-player-basic.png',
            'tests/visual/baselines/video-player-basic.png'
        )
    
    def test_ai_tutor_interface(self, page: Page):
        """Snapshot AI tutor chat interface"""
        login_as_tier(page, 'intermediate')
        page.goto("http://localhost:8501/AI_Tutor")
        
        # Take full page screenshot
        page.screenshot(
            path='tests/visual/snapshots/ai-tutor.png',
            full_page=True
        )
        
        assert_screenshot_matches(
            'tests/visual/snapshots/ai-tutor.png',
            'tests/visual/baselines/ai-tutor.png',
            threshold=0.01  # 1% difference allowed
        )
```

### Running Visual Tests

```bash
# Update baselines
pytest tests/visual/ --update-baselines

# Run visual tests
pytest tests/visual/ -m visual

# View diff on failure
open tests/visual/diffs/video-player-basic-diff.png
```

## Performance Tests

### Framework

**Tools**:
- `locust` - Load testing
- `pytest-benchmark` - Micro-benchmarks

### Performance Test Examples

**File**: `tests/performance/test_load.py`

```python
from locust import HttpUser, task, between

class CoursePlayerUser(HttpUser):
    """Simulated user for load testing"""
    wait_time = between(1, 5)
    
    def on_start(self):
        """Login on start"""
        self.client.post("/validate", {
            "license_key": "TEST-KEY"
        })
    
    @task(3)
    def view_course(self):
        """View course page"""
        self.client.get("/course/data-science-101")
    
    @task(1)
    def watch_video(self):
        """Watch video"""
        self.client.get("/video/stream/intro-to-pandas")
    
    @task(2)
    def ask_ai_tutor(self):
        """Ask AI tutor question"""
        self.client.post("/ai-tutor/query", {
            "question": "What is pandas?",
            "course_id": "data-science-101"
        })
```

**File**: `tests/performance/test_benchmarks.py`

```python
import pytest
from courseplayerapp.components import VideoPlayer

def test_video_player_render_performance(benchmark):
    """Benchmark video player rendering"""
    player = VideoPlayer('course-1', 'video-1')
    
    # Benchmark render time
    result = benchmark(player.render)
    
    # Assert render time < 100ms
    assert benchmark.stats['mean'] < 0.1
```

### Running Performance Tests

```bash
# Run load test
locust -f tests/performance/test_load.py --host http://localhost:8501

# Run benchmarks
pytest tests/performance/test_benchmarks.py --benchmark-only

# Generate performance report
pytest tests/performance/ --benchmark-autosave
```

## Test Data Management

### Fixtures

**File**: `tests/conftest.py`

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_license_basic():
    """Mock basic tier license"""
    return {
        'valid': True,
        'tier': 'basic',
        'expires_at': '2026-12-31',
        'user_id': 'test-user-basic'
    }

@pytest.fixture
def mock_license_advanced():
    """Mock advanced tier license"""
    return {
        'valid': True,
        'tier': 'advanced',
        'expires_at': '2026-12-31',
        'user_id': 'test-user-advanced'
    }

@pytest.fixture
def sample_course():
    """Sample course data"""
    return {
        'id': 'data-science-101',
        'title': 'Data Science 101',
        'lessons': [
            {'id': 'intro', 'title': 'Introduction'},
            {'id': 'pandas', 'title': 'Pandas Basics'}
        ]
    }
```

## CI/CD Integration

### GitHub Actions

**File**: `.github/workflows/test.yml`

```yaml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run unit tests
        run: pytest tests/unit/ --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  integration-tests:
    runs-on: ubuntu-latest
    services:
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Run integration tests
        run: pytest tests/integration/ -m integration
  
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Playwright
        run: |
          pip install playwright
          playwright install
      - name: Start app
        run: |
          docker-compose up -d
          sleep 10
      - name: Run E2E tests
        run: pytest tests/e2e/ --e2e
      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-screenshots
          path: tests/e2e/screenshots/
```

## Test Reporting

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=courseplayerapp --cov-report=html

# Open report
open htmlcov/index.html
```

### Test Metrics

- **Code Coverage**: >80% required
- **Test Execution Time**: Unit tests < 30s, Integration < 2min
- **Flaky Test Rate**: < 1%
- **Test Maintenance**: Tests updated with code changes

## Related Documentation

- [Architecture](./ARCHITECTURE.md)
- [Components](./COMPONENTS.md)
- [Feature Gates](./FEATURE_GATES.md)
- [Deployment Guide](./DEPLOYMENT.md)
