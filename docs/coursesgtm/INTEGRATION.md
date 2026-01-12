# CoursesGTM Integration Guide

## Overview

This guide explains how to integrate CoursesGTM with various frameworks and services. CoursesGTM can be used as an embedded Python library or consumed via REST API.

---

## Integration Patterns

### Pattern 1: Embedded Library (Recommended for Python Apps)

Import CoursesGTM as a Python package and use it directly.

**Pros**: No network latency, simpler deployment  
**Cons**: Requires Python, tight coupling

### Pattern 2: REST API Client

Call CoursesGTM API endpoints from any language.

**Pros**: Language-agnostic, service isolation  
**Cons**: Network latency, additional infrastructure

---

## Streamlit Integration

### Installation

```bash
pip install coursesgtm streamlit
```

### Basic Usage

```python
import streamlit as st
from coursesgtm import check_course_access, get_user_license

# Check if user has access to course
def require_course_access(course_code):
    """Decorator to protect course pages"""
    user_id = st.session_state.get('user_id')
    
    if not user_id:
        st.error("Please log in to access this course")
        st.stop()
    
    access = check_course_access(user_id, course_code)
    
    if not access['access_granted']:
        st.warning(f"⚠️ {access['reason']}")
        st.markdown(f"[Upgrade to {access['required_tier']['name']}]({access['upgrade_url']})")
        st.stop()
    
    return access

# Example course page
def philosophy_course():
    st.title("Philosophy of Modern Data Science")
    
    # Check access
    access = require_course_access("PHIL2026")
    
    # Show course content
    st.markdown("## Welcome to the course!")
    st.video("https://example.com/intro.mp4")
    
    # Track progress
    if st.button("Mark Lesson 1 Complete"):
        from coursesgtm import mark_lesson_complete
        mark_lesson_complete(
            st.session_state.user_id,
            "PHIL2026",
            "lesson-1"
        )
        st.success("✅ Lesson marked complete!")

if __name__ == "__main__":
    philosophy_course()
```

### User Dashboard

```python
import streamlit as st
from coursesgtm import get_user_progress, get_user_license, get_user_achievements

def user_dashboard():
    st.title("My Learning Dashboard")
    
    user_id = st.session_state.user_id
    
    # License info
    license = get_user_license(user_id)
    st.subheader(f"Your Plan: {license['tier']['name']}")
    st.metric("Days Remaining", license['days_remaining'])
    
    if license['days_remaining'] < 30:
        st.warning("Your license expires soon! [Renew now](/renew)")
    
    # Progress
    progress = get_user_progress(user_id)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Courses Completed", progress['summary']['completed_courses'])
    col2.metric("In Progress", progress['summary']['in_progress_courses'])
    col3.metric("Overall Progress", f"{progress['summary']['overall_completion']}%")
    
    # Course list
    st.subheader("Your Courses")
    for course_progress in progress['progress']:
        course = course_progress['course']
        with st.expander(f"{course['code']}: {course['title']}"):
            st.progress(course_progress['completion_percentage'] / 100)
            st.write(f"Completion: {course_progress['completion_percentage']}%")
            if st.button(f"Continue", key=course['code']):
                st.switch_page(f"courses/{course['code']}.py")
    
    # Achievements
    achievements = get_user_achievements(user_id)
    st.subheader("🏆 Achievements")
    for ach in achievements['achievements']:
        st.markdown(f"**{ach['icon']} {ach['name']}** - {ach['description']}")
```

### Upgrade Flow

```python
import streamlit as st
from coursesgtm import get_tiers, calculate_upgrade_price

def upgrade_page():
    st.title("Upgrade Your Plan")
    
    user_id = st.session_state.user_id
    current_license = get_user_license(user_id)
    current_tier = current_license['tier']
    
    # Get available tiers
    tiers = get_tiers()
    
    for tier in tiers:
        if tier['level'] <= current_tier['level']:
            continue  # Skip current and lower tiers
        
        with st.container(border=True):
            st.subheader(tier['name'])
            st.write(tier['description'])
            
            # Show what's included
            st.write("**Includes:**")
            for course_code in tier['access']['courses']['included']:
                st.write(f"✓ {course_code}")
            
            # Show features
            st.write("**Features:**")
            for feature, enabled in tier['access']['features'].items():
                if enabled:
                    st.write(f"✓ {feature.replace('_', ' ').title()}")
            
            # Pricing
            upgrade_price = calculate_upgrade_price(
                current_tier['id'],
                tier['id']
            )
            
            col1, col2 = st.columns([3, 1])
            col1.write(f"**Upgrade Price:** ${upgrade_price['price']}")
            col1.caption(f"Prorated credit: ${upgrade_price['credit']}")
            
            if col2.button("Upgrade", key=tier['id']):
                # Redirect to payment
                st.session_state.upgrade_tier = tier['id']
                st.switch_page("payment.py")
```

---

## Django Integration

### Installation

```bash
pip install coursesgtm django
```

### Middleware

```python
# middleware.py
from coursesgtm import validate_license, check_course_access

class CoursesGTMLicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip for public pages
        if request.path.startswith('/public/'):
            return self.get_response(request)
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Validate license
            license = validate_license(request.user.id)
            request.license = license
            
            # Add to request context
            if license and license['is_valid']:
                request.has_active_license = True
                request.user_tier = license['tier']
            else:
                request.has_active_license = False
        
        return self.get_response(request)

# settings.py
MIDDLEWARE = [
    # ... other middleware
    'myapp.middleware.CoursesGTMLicenseMiddleware',
]
```

### View Decorator

```python
# decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from coursesgtm import check_course_access

def require_course_access(course_code):
    """Decorator to protect course views"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this course")
                return redirect('login')
            
            access = check_course_access(request.user.id, course_code)
            
            if not access['access_granted']:
                messages.warning(request, access['reason'])
                return redirect('upgrade')
            
            # Add access info to request
            request.course_access = access
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator

# views.py
from django.shortcuts import render
from .decorators import require_course_access

@require_course_access("PHIL2026")
def philosophy_course(request):
    return render(request, 'courses/philosophy.html', {
        'course_code': 'PHIL2026',
        'course_title': 'Philosophy of Modern Data Science'
    })
```

### Template Context Processor

```python
# context_processors.py
from coursesgtm import get_user_license, get_user_progress

def coursesgtm_context(request):
    """Add license and progress to all templates"""
    if not request.user.is_authenticated:
        return {}
    
    license = get_user_license(request.user.id)
    progress = get_user_progress(request.user.id)
    
    return {
        'user_license': license,
        'user_progress': progress,
        'days_remaining': license.get('days_remaining', 0) if license else 0,
    }

# settings.py
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... other processors
                'myapp.context_processors.coursesgtm_context',
            ],
        },
    },
]
```

### Template Usage

```django
<!-- base.html -->
{% if user_license %}
  <div class="license-status">
    <span>{{ user_license.tier.name }} Plan</span>
    {% if days_remaining < 30 %}
      <a href="{% url 'renew' %}" class="btn-warning">Renew ({{ days_remaining }} days left)</a>
    {% endif %}
  </div>
{% else %}
  <a href="{% url 'purchase' %}" class="btn-primary">Get Started</a>
{% endif %}

<!-- course_list.html -->
{% for course in courses %}
  <div class="course-card">
    <h3>{{ course.title }}</h3>
    {% if course.code in user_license.tier.access.courses.included %}
      <a href="{% url 'course' course.code %}" class="btn-primary">Start Course</a>
    {% else %}
      <button class="btn-disabled" disabled>🔒 Requires {{ course.tier_access|title }}</button>
      <a href="{% url 'upgrade' %}">Upgrade</a>
    {% endif %}
  </div>
{% endfor %}
```

---

## Flask Integration

### Installation

```bash
pip install coursesgtm flask
```

### Flask Extension

```python
# coursesgtm_flask.py
from flask import g, redirect, url_for, flash
from functools import wraps
from coursesgtm import get_user_license, check_course_access

class CoursesGTM:
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        app.before_request(self._load_license)
        app.context_processor(self._context_processor)
    
    def _load_license(self):
        """Load user license before each request"""
        if hasattr(g, 'user') and g.user:
            g.license = get_user_license(g.user.id)
        else:
            g.license = None
    
    def _context_processor(self):
        """Add license to template context"""
        return {'user_license': g.get('license')}

def require_course_access(course_code):
    """Decorator to protect course routes"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not hasattr(g, 'user') or not g.user:
                flash("Please log in to access this course", "error")
                return redirect(url_for('login'))
            
            access = check_course_access(g.user.id, course_code)
            
            if not access['access_granted']:
                flash(access['reason'], "warning")
                return redirect(url_for('upgrade'))
            
            g.course_access = access
            return f(*args, **kwargs)
        
        return wrapper
    return decorator

# app.py
from flask import Flask
from coursesgtm_flask import CoursesGTM, require_course_access

app = Flask(__name__)
coursesgtm = CoursesGTM(app)

@app.route('/courses/PHIL2026')
@require_course_access('PHIL2026')
def philosophy_course():
    return render_template('courses/philosophy.html')
```

---

## FastAPI Integration

### Installation

```bash
pip install coursesgtm fastapi
```

### Dependency Injection

```python
from fastapi import FastAPI, Depends, HTTPException, status
from coursesgtm import get_user_license, check_course_access

app = FastAPI()

# Dependency to get current user (assumes JWT auth)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Decode JWT and return user
    user = decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user

# Dependency to check license
async def require_active_license(user = Depends(get_current_user)):
    license = get_user_license(user.id)
    if not license or not license['is_valid']:
        raise HTTPException(status_code=403, detail="No active license")
    return license

# Dependency to check course access
def require_course_access(course_code: str):
    async def _check_access(user = Depends(get_current_user)):
        access = check_course_access(user.id, course_code)
        if not access['access_granted']:
            raise HTTPException(
                status_code=403,
                detail=access['reason']
            )
        return access
    return _check_access

# Protected endpoint
@app.get("/courses/{course_code}")
async def get_course(
    course_code: str,
    access = Depends(require_course_access("PHIL2026"))
):
    return {
        "course_code": course_code,
        "access": access
    }
```

---

## Payment Provider Integration

### LemonSqueezy Webhook

```python
# webhook_handler.py
from fastapi import FastAPI, Request, HTTPException
from coursesgtm import process_payment_webhook
import hmac
import hashlib

app = FastAPI()

@app.post("/webhooks/lemonsqueezy")
async def lemonsqueezy_webhook(request: Request):
    # Verify signature
    signature = request.headers.get('X-Signature')
    payload = await request.body()
    
    secret = os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Process webhook
    data = await request.json()
    result = process_payment_webhook(
        provider='lemonsqueezy',
        event_type=data['meta']['event_name'],
        payload=data
    )
    
    return {"success": True, "license_key": result.get('license_key')}
```

### Stripe Webhook

```python
import stripe
from fastapi import FastAPI, Request, HTTPException
from coursesgtm import process_payment_webhook

app = FastAPI()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Process event
    result = process_payment_webhook(
        provider='stripe',
        event_type=event['type'],
        payload=event
    )
    
    return {"success": True}
```

---

## License Key Service Integration (Keygen.sh)

### Setup

```python
from coursesgtm import configure_license_provider

configure_license_provider(
    provider='keygen',
    api_key=os.getenv('KEYGEN_API_KEY'),
    account_id=os.getenv('KEYGEN_ACCOUNT_ID')
)
```

### Generate License

```python
from coursesgtm import issue_license

license = issue_license(
    user_id="user-123",
    tier_id="tier-intermediate",
    payment_id="payment-456",
    provider_options={
        'policy_id': 'keygen-policy-id',
        'max_machines': 2  # Allow 2 device activations
    }
)

print(f"License Key: {license['key']}")
```

---

## Client Libraries

### JavaScript/TypeScript

```typescript
// coursesgtm-client.ts
import axios from 'axios';

export class CoursesGTMClient {
  private baseURL: string;
  private apiKey: string;

  constructor(baseURL: string, apiKey: string) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
  }

  async checkCourseAccess(userId: string, courseCode: string) {
    const response = await axios.post(
      `${this.baseURL}/access/check-course`,
      { user_id: userId, course_id: courseCode },
      { headers: { 'Authorization': `Bearer ${this.apiKey}` } }
    );
    return response.data;
  }

  async getUserProgress(userId: string) {
    const response = await axios.get(
      `${this.baseURL}/users/${userId}/progress`,
      { headers: { 'Authorization': `Bearer ${this.apiKey}` } }
    );
    return response.data;
  }
}

// Usage
const client = new CoursesGTMClient(
  'https://api.example.com/api/v1',
  process.env.API_KEY
);

const access = await client.checkCourseAccess('user-123', 'PHIL2026');
if (!access.data.access_granted) {
  console.log('Access denied:', access.data.reason);
}
```

---

## Testing Integration

### Mock CoursesGTM in Tests

```python
# test_integration.py
import pytest
from unittest.mock import patch
from coursesgtm import check_course_access

@pytest.fixture
def mock_course_access():
    with patch('coursesgtm.check_course_access') as mock:
        mock.return_value = {
            'access_granted': True,
            'reason': 'Course included in user tier'
        }
        yield mock

def test_course_page_with_access(client, mock_course_access):
    response = client.get('/courses/PHIL2026')
    assert response.status_code == 200
    mock_course_access.assert_called_once()
```

---

## Related Documentation

- [API Specification](./API_SPEC.md)
- [Architecture Overview](./ARCHITECTURE.md)
- [Configuration Schema](./CONFIG_SCHEMA.md)
