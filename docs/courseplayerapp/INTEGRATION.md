# Integration Guide

This document provides comprehensive guidance on integrating CoursePlayerApp with external services including CoursesGTM API, OLLAMA, LemonSqueezy, Keygen.sh, and content storage systems.

## Table of Contents

1. [CoursesGTM API Integration](#coursesgtm-api-integration)
2. [OLLAMA Integration](#ollama-integration)
3. [LemonSqueezy Integration](#lemonsqueezy-integration)
4. [License Key Service (Keygen.sh)](#license-key-service-keygensh)
5. [Content Storage](#content-storage)

---

## CoursesGTM API Integration

### Overview

CoursesGTM serves as the business logic layer for CoursePlayerApp, handling license validation, feature permissions, course content management, and progress tracking.

### Client Library Usage

**File**: `courseplayerapp/integrations/coursesgtm_client.py`

```python
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import streamlit as st

class CoursesGTMClient:
    """
    Client for CoursesGTM API integration.
    Handles authentication, retries, and caching.
    """
    
    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or st.secrets.get("COURSESGTM_API_URL", "http://localhost:8000")
        self.api_key = api_key or st.secrets.get("COURSESGTM_API_KEY")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        self.cache_ttl = 300  # 5 minutes
        self._cache = {}
    
    def _get_cached(self, key: str):
        """Get cached value if not expired"""
        if key in self._cache:
            value, expires_at = self._cache[key]
            if datetime.now() < expires_at:
                return value
        return None
    
    def _set_cache(self, key: str, value: any, ttl: int = None):
        """Cache value with TTL"""
        ttl = ttl or self.cache_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = (value, expires_at)
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make HTTP request with retries"""
        url = f"{self.base_url}{endpoint}"
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, timeout=30, **kwargs)
                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code in [500, 502, 503, 504]:
                    # Retry on server errors
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (attempt + 1))
                        continue
                raise
            
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                raise
    
    # ===== License Validation =====
    
    def validate_license(self, license_key: str) -> Dict:
        """
        Validate license key and get user permissions.
        
        Returns:
            {
                "valid": bool,
                "tier": str,  # "basic", "intermediate", "advanced"
                "enabled_features": List[str],
                "expires_at": str,
                "user_id": str,
                "user_email": str
            }
        """
        cache_key = f"license_{license_key}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = self._request(
            "POST",
            "/api/v1/license/validate",
            json={"license_key": license_key}
        )
        
        # Cache for 5 minutes
        self._set_cache(cache_key, result, ttl=300)
        return result
    
    def get_license_features(self, license_key: str) -> List[str]:
        """Get list of enabled features for license"""
        validation = self.validate_license(license_key)
        return validation.get("enabled_features", [])
    
    # ===== Course Access =====
    
    def get_course(self, course_id: str) -> Dict:
        """
        Get course metadata and structure.
        
        Returns:
            {
                "id": str,
                "title": str,
                "description": str,
                "modules": List[{
                    "id": str,
                    "title": str,
                    "lessons": List[...]
                }],
                "tier_requirement": str
            }
        """
        cache_key = f"course_{course_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = self._request("GET", f"/api/v1/courses/{course_id}")
        self._set_cache(cache_key, result, ttl=600)
        return result
    
    def get_lesson(self, lesson_id: str) -> Dict:
        """Get lesson content including video, slides, and lab URLs"""
        return self._request("GET", f"/api/v1/lessons/{lesson_id}")
    
    def check_course_access(self, course_id: str, license_key: str) -> bool:
        """Check if license has access to course"""
        result = self._request(
            "POST",
            f"/api/v1/courses/{course_id}/check-access",
            json={"license_key": license_key}
        )
        return result.get("has_access", False)
    
    # ===== Video Management =====
    
    def get_video_metadata(self, video_id: str) -> Dict:
        """Get video metadata including stream URL"""
        return self._request("GET", f"/api/v1/videos/{video_id}/metadata")
    
    def get_video_stream_url(self, video_id: str, quality: str = "auto") -> str:
        """Get HLS/DASH stream URL"""
        result = self._request(
            "GET",
            f"/api/v1/videos/{video_id}/stream-url",
            params={"quality": quality}
        )
        return result.get("stream_url")
    
    def get_video_transcript(self, video_id: str) -> str:
        """Get video transcript text"""
        result = self._request("GET", f"/api/v1/videos/{video_id}/transcript")
        return result.get("transcript", "")
    
    def initiate_video_download(self, video_id: str, quality: str = "720p") -> Dict:
        """
        Initiate video download (Intermediate+ only).
        
        Returns:
            {
                "download_url": str,
                "expires_at": str,
                "file_size_mb": float
            }
        """
        return self._request(
            "POST",
            f"/api/v1/videos/{video_id}/download",
            json={"quality": quality}
        )
    
    def save_video_note(self, video_id: str, timestamp: str, note: str) -> Dict:
        """Save video annotation (Advanced only)"""
        return self._request(
            "POST",
            f"/api/v1/videos/{video_id}/notes",
            json={"timestamp": timestamp, "note": note}
        )
    
    # ===== Progress Tracking =====
    
    def get_progress(self, course_id: str) -> Dict:
        """
        Get user progress for course.
        
        Returns:
            {
                "course_id": str,
                "completion_percentage": float,
                "modules": List[...],
                "xp": int,
                "level": int,
                "streak_days": int,
                "last_activity": str
            }
        """
        return self._request("GET", f"/api/v1/progress/{course_id}")
    
    def update_progress(self, course_id: str, lesson_id: str, completed: bool = True) -> Dict:
        """Mark lesson as completed"""
        return self._request(
            "POST",
            f"/api/v1/progress/{course_id}/update",
            json={
                "lesson_id": lesson_id,
                "completed": completed,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    def get_analytics(self, course_id: str) -> Dict:
        """Get detailed learning analytics"""
        return self._request("GET", f"/api/v1/analytics/{course_id}")
    
    # ===== Rewards & Achievements =====
    
    def check_achievements(self) -> List[Dict]:
        """Check for newly unlocked achievements"""
        return self._request("GET", "/api/v1/rewards/check")
    
    def get_achievements(self) -> List[Dict]:
        """Get all user achievements"""
        return self._request("GET", "/api/v1/rewards/achievements")
    
    # ===== AI Tutor Quota =====
    
    def get_ai_tutor_quota(self) -> Dict:
        """
        Get AI tutor quota information.
        
        Returns:
            {
                "remaining": int or "unlimited",
                "total": int,
                "reset_date": str
            }
        """
        return self._request("GET", "/api/v1/ai-tutor/quota")
    
    def decrement_ai_quota(self) -> Dict:
        """Decrement AI tutor quota after question"""
        return self._request("POST", "/api/v1/ai-tutor/decrement")
    
    def search_course_content(self, course_id: str, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """RAG: Search course content for relevant context"""
        return self._request(
            "POST",
            f"/api/v1/ai-tutor/{course_id}/search-context",
            json={
                "embedding": query_embedding,
                "top_k": top_k
            }
        )
    
    # ===== Quiz & Assessment =====
    
    def get_quiz(self, quiz_id: str) -> Dict:
        """Get quiz questions and metadata"""
        return self._request("GET", f"/api/v1/quizzes/{quiz_id}")
    
    def submit_quiz(self, quiz_id: str, answers: Dict) -> Dict:
        """Submit quiz answers and get results"""
        return self._request(
            "POST",
            f"/api/v1/quizzes/{quiz_id}/submit",
            json={"answers": answers}
        )
    
    def run_code_tests(self, code: str, test_cases: List[Dict]) -> List[Dict]:
        """Execute code against test cases"""
        return self._request(
            "POST",
            "/api/v1/quizzes/run-code-tests",
            json={"code": code, "test_cases": test_cases}
        )
    
    # ===== Certificates =====
    
    def get_certificates(self) -> List[Dict]:
        """Get user's earned certificates"""
        return self._request("GET", "/api/v1/certificates")
    
    def generate_certificate(self, course_id: str) -> Dict:
        """Generate certificate for completed course"""
        return self._request("POST", f"/api/v1/certificates/generate/{course_id}")
    
    # ===== Code Review =====
    
    def submit_code_review(self, course_id: str, project_url: str, description: str) -> Dict:
        """Submit project for code review"""
        return self._request(
            "POST",
            f"/api/v1/code-review/{course_id}/submit",
            json={
                "project_url": project_url,
                "description": description
            }
        )
    
    def get_code_review_status(self, submission_id: str) -> Dict:
        """Get code review status and feedback"""
        return self._request("GET", f"/api/v1/code-review/submissions/{submission_id}")
```

### License Validation on Startup

```python
import streamlit as st
from courseplayerapp.integrations.coursesgtm_client import CoursesGTMClient

def initialize_app():
    """Initialize app with license validation"""
    
    # Get license key from environment or user input
    license_key = st.secrets.get("LICENSE_KEY") or st.session_state.get("license_key")
    
    if not license_key:
        render_license_activation_page()
        st.stop()
    
    # Validate license
    gtm_client = CoursesGTMClient()
    
    try:
        validation = gtm_client.validate_license(license_key)
        
        if not validation['valid']:
            st.error("Invalid license key. Please check your license or contact support.")
            st.stop()
        
        # Store in session
        st.session_state.license_valid = True
        st.session_state.tier = validation['tier']
        st.session_state.enabled_features = validation['enabled_features']
        st.session_state.user_id = validation['user_id']
        st.session_state.user_email = validation['user_email']
        
        # Check expiration
        expires_at = datetime.fromisoformat(validation['expires_at'])
        if expires_at < datetime.now():
            st.warning("Your license has expired. Please renew to continue.")
            show_renewal_link()
            st.stop()
        
    except Exception as e:
        st.error(f"Error validating license: {str(e)}")
        st.caption("Please check your internet connection or contact support.")
        st.stop()
```

### Error Handling and Retries

```python
from requests.exceptions import RequestException, Timeout, ConnectionError

def safe_api_call(func, *args, **kwargs):
    """Wrapper for safe API calls with error handling"""
    try:
        return func(*args, **kwargs)
    
    except Timeout:
        st.error("⏱️ Request timeout. Please try again.")
        return None
    
    except ConnectionError:
        st.error("🔌 Connection error. Check your internet connection.")
        return None
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("🔒 Authentication failed. Please check your license key.")
        elif e.response.status_code == 403:
            st.error("⛔ Access denied. This feature requires a higher tier license.")
            show_upgrade_button()
        elif e.response.status_code == 404:
            st.error("❌ Resource not found.")
        elif e.response.status_code == 429:
            st.error("⏸️ Rate limit exceeded. Please wait a moment.")
        else:
            st.error(f"❌ API error: {e.response.status_code}")
        return None
    
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None
```

---

## OLLAMA Integration

### Overview

OLLAMA provides local LLM inference for AI tutoring capabilities, supporting different models based on user tier.

### Model Selection by Tier

```python
OLLAMA_MODELS = {
    'intermediate': {
        'model_name': 'llama3.2:3b',
        'context_window': 4096,
        'temperature': 0.7,
        'description': 'Lightweight model optimized for speed'
    },
    'advanced': {
        'model_name': 'llama3.1:8b',
        'context_window': 8192,
        'temperature': 0.7,
        'description': 'Higher quality model with better reasoning'
    }
}
```

### Client Implementation

**File**: `courseplayerapp/integrations/ollama_client.py`

```python
import requests
import json
from typing import Iterator, List, Dict
import streamlit as st

class OllamaClient:
    """
    Client for OLLAMA API integration.
    Handles chat completions, streaming, and embeddings.
    """
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or st.secrets.get("OLLAMA_URL", "http://localhost:11434")
        self.tier = st.session_state.get('tier', 'basic')
        self.model_config = OLLAMA_MODELS.get(self.tier, {})
    
    def chat(self, prompt: str, system_prompt: str = None) -> str:
        """Non-streaming chat completion"""
        model = self.model_config.get('model_name')
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": self.model_config.get('temperature', 0.7),
                    "num_ctx": self.model_config.get('context_window', 4096)
                }
            },
            timeout=60
        )
        
        response.raise_for_status()
        return response.json()['message']['content']
    
    def stream_chat(self, prompt: str, system_prompt: str = None, conversation_history: List[Dict] = None) -> Iterator[str]:
        """
        Streaming chat completion.
        Yields response chunks for real-time display.
        """
        model = self.model_config.get('model_name')
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": prompt})
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": self.model_config.get('temperature', 0.7),
                    "num_ctx": self.model_config.get('context_window', 4096)
                }
            },
            stream=True,
            timeout=60
        )
        
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                if 'message' in chunk:
                    content = chunk['message'].get('content', '')
                    if content:
                        yield content
    
    def get_embeddings(self, text: str) -> List[float]:
        """Get text embeddings for RAG"""
        model = self.model_config.get('model_name')
        
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={
                "model": model,
                "prompt": text
            },
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()['embedding']
    
    def check_model_availability(self) -> bool:
        """Check if required model is available"""
        model = self.model_config.get('model_name')
        
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            
            models = response.json().get('models', [])
            available_models = [m['name'] for m in models]
            
            return model in available_models
        
        except Exception:
            return False
    
    def pull_model(self) -> Iterator[Dict]:
        """Download model if not available (streaming progress)"""
        model = self.model_config.get('model_name')
        
        response = requests.post(
            f"{self.base_url}/api/pull",
            json={"name": model},
            stream=True,
            timeout=600
        )
        
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                yield json.loads(line)
```

### Prompt Engineering for Course Context

```python
def build_tutor_prompt(question: str, course_context: str, difficulty_level: str = "intermediate") -> str:
    """
    Build optimized prompt for AI tutor.
    
    Args:
        question: Student's question
        course_context: Relevant content from RAG
        difficulty_level: Adjust explanation complexity
    """
    
    system_prompt = f"""You are an expert AI tutor specializing in data science and machine learning.

Your teaching style:
- Clear, step-by-step explanations
- Use analogies and examples
- Encourage critical thinking
- Provide code examples when relevant
- Be patient and supportive

Difficulty level: {difficulty_level}
- If "beginner": Use simple language, more examples, break down concepts
- If "intermediate": Balanced explanation with some technical depth
- If "advanced": Technical explanations, assume prior knowledge

Context from the course:
{course_context}

Student's question: {question}

Provide a helpful, educational response. If the question is outside the course scope, politely guide the student back to course topics."""

    return system_prompt
```

### RAG Implementation

```python
from chromadb import Client as ChromaClient
from chromadb.config import Settings

class RAGEngine:
    """RAG engine for course content retrieval"""
    
    def __init__(self, course_id: str):
        self.course_id = course_id
        self.ollama = OllamaClient()
        self.chroma_client = ChromaClient(Settings(persist_directory=f"./data/chroma/{course_id}"))
        self.collection = self.chroma_client.get_or_create_collection(f"course_{course_id}")
    
    def index_course_content(self, content_items: List[Dict]):
        """Index course content for retrieval"""
        for item in content_items:
            # Get embedding
            embedding = self.ollama.get_embeddings(item['text'])
            
            # Store in vector database
            self.collection.add(
                embeddings=[embedding],
                documents=[item['text']],
                metadatas=[{
                    'lesson_id': item['lesson_id'],
                    'type': item['type'],  # 'transcript', 'slide', 'lab'
                    'title': item['title']
                }],
                ids=[item['id']]
            )
    
    def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """Retrieve relevant context for query"""
        # Get query embedding
        query_embedding = self.ollama.get_embeddings(query)
        
        # Search vector database
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format context
        context_parts = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            context_parts.append(f"[{metadata['type']}] {metadata['title']}\n{doc}")
        
        return "\n\n".join(context_parts)
```

### Streaming Response Handler

```python
def render_streaming_response(prompt: str):
    """Render AI response with streaming"""
    ollama = OllamaClient()
    
    # Build prompt with RAG context
    rag = RAGEngine(st.session_state.course_id)
    context = rag.retrieve_context(prompt)
    full_prompt = build_tutor_prompt(prompt, context)
    
    # Stream response
    response_placeholder = st.empty()
    full_response = ""
    
    try:
        for chunk in ollama.stream_chat(prompt, system_prompt=full_prompt):
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")  # Cursor effect
        
        # Final response without cursor
        response_placeholder.markdown(full_response)
        
        return full_response
    
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None
```

### Model Switching for Performance

```python
def switch_model_if_needed(query_complexity: str):
    """Dynamically switch models based on query"""
    tier = st.session_state.get('tier')
    
    if tier == 'advanced':
        # Advanced users can manually select
        model_options = ['llama3.1:8b', 'llama3.2:3b', 'codellama:7b']
        selected = st.selectbox("Model", model_options)
        return selected
    else:
        # Auto-select for intermediate
        return 'llama3.2:3b'
```

### Fallback Strategies

```python
def ask_ai_with_fallback(question: str) -> str:
    """Ask AI with fallback strategies"""
    ollama = OllamaClient()
    
    try:
        # Try primary model
        return ollama.chat(question)
    
    except requests.exceptions.Timeout:
        # Timeout - try with lower context window
        st.warning("Response taking longer than expected, trying with simplified context...")
        return ollama.chat(question, max_tokens=512)
    
    except requests.exceptions.ConnectionError:
        # OLLAMA offline - show cached responses or error
        st.error("AI service temporarily unavailable")
        return show_cached_faq_answer(question)
    
    except Exception as e:
        st.error(f"AI error: {str(e)}")
        return None
```

---

## LemonSqueezy Integration

### License Activation Flow

```python
def handle_license_activation():
    """Process license activation from LemonSqueezy purchase"""
    st.title("Activate Your License")
    
    license_key = st.text_input("Enter your license key:", type="password")
    
    if st.button("Activate"):
        gtm_client = CoursesGTMClient()
        
        try:
            # Activate via CoursesGTM (which validates with LemonSqueezy)
            result = gtm_client.activate_license(license_key)
            
            if result['success']:
                st.success("License activated successfully!")
                st.session_state.license_key = license_key
                st.experimental_rerun()
            else:
                st.error(result['message'])
        
        except Exception as e:
            st.error(f"Activation failed: {str(e)}")
```

### Webhook Handling

Webhooks are handled by CoursesGTM, but CoursePlayerApp can react to webhook events:

```python
def check_subscription_status():
    """Check if subscription has changed (renewal, upgrade, cancellation)"""
    gtm_client = CoursesGTMClient()
    
    status = gtm_client.get_subscription_status()
    
    if status['status'] == 'cancelled':
        st.warning("Your subscription has been cancelled. Access will end on " + status['expires_at'])
    
    elif status['status'] == 'past_due':
        st.error("Payment failed. Please update your payment method.")
        st.button("Update Payment Method", on_click=lambda: redirect_to_billing_portal())
    
    elif status.get('upgraded'):
        st.success(f"Congratulations! You've been upgraded to {status['new_tier']}!")
        st.session_state.tier = status['new_tier']
        st.experimental_rerun()
```

### Upgrade Flow

```python
def initiate_upgrade(target_tier: str):
    """Redirect to LemonSqueezy checkout for upgrade"""
    gtm_client = CoursesGTMClient()
    
    # Get checkout URL from CoursesGTM
    checkout_info = gtm_client.get_upgrade_checkout_url(
        current_tier=st.session_state.tier,
        target_tier=target_tier,
        user_email=st.session_state.user_email
    )
    
    # Redirect to LemonSqueezy checkout
    st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_info[\'checkout_url\']}">', unsafe_allow_html=True)
```

---

## License Key Service (Keygen.sh)

### Key Validation

```python
def validate_license_offline(license_key: str, public_key: str) -> bool:
    """
    Validate license signature offline (for Advanced tier offline mode).
    
    Args:
        license_key: License key string
        public_key: Public key for signature verification
    
    Returns:
        bool: True if signature is valid
    """
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    
    try:
        # Parse license (format: KEY_DATA.SIGNATURE)
        key_data, signature = license_key.split('.')
        signature_bytes = bytes.fromhex(signature)
        
        # Load public key
        public_key_obj = serialization.load_pem_public_key(public_key.encode())
        
        # Verify signature
        public_key_obj.verify(
            signature_bytes,
            key_data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Check expiration in key_data
        import json
        license_info = json.loads(base64.b64decode(key_data))
        
        expires_at = datetime.fromisoformat(license_info['expires_at'])
        if expires_at < datetime.now():
            return False
        
        return True
    
    except Exception:
        return False
```

---

## Content Storage

### Video Storage Integration

```python
import boto3
from botocore.exceptions import ClientError

class VideoStorage:
    """Manage video content storage"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3',
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
        )
        self.bucket_name = st.secrets["S3_BUCKET_NAME"]
        self.cdn_url = st.secrets.get("CDN_URL", "")
    
    def get_video_url(self, video_id: str, quality: str = "auto") -> str:
        """Get video stream URL (HLS manifest)"""
        if self.cdn_url:
            return f"{self.cdn_url}/videos/{video_id}/{quality}/master.m3u8"
        else:
            # Generate presigned URL
            try:
                url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': self.bucket_name,
                        'Key': f"videos/{video_id}/{quality}/master.m3u8"
                    },
                    ExpiresIn=3600  # 1 hour
                )
                return url
            except ClientError as e:
                st.error(f"Error generating video URL: {e}")
                return None
```

This integration guide provides comprehensive coverage of all external service integrations required by CoursePlayerApp.
