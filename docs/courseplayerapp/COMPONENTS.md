# CoursePlayerApp Components Specification

This document provides detailed specifications for all major components in CoursePlayerApp, including tier-based behavior, API dependencies, UI mockups, and implementation guidelines.

## Table of Contents

1. [Video Player Component](#video-player-component)
2. [AI Tutor Component](#ai-tutor-component)
3. [Lab Runner Component](#lab-runner-component)
4. [Quiz Engine Component](#quiz-engine-component)
5. [Progress Tracker Component](#progress-tracker-component)
6. [Certificate Generator Component](#certificate-generator-component)
7. [Dataset Explorer Component](#dataset-explorer-component)
8. [Code Review Component](#code-review-component)

---

## Video Player Component

### Purpose
Deliver video lessons with adaptive features based on license tier, supporting streaming, downloading, and enhanced playback features.

### Tier-Based Behavior

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Streaming (HLS/DASH) | ✅ | ✅ | ✅ |
| Quality Selection | Auto only | Manual selection | Manual + Auto |
| Playback Speed | 1x only | 0.5x - 2x | 0.25x - 3x |
| Download | ❌ | ✅ (720p max) | ✅ (1080p) |
| Transcripts | ❌ | View only | View + Search |
| Annotations | ❌ | ❌ | ✅ Create notes |
| Offline Playback | ❌ | Limited | Full support |
| Picture-in-Picture | ❌ | ✅ | ✅ |

### Implementation

**File**: `courseplayerapp/components/video/player.py`

```python
import streamlit as st
from typing import Optional, Dict, List
from courseplayerapp.middleware.feature_gates import requires_feature, requires_tier
from courseplayerapp.integrations.coursesgtm_client import CoursesGTMClient

class VideoPlayer:
    """
    Video player component with tier-aware features.
    """
    
    def __init__(self, video_id: str, coursesgtm_client: CoursesGTMClient):
        self.video_id = video_id
        self.client = coursesgtm_client
        self.tier = st.session_state.get('tier', 'basic')
        
    def render(self):
        """Render the video player UI"""
        video_data = self.client.get_video_metadata(self.video_id)
        
        # Video player container
        st.video(video_data['stream_url'])
        
        # Tier-based controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self._render_quality_selector(video_data)
        
        with col2:
            self._render_speed_control()
        
        with col3:
            self._render_download_button(video_data)
        
        # Advanced features
        if self.tier in ['intermediate', 'advanced']:
            self._render_transcript_panel(video_data)
        
        if self.tier == 'advanced':
            self._render_annotation_panel(video_data)
    
    def _render_quality_selector(self, video_data: Dict):
        """Quality selection based on tier"""
        if self.tier == 'basic':
            st.caption("Quality: Auto")
        else:
            qualities = video_data.get('available_qualities', ['auto', '720p', '1080p'])
            st.selectbox("Quality", qualities, key=f"quality_{self.video_id}")
    
    def _render_speed_control(self):
        """Playback speed control"""
        if self.tier == 'basic':
            st.caption("Speed: 1x")
        elif self.tier == 'intermediate':
            st.select_slider("Speed", options=[0.5, 0.75, 1.0, 1.25, 1.5, 2.0], value=1.0)
        else:  # advanced
            st.select_slider("Speed", options=[0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0], value=1.0)
    
    @requires_feature('video_download')
    def _render_download_button(self, video_data: Dict):
        """Download button for Intermediate+ tiers"""
        max_quality = '720p' if self.tier == 'intermediate' else '1080p'
        if st.button(f"Download ({max_quality})"):
            self._initiate_download(video_data, max_quality)
    
    def _render_transcript_panel(self, video_data: Dict):
        """Transcript viewer"""
        with st.expander("📝 Transcript"):
            transcript = self.client.get_video_transcript(self.video_id)
            
            if self.tier == 'advanced':
                # Searchable transcript
                search_query = st.text_input("Search transcript", key=f"search_{self.video_id}")
                if search_query:
                    transcript = self._highlight_search_results(transcript, search_query)
            
            st.markdown(transcript)
    
    @requires_tier('advanced')
    def _render_annotation_panel(self, video_data: Dict):
        """Personal note-taking panel"""
        with st.expander("✏️ My Notes"):
            timestamp = st.time_input("Timestamp")
            note = st.text_area("Note")
            if st.button("Save Note"):
                self.client.save_video_note(self.video_id, timestamp, note)
```

### API Dependencies

**CoursesGTM Calls:**
- `GET /api/v1/videos/{video_id}/metadata` - Get video details
- `GET /api/v1/videos/{video_id}/stream-url` - Get streaming URL
- `GET /api/v1/videos/{video_id}/transcript` - Get transcript text
- `POST /api/v1/videos/{video_id}/download` - Initiate download (Intermediate+)
- `POST /api/v1/videos/{video_id}/notes` - Save annotation (Advanced)
- `GET /api/v1/license/check-feature?feature=video_download` - Feature check

### UI States

```
┌─────────────────────────────────────────┐
│  Video Lesson: Introduction to ML       │
├─────────────────────────────────────────┤
│                                         │
│     ┌───────────────────────────┐      │
│     │                           │      │
│     │   [Video Player Area]     │      │
│     │                           │      │
│     └───────────────────────────┘      │
│                                         │
│  Quality: [Auto ▼]  Speed: [1x ▼]      │
│                                         │
│  [Download] (Intermediate+)             │
│                                         │
│  📝 Transcript (Intermediate+)          │
│  └─ Searchable (Advanced)               │
│                                         │
│  ✏️ My Notes (Advanced)                 │
│  └─ Timestamp + Note                    │
└─────────────────────────────────────────┘
```

### Configuration Options

**`config/feature_flags.json`**:
```json
{
  "video_streaming": {
    "enabled_tiers": ["basic", "intermediate", "advanced"]
  },
  "video_download": {
    "enabled_tiers": ["intermediate", "advanced"],
    "max_quality_by_tier": {
      "intermediate": "720p",
      "advanced": "1080p"
    }
  },
  "video_transcripts": {
    "enabled_tiers": ["intermediate", "advanced"]
  },
  "video_annotations": {
    "enabled_tiers": ["advanced"]
  }
}
```

### Error Handling

- **Stream Failure**: Retry with lower quality, show error message
- **Download Failure**: Queue for background retry, notify user
- **Transcript Unavailable**: Show "Transcript not available" message
- **Quota Exceeded**: Prompt to upgrade or wait for quota reset

---

## AI Tutor Component

### Purpose
Provide AI-powered tutoring assistance with context awareness from course content, quota management, and tier-based model selection.

### Tier-Based Behavior

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Access | ❌ | ✅ | ✅ |
| Questions/Month | 0 | 50 | Unlimited |
| Model | N/A | llama3.2:3b | llama3.1:8b |
| Context Window | N/A | 4K tokens | 8K tokens |
| Response Priority | N/A | Normal | High priority |
| Chat Export | ❌ | ❌ | ✅ PDF/Markdown |
| Code Highlighting | ❌ | ✅ | ✅ + Execution |
| Conversation History | ❌ | 10 chats | Unlimited |

### Implementation

**File**: `courseplayerapp/components/ai_tutor/chat_interface.py`

```python
import streamlit as st
from typing import List, Dict
from courseplayerapp.middleware.feature_gates import requires_tier, quota_limited
from courseplayerapp.integrations.ollama_client import OllamaClient
from courseplayerapp.integrations.coursesgtm_client import CoursesGTMClient

class AITutorChat:
    """
    AI Tutor chat interface with RAG and quota management.
    """
    
    def __init__(self, course_id: str):
        self.course_id = course_id
        self.tier = st.session_state.get('tier', 'basic')
        self.ollama = OllamaClient()
        self.gtm = CoursesGTMClient()
        
        # Model selection by tier
        self.model = {
            'intermediate': 'llama3.2:3b',
            'advanced': 'llama3.1:8b'
        }.get(self.tier, None)
    
    @requires_tier('intermediate')
    def render(self):
        """Render the AI tutor interface"""
        st.title("🤖 AI Tutor")
        
        # Quota display
        self._render_quota_display()
        
        # Chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Display messages
        for message in st.session_state.chat_history:
            with st.chat_message(message['role']):
                st.markdown(message['content'])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about this course..."):
            self._handle_user_message(prompt)
        
        # Advanced features
        if self.tier == 'advanced':
            self._render_export_button()
    
    def _render_quota_display(self):
        """Display remaining quota"""
        quota = self.gtm.get_ai_tutor_quota()
        
        if self.tier == 'intermediate':
            remaining = quota['remaining']
            total = quota['total']
            st.progress(remaining / total)
            st.caption(f"Questions remaining: {remaining}/{total} (resets monthly)")
        else:  # advanced
            st.success("Unlimited questions ✨")
    
    @quota_limited('ai_tutor_quota')
    def _handle_user_message(self, prompt: str):
        """Process user question with quota check"""
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': prompt
        })
        
        # Get RAG context
        context = self._get_course_context(prompt)
        
        # Build full prompt
        full_prompt = self._build_prompt_with_context(prompt, context)
        
        # Stream response from OLLAMA
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            for chunk in self.ollama.stream_chat(self.model, full_prompt):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        
        # Save to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': full_response
        })
        
        # Decrement quota
        self.gtm.decrement_ai_quota()
    
    def _get_course_context(self, query: str) -> str:
        """Retrieve relevant context using RAG"""
        # Get embeddings for query
        query_embedding = self.ollama.get_embeddings(query)
        
        # Search vector store
        relevant_docs = self.gtm.search_course_content(
            self.course_id, 
            query_embedding,
            top_k=3
        )
        
        return "\n\n".join([doc['content'] for doc in relevant_docs])
    
    def _build_prompt_with_context(self, question: str, context: str) -> str:
        """Build prompt with RAG context"""
        return f"""You are an AI tutor for this course. Use the following context to answer the student's question accurately.

Context:
{context}

Student Question: {question}

Provide a clear, educational answer. Use code examples when relevant."""
    
    @requires_tier('advanced')
    def _render_export_button(self):
        """Export chat history"""
        if st.button("📥 Export Chat"):
            chat_md = self._format_chat_as_markdown()
            st.download_button(
                "Download Markdown",
                chat_md,
                file_name="ai_tutor_chat.md",
                mime="text/markdown"
            )
```

### Features

#### RAG-Based Context
- Course content indexed in vector store (ChromaDB)
- Semantic search for relevant context
- Top-k retrieval (k=3 for Intermediate, k=5 for Advanced)
- Context injection into prompt

#### Quota Tracking
- Monthly quota for Intermediate tier (50 questions)
- Unlimited for Advanced tier
- Quota stored in CoursesGTM database
- Visual quota meter in UI

#### Conversation History
- Stored in session state (current session)
- Persistent storage in database (optional)
- 10 chats max for Intermediate
- Unlimited for Advanced

#### Code Snippet Highlighting
- Automatic detection of code blocks
- Syntax highlighting with Pygments
- Copy button for code snippets

### OLLAMA Integration

**Model Selection**:
```python
MODELS_BY_TIER = {
    'intermediate': {
        'name': 'llama3.2:3b',
        'context_window': 4096,
        'temperature': 0.7
    },
    'advanced': {
        'name': 'llama3.1:8b',
        'context_window': 8192,
        'temperature': 0.7
    }
}
```

**Prompt Templates**:
```python
SYSTEM_PROMPT = """You are an expert AI tutor specializing in data science and machine learning. 
Your goal is to help students learn by:
1. Providing clear, accurate explanations
2. Using examples and analogies
3. Encouraging critical thinking
4. Offering code examples when relevant
5. Breaking down complex topics

Be encouraging and patient. If you don't know something, say so."""
```

### API Dependencies

**CoursesGTM Calls:**
- `GET /api/v1/ai-tutor/quota` - Get remaining quota
- `POST /api/v1/ai-tutor/decrement` - Decrement quota
- `POST /api/v1/ai-tutor/search-context` - RAG context search
- `POST /api/v1/ai-tutor/save-chat` - Save conversation

**OLLAMA Calls:**
- `POST /api/generate` - Stream chat completion
- `POST /api/embeddings` - Get text embeddings

### UI Mockup

```
┌─────────────────────────────────────────┐
│  🤖 AI Tutor                            │
├─────────────────────────────────────────┤
│  Questions: [████████░░] 45/50          │
│  (resets in 12 days)                    │
├─────────────────────────────────────────┤
│  👤 User:                               │
│  What is gradient descent?              │
│                                         │
│  🤖 Assistant:                          │
│  Gradient descent is an optimization... │
│  [code example]                         │
│                                         │
│  👤 User:                               │
│  Can you show a Python example?         │
│                                         │
│  🤖 Assistant: ▌ (typing...)            │
├─────────────────────────────────────────┤
│  Ask me anything... [Send]              │
│                                         │
│  [📥 Export Chat] (Advanced only)       │
└─────────────────────────────────────────┘
```

### Configuration

**Feature Flags**:
```json
{
  "ai_tutor": {
    "enabled_tiers": ["intermediate", "advanced"],
    "quota_by_tier": {
      "intermediate": 50,
      "advanced": "unlimited"
    },
    "models_by_tier": {
      "intermediate": "llama3.2:3b",
      "advanced": "llama3.1:8b"
    },
    "context_retrieval": {
      "top_k_intermediate": 3,
      "top_k_advanced": 5
    }
  }
}
```

### Error Handling

- **OLLAMA Offline**: Show error, suggest checking service
- **Quota Exceeded**: Disable input, show upgrade prompt
- **Context Retrieval Failed**: Proceed without RAG context
- **Slow Response**: Show loading indicator, timeout after 60s

---

## Lab Runner Component

### Purpose
Provide interactive coding environment for hands-on practice, with execution capabilities based on tier.

### Tier-Based Behavior

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| View Notebooks | ✅ (Static HTML) | ✅ | ✅ |
| Execute Code | ❌ | ✅ (JupyterLite) | ✅ (JupyterLab) |
| Save Work | ❌ | ✅ (Browser storage) | ✅ (Persistent) |
| Install Packages | ❌ | Limited (Pyodide) | ✅ (pip) |
| Dataset Access | ❌ | ✅ | ✅ |
| GPU Acceleration | ❌ | ❌ | ✅ |
| Kernel Restart | ❌ | ✅ | ✅ |
| Export Results | ❌ | ✅ (HTML) | ✅ (ipynb, HTML, PDF) |

### Implementation

**File**: `courseplayerapp/components/labs/notebook_runner.py`

```python
import streamlit as st
import streamlit.components.v1 as components
from courseplayerapp.middleware.feature_gates import requires_tier

class NotebookRunner:
    """
    Interactive notebook runner with tier-based execution.
    """
    
    def __init__(self, notebook_id: str):
        self.notebook_id = notebook_id
        self.tier = st.session_state.get('tier', 'basic')
    
    def render(self):
        """Render notebook interface"""
        st.title("🧪 Interactive Lab")
        
        if self.tier == 'basic':
            self._render_static_view()
        elif self.tier == 'intermediate':
            self._render_jupyterlite()
        else:  # advanced
            self._render_jupyterlab()
    
    def _render_static_view(self):
        """Static HTML view for Basic tier"""
        st.info("Upgrade to Intermediate to run code interactively")
        
        # Render notebook as static HTML
        notebook_html = self._get_notebook_html()
        components.html(notebook_html, height=800, scrolling=True)
        
        # Upgrade CTA
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("🚀 Upgrade to Run Code", use_container_width=True)
    
    @requires_tier('intermediate')
    def _render_jupyterlite(self):
        """Browser-based JupyterLite for Intermediate"""
        st.success("Interactive mode enabled ✨")
        
        # JupyterLite iframe
        jupyterlite_url = self._get_jupyterlite_url()
        components.iframe(jupyterlite_url, height=800)
        
        # Save/Export
        col1, col2 = st.columns(2)
        with col1:
            st.button("💾 Save to Browser")
        with col2:
            st.button("📥 Export as HTML")
    
    @requires_tier('advanced')
    def _render_jupyterlab(self):
        """Full JupyterLab for Advanced tier"""
        st.success("Full JupyterLab with persistent storage 🎉")
        
        # Launch or connect to JupyterLab instance
        lab_url = self._get_or_create_jupyterlab_instance()
        components.iframe(lab_url, height=800)
        
        # Advanced controls
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Restart Kernel"):
                self._restart_kernel()
        with col2:
            if st.button("📦 Install Package"):
                self._show_package_installer()
        with col3:
            if st.button("📥 Export"):
                self._show_export_options()
```

### Features

#### Notebook Preview
- Syntax-highlighted code cells
- Rendered markdown cells
- Output display (text, images, plots)

#### Code Execution
- **Intermediate**: Pyodide in browser (WebAssembly Python)
- **Advanced**: Full Python kernel on server

#### Output Saving
- **Intermediate**: Local browser storage
- **Advanced**: Server-side persistent storage

#### Dataset Integration
- Pre-loaded course datasets
- Custom dataset upload (Advanced)

### Security

**Sandboxed Execution:**
```python
# Resource limits for notebook execution
LIMITS_BY_TIER = {
    'intermediate': {
        'max_memory_mb': 512,
        'max_cpu_seconds': 60,
        'network_access': False,
        'file_system': 'virtual'
    },
    'advanced': {
        'max_memory_mb': 2048,
        'max_cpu_seconds': 300,
        'network_access': True,
        'file_system': 'persistent'
    }
}
```

### API Dependencies

**CoursesGTM Calls:**
- `GET /api/v1/labs/{lab_id}/notebook` - Get notebook content
- `POST /api/v1/labs/{lab_id}/save` - Save notebook state
- `POST /api/v1/labs/{lab_id}/kernel/start` - Start JupyterLab kernel (Advanced)
- `POST /api/v1/labs/{lab_id}/kernel/restart` - Restart kernel

### UI Mockup

```
┌─────────────────────────────────────────┐
│  🧪 Lab: Data Cleaning Exercise         │
├─────────────────────────────────────────┤
│  Tier: [Intermediate] ✨                │
│  [🔄 Restart] [📦 Install] [📥 Export]  │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │
│  │ # Data Cleaning Lab               │  │
│  │                                   │  │
│  │ In [1]: import pandas as pd       │  │
│  │         df = pd.read_csv(...)     │  │
│  │ [▶ Run]                           │  │
│  │                                   │  │
│  │ Out[1]: <DataFrame preview>       │  │
│  │                                   │  │
│  │ In [2]: # Your code here          │  │
│  │ [ ]                               │  │
│  └───────────────────────────────────┘  │
│                                         │
│  💾 Last saved: 2 minutes ago           │
└─────────────────────────────────────────┘
```

### Configuration

```json
{
  "lab_runner": {
    "enabled_tiers": ["basic", "intermediate", "advanced"],
    "execution_modes": {
      "basic": "static_html",
      "intermediate": "jupyterlite",
      "advanced": "jupyterlab"
    },
    "resource_limits": {
      "intermediate": {
        "memory_mb": 512,
        "timeout_seconds": 60
      },
      "advanced": {
        "memory_mb": 2048,
        "timeout_seconds": 300
      }
    }
  }
}
```

---

## Quiz Engine Component

### Purpose
Deliver assessments with auto-grading, instant feedback, and adaptive difficulty.

### Tier-Based Behavior

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Multiple Choice | ✅ | ✅ | ✅ |
| Code Challenges | ✅ (View only) | ✅ (Interactive) | ✅ |
| Auto-Grading | ✅ | ✅ | ✅ |
| Instant Feedback | Basic | Detailed | Detailed + Hints |
| Retry Attempts | 3 | 5 | Unlimited |
| Time Limit | ❌ | ✅ (Configurable) | ✅ |
| Adaptive Difficulty | ❌ | ✅ | ✅ |
| Performance Analytics | Basic | Advanced | Advanced + ML insights |

### Implementation

**File**: `courseplayerapp/components/quiz/engine.py`

```python
import streamlit as st
from typing import List, Dict, Any
from courseplayerapp.integrations.coursesgtm_client import CoursesGTMClient

class QuizEngine:
    """
    Quiz engine with adaptive difficulty and analytics.
    """
    
    def __init__(self, quiz_id: str):
        self.quiz_id = quiz_id
        self.tier = st.session_state.get('tier', 'basic')
        self.gtm = CoursesGTMClient()
        
    def render(self):
        """Render quiz interface"""
        quiz_data = self.gtm.get_quiz(self.quiz_id)
        
        st.title(f"📝 {quiz_data['title']}")
        st.write(quiz_data['description'])
        
        # Progress indicator
        self._render_progress()
        
        # Current question
        current_q = st.session_state.get('current_question', 0)
        question = quiz_data['questions'][current_q]
        
        self._render_question(question, current_q)
        
        # Navigation
        col1, col2, col3 = st.columns(3)
        with col1:
            if current_q > 0:
                st.button("⬅️ Previous", on_click=self._previous_question)
        with col2:
            st.button("Skip", on_click=self._next_question)
        with col3:
            if current_q < len(quiz_data['questions']) - 1:
                st.button("Next ➡️", on_click=self._next_question)
            else:
                st.button("Submit Quiz", on_click=self._submit_quiz)
    
    def _render_question(self, question: Dict, index: int):
        """Render individual question"""
        st.subheader(f"Question {index + 1}")
        st.write(question['text'])
        
        answer_key = f"answer_{self.quiz_id}_{index}"
        
        if question['type'] == 'multiple_choice':
            answer = st.radio(
                "Select your answer:",
                question['options'],
                key=answer_key
            )
        
        elif question['type'] == 'code_challenge':
            if self.tier == 'basic':
                st.code(question['starter_code'], language='python')
                st.info("Upgrade to Intermediate to write and test code")
            else:
                answer = st.text_area(
                    "Write your code:",
                    value=question['starter_code'],
                    height=200,
                    key=answer_key
                )
                if st.button("Test Code"):
                    self._test_code(answer, question['test_cases'])
        
        elif question['type'] == 'open_ended':
            answer = st.text_area(
                "Your answer:",
                height=150,
                key=answer_key
            )
        
        # Show feedback if answered
        if answer_key in st.session_state.submitted_answers:
            self._render_feedback(question, answer)
    
    def _render_feedback(self, question: Dict, user_answer: Any):
        """Display feedback based on tier"""
        is_correct = self._check_answer(question, user_answer)
        
        if is_correct:
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect")
            
            if self.tier == 'basic':
                st.caption("Try again (2 attempts remaining)")
            
            elif self.tier in ['intermediate', 'advanced']:
                # Detailed explanation
                st.info(f"**Explanation:** {question['explanation']}")
                
                if self.tier == 'advanced':
                    # Hints for advanced tier
                    with st.expander("💡 Hint"):
                        st.write(question['hint'])
    
    def _test_code(self, code: str, test_cases: List[Dict]):
        """Test code submission"""
        results = self.gtm.run_code_tests(code, test_cases)
        
        for i, result in enumerate(results):
            if result['passed']:
                st.success(f"Test {i+1}: ✅ Passed")
            else:
                st.error(f"Test {i+1}: ❌ Failed")
                st.code(f"Expected: {result['expected']}\nGot: {result['actual']}")
    
    def _submit_quiz(self):
        """Submit quiz and show results"""
        score = self._calculate_score()
        self.gtm.save_quiz_result(self.quiz_id, score)
        
        st.balloons()
        st.success(f"Quiz completed! Score: {score['percentage']}%")
        
        if self.tier in ['intermediate', 'advanced']:
            self._show_detailed_analytics(score)
```

### Features

#### Question Types
1. **Multiple Choice**: Radio button selection
2. **Code Challenges**: Interactive code editor with test cases
3. **Open-Ended**: Text area for written responses

#### Auto-Grading
- Immediate grading for multiple choice
- Test case execution for code challenges
- ML-based grading for open-ended (Advanced)

#### Performance Tracking
- Question-by-question analytics
- Time spent per question
- Attempt history
- Weak topic identification

### API Dependencies

**CoursesGTM Calls:**
- `GET /api/v1/quizzes/{quiz_id}` - Get quiz data
- `POST /api/v1/quizzes/{quiz_id}/submit` - Submit answers
- `POST /api/v1/quizzes/{quiz_id}/test-code` - Run code tests
- `GET /api/v1/quizzes/{quiz_id}/analytics` - Get performance data

### Configuration

```json
{
  "quiz_engine": {
    "retry_attempts": {
      "basic": 3,
      "intermediate": 5,
      "advanced": "unlimited"
    },
    "feedback_level": {
      "basic": "simple",
      "intermediate": "detailed",
      "advanced": "detailed_with_hints"
    },
    "adaptive_difficulty": {
      "enabled_tiers": ["intermediate", "advanced"]
    }
  }
}
```

---

## Progress Tracker Component

### Purpose
Track learning progress, implement gamification, and provide analytics.

### Tier-Based Behavior

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Completion Tracking | ✅ | ✅ | ✅ |
| Daily Streak | ❌ | ✅ | ✅ |
| XP & Levels | ❌ | ✅ | ✅ |
| Achievements | Basic | Full | Full + Rare |
| Analytics Dashboard | Basic | Advanced | Advanced + Predictions |
| Leaderboard | ❌ | ❌ | ✅ (Team/Enterprise) |

### Implementation

**File**: `courseplayerapp/components/progress/tracker.py`

```python
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from courseplayerapp.integrations.coursesgtm_client import CoursesGTMClient

class ProgressTracker:
    """
    Progress tracking with gamification.
    """
    
    def __init__(self, course_id: str):
        self.course_id = course_id
        self.tier = st.session_state.get('tier', 'basic')
        self.gtm = CoursesGTMClient()
    
    def render(self):
        """Render progress dashboard"""
        st.title("📊 Your Progress")
        
        progress_data = self.gtm.get_progress(self.course_id)
        
        # Course completion
        self._render_completion_widget(progress_data)
        
        # Tier-specific features
        if self.tier in ['intermediate', 'advanced']:
            self._render_streak_counter(progress_data)
            self._render_xp_level_system(progress_data)
            self._render_detailed_analytics(progress_data)
        
        if self.tier == 'advanced':
            self._render_predictions(progress_data)
    
    def _render_completion_widget(self, data: Dict):
        """Show course completion percentage"""
        completion = data['completion_percentage']
        
        # Progress bar
        st.progress(completion / 100)
        st.metric("Course Completion", f"{completion}%")
        
        # Module breakdown
        with st.expander("📚 Module Progress"):
            for module in data['modules']:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(module['name'])
                with col2:
                    st.write(f"{module['completion']}%")
    
    def _render_streak_counter(self, data: Dict):
        """Daily streak tracker"""
        streak_days = data['streak_days']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔥 Current Streak", f"{streak_days} days")
        with col2:
            st.metric("📅 Longest Streak", f"{data['longest_streak']} days")
        with col3:
            st.metric("🎯 This Week", f"{data['days_active_this_week']}/7 days")
        
        # Streak calendar
        self._render_streak_calendar(data['activity_calendar'])
    
    def _render_xp_level_system(self, data: Dict):
        """XP and level display"""
        current_xp = data['xp']
        current_level = data['level']
        xp_for_next_level = self._calculate_xp_for_level(current_level + 1)
        xp_progress = current_xp % 1000  # XP within current level
        
        st.subheader(f"Level {current_level}")
        st.progress(xp_progress / 1000)
        st.caption(f"{xp_progress}/1000 XP to Level {current_level + 1}")
        
        # XP breakdown
        with st.expander("💎 XP Sources"):
            st.write("- Complete lesson: 50 XP")
            st.write("- Pass quiz: 100 XP")
            st.write("- Finish lab: 150 XP")
            st.write("- Daily streak: 25 XP/day")
            st.write("- Ask AI question: 10 XP (Advanced)")
    
    def _render_detailed_analytics(self, data: Dict):
        """Advanced analytics dashboard"""
        st.subheader("📈 Learning Analytics")
        
        # Time spent chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data['daily_time']['dates'],
            y=data['daily_time']['minutes'],
            name='Time Spent'
        ))
        fig.update_layout(title="Daily Learning Time (Last 30 Days)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance by topic
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Strong Topics:**")
            for topic in data['strong_topics']:
                st.success(f"✅ {topic['name']} ({topic['score']}%)")
        
        with col2:
            st.write("**Needs Review:**")
            for topic in data['weak_topics']:
                st.warning(f"⚠️ {topic['name']} ({topic['score']}%)")
    
    def _render_predictions(self, data: Dict):
        """ML-powered predictions (Advanced tier)"""
        st.subheader("🔮 Predictions")
        
        col1, col2 = st.columns(2)
        with col1:
            completion_date = data['predicted_completion_date']
            st.metric(
                "Estimated Completion",
                completion_date.strftime("%B %d, %Y")
            )
        
        with col2:
            final_score = data['predicted_final_score']
            st.metric(
                "Predicted Final Score",
                f"{final_score}%"
            )
```

### Features

#### Gamification Elements
- **XP Points**: Earned for activities
- **Levels**: Progress through levels (1-100)
- **Streaks**: Daily activity tracking
- **Achievements**: Unlockable badges

#### Analytics
- Course completion percentage
- Time spent learning
- Performance by topic
- Weak area identification

### API Dependencies

**CoursesGTM Calls:**
- `GET /api/v1/progress/{course_id}` - Get progress data
- `POST /api/v1/progress/{course_id}/update` - Update progress
- `GET /api/v1/rewards/achievements` - Get unlocked achievements
- `GET /api/v1/analytics/predictions` - Get ML predictions (Advanced)

---

## Certificate Generator Component

### Purpose
Generate verifiable course completion certificates with digital signatures.

### Tier-Based Behavior

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Certificate | ❌ | ✅ Verifiable | ✅ Professional |
| Format | N/A | PDF | PDF + PNG |
| Verification | N/A | QR Code | QR + Digital Signature |
| LinkedIn Integration | ❌ | ✅ | ✅ |
| Custom Branding | ❌ | ❌ | ✅ |
| Batch Export | ❌ | ❌ | ✅ (Enterprise) |

### Implementation

**File**: `courseplayerapp/components/certificates/generator.py`

```python
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from courseplayerapp.middleware.feature_gates import requires_tier

class CertificateGenerator:
    """
    Certificate generation with verification.
    """
    
    def __init__(self, course_id: str):
        self.course_id = course_id
        self.tier = st.session_state.get('tier', 'basic')
    
    @requires_tier('intermediate')
    def render(self):
        """Render certificate page"""
        st.title("📜 Your Certificates")
        
        if self.tier == 'basic':
            self._render_upgrade_prompt()
            return
        
        certificates = self._get_earned_certificates()
        
        if not certificates:
            st.info("Complete a course to earn your first certificate!")
            return
        
        for cert in certificates:
            self._render_certificate_card(cert)
    
    def _render_certificate_card(self, cert: Dict):
        """Display certificate card"""
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.subheader(cert['course_name'])
                st.caption(f"Completed: {cert['completion_date']}")
                st.caption(f"Score: {cert['final_score']}%")
            
            with col2:
                if cert['verified']:
                    st.success("✅ Verified")
                else:
                    st.warning("⏳ Pending Verification")
            
            with col3:
                if st.button("📥 Download", key=f"dl_{cert['id']}"):
                    self._download_certificate(cert)
                
                if self.tier == 'advanced' and st.button("🔗 LinkedIn", key=f"li_{cert['id']}"):
                    self._share_to_linkedin(cert)
    
    def _download_certificate(self, cert: Dict):
        """Generate and download certificate PDF"""
        pdf_bytes = self._generate_pdf(cert)
        
        st.download_button(
            "Download PDF",
            pdf_bytes,
            file_name=f"certificate_{cert['id']}.pdf",
            mime="application/pdf"
        )
    
    def _generate_pdf(self, cert: Dict) -> bytes:
        """Generate certificate PDF"""
        # Create PDF with reportlab
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Certificate design
        width, height = letter
        
        # Border
        c.setLineWidth(3)
        c.rect(50, 50, width - 100, height - 100)
        
        # Title
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(width / 2, height - 100, "Certificate of Completion")
        
        # Recipient
        c.setFont("Helvetica", 24)
        c.drawCentredString(width / 2, height - 200, cert['recipient_name'])
        
        # Course
        c.setFont("Helvetica", 18)
        c.drawCentredString(width / 2, height - 280, f"has successfully completed")
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width / 2, height - 320, cert['course_name'])
        
        # Date and Score
        c.setFont("Helvetica", 14)
        c.drawCentredString(width / 2, height - 380, 
                          f"Completion Date: {cert['completion_date']}")
        c.drawCentredString(width / 2, height - 400, 
                          f"Final Score: {cert['final_score']}%")
        
        # QR Code for verification
        qr_img = self._generate_qr_code(cert['verification_url'])
        c.drawImage(qr_img, 50, 70, width=100, height=100)
        
        # Digital signature (Advanced tier)
        if self.tier == 'advanced':
            signature = self._sign_certificate(cert)
            c.setFont("Courier", 8)
            c.drawString(170, 70, f"Signature: {signature[:40]}...")
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def _generate_qr_code(self, url: str):
        """Generate QR code for verification"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white")
    
    @requires_tier('advanced')
    def _sign_certificate(self, cert: Dict) -> str:
        """Digitally sign certificate (Advanced tier)"""
        # Load private key (stored securely)
        private_key = self._load_signing_key()
        
        # Create signature
        message = f"{cert['id']}:{cert['recipient_name']}:{cert['course_id']}".encode()
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return signature.hex()
```

### Features

#### PDF Generation
- Professional certificate design
- Customizable templates
- High-resolution output

#### Verification
- QR code linking to verification page
- Digital signature (RSA-2048) for Advanced tier
- Public verification portal

#### LinkedIn Integration
- One-click sharing to LinkedIn
- Auto-filled certificate details
- License credential display

### API Dependencies

**CoursesGTM Calls:**
- `GET /api/v1/certificates` - List earned certificates
- `POST /api/v1/certificates/{id}/generate` - Generate certificate
- `GET /api/v1/certificates/{id}/verify` - Verify certificate

---

## Dataset Explorer Component

### Purpose
Browse and download course-related datasets.

### Tier-Based Behavior

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Browse Catalog | ✅ | ✅ | ✅ |
| Preview Data | ❌ | ✅ (100 rows) | ✅ (Full) |
| Download | ❌ | ✅ | ✅ |
| Custom Upload | ❌ | ❌ | ✅ |
| Data Viewer | ❌ | ✅ | ✅ Enhanced |

### Implementation

**File**: `courseplayerapp/components/datasets/explorer.py`

```python
import streamlit as st
import pandas as pd
from courseplayerapp.middleware.feature_gates import requires_tier

class DatasetExplorer:
    """
    Dataset browser and downloader.
    """
    
    @requires_tier('intermediate')
    def render(self):
        """Render dataset explorer"""
        st.title("💾 Datasets")
        
        datasets = self._get_available_datasets()
        
        # Search and filter
        search = st.text_input("Search datasets", "")
        category = st.selectbox("Category", ["All", "Tabular", "Images", "Text"])
        
        # Dataset grid
        for dataset in datasets:
            if search.lower() in dataset['name'].lower():
                self._render_dataset_card(dataset)
    
    def _render_dataset_card(self, dataset: Dict):
        """Display dataset card"""
        with st.expander(f"📊 {dataset['name']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(dataset['description'])
                st.caption(f"Size: {dataset['size']} | Format: {dataset['format']}")
            
            with col2:
                if st.button("👁️ Preview", key=f"prev_{dataset['id']}"):
                    self._preview_dataset(dataset)
                
                if st.button("📥 Download", key=f"dl_{dataset['id']}"):
                    self._download_dataset(dataset)
    
    def _preview_dataset(self, dataset: Dict):
        """Preview dataset (Intermediate: 100 rows, Advanced: all)"""
        if dataset['format'] == 'csv':
            df = pd.read_csv(dataset['url'], nrows=100 if self.tier == 'intermediate' else None)
            st.dataframe(df)
            
            if self.tier == 'advanced':
                st.write("**Statistics:**")
                st.write(df.describe())
```

---

## Code Review Component

### Purpose
Submit projects for automated and manual review.

### Tier-Based Behavior

| Feature | Basic | Intermediate | Advanced |
|---------|-------|--------------|----------|
| Submission | ❌ | ✅ (3 per course) | ✅ (5 per course) |
| Automated Review | ❌ | ✅ | ✅ |
| Human Review | ❌ | ❌ | ✅ |
| Review Turnaround | N/A | N/A | 48 hours |

### Implementation

**File**: `courseplayerapp/components/code_review/submission.py`

```python
import streamlit as st
from courseplayerapp.middleware.feature_gates import requires_tier, quota_limited

class CodeReviewSubmission:
    """
    Project submission and review system.
    """
    
    @requires_tier('intermediate')
    @quota_limited('code_review_quota')
    def render(self):
        """Render submission interface"""
        st.title("🔍 Code Review")
        
        # Submission form
        st.subheader("Submit Your Project")
        
        project_file = st.file_uploader("Upload project (.zip or .py)", type=['zip', 'py'])
        description = st.text_area("Project description")
        
        if st.button("Submit for Review"):
            self._submit_project(project_file, description)
        
        # Previous submissions
        st.subheader("Your Submissions")
        submissions = self._get_submissions()
        
        for sub in submissions:
            self._render_submission_card(sub)
    
    def _submit_project(self, file, description):
        """Submit project for review"""
        # Upload file
        file_url = self._upload_file(file)
        
        # Request automated review
        review_result = self.gtm.submit_for_review(file_url, description)
        
        st.success("Project submitted! Automated review in progress...")
```

---

This completes the comprehensive component specifications. Each component is designed with clear tier boundaries, API dependencies, and implementation guidelines.
