# Integrations Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Define external system integrations for CoursePlayerApp

---

## Overview

CoursePlayerApp integrates with three primary external systems and several third-party services. All integrations use RESTful APIs with JWT authentication.

---

## Core System Integrations

### 1. CoursesGTM Integration

**Purpose**: License validation, tier management, feature access control, usage tracking

#### API Endpoints

```python
# integrations/coursesgtm_client.py

import httpx
from typing import Optional, List, Dict

class CoursesGTMClient:
    """Client for CoursesGTM API integration"""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=api_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=10.0
        )
    
    async def validate_license(self, license_key: str) -> Dict:
        """
        Validate user license and get tier information
        
        Args:
            license_key: User's license key
        
        Returns:
            {
                "valid": True,
                "user_id": "user123",
                "tier": "intermediate",
                "expires_at": "2027-01-12T00:00:00Z",
                "features": ["video_download", "ai_tutor", ...]
            }
        
        Raises:
            LicenseInvalidError: If license is invalid or expired
        """
        
        response = await self.client.post(
            "/api/licenses/validate",
            json={"license_key": license_key}
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise LicenseInvalidError("License key is invalid")
        elif response.status_code == 410:
            raise LicenseExpiredError("License has expired")
        else:
            raise APIError(f"Unexpected error: {response.status_code}")
    
    async def get_accessible_courses(
        self,
        user_id: str,
        tier: str
    ) -> List[Dict]:
        """
        Get list of courses user can access based on tier
        
        Args:
            user_id: User ID
            tier: User's tier (basic, intermediate, advanced)
        
        Returns:
            [
                {
                    "course_id": "ml-fundamentals",
                    "title": "Machine Learning Fundamentals",
                    "tier_required": "basic",
                    "accessible": True
                },
                ...
            ]
        """
        
        response = await self.client.get(
            "/api/users/{user_id}/courses",
            params={"tier": tier}
        )
        
        return response.json()["courses"]
    
    async def check_feature_access(
        self,
        user_id: str,
        feature: str
    ) -> bool:
        """
        Check if user has access to a specific feature
        
        Args:
            user_id: User ID
            feature: Feature name (e.g., "video_download", "ai_tutor")
        
        Returns:
            bool: True if user has access, False otherwise
        """
        
        response = await self.client.get(
            f"/api/users/{user_id}/features/{feature}"
        )
        
        return response.json()["has_access"]
    
    async def track_usage(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        metadata: Optional[Dict] = None
    ):
        """
        Track user resource usage
        
        Args:
            user_id: User ID
            resource_type: Type of resource (video, lab, ai_tutor)
            resource_id: Resource identifier
            action: Action performed (watch, complete, download, ask)
            metadata: Additional data (video_duration, question_text, etc.)
        """
        
        await self.client.post(
            "/api/usage/track",
            json={
                "user_id": user_id,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "action": action,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    async def get_quota_info(
        self,
        user_id: str,
        quota_type: str
    ) -> Dict:
        """
        Get quota information for user
        
        Args:
            user_id: User ID
            quota_type: Type of quota (ai_tutor, video_download, etc.)
        
        Returns:
            {
                "total": 50,
                "used": 23,
                "remaining": 27,
                "reset_date": "2026-02-01"
            }
        """
        
        response = await self.client.get(
            f"/api/users/{user_id}/quotas/{quota_type}"
        )
        
        return response.json()
    
    async def update_user_progress(
        self,
        user_id: str,
        course_id: str,
        progress_data: Dict
    ):
        """
        Sync user progress to CoursesGTM
        
        Args:
            user_id: User ID
            course_id: Course ID
            progress_data: Progress information
        """
        
        await self.client.post(
            f"/api/users/{user_id}/progress",
            json={
                "course_id": course_id,
                **progress_data
            }
        )
```

#### Usage Examples

```python
# Example 1: Validate license on login
async def handle_login(license_key: str):
    gtm_client = CoursesGTMClient(GTM_API_URL, GTM_API_KEY)
    
    try:
        license_info = await gtm_client.validate_license(license_key)
        
        # Create session
        session = create_user_session(
            user_id=license_info["user_id"],
            tier=license_info["tier"],
            expires_at=license_info["expires_at"]
        )
        
        return session
        
    except LicenseInvalidError:
        raise HTTPException(401, "Invalid license key")

# Example 2: Check feature access before allowing download
async def download_video(video_id: str, user_id: str, quality: str):
    gtm_client = CoursesGTMClient(GTM_API_URL, GTM_API_KEY)
    
    # Check feature access
    has_access = await gtm_client.check_feature_access(
        user_id,
        "video_download"
    )
    
    if not has_access:
        raise HTTPException(403, "Upgrade to Intermediate for video downloads")
    
    # Check quality-specific access for 1080p
    if quality == "1080p":
        has_1080p = await gtm_client.check_feature_access(
            user_id,
            "video_download_1080p"
        )
        if not has_1080p:
            raise HTTPException(403, "1080p downloads require Advanced tier")
    
    # Track usage
    await gtm_client.track_usage(
        user_id=user_id,
        resource_type="video",
        resource_id=video_id,
        action="download",
        metadata={"quality": quality}
    )
    
    # Generate download URL
    return generate_video_download_url(video_id, quality)
```

---

### 2. SimulationPlayer Integration

**Purpose**: Launch simulations, track completion, sync results

#### API Endpoints

```python
# integrations/simulationplayer_client.py

class SimulationPlayerClient:
    """Client for SimulationPlayer API integration"""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=api_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )
    
    async def launch_simulation(
        self,
        simulation_id: str,
        user_id: str,
        context: Dict
    ) -> str:
        """
        Launch a simulation environment
        
        Args:
            simulation_id: Unique simulation identifier
            user_id: User ID
            context: Context data (course_id, module_id, lab_id)
        
        Returns:
            simulation_url: URL to access simulation
        """
        
        response = await self.client.post(
            "/api/simulations/launch",
            json={
                "simulation_id": simulation_id,
                "user_id": user_id,
                "context": context,
                "callback_url": f"{COURSEPLAYERAPP_API}/api/simulations/callback",
                "return_url": f"{COURSEPLAYERAPP_URL}/courses/{context['course_id']}"
            }
        )
        
        return response.json()["simulation_url"]
    
    async def get_simulation_progress(
        self,
        user_id: str,
        simulation_id: str
    ) -> Dict:
        """
        Get simulation completion status and results
        
        Returns:
            {
                "status": "completed" | "in_progress" | "not_started",
                "score": 85,
                "completed_at": "2026-01-12T10:30:00Z",
                "attempts": 2,
                "time_spent_seconds": 1200,
                "results": {...}
            }
        """
        
        response = await self.client.get(
            f"/api/simulations/{simulation_id}/progress",
            params={"user_id": user_id}
        )
        
        return response.json()
    
    async def get_available_simulations(
        self,
        course_id: str,
        user_tier: str
    ) -> List[Dict]:
        """
        Get simulations available for a course and tier
        
        Returns:
            [
                {
                    "simulation_id": "ml-gradient-descent-sim",
                    "title": "Gradient Descent Visualization",
                    "tier_required": "intermediate",
                    "accessible": True,
                    "estimated_time_minutes": 30
                },
                ...
            ]
        """
        
        response = await self.client.get(
            f"/api/courses/{course_id}/simulations",
            params={"tier": user_tier}
        )
        
        return response.json()["simulations"]
    
    async def record_simulation_result(
        self,
        user_id: str,
        simulation_id: str,
        result_data: Dict
    ):
        """
        Record simulation completion (called via callback)
        
        Args:
            user_id: User ID
            simulation_id: Simulation ID
            result_data: Simulation results
        """
        
        # Save to local database
        await db.execute(
            """
            INSERT INTO simulation_results
                (user_id, simulation_id, score, completed_at, result_data)
            VALUES
                (:user_id, :simulation_id, :score, NOW(), :result_data)
            """,
            {
                "user_id": user_id,
                "simulation_id": simulation_id,
                "score": result_data["score"],
                "result_data": json.dumps(result_data)
            }
        )
        
        # Update progress tracking
        await update_user_progress(
            user_id=user_id,
            resource_type="simulation",
            resource_id=simulation_id,
            status="completed"
        )
```

#### Usage Examples

```python
# Example 1: Launch simulation from lab
async def launch_sim_from_lab(lab_id: str, user_id: str):
    # Get lab configuration
    lab = await get_lab_config(lab_id)
    
    if not lab.get("simulation_id"):
        raise ValueError("This lab has no associated simulation")
    
    # Check tier access
    user = await get_user(user_id)
    if not can_access_simulation(user.tier, lab["simulation_tier"]):
        raise HTTPException(403, "Upgrade to access this simulation")
    
    # Launch simulation
    sim_client = SimulationPlayerClient(SIM_API_URL, SIM_API_KEY)
    
    simulation_url = await sim_client.launch_simulation(
        simulation_id=lab["simulation_id"],
        user_id=user_id,
        context={
            "course_id": lab["course_id"],
            "module_id": lab["module_id"],
            "lab_id": lab_id
        }
    )
    
    return {"simulation_url": simulation_url}

# Example 2: Display simulation progress in course page
async def get_course_simulation_status(course_id: str, user_id: str):
    sim_client = SimulationPlayerClient(SIM_API_URL, SIM_API_KEY)
    
    # Get available simulations for course
    simulations = await sim_client.get_available_simulations(
        course_id,
        user.tier
    )
    
    # Get progress for each
    results = []
    for sim in simulations:
        progress = await sim_client.get_simulation_progress(
            user_id,
            sim["simulation_id"]
        )
        
        results.append({
            **sim,
            "progress": progress
        })
    
    return results
```

---

### 3. CertificationExam Integration

**Purpose**: Launch exams, retrieve certificates, verify credentials

#### API Endpoints

```python
# integrations/certificationexam_client.py

class CertificationExamClient:
    """Client for CertificationExam API integration"""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=api_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )
    
    async def launch_exam(
        self,
        exam_id: str,
        user_id: str,
        tier: str
    ) -> str:
        """
        Launch certification exam
        
        Args:
            exam_id: Unique exam identifier
            user_id: User ID
            tier: User tier (affects certificate template)
        
        Returns:
            exam_url: URL to take exam
        """
        
        response = await self.client.post(
            "/api/exams/launch",
            json={
                "exam_id": exam_id,
                "user_id": user_id,
                "tier": tier,
                "callback_url": f"{COURSEPLAYERAPP_API}/api/exams/callback"
            }
        )
        
        return response.json()["exam_url"]
    
    async def get_exam_results(
        self,
        user_id: str,
        exam_id: str
    ) -> Dict:
        """
        Get exam score and status
        
        Returns:
            {
                "status": "passed" | "failed" | "in_progress",
                "score": 85,
                "passing_score": 70,
                "completed_at": "2026-01-12T15:00:00Z",
                "attempts": 1,
                "certificate_id": "CERT-123456"
            }
        """
        
        response = await self.client.get(
            f"/api/exams/{exam_id}/results",
            params={"user_id": user_id}
        )
        
        return response.json()
    
    async def get_user_certificates(
        self,
        user_id: str
    ) -> List[Dict]:
        """
        Get all certificates earned by user
        
        Returns:
            [
                {
                    "certificate_id": "CERT-123456",
                    "course_id": "ml-fundamentals",
                    "course_title": "Machine Learning Fundamentals",
                    "issue_date": "2026-01-12",
                    "grade": 92,
                    "tier": "intermediate",
                    "pdf_url": "https://...",
                    "png_url": "https://...",
                    "verification_url": "https://gai-observe.online/verify/...",
                    "blockchain_tx_id": "0x..." (if Advanced tier)
                },
                ...
            ]
        """
        
        response = await self.client.get(
            f"/api/users/{user_id}/certificates"
        )
        
        return response.json()["certificates"]
    
    async def download_certificate(
        self,
        certificate_id: str,
        format: str = "pdf"
    ) -> bytes:
        """
        Download certificate file
        
        Args:
            certificate_id: Certificate ID
            format: pdf, png, or svg
        
        Returns:
            Certificate file bytes
        """
        
        response = await self.client.get(
            f"/api/certificates/{certificate_id}/download",
            params={"format": format}
        )
        
        return response.content
    
    async def verify_certificate(
        self,
        certificate_id: str
    ) -> Dict:
        """
        Verify certificate authenticity
        
        Returns:
            {
                "valid": True,
                "student_name": "John Doe",
                "course": "Machine Learning Fundamentals",
                "issue_date": "2026-01-12",
                "grade": 92,
                "blockchain_verified": True,
                "blockchain_tx": "0x..."
            }
        """
        
        response = await self.client.get(
            f"/api/verify/{certificate_id}"
        )
        
        return response.json()
    
    async def check_exam_eligibility(
        self,
        user_id: str,
        course_id: str
    ) -> Dict:
        """
        Check if user is eligible to take final exam
        
        Returns:
            {
                "eligible": True,
                "requirements_met": {
                    "videos_completed": True,
                    "labs_completed": True,
                    "quizzes_passed": True
                },
                "completion_percentage": 100
            }
        """
        
        response = await self.client.get(
            f"/api/courses/{course_id}/exam/eligibility",
            params={"user_id": user_id}
        )
        
        return response.json()
```

#### Usage Examples

```python
# Example 1: Check exam eligibility and launch
async def start_certification_exam(course_id: str, user_id: str):
    exam_client = CertificationExamClient(EXAM_API_URL, EXAM_API_KEY)
    
    # Check eligibility
    eligibility = await exam_client.check_exam_eligibility(user_id, course_id)
    
    if not eligibility["eligible"]:
        missing = [k for k, v in eligibility["requirements_met"].items() if not v]
        raise HTTPException(
            403,
            f"Complete all requirements first: {', '.join(missing)}"
        )
    
    # Get user tier
    user = await get_user(user_id)
    
    # Launch exam
    exam_url = await exam_client.launch_exam(
        exam_id=f"{course_id}-final-exam",
        user_id=user_id,
        tier=user.tier
    )
    
    return {"exam_url": exam_url}

# Example 2: Display certificates in gallery
async def get_certificates_gallery(user_id: str):
    exam_client = CertificationExamClient(EXAM_API_URL, EXAM_API_KEY)
    
    certificates = await exam_client.get_user_certificates(user_id)
    
    return certificates
```

---

## Third-Party Integrations

### 4. OLLAMA (AI Service)

**Purpose**: Power AI Tutor functionality

```python
# integrations/ollama_client.py

import ollama

class OLLAMAClient:
    """Client for OLLAMA AI service"""
    
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.client = ollama.Client(host=host)
    
    async def generate_response(
        self,
        prompt: str,
        model: str = "llama3:70b",
        context: Optional[List] = None
    ) -> Dict:
        """
        Generate AI response
        
        Args:
            prompt: User prompt
            model: Model to use
            context: Conversation context
        
        Returns:
            {
                "response": "AI generated response",
                "model": "llama3:70b",
                "total_duration": 1234567890,
                "load_duration": 123456,
                "prompt_eval_duration": 234567
            }
        """
        
        response = await self.client.generate(
            model=model,
            prompt=prompt,
            context=context,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40
            }
        )
        
        return response
```

### 5. Video CDN (Cloudflare Stream / Bunny.net)

**Purpose**: Video delivery and streaming

```python
# integrations/video_cdn_client.py

class CloudflareStreamClient:
    """Client for Cloudflare Stream CDN"""
    
    async def get_video_url(
        self,
        video_id: str,
        user_id: str,
        tier: str
    ) -> str:
        """Generate signed HLS URL for video streaming"""
        
        # Generate signed token
        token = generate_signed_token(
            video_id=video_id,
            user_id=user_id,
            expires_in=3600  # 1 hour
        )
        
        return f"https://videodelivery.net/{video_id}/manifest/video.m3u8?token={token}"
    
    async def get_download_url(
        self,
        video_id: str,
        quality: str,
        user_id: str
    ) -> str:
        """Generate signed download URL"""
        
        # Check quota
        if not await check_download_quota(user_id):
            raise QuotaExceededError("Monthly download limit reached")
        
        # Generate signed download URL
        token = generate_download_token(
            video_id=video_id,
            quality=quality,
            user_id=user_id,
            expires_in=1800  # 30 minutes
        )
        
        return f"https://videodelivery.net/{video_id}/downloads/{quality}.mp4?token={token}"
```

---

## Webhook Callbacks

### Simulation Completion Callback

```python
# api/webhooks.py

@app.post("/api/simulations/callback")
async def simulation_completion_callback(
    payload: Dict,
    signature: str = Header(None)
):
    """
    Receive simulation completion notification from SimulationPlayer
    
    Payload:
        {
            "user_id": "user123",
            "simulation_id": "ml-sim-001",
            "status": "completed",
            "score": 85,
            "time_spent": 1200,
            "results": {...}
        }
    """
    
    # Verify webhook signature
    if not verify_webhook_signature(payload, signature, SIM_WEBHOOK_SECRET):
        raise HTTPException(401, "Invalid signature")
    
    # Record result
    await record_simulation_result(
        user_id=payload["user_id"],
        simulation_id=payload["simulation_id"],
        result_data=payload
    )
    
    # Update progress
    await update_user_progress(
        user_id=payload["user_id"],
        resource_type="simulation",
        resource_id=payload["simulation_id"],
        status="completed"
    )
    
    # Award achievement if applicable
    if payload["score"] >= 90:
        await award_achievement(payload["user_id"], "simulation_master")
    
    return {"status": "received"}
```

### Exam Completion Callback

```python
@app.post("/api/exams/callback")
async def exam_completion_callback(
    payload: Dict,
    signature: str = Header(None)
):
    """
    Receive exam completion notification from CertificationExam
    
    Payload:
        {
            "user_id": "user123",
            "exam_id": "ml-final-exam",
            "score": 92,
            "status": "passed",
            "certificate_id": "CERT-123456"
        }
    """
    
    # Verify signature
    if not verify_webhook_signature(payload, signature, EXAM_WEBHOOK_SECRET):
        raise HTTPException(401, "Invalid signature")
    
    # Update course completion
    if payload["status"] == "passed":
        await mark_course_complete(
            user_id=payload["user_id"],
            course_id=extract_course_id(payload["exam_id"])
        )
        
        # Award completion achievement
        await award_achievement(payload["user_id"], "course_graduate")
    
    return {"status": "received"}
```

---

## Error Handling

### Retry Logic

```python
# integrations/retry_handler.py

from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def api_call_with_retry(func, *args, **kwargs):
    """Retry API calls with exponential backoff"""
    return await func(*args, **kwargs)
```

### Circuit Breaker

```python
# integrations/circuit_breaker.py

from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
async def call_external_api(client, method, *args, **kwargs):
    """Call external API with circuit breaker"""
    return await getattr(client, method)(*args, **kwargs)
```

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [Feature Gating](./FEATURE_GATING.md)
- [Certificate Display](./CERTIFICATE_DISPLAY.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
