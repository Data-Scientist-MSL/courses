# CoursePlayerApp - Component Specifications

## Overview

This document provides detailed specifications for all major components in CoursePlayerApp. Each component is designed with tier-based feature gating, consistent APIs, and integration with CoursesGTM for access control.

## Component Architecture Pattern

All components follow a consistent pattern:

```python
class Component:
    def __init__(self, course_id: str, resource_id: str):
        self.course_id = course_id
        self.resource_id = resource_id
        self.gtm_client = CoursesGTMClient.get_instance()
        
    def render(self) -> None:
        """Main rendering method with feature gate checks"""
        if not self._check_access():
            self._render_upgrade_prompt()
            return
        self._render_content()
    
    def _check_access(self) -> bool:
        """Verify user has access to this component"""
        return self.gtm_client.can_access_resource(
            self.course_id, 
            self.resource_id
        )
```

---

## 1. Video Player Component

### Purpose
Provides adaptive video playback with tier-based features including streaming, downloads, transcripts, and interactive annotations.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Streaming (HLS/DASH) | ✅ | ✅ | ✅ |
| Quality Selection | 720p max | 1080p | 4K |
| Download for Offline | ❌ | ✅ | ✅ |
| Playback Speed Control | 1x only | 0.5x - 2x | 0.25x - 3x |
| Transcripts/Captions | ❌ | ✅ | ✅ |
| Interactive Annotations | ❌ | ❌ | ✅ |
| Bookmarks | ❌ | ✅ | ✅ |
| Watch History | ✅ | ✅ | ✅ |

### API Usage

```python
from courseplayerapp.components import VideoPlayer

# Initialize video player
player = VideoPlayer(
    course_id="data-science-101",
    video_id="intro-to-pandas"
)

# Render in Streamlit
player.render()

# Advanced: Custom configuration
player = VideoPlayer(
    course_id="ml-advanced",
    video_id="neural-networks-deep-dive",
    autoplay=False,
    start_time=120,  # Start at 2 minutes
    quality_preference="1080p"
)
player.render()
```

### Feature Gates

- `video_streaming`: Always enabled (all tiers)
- `video_download`: Intermediate, Advanced
- `video_transcript`: Intermediate, Advanced
- `video_annotations`: Advanced only
- `video_bookmarks`: Intermediate, Advanced

### Component Structure

```python
class VideoPlayer:
    def render(self):
        """Main render method"""
        # Display video player
        st.video(self._get_stream_url())
        
        # Show controls based on tier
        if self._has_feature('video_download'):
            st.download_button("Download Video", ...)
        
        if self._has_feature('video_transcript'):
            self._render_transcript()
        
        if self._has_feature('video_annotations'):
            self._render_annotations()
    
    def _get_stream_url(self) -> str:
        """Get HLS/DASH stream URL based on tier"""
        tier = self.gtm_client.get_user_tier()
        quality = self._get_max_quality(tier)
        return f"{CDN_URL}/{self.video_id}/playlist_{quality}.m3u8"
    
    def _get_max_quality(self, tier: str) -> str:
        quality_map = {
            "basic": "720p",
            "intermediate": "1080p",
            "advanced": "4k"
        }
        return quality_map.get(tier, "720p")
```

### Dependencies

- **Video.js**: HTML5 video player
- **HLS.js**: HLS streaming support
- **Streamlit**: UI framework
- **CoursesGTM SDK**: Access control
- **FFmpeg**: Video processing (backend)

### Security Considerations

- **DRM Protection**: Optional for premium content
- **Signed URLs**: Time-limited access to streams
- **Download Limits**: Track and enforce download quotas
- **Watermarking**: Embed user ID in downloaded videos

---

## 2. Slides Viewer Component

### Purpose
Display presentation slides with tier-based export and download capabilities.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| View Slides In-App | ✅ | ✅ | ✅ |
| Navigation Controls | ✅ | ✅ | ✅ |
| Search in Slides | ❌ | ✅ | ✅ |
| PDF Export | ❌ | ✅ | ✅ |
| Source Download (Marp/PPTX) | ❌ | ❌ | ✅ |
| Print | ❌ | ✅ | ✅ |
| Annotations | ❌ | ❌ | ✅ |

### API Usage

```python
from courseplayerapp.components import SlidesViewer

# Initialize slides viewer
viewer = SlidesViewer(
    course_id="data-science-101",
    slide_deck_id="intro-to-ml"
)

# Render in Streamlit
viewer.render()

# Advanced: Jump to specific slide
viewer = SlidesViewer(
    course_id="data-science-101",
    slide_deck_id="intro-to-ml",
    start_slide=5
)
viewer.render()
```

### Feature Gates

- `slide_view`: Always enabled
- `slide_download`: Intermediate, Advanced (PDF export)
- `slide_source_download`: Advanced only (source files)
- `slide_search`: Intermediate, Advanced
- `slide_annotations`: Advanced only

### Component Structure

```python
class SlidesViewer:
    def render(self):
        """Render slide deck"""
        # Display current slide
        self._display_slide(st.session_state.current_slide)
        
        # Navigation
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button("← Previous"):
                self._previous_slide()
        with col3:
            if st.button("Next →"):
                self._next_slide()
        
        # Export options
        if self._has_feature('slide_download'):
            st.download_button("Download as PDF", ...)
        
        if self._has_feature('slide_source_download'):
            st.download_button("Download Source", ...)
    
    def _display_slide(self, slide_num: int):
        """Display slide as image or HTML"""
        slide_url = self._get_slide_url(slide_num)
        st.image(slide_url, use_column_width=True)
```

### Dependencies

- **PDF.js**: PDF rendering
- **Marp**: Markdown slide generation
- **Streamlit**: UI framework
- **Pillow**: Image processing

### Security Considerations

- **Watermarking**: Add user ID to exported PDFs
- **Download Tracking**: Monitor export frequency
- **Content Protection**: Disable right-click/screenshots (optional)

---

## 3. Lab Runner Component

### Purpose
Execute Jupyter notebooks with tier-appropriate execution environments, from view-only to full JupyterLab with GPU access.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| View Static Notebook | ✅ | ✅ | ✅ |
| Interactive Execution | ❌ | ✅ (JupyterLite) | ✅ (JupyterLab) |
| Edit Cells | ❌ | ✅ | ✅ |
| Download Notebook | ❌ | ✅ | ✅ |
| Install Packages | ❌ | Limited | Full |
| GPU Access | ❌ | ❌ | ✅ |
| Persistent Environment | ❌ | ❌ | ✅ |
| Save Progress | ❌ | Browser only | Server-side |
| Custom Kernels | ❌ | ❌ | ✅ |

### API Usage

```python
from courseplayerapp.components import LabRunner

# Initialize lab runner
lab = LabRunner(
    course_id="data-science-101",
    lab_id="pandas-tutorial"
)

# Render in Streamlit
lab.render()

# Advanced: Configure execution environment
lab = LabRunner(
    course_id="ml-advanced",
    lab_id="gpu-training",
    kernel="python3",
    gpu_enabled=True,
    memory_limit="8GB"
)
lab.render()
```

### Feature Gates

- `notebook_view`: Always enabled
- `notebook_execution`: Intermediate, Advanced
- `notebook_download`: Intermediate, Advanced
- `notebook_gpu`: Advanced only
- `notebook_persistence`: Advanced only

### Component Structure

```python
class LabRunner:
    def render(self):
        """Render notebook interface"""
        tier = self.gtm_client.get_user_tier()
        
        if tier == "basic":
            self._render_static_notebook()
        elif tier == "intermediate":
            self._render_jupyterlite()
        else:  # advanced
            self._render_jupyterlab()
        
        if self._has_feature('notebook_download'):
            self._render_download_button()
    
    def _render_static_notebook(self):
        """Display notebook as HTML"""
        html = self._get_notebook_html()
        st.components.v1.html(html, height=800, scrolling=True)
    
    def _render_jupyterlite(self):
        """Embed JupyterLite iframe"""
        jupyterlite_url = self._get_jupyterlite_url()
        st.components.v1.iframe(jupyterlite_url, height=800)
    
    def _render_jupyterlab(self):
        """Launch full JupyterLab session"""
        lab_url = self._create_jupyterlab_session()
        st.markdown(f"[Open in JupyterLab]({lab_url})")
        
        # Embed option
        if st.checkbox("Embed in page"):
            st.components.v1.iframe(lab_url, height=800)
```

### Dependencies

- **JupyterLite**: Browser-based Jupyter (Intermediate)
- **JupyterLab**: Full Jupyter environment (Advanced)
- **Pyodide**: Python in browser (JupyterLite)
- **nbconvert**: Notebook conversion
- **Docker**: Container isolation (Advanced)

### Security Considerations

- **Sandboxed Execution**: Isolated file system access
- **Resource Limits**: CPU/memory quotas
- **Network Isolation**: Restricted internet access
- **Code Review**: Static analysis before execution
- **Timeout**: Maximum execution time
- **Storage Quotas**: Limit persistent storage

---

## 4. AI Tutor Component

### Purpose
OLLAMA-powered course assistant providing context-aware help with tier-based quotas and model selection.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| AI Tutor Access | ❌ | ✅ | ✅ |
| Questions per Month | 0 | 50 | Unlimited |
| Model | - | llama3.2:3b | llama3.1:8b |
| Response Priority | - | Standard | High |
| Context Window | - | 2K tokens | 8K tokens |
| Quota Rollover | - | No | Yes |
| Conversation History | - | 24 hours | 30 days |
| Custom Instructions | - | No | Yes |

### API Usage

```python
from courseplayerapp.components import AITutorChat

# Initialize AI tutor
tutor = AITutorChat(
    course_id="data-science-101"
)

# Render chat interface
tutor.render()

# Advanced: Configure behavior
tutor = AITutorChat(
    course_id="ml-advanced",
    system_prompt="You are an expert ML engineer...",
    temperature=0.7,
    max_tokens=500
)
tutor.render()
```

### Feature Gates

- `ai_tutor`: Intermediate, Advanced
- `ai_tutor_quota`: Tier-specific limits
- `ai_tutor_priority`: Advanced only
- `ai_tutor_history`: Tier-specific retention

### Quota Management

```python
class AITutorChat:
    def _check_quota(self) -> bool:
        """Check if user has remaining quota"""
        tier = self.gtm_client.get_user_tier()
        
        if tier == "advanced":
            return True  # Unlimited
        
        usage = self.gtm_client.get_feature_usage("ai_tutor_quota")
        limit = 50  # Intermediate tier limit
        
        return usage < limit
    
    def _track_usage(self):
        """Increment usage counter"""
        self.gtm_client.track_feature_usage(
            feature="ai_tutor_quota",
            course_id=self.course_id
        )
```

### Component Structure

```python
class AITutorChat:
    def render(self):
        """Render chat interface"""
        # Check access
        if not self._has_feature('ai_tutor'):
            self._render_upgrade_prompt()
            return
        
        # Check quota
        if not self._check_quota():
            self._render_quota_exceeded()
            return
        
        # Display chat interface
        self._render_chat_history()
        
        # Input field
        user_input = st.chat_input("Ask a question...")
        if user_input:
            self._handle_message(user_input)
    
    def _handle_message(self, message: str):
        """Process user message"""
        # Build context from course materials
        context = self._build_context()
        
        # Get AI response
        response = self._query_ollama(message, context)
        
        # Track usage
        self._track_usage()
        
        # Display response
        self._add_to_history(message, response)
```

### Context Building (RAG)

```python
def _build_context(self) -> str:
    """Build context from course materials"""
    # Get current lesson
    current_lesson = self._get_current_lesson()
    
    # Extract relevant content
    content = []
    content.append(current_lesson.transcript)
    content.append(current_lesson.slides_text)
    content.append(current_lesson.notes)
    
    # Vector search for relevant materials
    query_embedding = self._get_embedding(st.session_state.last_user_message)
    similar_content = self._vector_search(query_embedding, top_k=3)
    content.extend(similar_content)
    
    return "\n\n".join(content)
```

### Dependencies

- **OLLAMA**: Local LLM inference
- **LangChain**: Prompt management and RAG
- **ChromaDB**: Vector database for embeddings
- **Sentence Transformers**: Embedding models
- **Streamlit**: Chat UI

### Security Considerations

- **Input Sanitization**: Clean user inputs
- **Output Filtering**: Remove sensitive information
- **Rate Limiting**: Prevent abuse
- **Quota Enforcement**: Hard limits on usage
- **Content Moderation**: Filter inappropriate content

---

## 5. Quiz Engine Component

### Purpose
Deliver assessments and knowledge checks with auto-grading and performance analytics.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Multiple Choice | ✅ | ✅ | ✅ |
| Code Challenges | ✅ | ✅ | ✅ |
| Free Response | ✅ | ✅ | ✅ |
| Auto-Grading | ✅ | ✅ | ✅ |
| Unlimited Attempts | ✅ | ✅ | ✅ |
| Detailed Explanations | ✅ | ✅ | ✅ |
| Performance Analytics | Basic | Detailed | Advanced |
| Peer Comparison | ❌ | ✅ | ✅ |
| Export Results | ❌ | ✅ | ✅ |

### API Usage

```python
from courseplayerapp.components import QuizEngine

# Initialize quiz
quiz = QuizEngine(
    course_id="data-science-101",
    quiz_id="pandas-basics"
)

# Render quiz
quiz.render()

# Custom configuration
quiz = QuizEngine(
    course_id="ml-advanced",
    quiz_id="neural-networks",
    shuffle_questions=True,
    show_feedback=True,
    passing_score=80
)
quiz.render()
```

### Feature Gates

- `quiz_access`: Always enabled
- `quiz_analytics`: Tier-based detail level
- `quiz_export`: Intermediate, Advanced

### Component Structure

```python
class QuizEngine:
    def render(self):
        """Render quiz interface"""
        # Load quiz data
        quiz_data = self._load_quiz()
        
        # Display questions
        for i, question in enumerate(quiz_data.questions):
            self._render_question(i, question)
        
        # Submit button
        if st.button("Submit Quiz"):
            self._grade_quiz()
            self._show_results()
    
    def _render_question(self, index: int, question: dict):
        """Render individual question"""
        st.subheader(f"Question {index + 1}")
        st.markdown(question['text'])
        
        if question['type'] == 'multiple_choice':
            answer = st.radio(
                "Select answer:",
                question['options'],
                key=f"q_{index}"
            )
        elif question['type'] == 'code':
            answer = st.text_area(
                "Enter your code:",
                key=f"q_{index}"
            )
        elif question['type'] == 'free_response':
            answer = st.text_input(
                "Your answer:",
                key=f"q_{index}"
            )
        
        st.session_state.answers[index] = answer
    
    def _grade_quiz(self) -> dict:
        """Auto-grade quiz responses"""
        results = {
            'score': 0,
            'total': len(self.quiz_data.questions),
            'feedback': []
        }
        
        for i, question in enumerate(self.quiz_data.questions):
            user_answer = st.session_state.answers.get(i)
            is_correct = self._check_answer(question, user_answer)
            
            if is_correct:
                results['score'] += 1
            
            results['feedback'].append({
                'question': i,
                'correct': is_correct,
                'explanation': question.get('explanation', '')
            })
        
        return results
```

### Dependencies

- **Streamlit**: UI framework
- **CodeRunner**: Execute code challenges safely
- **CoursesGTM SDK**: Progress tracking

### Security Considerations

- **Code Execution**: Sandboxed environment for code challenges
- **Time Limits**: Prevent long-running code
- **Input Validation**: Sanitize all inputs

---

## 6. Progress Tracker Component

### Purpose
Track and visualize course completion, learning streaks, and achievements.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Lesson Completion | ✅ | ✅ | ✅ |
| Progress Percentage | ✅ | ✅ | ✅ |
| Learning Streak | ✅ | ✅ | ✅ |
| Time Estimates | ✅ | ✅ | ✅ |
| Achievement Badges | ✅ | ✅ | ✅ |
| Detailed Analytics | ❌ | ✅ | ✅ |
| Export Progress | ❌ | ✅ | ✅ |
| Goal Setting | ❌ | ✅ | ✅ |
| Leaderboard | ❌ | ❌ | ✅ |

### API Usage

```python
from courseplayerapp.components import ProgressDashboard

# Initialize dashboard
dashboard = ProgressDashboard(
    user_id="user123"
)

# Render dashboard
dashboard.render()

# Course-specific progress
dashboard = ProgressDashboard(
    user_id="user123",
    course_id="data-science-101"
)
dashboard.render()
```

### Feature Gates

- `progress_tracking`: Always enabled
- `progress_analytics`: Intermediate, Advanced
- `progress_export`: Intermediate, Advanced
- `progress_leaderboard`: Advanced only

### Component Structure

```python
class ProgressDashboard:
    def render(self):
        """Render progress dashboard"""
        # Overall stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Courses Completed", self._get_completed_count())
        with col2:
            st.metric("Current Streak", f"{self._get_streak()} days")
        with col3:
            st.metric("Total Hours", self._get_total_hours())
        with col4:
            st.metric("Achievements", self._get_achievement_count())
        
        # Course progress
        self._render_course_progress()
        
        # Learning streak calendar
        self._render_streak_calendar()
        
        # Achievements
        self._render_achievements()
        
        # Analytics (tier-gated)
        if self._has_feature('progress_analytics'):
            self._render_analytics()
    
    def _render_course_progress(self):
        """Display progress for each course"""
        courses = self._get_enrolled_courses()
        
        for course in courses:
            progress = self._get_course_progress(course.id)
            
            st.subheader(course.title)
            st.progress(progress / 100)
            st.caption(f"{progress}% complete")
```

### Dependencies

- **Streamlit**: UI framework
- **Plotly**: Interactive charts
- **CoursesGTM SDK**: Progress data

---

## 7. Certificate Generator Component

### Purpose
Generate verifiable completion certificates with tier-appropriate features and verification.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Certificate Generation | ❌ | ✅ | ✅ |
| Certificate Type | - | Verifiable PDF | Professional Signed |
| QR Code Verification | - | ✅ | ✅ |
| Digital Signature | - | Standard | Enhanced |
| Custom Branding | - | ❌ | ✅ |
| LinkedIn Share | - | ✅ | ✅ |
| Blockchain Verification | - | ❌ | 🔜 Future |
| Print-Ready Format | - | ✅ | ✅ |

### API Usage

```python
from courseplayerapp.components import CertificateGenerator

# Generate certificate
cert_gen = CertificateGenerator(
    user_id="user123",
    course_id="data-science-101"
)

# Check eligibility and generate
if cert_gen.is_eligible():
    certificate = cert_gen.generate()
    st.download_button("Download Certificate", certificate)

# Render certificate preview
cert_gen.render()
```

### Feature Gates

- `certificate_generation`: Intermediate, Advanced
- `certificate_type`: Tier-specific types
- `certificate_branding`: Advanced only

### Component Structure

```python
class CertificateGenerator:
    def is_eligible(self) -> bool:
        """Check if user can receive certificate"""
        # Must have appropriate tier
        if not self._has_feature('certificate_generation'):
            return False
        
        # Must have completed course
        progress = self.gtm_client.get_course_progress(
            self.user_id,
            self.course_id
        )
        return progress >= 100
    
    def generate(self) -> bytes:
        """Generate certificate PDF"""
        tier = self.gtm_client.get_user_tier()
        
        # Create PDF
        pdf = self._create_pdf_base()
        
        # Add content
        self._add_user_info(pdf)
        self._add_course_info(pdf)
        self._add_completion_date(pdf)
        
        # Add QR code for verification
        verification_url = self._generate_verification_url()
        self._add_qr_code(pdf, verification_url)
        
        # Add signature
        if tier == "advanced":
            self._add_digital_signature(pdf)
        
        return pdf.getvalue()
    
    def _generate_verification_url(self) -> str:
        """Create unique verification URL"""
        cert_id = self._generate_cert_id()
        return f"https://gai-observe.online/verify/{cert_id}"
```

### Dependencies

- **ReportLab**: PDF generation
- **Cryptography**: Digital signatures
- **qrcode**: QR code generation
- **Pillow**: Image processing

### Security Considerations

- **Unique IDs**: Prevent certificate duplication
- **Digital Signatures**: Verify authenticity
- **Tamper Detection**: Detect modified certificates
- **Verification API**: Public endpoint for validation

---

## 8. Dataset Explorer Component

### Purpose
Browse and download course datasets with tier-based access to standard and production-grade datasets.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Dataset Access | ❌ | ✅ | ✅ |
| Dataset Types | - | Standard | Standard + Production |
| Preview Data | - | ✅ | ✅ |
| Download Formats | - | CSV, JSON | All formats |
| Sample Size | - | 100 rows | Full dataset |
| Data Dictionary | - | ✅ | ✅ |
| SQL Export | - | ❌ | ✅ |
| API Access | - | ❌ | ✅ |

### API Usage

```python
from courseplayerapp.components import DatasetExplorer

# Initialize explorer
explorer = DatasetExplorer(
    course_id="data-science-101"
)

# Render explorer
explorer.render()

# Access specific dataset
explorer = DatasetExplorer(
    course_id="ml-advanced",
    dataset_id="customer-churn"
)
explorer.render()
```

### Feature Gates

- `datasets`: Intermediate, Advanced
- `datasets_production`: Advanced only
- `datasets_api`: Advanced only

### Component Structure

```python
class DatasetExplorer:
    def render(self):
        """Render dataset browser"""
        # Check access
        if not self._has_feature('datasets'):
            self._render_upgrade_prompt()
            return
        
        # List available datasets
        datasets = self._get_available_datasets()
        
        # Filter by tier
        tier = self.gtm_client.get_user_tier()
        if tier != "advanced":
            datasets = [d for d in datasets if d.type != "production"]
        
        # Display dataset list
        selected = st.selectbox(
            "Select Dataset",
            datasets,
            format_func=lambda d: d.name
        )
        
        if selected:
            self._render_dataset_details(selected)
    
    def _render_dataset_details(self, dataset):
        """Show dataset preview and download options"""
        # Metadata
        st.subheader(dataset.name)
        st.markdown(dataset.description)
        
        # Preview
        preview_df = self._load_preview(dataset)
        st.dataframe(preview_df)
        
        # Download options
        tier = self.gtm_client.get_user_tier()
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("Download CSV", ...)
        
        if tier == "advanced":
            with col2:
                st.download_button("Download Parquet", ...)
```

### Dependencies

- **Pandas**: Data manipulation
- **Streamlit**: UI framework
- **PyArrow**: Parquet support

---

## 9. Code Review Component

### Purpose
Submit projects for automated and manual code review with tier-based review types and quotas.

### Tier-Based Features

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Code Review Access | ❌ | ✅ | ✅ |
| Review Type | - | Automated | Automated + Manual |
| Submissions per Course | - | 3 | 5 |
| Review Turnaround | - | Instant | 24-48 hours |
| Detailed Feedback | - | ✅ | ✅ |
| Code Quality Score | - | ✅ | ✅ |
| Video Feedback | - | ❌ | ✅ |
| Revision Submissions | - | 1 | 3 |

### API Usage

```python
from courseplayerapp.components import CodeReview

# Initialize code review
review = CodeReview(
    user_id="user123",
    submission_id="proj-001"
)

# Render submission interface
review.render()

# Submit code
review = CodeReview(user_id="user123")
review.submit_code(
    course_id="ml-advanced",
    project_id="capstone",
    files=uploaded_files
)
```

### Feature Gates

- `code_review`: Intermediate, Advanced
- `code_review_quota`: Tier-specific limits
- `code_review_manual`: Advanced only

### Component Structure

```python
class CodeReview:
    def render(self):
        """Render code review interface"""
        # Check access and quota
        if not self._check_quota():
            self._render_quota_exceeded()
            return
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload project files",
            accept_multiple_files=True
        )
        
        # Submission details
        description = st.text_area("Project description")
        
        # Submit button
        if st.button("Submit for Review"):
            self._submit_for_review(uploaded_files, description)
    
    def _submit_for_review(self, files, description):
        """Submit code for review"""
        # Run automated checks
        results = self._run_static_analysis(files)
        results.update(self._run_style_check(files))
        results.update(self._run_ai_review(files))
        
        # Queue for manual review (Advanced tier)
        if self._has_feature('code_review_manual'):
            self._queue_manual_review(files, description, results)
        
        # Display results
        self._display_results(results)
        
        # Track usage
        self._track_submission()
```

### Dependencies

- **Pylint/Flake8**: Static analysis
- **Black**: Code formatting checks
- **AI Model**: Code review feedback
- **GitHub API**: For repository submissions

### Security Considerations

- **File Scanning**: Virus and malware detection
- **Size Limits**: Prevent large uploads
- **Execution Safety**: Never execute submitted code
- **Privacy**: Secure storage of submissions

---

## Component Communication

### Event System

Components communicate via Streamlit session state and a simple event system:

```python
# Publishing an event
st.session_state.event_bus.publish(
    "lesson_completed",
    {
        "course_id": "data-science-101",
        "lesson_id": "intro-to-pandas"
    }
)

# Subscribing to events
st.session_state.event_bus.subscribe(
    "lesson_completed",
    self._on_lesson_complete
)
```

### Shared State

Common state management pattern:

```python
class ComponentState:
    @staticmethod
    def get_current_course() -> str:
        return st.session_state.get('current_course_id')
    
    @staticmethod
    def set_current_course(course_id: str):
        st.session_state.current_course_id = course_id
    
    @staticmethod
    def get_user_tier() -> str:
        return st.session_state.get('user_tier', 'basic')
```

## Testing Components

Each component includes unit tests:

```python
def test_video_player_basic_tier():
    """Test video player with basic tier"""
    player = VideoPlayer("course-1", "video-1")
    
    # Mock tier
    with mock_tier("basic"):
        assert not player._has_feature('video_download')
        assert player._get_max_quality("basic") == "720p"

def test_ai_tutor_quota():
    """Test AI tutor quota enforcement"""
    tutor = AITutorChat("course-1")
    
    # Mock intermediate tier with quota exceeded
    with mock_tier("intermediate"), mock_usage(50):
        assert not tutor._check_quota()
```

## Related Documentation

- [Architecture](./ARCHITECTURE.md)
- [Feature Gates](./FEATURE_GATES.md)
- [Integration Guide](./INTEGRATION.md)
- [UI/UX Specifications](./UI_UX_SPEC.md)
