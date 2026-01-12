# CoursesGTM Testing Strategy

## Overview

This document outlines the testing approach for CoursesGTM to ensure reliability, correctness, and security.

**Coverage Target**: >80%  
**Testing Framework**: pytest  
**CI/CD**: GitHub Actions

---

## Testing Pyramid

```
        /\
       /  \
      / E2E \         10% - End-to-End Tests
     /______\
    /        \
   /Integration\     30% - Integration Tests
  /____________\
 /              \
/   Unit Tests   \   60% - Unit Tests
/________________\
```

### Unit Tests (60%)

**Scope**: Individual functions, methods, and classes in isolation

**Tools**:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `factory_boy` - Test data factories
- `freezegun` - Time mocking

**What to Test**:
- Model methods and properties
- Validator logic
- Service methods with mocked dependencies
- Configuration parsing

### Integration Tests (30%)

**Scope**: Multiple components working together

**Tools**:
- `pytest` - Testing framework
- `pytest-django` / `pytest-flask` - Framework integration
- `TestClient` (FastAPI) - API testing
- SQLite in-memory database

**What to Test**:
- Database queries and relationships
- API endpoints
- Service + database interactions
- Webhook processing

### End-to-End Tests (10%)

**Scope**: Complete user flows

**Tools**:
- `playwright` or `selenium` - Browser automation
- `pytest` - Test runner

**What to Test**:
- Purchase → License → Access flow
- Upgrade flow
- Renewal flow
- Progress tracking flow

---

## Test Organization

### Directory Structure

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_validators.py
│   ├── test_services.py
│   └── test_config_loader.py
├── integration/
│   ├── test_api_curriculum.py
│   ├── test_api_licenses.py
│   ├── test_api_access.py
│   ├── test_api_progress.py
│   └── test_webhooks.py
├── e2e/
│   ├── test_purchase_flow.py
│   ├── test_upgrade_flow.py
│   └── test_course_access_flow.py
├── fixtures/
│   ├── curriculum.json
│   ├── tiers.json
│   └── test_data.py
└── conftest.py
```

---

## Unit Tests

### Model Tests

```python
# tests/unit/test_models.py
import pytest
from datetime import datetime, timedelta
from coursesgtm.models import License, Tier, User

class TestLicense:
    def test_generate_license_key_format(self):
        """License key should match CTMV2-XXXX-XXXX-XXXX-XXXX format"""
        license = License.generate_key()
        assert license.startswith("CTMV2-")
        assert len(license) == 29
        parts = license.split("-")
        assert len(parts) == 5
        assert all(len(part) == 4 for part in parts[1:])
    
    def test_is_active_valid_license(self, valid_license):
        """Active license with future expiry should be active"""
        assert valid_license.is_active() is True
    
    def test_is_active_expired_license(self, expired_license):
        """Expired license should not be active"""
        assert expired_license.is_active() is False
    
    def test_days_remaining(self, valid_license):
        """Should calculate days remaining correctly"""
        valid_license.expires_at = datetime.utcnow() + timedelta(days=30)
        assert valid_license.days_remaining() == 30
    
    def test_days_remaining_expired(self, expired_license):
        """Expired license should have 0 days remaining"""
        assert expired_license.days_remaining() == 0

class TestTier:
    def test_includes_course(self, basic_tier):
        """Should check if tier includes course"""
        assert basic_tier.includes_course("PHIL2026") is True
        assert basic_tier.includes_course("ETHI2026") is False
    
    def test_tier_level_ordering(self, basic_tier, intermediate_tier, advanced_tier):
        """Tier levels should be ordered correctly"""
        assert basic_tier.level < intermediate_tier.level
        assert intermediate_tier.level < advanced_tier.level
```

### Validator Tests

```python
# tests/unit/test_validators.py
import pytest
from coursesgtm.validators import ConfigValidator, LicenseValidator, AccessValidator
from coursesgtm.exceptions import ValidationError

class TestConfigValidator:
    def test_validate_curriculum_valid(self, valid_curriculum_json):
        """Valid curriculum should pass validation"""
        validator = ConfigValidator()
        assert validator.validate_curriculum(valid_curriculum_json) is True
    
    def test_validate_curriculum_missing_required_field(self):
        """Curriculum missing required field should fail"""
        validator = ConfigValidator()
        invalid = {"product_id": "test"}  # Missing curriculum
        with pytest.raises(ValidationError) as exc:
            validator.validate_curriculum(invalid)
        assert "curriculum" in str(exc.value)
    
    def test_validate_prerequisite_chain_valid(self, curriculum_with_prerequisites):
        """Valid prerequisite chain should pass"""
        validator = ConfigValidator()
        assert validator.check_prerequisite_chain(curriculum_with_prerequisites) is True
    
    def test_validate_prerequisite_chain_circular(self, curriculum_with_circular_prereqs):
        """Circular prerequisites should be detected"""
        validator = ConfigValidator()
        with pytest.raises(ValidationError) as exc:
            validator.check_prerequisite_chain(curriculum_with_circular_prereqs)
        assert "circular" in str(exc.value).lower()

class TestLicenseValidator:
    def test_check_license_format_valid(self):
        """Valid license key format should pass"""
        validator = LicenseValidator()
        assert validator.check_format("CTMV2-A1B2-C3D4-E5F6-G7H8") is True
    
    def test_check_license_format_invalid(self):
        """Invalid license key format should fail"""
        validator = LicenseValidator()
        assert validator.check_format("INVALID-KEY") is False
    
    def test_check_expiry_valid(self, valid_license):
        """License with future expiry should pass"""
        validator = LicenseValidator()
        assert validator.check_expiry(valid_license) is True
    
    def test_check_expiry_expired(self, expired_license):
        """Expired license should fail"""
        validator = LicenseValidator()
        assert validator.check_expiry(expired_license) is False

class TestAccessValidator:
    def test_check_course_access_allowed(self, user_with_basic_license, basic_course):
        """User with appropriate license should have access"""
        validator = AccessValidator()
        result = validator.check_course_access(user_with_basic_license.id, basic_course.id)
        assert result['access_granted'] is True
    
    def test_check_course_access_denied(self, user_with_basic_license, advanced_course):
        """User with insufficient license should not have access"""
        validator = AccessValidator()
        result = validator.check_course_access(user_with_basic_license.id, advanced_course.id)
        assert result['access_granted'] is False
        assert result['required_tier']['level'] > 1
```

### Service Tests

```python
# tests/unit/test_services.py
import pytest
from unittest.mock import Mock, patch
from coursesgtm.services import LicenseService, EnrollmentService, ProgressService

class TestLicenseService:
    def test_issue_license_success(self, user, basic_tier, payment):
        """Should create license with valid key"""
        service = LicenseService()
        license = service.issue_license(
            user_id=user.id,
            tier_id=basic_tier.id,
            payment_id=payment.id
        )
        assert license.key.startswith("CTMV2-")
        assert license.status == "active"
        assert license.tier_id == basic_tier.id
    
    def test_issue_license_duplicate_active(self, user_with_active_license, basic_tier, payment):
        """Should not issue license if user has active license"""
        service = LicenseService()
        with pytest.raises(ValidationError) as exc:
            service.issue_license(user_with_active_license.id, basic_tier.id, payment.id)
        assert "active license" in str(exc.value).lower()
    
    def test_upgrade_license_success(self, user_with_basic_license, intermediate_tier, payment):
        """Should upgrade license to higher tier"""
        service = LicenseService()
        result = service.upgrade_license(
            license_key=user_with_basic_license.license.key,
            new_tier_id=intermediate_tier.id,
            payment_id=payment.id
        )
        assert result['new_tier']['level'] == 2
        assert result['old_tier']['level'] == 1
    
    def test_upgrade_license_downgrade_not_allowed(self, user_with_intermediate_license, basic_tier):
        """Should not allow downgrade"""
        service = LicenseService()
        with pytest.raises(ValidationError) as exc:
            service.upgrade_license(
                user_with_intermediate_license.license.key,
                basic_tier.id,
                None
            )
        assert "downgrade" in str(exc.value).lower()

class TestEnrollmentService:
    def test_enroll_user_success(self, user_with_basic_license, basic_course):
        """Should enroll user in accessible course"""
        service = EnrollmentService()
        enrollment = service.enroll_user(user_with_basic_license.id, basic_course.id)
        assert enrollment.user_id == user_with_basic_license.id
        assert enrollment.course_id == basic_course.id
        assert enrollment.status == "active"
    
    def test_sync_enrollments_on_upgrade(self, user_with_basic_license, intermediate_tier):
        """Should auto-enroll in new courses on upgrade"""
        service = EnrollmentService()
        # User upgrades to intermediate
        user_with_basic_license.license.tier = intermediate_tier
        
        # Sync enrollments
        new_enrollments = service.sync_enrollments_with_license(user_with_basic_license.id)
        
        # Should have new courses from intermediate tier
        assert len(new_enrollments) > 0
```

---

## Integration Tests

### API Tests

```python
# tests/integration/test_api_licenses.py
import pytest
from fastapi.testclient import TestClient
from coursesgtm.api import app

@pytest.fixture
def client():
    return TestClient(app)

class TestLicenseAPI:
    def test_issue_license_success(self, client, auth_headers, user, basic_tier, payment):
        """POST /licenses should create license"""
        response = client.post(
            "/api/v1/licenses",
            json={
                "user_id": str(user.id),
                "tier_id": str(basic_tier.id),
                "payment_id": str(payment.id)
            },
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data['success'] is True
        assert data['data']['license']['key'].startswith("CTMV2-")
    
    def test_validate_license_success(self, client, auth_headers, valid_license):
        """GET /licenses/{key} should return license details"""
        response = client.get(
            f"/api/v1/licenses/{valid_license.key}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data['data']['license']['is_valid'] is True
    
    def test_validate_license_not_found(self, client, auth_headers):
        """GET /licenses/{key} should return 404 for invalid key"""
        response = client.get(
            "/api/v1/licenses/CTMV2-INVALID-KEY",
            headers=auth_headers
        )
        assert response.status_code == 404

class TestAccessAPI:
    def test_check_course_access_allowed(self, client, auth_headers, user_with_basic_license, basic_course):
        """POST /access/check-course should return access granted"""
        response = client.post(
            "/api/v1/access/check-course",
            json={
                "user_id": str(user_with_basic_license.id),
                "course_id": str(basic_course.id)
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data['data']['access_granted'] is True
    
    def test_check_course_access_denied(self, client, auth_headers, user_with_basic_license, advanced_course):
        """POST /access/check-course should return access denied"""
        response = client.post(
            "/api/v1/access/check-course",
            json={
                "user_id": str(user_with_basic_license.id),
                "course_id": str(advanced_course.id)
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data['data']['access_granted'] is False
        assert 'required_tier' in data['data']
```

### Webhook Tests

```python
# tests/integration/test_webhooks.py
import pytest
import hmac
import hashlib
from fastapi.testclient import TestClient

class TestLemonSqueezyWebhook:
    def test_webhook_creates_license(self, client, lemonsqueezy_webhook_payload):
        """LemonSqueezy webhook should create license"""
        payload = lemonsqueezy_webhook_payload
        signature = self._generate_signature(payload)
        
        response = client.post(
            "/api/v1/webhooks/lemonsqueezy",
            json=payload,
            headers={"X-Signature": signature}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert 'license_key' in data['data']
    
    def test_webhook_invalid_signature(self, client, lemonsqueezy_webhook_payload):
        """Webhook with invalid signature should be rejected"""
        response = client.post(
            "/api/v1/webhooks/lemonsqueezy",
            json=lemonsqueezy_webhook_payload,
            headers={"X-Signature": "invalid"}
        )
        assert response.status_code == 400
    
    def _generate_signature(self, payload):
        secret = "test_secret"
        return hmac.new(
            secret.encode(),
            json.dumps(payload).encode(),
            hashlib.sha256
        ).hexdigest()
```

---

## End-to-End Tests

### Purchase Flow

```python
# tests/e2e/test_purchase_flow.py
import pytest
from playwright.sync_api import sync_playwright

class TestPurchaseFlow:
    def test_complete_purchase_flow(self, browser):
        """Full flow: Browse → Select tier → Purchase → Access course"""
        page = browser.new_page()
        
        # 1. Browse courses
        page.goto("http://localhost:8000")
        page.click("text=Browse Courses")
        
        # 2. Try to access locked course
        page.click("text=Philosophy of Modern Data Science")
        assert "Upgrade Required" in page.content()
        
        # 3. Select tier
        page.click("text=Upgrade to Basic")
        assert "Basic Tier" in page.content()
        
        # 4. Complete purchase (mock payment)
        page.fill("#email", "test@example.com")
        page.click("#purchase-button")
        
        # 5. Verify license received
        page.wait_for_selector("text=License Key:")
        license_key = page.locator(".license-key").inner_text()
        assert license_key.startswith("CTMV2-")
        
        # 6. Access course
        page.goto("http://localhost:8000/courses/PHIL2026")
        assert "Welcome to the course" in page.content()
        assert "Upgrade Required" not in page.content()
```

---

## Test Fixtures

### Conftest.py

```python
# tests/conftest.py
import pytest
from datetime import datetime, timedelta
from coursesgtm.models import User, License, Tier, Course, Track, Product
from coursesgtm.database import init_db, Session

@pytest.fixture(scope="session")
def db():
    """Initialize test database"""
    init_db("sqlite:///:memory:")
    yield
    # Cleanup handled by in-memory database

@pytest.fixture
def session(db):
    """Create database session for test"""
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def user(session):
    """Create test user"""
    user = User(
        email="test@example.com",
        name="Test User"
    )
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def basic_tier(session):
    """Create basic tier"""
    tier = Tier(
        name="Basic",
        level=1,
        pricing_config={"one_time": 99, "expiry_months": 12},
        access_config={
            "courses": {"included": ["PHIL2026", "TOOL2026", "DENG2026", "SLML2026", "DEEP2026"]}
        }
    )
    session.add(tier)
    session.commit()
    return tier

@pytest.fixture
def valid_license(session, user, basic_tier):
    """Create active license"""
    license = License(
        key=License.generate_key(),
        user_id=user.id,
        tier_id=basic_tier.id,
        status="active",
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=365)
    )
    session.add(license)
    session.commit()
    return license

@pytest.fixture
def expired_license(session, user, basic_tier):
    """Create expired license"""
    license = License(
        key=License.generate_key(),
        user_id=user.id,
        tier_id=basic_tier.id,
        status="expired",
        issued_at=datetime.utcnow() - timedelta(days=400),
        expires_at=datetime.utcnow() - timedelta(days=35)
    )
    session.add(license)
    session.commit()
    return license
```

---

## Performance Tests

### Load Testing

```python
# tests/performance/test_load.py
import pytest
from locust import HttpUser, task, between

class CoursesGTMUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def validate_license(self):
        """Most common operation"""
        self.client.get(
            f"/api/v1/licenses/{self.license_key}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    @task(1)
    def check_course_access(self):
        """Check course access"""
        self.client.post(
            "/api/v1/access/check-course",
            json={"user_id": self.user_id, "course_id": self.course_id},
            headers={"Authorization": f"Bearer {self.token}"}
        )
    
    def on_start(self):
        """Setup test user"""
        self.token = "test_token"
        self.user_id = "test_user"
        self.license_key = "CTMV2-TEST-TEST-TEST-TEST"
        self.course_id = "test_course"
```

**Run Load Test**:
```bash
locust -f tests/performance/test_load.py --host=http://localhost:8000
```

**Performance Targets**:
- License validation: p95 < 100ms
- Course access check: p95 < 100ms
- Throughput: 100 requests/second
- Concurrent users: 1000

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run unit tests
        run: pytest tests/unit --cov=coursesgtm --cov-report=xml
      
      - name: Run integration tests
        run: pytest tests/integration
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
      
      - name: Check coverage threshold
        run: |
          coverage report --fail-under=80
```

---

## Test Data Management

### Factory Boy

```python
# tests/factories.py
import factory
from coursesgtm.models import User, License, Tier, Course

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    name = factory.Faker('name')

class TierFactory(factory.Factory):
    class Meta:
        model = Tier
    
    name = factory.Iterator(["Basic", "Intermediate", "Advanced"])
    level = factory.Sequence(lambda n: n + 1)
    pricing_config = {"one_time": 99, "expiry_months": 12}
    access_config = {"courses": {"included": []}}

class LicenseFactory(factory.Factory):
    class Meta:
        model = License
    
    key = factory.LazyFunction(License.generate_key)
    user = factory.SubFactory(UserFactory)
    tier = factory.SubFactory(TierFactory)
    status = "active"
    issued_at = factory.LazyFunction(datetime.utcnow)
    expires_at = factory.LazyFunction(
        lambda: datetime.utcnow() + timedelta(days=365)
    )
```

---

## Coverage Reporting

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=coursesgtm --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Coverage Targets

- **Overall**: >80%
- **Models**: >90%
- **Services**: >85%
- **Validators**: >95%
- **API**: >75%

---

## Related Documentation

- [Architecture Overview](./ARCHITECTURE.md)
- [Implementation Roadmap](./ROADMAP.md)
- [API Specification](./API_SPEC.md)
