# CoursePlayerApp - Integration Guide

## Overview

This guide covers integrating CoursePlayerApp with external services including CoursesGTM, OLLAMA, LemonSqueezy payments, and analytics platforms.

## Integrating with CoursesGTM

### Setup

Install the CoursesGTM Python SDK:

```bash
pip install coursesgtm-sdk
```

Configure the SDK with your API credentials:

```python
# config.py
import os
from coursesgtm import CoursesGTMConfig

config = CoursesGTMConfig(
    api_key=os.getenv('COURSESGTM_API_KEY'),
    api_endpoint=os.getenv('COURSESGTM_API_ENDPOINT', 'https://api.coursesgtm.com/v1'),
    cache_ttl=300,  # 5 minutes
    timeout=30  # 30 seconds
)
```

### Client Initialization

The CoursesGTM client uses a singleton pattern:

```python
from coursesgtm import CoursesGTMClient

# Initialize client (done once at app startup)
def init_gtm_client():
    """Initialize CoursesGTM client"""
    client = CoursesGTMClient.initialize(
        api_key=os.getenv('COURSESGTM_API_KEY'),
        cache_backend='redis',  # or 'memory'
        cache_config={
            'host': 'localhost',
            'port': 6379,
            'db': 0
        }
    )
    return client

# Get client instance anywhere in the app
gtm = CoursesGTMClient.get_instance()
```

### License Validation

Validate license on app startup:

```python
from coursesgtm import CoursesGTMClient, LicenseError

def validate_license(license_key: str) -> dict:
    """Validate license and get user profile"""
    gtm = CoursesGTMClient.get_instance()
    
    try:
        # Validate license
        license_info = gtm.validate_license(license_key)
        
        if not license_info['valid']:
            raise LicenseError("Invalid license key")
        
        if license_info['expired']:
            raise LicenseError("License has expired")
        
        # Get user profile and tier
        profile = gtm.get_user_profile(license_key)
        
        return {
            'valid': True,
            'tier': profile['tier'],
            'expires_at': license_info['expires_at'],
            'features': profile['features'],
            'user_id': profile['user_id'],
            'email': profile['email']
        }
        
    except LicenseError as e:
        return {
            'valid': False,
            'error': str(e)
        }
```

Example Streamlit integration:

```python
def main():
    """Main app entry point"""
    # Check if license is in session
    if 'license_validated' not in st.session_state:
        license_key = st.text_input("Enter License Key:", type="password")
        
        if st.button("Validate License"):
            result = validate_license(license_key)
            
            if result['valid']:
                st.session_state.license_validated = True
                st.session_state.license_key = license_key
                st.session_state.user_tier = result['tier']
                st.session_state.user_id = result['user_id']
                st.success(f"Welcome! Your tier: {result['tier']}")
                st.rerun()
            else:
                st.error(result['error'])
        return
    
    # License is valid, show app
    render_app()
```

### API Calls

#### can_access_course

Check if user can access a course:

```python
def check_course_access(course_id: str) -> bool:
    """Check if user can access a course"""
    gtm = CoursesGTMClient.get_instance()
    
    try:
        access = gtm.can_access_course(
            course_id=course_id,
            user_id=st.session_state.user_id
        )
        return access['allowed']
    except Exception as e:
        st.error(f"Error checking course access: {e}")
        return False
```

#### can_use_feature

Check if user can use a feature:

```python
def check_feature_access(feature_name: str) -> dict:
    """Check if user can use a feature"""
    gtm = CoursesGTMClient.get_instance()
    
    result = gtm.can_use_feature(
        feature_name=feature_name,
        user_id=st.session_state.user_id
    )
    
    return {
        'allowed': result['allowed'],
        'tier': result['user_tier'],
        'required_tier': result.get('required_tier'),
        'upgrade_message': result.get('upgrade_message')
    }
```

#### track_progress

Track user progress through course:

```python
def track_lesson_completion(course_id: str, lesson_id: str):
    """Mark a lesson as completed"""
    gtm = CoursesGTMClient.get_instance()
    
    gtm.track_progress(
        user_id=st.session_state.user_id,
        course_id=course_id,
        lesson_id=lesson_id,
        status='completed',
        progress_percentage=100,
        time_spent_seconds=st.session_state.get('lesson_time', 0)
    )
    
    # Check for rewards
    check_unlock_rewards(course_id)
```

#### check_unlock_rewards

Check if user unlocked any rewards:

```python
def check_unlock_rewards(course_id: str):
    """Check and display unlocked rewards"""
    gtm = CoursesGTMClient.get_instance()
    
    rewards = gtm.check_unlock_rewards(
        user_id=st.session_state.user_id,
        course_id=course_id
    )
    
    if rewards['new_rewards']:
        for reward in rewards['new_rewards']:
            st.balloons()
            st.success(f"🏆 Achievement Unlocked: {reward['title']}")
            st.info(reward['description'])
```

### Error Handling

Handle common API errors:

```python
from coursesgtm import (
    LicenseError,
    FeatureNotAvailableError,
    QuotaExceededError,
    APIError
)

def safe_gtm_call(func, *args, **kwargs):
    """Wrapper for safe GTM API calls"""
    try:
        return func(*args, **kwargs)
    except LicenseError as e:
        st.error("Invalid or expired license")
        st.session_state.clear()
        st.rerun()
    except FeatureNotAvailableError as e:
        st.warning(e.message)
        if st.button("Upgrade"):
            show_upgrade_page()
    except QuotaExceededError as e:
        st.error(f"Quota exceeded: {e.quota_name}")
        st.info(f"Resets on: {e.reset_date}")
    except APIError as e:
        st.error(f"Service error: {e}")
        # Log for debugging
        logging.error(f"CoursesGTM API error: {e}")
```

### Caching Strategy

Implement client-side caching to reduce API calls:

```python
from functools import lru_cache
from datetime import datetime, timedelta

class GTMCache:
    """Cache for CoursesGTM API responses"""
    
    def __init__(self):
        self.cache = {}
        self.ttl = 300  # 5 minutes
    
    def get(self, key: str):
        """Get cached value"""
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.utcnow() < expiry:
                return value
            del self.cache[key]
        return None
    
    def set(self, key: str, value, ttl: int = None):
        """Cache a value"""
        ttl = ttl or self.ttl
        expiry = datetime.utcnow() + timedelta(seconds=ttl)
        self.cache[key] = (value, expiry)

# Usage
cache = GTMCache()

def get_user_tier_cached():
    """Get user tier with caching"""
    key = f"tier:{st.session_state.user_id}"
    tier = cache.get(key)
    
    if tier is None:
        gtm = CoursesGTMClient.get_instance()
        tier = gtm.get_user_tier(st.session_state.user_id)
        cache.set(key, tier)
    
    return tier
```

## OLLAMA Integration

### Setup

Install OLLAMA locally:

```bash
# Linux/Mac
curl https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3.2:3b  # Intermediate tier
ollama pull llama3.1:8b  # Advanced tier
```

Start OLLAMA service:

```bash
# Start service
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

### Model Selection

Select model based on user tier:

```python
def get_ollama_model() -> str:
    """Get appropriate OLLAMA model for user tier"""
    tier = st.session_state.get('user_tier', 'basic')
    
    model_map = {
        'basic': None,  # No access
        'intermediate': 'llama3.2:3b',
        'advanced': 'llama3.1:8b',
        'enterprise': 'llama3.1:8b'
    }
    
    return model_map.get(tier)
```

### Context Building

Build context using RAG from course materials:

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

class CourseContextBuilder:
    """Build context from course materials for AI tutor"""
    
    def __init__(self, course_id: str):
        self.course_id = course_id
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = self._load_vector_store()
    
    def _load_vector_store(self):
        """Load or create vector store for course"""
        # Load course materials
        materials = self._get_course_materials()
        
        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(materials)
        
        # Create vector store
        return Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=f"data/vectors/{self.course_id}"
        )
    
    def get_relevant_context(self, query: str, k: int = 3) -> str:
        """Get relevant context for a query"""
        docs = self.vector_store.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
```

### OLLAMA Client

```python
import requests
from typing import Generator

class OLLAMAClient:
    """Client for OLLAMA API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def query(
        self,
        prompt: str,
        model: str,
        context: str = "",
        temperature: float = 0.7,
        stream: bool = True
    ) -> Generator[str, None, None]:
        """Query OLLAMA model"""
        # Build full prompt with context
        full_prompt = self._build_prompt(prompt, context)
        
        # Make request
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": full_prompt,
                "temperature": temperature,
                "stream": stream
            },
            stream=stream
        )
        
        # Stream response
        if stream:
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    yield data.get('response', '')
        else:
            yield response.json()['response']
    
    def _build_prompt(self, query: str, context: str) -> str:
        """Build prompt with context"""
        return f"""You are a helpful AI tutor for this course.

Context from course materials:
{context}

Student question: {query}

Provide a clear, educational answer based on the course context."""
```

### Quota Management

Track and enforce AI tutor quota:

```python
def check_ai_tutor_quota() -> dict:
    """Check AI tutor quota status"""
    gtm = CoursesGTMClient.get_instance()
    tier = st.session_state.user_tier
    
    if tier == 'advanced':
        return {'allowed': True, 'unlimited': True}
    
    if tier == 'basic':
        return {'allowed': False, 'reason': 'Not available for Basic tier'}
    
    # Intermediate tier - check quota
    usage = gtm.get_feature_usage('ai_tutor_quota', st.session_state.user_id)
    limit = 50
    
    return {
        'allowed': usage < limit,
        'usage': usage,
        'limit': limit,
        'remaining': max(0, limit - usage)
    }

def use_ai_tutor_quota():
    """Increment AI tutor usage"""
    gtm = CoursesGTMClient.get_instance()
    gtm.increment_feature_usage(
        'ai_tutor_quota',
        st.session_state.user_id
    )
```

### Streamlit Integration

```python
def render_ai_tutor():
    """Render AI tutor chat interface"""
    # Check quota
    quota = check_ai_tutor_quota()
    
    if not quota['allowed']:
        st.warning(quota.get('reason', 'Quota exceeded'))
        return
    
    # Display quota info
    if not quota.get('unlimited'):
        st.caption(f"Questions remaining: {quota['remaining']}/{quota['limit']}")
    
    # Chat interface
    for msg in st.session_state.chat_history:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])
    
    # Input
    if prompt := st.chat_input("Ask a question..."):
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': prompt
        })
        
        # Get context
        context_builder = CourseContextBuilder(st.session_state.course_id)
        context = context_builder.get_relevant_context(prompt)
        
        # Get AI response
        model = get_ollama_model()
        ollama = OLLAMAClient()
        
        response = ""
        with st.chat_message("assistant"):
            placeholder = st.empty()
            for chunk in ollama.query(prompt, model, context):
                response += chunk
                placeholder.markdown(response + "▌")
            placeholder.markdown(response)
        
        # Save response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
        
        # Track usage
        use_ai_tutor_quota()
```

## Payment Integration (LemonSqueezy)

### Setup

Configure LemonSqueezy:

```python
import os
import lemonsqueezy

lemonsqueezy.api_key = os.getenv('LEMONSQUEEZY_API_KEY')
lemonsqueezy.store_id = os.getenv('LEMONSQUEEZY_STORE_ID')
```

### Webhook Handling

Handle license activation on payment:

```python
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib

app = FastAPI()

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify LemonSqueezy webhook signature"""
    secret = os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

@app.post("/webhooks/lemonsqueezy")
async def handle_lemonsqueezy_webhook(request: Request):
    """Handle LemonSqueezy webhook events"""
    # Verify signature
    signature = request.headers.get('X-Signature')
    payload = await request.body()
    
    if not verify_webhook_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse event
    event = await request.json()
    event_type = event['meta']['event_name']
    
    if event_type == 'order_created':
        await handle_order_created(event['data'])
    elif event_type == 'subscription_created':
        await handle_subscription_created(event['data'])
    elif event_type == 'subscription_updated':
        await handle_subscription_updated(event['data'])
    
    return {"status": "ok"}

async def handle_order_created(data: dict):
    """Handle new order - activate license"""
    # Create license in CoursesGTM
    gtm = CoursesGTMClient.get_instance()
    
    license = gtm.create_license(
        email=data['attributes']['user_email'],
        tier=data['attributes']['first_order_item']['variant_name'],
        order_id=data['id']
    )
    
    # Send license key via email
    send_license_email(
        email=data['attributes']['user_email'],
        license_key=license['key']
    )
```

### Upgrade Flow

Handle tier upgrade purchases:

```python
def create_upgrade_checkout(target_tier: str):
    """Create checkout session for upgrade"""
    current_tier = st.session_state.user_tier
    
    # Get product variant for tier
    variant_id = get_variant_for_tier(target_tier)
    
    # Create checkout
    checkout = lemonsqueezy.Checkout.create(
        store_id=lemonsqueezy.store_id,
        variant_id=variant_id,
        checkout_data={
            'email': st.session_state.user_email,
            'custom': {
                'user_id': st.session_state.user_id,
                'current_tier': current_tier,
                'upgrade_to': target_tier
            }
        }
    )
    
    return checkout.url

def render_upgrade_page():
    """Render upgrade options"""
    st.title("Upgrade Your Plan")
    
    current_tier = st.session_state.user_tier
    
    # Show tier options
    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.subheader("Intermediate")
        st.write("$247/year")
        st.write("✅ 50 AI questions/month")
        st.write("✅ Download videos")
        st.write("✅ Interactive notebooks")
        
        if current_tier == 'basic':
            if st.button("Upgrade to Intermediate"):
                checkout_url = create_upgrade_checkout('intermediate')
                st.markdown(f"[Complete Purchase]({checkout_url})")
    
    with col3:
        st.subheader("Advanced")
        st.write("$497/year")
        st.write("✅ Unlimited AI questions")
        st.write("✅ All Intermediate features")
        st.write("✅ GPU notebook access")
        st.write("✅ Commercial license")
        
        if current_tier in ['basic', 'intermediate']:
            if st.button("Upgrade to Advanced"):
                checkout_url = create_upgrade_checkout('advanced')
                st.markdown(f"[Complete Purchase]({checkout_url})")
```

### Renewal Flow

Handle license renewal:

```python
def check_license_expiry():
    """Check if license is expiring soon"""
    gtm = CoursesGTMClient.get_instance()
    license_info = gtm.get_license_info(st.session_state.license_key)
    
    expires_at = datetime.fromisoformat(license_info['expires_at'])
    days_until_expiry = (expires_at - datetime.utcnow()).days
    
    if days_until_expiry <= 30:
        st.warning(f"⚠️ Your license expires in {days_until_expiry} days")
        
        if st.button("Renew Now"):
            renewal_url = create_renewal_checkout()
            st.markdown(f"[Renew License]({renewal_url})")
```

## Analytics Integration

### Events to Track

Track key user actions:

```python
from mixpanel import Mixpanel

mp = Mixpanel(os.getenv('MIXPANEL_TOKEN'))

def track_event(event_name: str, properties: dict = None):
    """Track analytics event"""
    # Add common properties
    props = {
        'user_id': st.session_state.user_id,
        'tier': st.session_state.user_tier,
        'course_id': st.session_state.get('course_id'),
        **( properties or {})
    }
    
    # Track in Mixpanel
    mp.track(st.session_state.user_id, event_name, props)

# Track lesson completion
track_event('lesson_completed', {
    'lesson_id': 'intro-to-pandas',
    'time_spent': 450
})

# Track quiz attempt
track_event('quiz_attempted', {
    'quiz_id': 'pandas-basics',
    'score': 85,
    'attempts': 1
})

# Track AI tutor usage
track_event('ai_tutor_used', {
    'question_length': len(question),
    'quota_remaining': quota['remaining']
})

# Track feature usage
track_event('feature_used', {
    'feature': 'video_download',
    'video_id': 'intro-to-ml'
})

# Track upgrade prompt
track_event('upgrade_prompt_shown', {
    'feature': 'ai_tutor',
    'current_tier': 'basic',
    'target_tier': 'intermediate'
})

# Track upgrade click
track_event('upgrade_clicked', {
    'current_tier': 'basic',
    'target_tier': 'intermediate',
    'trigger': 'ai_tutor_gate'
})
```

### Privacy

Implement privacy-conscious analytics:

```python
def should_track_analytics() -> bool:
    """Check if user has opted into analytics"""
    return st.session_state.get('analytics_enabled', True)

def track_event_safe(event_name: str, properties: dict = None):
    """Track event with privacy check"""
    if not should_track_analytics():
        return
    
    # Anonymize sensitive data
    props = properties or {}
    if 'email' in props:
        props['email_hash'] = hashlib.sha256(
            props['email'].encode()
        ).hexdigest()
        del props['email']
    
    track_event(event_name, props)

def render_privacy_settings():
    """Render privacy settings"""
    st.subheader("Privacy Settings")
    
    analytics_enabled = st.checkbox(
        "Enable anonymous analytics",
        value=st.session_state.get('analytics_enabled', True)
    )
    
    st.session_state.analytics_enabled = analytics_enabled
    
    st.caption(
        "We collect anonymous usage data to improve the learning experience. "
        "No personally identifiable information is tracked."
    )
```

## Authentication Integration

### Session Management

Store license key securely:

```python
import streamlit_authenticator as stauth

def store_license_securely(license_key: str):
    """Store license in encrypted session"""
    # Encrypt license key
    from cryptography.fernet import Fernet
    
    # Generate key from app secret
    key = Fernet(os.getenv('APP_SECRET_KEY').encode())
    encrypted = key.encrypt(license_key.encode())
    
    # Store in session
    st.session_state.encrypted_license = encrypted

def get_license_securely() -> str:
    """Retrieve encrypted license from session"""
    from cryptography.fernet import Fernet
    
    key = Fernet(os.getenv('APP_SECRET_KEY').encode())
    encrypted = st.session_state.encrypted_license
    
    return key.decrypt(encrypted).decode()
```

### User Context

Maintain user context throughout session:

```python
class UserContext:
    """User session context"""
    
    @staticmethod
    def initialize(license_validation: dict):
        """Initialize user context from license validation"""
        st.session_state.user_id = license_validation['user_id']
        st.session_state.user_tier = license_validation['tier']
        st.session_state.user_email = license_validation['email']
        st.session_state.features = license_validation['features']
        st.session_state.license_expires = license_validation['expires_at']
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return 'user_id' in st.session_state
    
    @staticmethod
    def get_tier() -> str:
        """Get user tier"""
        return st.session_state.get('user_tier', 'basic')
    
    @staticmethod
    def has_feature(feature: str) -> bool:
        """Check if user has access to feature"""
        return feature in st.session_state.get('features', [])
```

### Multi-User Support (Enterprise)

Enterprise tier multi-user support:

```python
def handle_enterprise_login():
    """Handle enterprise multi-user login"""
    # Organization license
    org_license = st.text_input("Organization License:")
    
    # User email
    user_email = st.text_input("Your Email:")
    
    if st.button("Login"):
        gtm = CoursesGTMClient.get_instance()
        
        # Validate org license
        org = gtm.validate_org_license(org_license)
        
        # Check if user is member
        if user_email in org['members']:
            # Create user session
            UserContext.initialize({
                'user_id': user_email,
                'tier': 'enterprise',
                'email': user_email,
                'features': org['features'],
                'expires_at': org['expires_at']
            })
            st.success("Welcome to your organization's courses!")
        else:
            st.error("Email not found in organization")
```

## Related Documentation

- [Architecture](./ARCHITECTURE.md)
- [Components](./COMPONENTS.md)
- [Feature Gates](./FEATURE_GATES.md)
- [Deployment Guide](./DEPLOYMENT.md)
