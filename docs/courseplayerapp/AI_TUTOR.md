# CoursePlayerApp - AI Tutor Specification

## Overview

The AI Tutor is an OLLAMA-powered intelligent assistant that provides context-aware learning support. It helps students understand concepts, debug code, and get unstuck—with tier-based quota management to encourage upgrades.

---

## OLLAMA Integration

### What is OLLAMA?

OLLAMA is a local LLM (Large Language Model) runtime that enables running AI models without external API calls.

**Benefits**:
- **Privacy**: All data stays on-premise (no data sent to OpenAI, Anthropic, etc.)
- **Cost**: No per-token charges
- **Speed**: Low latency (local inference)
- **Offline**: Works without internet (after model download)

**Model**: `llama3.1:8b` (Meta's Llama 3.1 with 8 billion parameters)
- Context window: 128K tokens
- Strong reasoning and code understanding
- Multilingual support

### OLLAMA Setup

**Installation**:
```bash
# On server running CoursePlayerApp
curl -fsSL https://ollama.com/install.sh | sh

# Pull the model (one-time, ~4.7 GB download)
ollama pull llama3.1:8b

# Verify installation
ollama list
```

**Docker Deployment** (recommended):
```yaml
# docker-compose.yml
services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_ORIGINS=http://courseplayerapp:8501
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  courseplayerapp:
    image: courseplayerapp:latest
    depends_on:
      - ollama
    environment:
      - OLLAMA_HOST=http://ollama:11434

volumes:
  ollama_data:
```

**Python SDK**:
```bash
pip install ollama
```

---

## Quota Management

### Tier-Based Quotas

| Tier | Monthly Quota | Reset Period | Context Awareness | Response Priority |
|------|--------------|--------------|-------------------|-------------------|
| **Basic** | 0 (Disabled) | N/A | N/A | N/A |
| **Intermediate** | 50 questions | 1st of each month | Course + module + topic | Standard |
| **Advanced** | Unlimited | N/A | Course + module + topic + chat history | Priority |

### Quota Tracking Schema

**Database Table**: `ai_tutor_usage`

```sql
CREATE TABLE ai_tutor_usage (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    tier VARCHAR(50) NOT NULL,
    month DATE NOT NULL,  -- First day of month (e.g., '2026-01-01')
    question_count INT DEFAULT 0,
    tokens_used INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, month)
);

-- Index for fast lookups
CREATE INDEX idx_user_month ON ai_tutor_usage(user_id, month);
```

**Usage Record**:
```json
{
  "user_id": "user123",
  "tier": "intermediate",
  "month": "2026-01-01",
  "question_count": 45,
  "tokens_used": 67500,
  "questions": [
    {
      "question_id": "q1",
      "timestamp": "2026-01-05T10:30:00Z",
      "course_id": "ai-03",
      "module_id": "module-02",
      "question": "What is the difference between BERT and GPT?",
      "tokens": 1500
    }
  ]
}
```

### Quota Enforcement Implementation

```python
# utils/quota_tracker.py
from datetime import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st

class QuotaTracker:
    def __init__(self, user_id: str, tier: str):
        self.user_id = user_id
        self.tier = tier
        self.current_month = self._get_current_month()
        self.quota = self._get_quota()
        self.usage = self._get_usage()
    
    def _get_current_month(self) -> str:
        """Get first day of current month as string"""
        now = datetime.now()
        return datetime(now.year, now.month, 1).strftime('%Y-%m-%d')
    
    def _get_quota(self) -> int:
        """Get quota limit for tier"""
        quotas = {
            "basic": 0,
            "intermediate": 50,
            "advanced": -1  # Unlimited
        }
        return quotas.get(self.tier, 0)
    
    def _get_usage(self) -> int:
        """Fetch current month's usage from database"""
        from database import db
        
        result = db.query(
            "SELECT question_count FROM ai_tutor_usage WHERE user_id = %s AND month = %s",
            (self.user_id, self.current_month)
        )
        
        if result:
            return result[0]['question_count']
        else:
            # Create new record for this month
            db.execute(
                "INSERT INTO ai_tutor_usage (user_id, tier, month, question_count) VALUES (%s, %s, %s, 0)",
                (self.user_id, self.tier, self.current_month)
            )
            return 0
    
    def can_ask_question(self) -> tuple[bool, str]:
        """
        Check if user can ask a question
        
        Returns:
            tuple: (can_ask: bool, message: str)
        """
        if self.tier == "basic":
            return (False, "🔒 AI Tutor is available starting from **Intermediate tier ($247)**. "
                          "Upgrade to unlock 50 AI-assisted questions per month!")
        
        if self.tier == "intermediate":
            remaining = self.quota - self.usage
            if remaining <= 0:
                next_month = (datetime.now() + relativedelta(months=1)).replace(day=1).strftime('%B %d, %Y')
                return (False, f"📊 You've used all {self.quota} questions this month. "
                              f"Quota resets on {next_month}. "
                              f"Upgrade to **Advanced tier ($497)** for unlimited AI assistance!")
            else:
                return (True, f"✅ {remaining}/{self.quota} questions remaining this month")
        
        if self.tier == "advanced":
            return (True, "✅ Unlimited questions")
        
        return (False, "Unknown tier")
    
    def increment_usage(self, tokens_used: int = 0):
        """Increment usage count after successful question"""
        from database import db
        
        db.execute(
            """
            UPDATE ai_tutor_usage 
            SET question_count = question_count + 1,
                tokens_used = tokens_used + %s,
                updated_at = NOW()
            WHERE user_id = %s AND month = %s
            """,
            (tokens_used, self.user_id, self.current_month)
        )
        
        self.usage += 1
    
    def get_usage_stats(self) -> dict:
        """Get detailed usage statistics"""
        remaining = max(0, self.quota - self.usage) if self.quota != -1 else -1
        
        return {
            "quota": self.quota,
            "used": self.usage,
            "remaining": remaining,
            "percentage": (self.usage / self.quota * 100) if self.quota > 0 else 0,
            "resets_on": (datetime.now() + relativedelta(months=1)).replace(day=1).strftime('%Y-%m-%d')
        }
```

---

## AI Tutor Features

### Context Awareness

The AI Tutor is aware of:
1. **Current course**: Course ID, title, description
2. **Current module**: Module ID, title, learning objectives
3. **Current topic**: Video/slides being viewed
4. **User's tier**: To adjust response depth
5. **Chat history**: Previous questions in session (Advanced tier)

**Context Building**:

```python
# ai_tutor/context_builder.py
def build_context(session_state: dict) -> dict:
    """Build context dictionary for AI Tutor"""
    context = {
        "course_id": session_state.get("current_course"),
        "course_title": session_state.get("course_title"),
        "module_id": session_state.get("current_module"),
        "module_title": session_state.get("module_title"),
        "current_topic": session_state.get("current_topic"),
        "tier": session_state.get("tier"),
        "user_id": session_state.get("user_id")
    }
    
    # Fetch course details
    if context["course_id"]:
        from utils.api_client import CoursesGTMClient
        client = CoursesGTMClient()
        course_data = client.get_course(context["course_id"])
        context["course_description"] = course_data.get("description")
        context["learning_objectives"] = course_data.get("objectives", [])
    
    # Include chat history for Advanced tier
    if context["tier"] == "advanced":
        context["chat_history"] = session_state.get("ai_tutor_history", [])
    
    return context
```

### Question Types Supported

1. **Concept Clarification**
   - "Can you explain what a neural network is in simple terms?"
   - "What's the difference between supervised and unsupervised learning?"

2. **Code Debugging**
   - "Why is my Python code throwing a KeyError?"
   - "How do I fix this TensorFlow shape mismatch?"

3. **Hints (Not Full Answers)**
   - "I'm stuck on the lab exercise. Can you give me a hint?"
   - "What approach should I use for this problem?"

4. **Related Resources**
   - "Are there any good resources to learn more about transformers?"
   - "Can you recommend a paper on this topic?"

5. **Problem-Solving Guidance**
   - "How would you approach this machine learning problem?"
   - "What are the steps to build a recommendation system?"

---

## AITutor Class Implementation

```python
# ai_tutor/tutor.py
import ollama
import streamlit as st
from utils.quota_tracker import QuotaTracker
from ai_tutor.context_builder import build_context

class AITutor:
    """OLLAMA-powered AI Tutor with quota management"""
    
    SYSTEM_PROMPT = """You are a helpful, patient AI tutor for an online learning platform.

Your role:
- Help students understand concepts, don't just give answers
- Provide hints and guidance for labs, don't solve them completely
- Explain things in multiple ways if the student doesn't understand
- Encourage critical thinking
- Be encouraging and supportive

Guidelines:
- Keep responses concise (2-3 paragraphs max)
- Use analogies and examples when explaining concepts
- For coding questions, point out the issue but let them fix it
- For lab exercises, give hints not solutions
- If unsure, say so and suggest resources

Tone: Friendly, professional, educational
"""
    
    def __init__(self, user_id: str, tier: str):
        self.user_id = user_id
        self.tier = tier
        self.quota_tracker = QuotaTracker(user_id, tier)
        self.context = build_context(st.session_state)
        
        # Initialize chat history in session
        if "ai_tutor_history" not in st.session_state:
            st.session_state["ai_tutor_history"] = []
    
    def ask_question(self, question: str) -> dict:
        """
        Ask a question to the AI Tutor
        
        Args:
            question: User's question
        
        Returns:
            dict: {
                "success": bool,
                "answer": str,
                "tokens_used": int,
                "quota_status": str
            }
        """
        # Check quota
        can_ask, quota_message = self.quota_tracker.can_ask_question()
        
        if not can_ask:
            return {
                "success": False,
                "answer": quota_message,
                "tokens_used": 0,
                "quota_status": quota_message
            }
        
        # Build prompt with context
        prompt = self._build_prompt(question)
        
        try:
            # Call OLLAMA
            response = ollama.chat(
                model="llama3.1:8b",
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            )
            
            answer = response['message']['content']
            tokens_used = response.get('eval_count', 0)  # Approximate token count
            
            # Increment quota (except for Advanced tier with unlimited)
            if self.tier == "intermediate":
                self.quota_tracker.increment_usage(tokens_used)
            
            # Save to chat history
            self._save_to_history(question, answer)
            
            # Get updated quota status
            stats = self.quota_tracker.get_usage_stats()
            quota_status = self._format_quota_status(stats)
            
            return {
                "success": True,
                "answer": answer,
                "tokens_used": tokens_used,
                "quota_status": quota_status
            }
        
        except Exception as e:
            return {
                "success": False,
                "answer": f"❌ Error: {str(e)}. Please try again or contact support.",
                "tokens_used": 0,
                "quota_status": ""
            }
    
    def _build_prompt(self, question: str) -> str:
        """Build context-aware prompt"""
        context_str = f"""
Current Learning Context:
- Course: {self.context.get('course_title', 'N/A')}
- Module: {self.context.get('module_title', 'N/A')}
- Topic: {self.context.get('current_topic', 'N/A')}

"""
        
        # Include chat history for Advanced tier
        if self.tier == "advanced" and self.context.get('chat_history'):
            history = self.context['chat_history'][-3:]  # Last 3 exchanges
            history_str = "\n".join([
                f"Student: {h['question']}\nTutor: {h['answer']}"
                for h in history
            ])
            context_str += f"\nRecent Conversation:\n{history_str}\n\n"
        
        full_prompt = f"{context_str}Student Question: {question}"
        return full_prompt
    
    def _save_to_history(self, question: str, answer: str):
        """Save Q&A to session history"""
        st.session_state["ai_tutor_history"].append({
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 20 exchanges
        if len(st.session_state["ai_tutor_history"]) > 20:
            st.session_state["ai_tutor_history"] = st.session_state["ai_tutor_history"][-20:]
    
    def _format_quota_status(self, stats: dict) -> str:
        """Format quota status message"""
        if stats["quota"] == -1:
            return "✅ Unlimited questions"
        
        used = stats["used"]
        quota = stats["quota"]
        remaining = stats["remaining"]
        
        if remaining > 10:
            return f"✅ {remaining}/{quota} questions remaining this month"
        elif remaining > 0:
            return f"⚠️ Only {remaining} questions left this month!"
        else:
            return f"❌ Quota exhausted. Resets on {stats['resets_on']}"
    
    def get_hint_mode(self, question: str) -> dict:
        """
        Hint mode: Give minimal guidance without solving
        
        Use case: Student is stuck on a lab exercise
        """
        hint_instruction = """
HINT MODE: The student is working on a lab exercise and needs a nudge in the right direction.
- Do NOT solve the problem for them
- Point them to the relevant concept or approach
- Ask leading questions to help them think
- Give a small example or analogy if helpful

Keep it brief (1-2 sentences).
"""
        
        modified_question = f"{hint_instruction}\n\nStudent's question: {question}"
        return self.ask_question(modified_question)
    
    def get_explain_mode(self, concept: str) -> dict:
        """
        Explain mode: Deep dive into a concept
        
        Use case: Student wants to understand a topic better
        """
        explain_instruction = """
EXPLAIN MODE: Break down this concept in detail.
- Start with a simple definition
- Use an analogy or real-world example
- Explain the key components
- Mention common misconceptions
- Suggest how to practice/apply this concept

Aim for 3-4 paragraphs.
"""
        
        modified_question = f"{explain_instruction}\n\nConcept: {concept}"
        return self.ask_question(modified_question)
```

---

## UI Implementation

### AI Tutor Chat Interface

```python
# components/ai_tutor_chat.py
import streamlit as st
from ai_tutor.tutor import AITutor

def render_ai_tutor():
    """Render AI Tutor chat interface"""
    user_id = st.session_state.get("user_id")
    tier = st.session_state.get("tier", "basic")
    
    st.sidebar.markdown("---")
    st.sidebar.header("🤖 AI Tutor")
    
    # Check if AI Tutor is enabled for tier
    from utils.feature_flags import FeatureFlags
    flags = FeatureFlags.get_flags(tier)
    
    if not flags["ai_tutor_enabled"]:
        st.sidebar.info("🔒 AI Tutor is available starting from **Intermediate tier ($247)**")
        st.sidebar.button("Upgrade to Unlock", key="upgrade_ai_tutor")
        return
    
    # Initialize AI Tutor
    tutor = AITutor(user_id, tier)
    
    # Display quota status
    stats = tutor.quota_tracker.get_usage_stats()
    if stats["quota"] == -1:
        st.sidebar.success("✅ Unlimited questions")
    else:
        st.sidebar.progress(stats["percentage"] / 100)
        st.sidebar.caption(f"{stats['used']}/{stats['quota']} questions used")
    
    # Chat mode selector
    mode = st.sidebar.radio(
        "Mode",
        ["Chat", "Hint", "Explain"],
        help="Chat: General Q&A | Hint: Get a nudge | Explain: Deep dive"
    )
    
    # Chat history display
    st.sidebar.markdown("### Conversation")
    
    # Display chat history
    if st.session_state.get("ai_tutor_history"):
        for i, exchange in enumerate(st.session_state["ai_tutor_history"][-5:]):  # Show last 5
            with st.sidebar.expander(f"Q{i+1}: {exchange['question'][:50]}..."):
                st.markdown(f"**You:** {exchange['question']}")
                st.markdown(f"**AI Tutor:** {exchange['answer']}")
    
    # Input area
    st.sidebar.markdown("---")
    question = st.sidebar.text_area(
        "Ask a question:",
        placeholder="E.g., What is gradient descent?",
        height=100
    )
    
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        ask_button = st.button("Ask 🚀", key="ask_ai_tutor")
    with col2:
        clear_button = st.button("Clear 🗑️", key="clear_ai_tutor")
    
    if clear_button:
        st.session_state["ai_tutor_history"] = []
        st.rerun()
    
    if ask_button and question:
        with st.sidebar:
            with st.spinner("🤔 Thinking..."):
                # Call appropriate mode
                if mode == "Hint":
                    result = tutor.get_hint_mode(question)
                elif mode == "Explain":
                    result = tutor.get_explain_mode(question)
                else:
                    result = tutor.ask_question(question)
                
                if result["success"]:
                    st.success("✅ Answer:")
                    st.markdown(result["answer"])
                    st.caption(result["quota_status"])
                else:
                    st.error(result["answer"])
```

### Alternative: Full-Page Chat Interface

```python
# pages/AI_Tutor.py
import streamlit as st
from ai_tutor.tutor import AITutor

st.set_page_config(page_title="AI Tutor", page_icon="🤖")

st.title("🤖 AI Tutor")
st.markdown("Your personal learning assistant powered by OLLAMA")

# Check authentication
if not st.session_state.get("authenticated"):
    st.warning("Please log in to access the AI Tutor")
    st.stop()

user_id = st.session_state["user_id"]
tier = st.session_state["tier"]

# Initialize tutor
tutor = AITutor(user_id, tier)

# Quota display
col1, col2, col3 = st.columns(3)
stats = tutor.quota_tracker.get_usage_stats()

with col1:
    if stats["quota"] == -1:
        st.metric("Monthly Quota", "Unlimited ♾️")
    else:
        st.metric("Monthly Quota", f"{stats['quota']} questions")

with col2:
    st.metric("Used This Month", stats["used"])

with col3:
    if stats["quota"] == -1:
        st.metric("Remaining", "Unlimited")
    else:
        st.metric("Remaining", stats["remaining"])

# Chat interface
st.markdown("---")

# Display chat history
for exchange in st.session_state.get("ai_tutor_history", []):
    with st.chat_message("user"):
        st.write(exchange["question"])
    with st.chat_message("assistant"):
        st.write(exchange["answer"])

# Input
if prompt := st.chat_input("Ask me anything about the course..."):
    # Show user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = tutor.ask_question(prompt)
            
            if result["success"]:
                st.write(result["answer"])
                st.caption(f"_{result['quota_status']}_")
            else:
                st.error(result["answer"])
```

---

## Advanced Features

### Code Snippet Support

When students paste code, format it nicely:

```python
def detect_code_in_question(question: str) -> bool:
    """Detect if question contains code"""
    code_indicators = ["```", "def ", "class ", "import ", "function", "{", "}"]
    return any(indicator in question for indicator in code_indicators)

def format_code_response(answer: str) -> str:
    """Format code blocks in AI response"""
    # Replace ```python ... ``` with st.code()
    import re
    
    code_blocks = re.findall(r'```(\w+)?\n(.*?)```', answer, re.DOTALL)
    for lang, code in code_blocks:
        formatted_code = f"```{lang}\n{code}\n```"
        st.code(code, language=lang or "python")
    
    return answer
```

### Multi-Turn Conversations (Advanced Tier)

Enable follow-up questions:

```python
def handle_followup(tutor: AITutor, question: str):
    """Handle follow-up questions with context from previous answers"""
    if len(st.session_state.get("ai_tutor_history", [])) > 0:
        last_exchange = st.session_state["ai_tutor_history"][-1]
        
        # Check if this is a follow-up
        followup_indicators = ["what about", "how about", "can you explain", "also", "and"]
        is_followup = any(q in question.lower() for q in followup_indicators)
        
        if is_followup:
            # Augment question with previous context
            augmented_question = f"Previous question: {last_exchange['question']}\nPrevious answer: {last_exchange['answer'][:200]}...\n\nFollow-up: {question}"
            return tutor.ask_question(augmented_question)
    
    return tutor.ask_question(question)
```

### Suggested Questions

Provide quick-start questions:

```python
def show_suggested_questions(context: dict):
    """Show suggested questions based on current context"""
    st.markdown("### 💡 Suggested Questions:")
    
    suggestions = [
        f"What are the key concepts in {context.get('module_title', 'this module')}?",
        "Can you summarize this lecture in simple terms?",
        "How does this relate to real-world applications?",
        "What are common mistakes students make here?"
    ]
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggest_{i}"):
                # Auto-fill the question
                st.session_state["ai_tutor_question"] = suggestion
                st.rerun()
```

---

## Performance Optimization

### Response Caching

Cache common questions to reduce OLLAMA calls:

```python
import hashlib
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_response(question_hash: str, context_hash: str) -> str:
    """Get cached AI response if available"""
    # Check cache database
    from database import db
    result = db.query(
        "SELECT answer FROM ai_tutor_cache WHERE question_hash = %s AND context_hash = %s",
        (question_hash, context_hash)
    )
    return result[0]['answer'] if result else None

def ask_with_cache(tutor: AITutor, question: str) -> dict:
    """Ask question with caching"""
    question_hash = hashlib.md5(question.encode()).hexdigest()
    context_hash = hashlib.md5(str(tutor.context).encode()).hexdigest()
    
    # Check cache
    cached_answer = get_cached_response(question_hash, context_hash)
    
    if cached_answer:
        return {
            "success": True,
            "answer": cached_answer,
            "tokens_used": 0,
            "quota_status": "✅ Cached response (no quota used)",
            "cached": True
        }
    
    # No cache, ask OLLAMA
    result = tutor.ask_question(question)
    
    # Cache the response
    if result["success"]:
        db.execute(
            "INSERT INTO ai_tutor_cache (question_hash, context_hash, answer) VALUES (%s, %s, %s)",
            (question_hash, context_hash, result["answer"])
        )
    
    return result
```

### GPU Acceleration

For faster responses, run OLLAMA on GPU:

```bash
# Check GPU availability
nvidia-smi

# Run OLLAMA with GPU
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 ollama/ollama
```

Response time comparison:
- **CPU**: ~5-10 seconds per response
- **GPU**: ~1-2 seconds per response

---

## Monitoring & Analytics

### Track AI Tutor Metrics

```python
# utils/ai_tutor_analytics.py
def log_ai_tutor_interaction(
    user_id: str,
    tier: str,
    question: str,
    answer: str,
    tokens_used: int,
    response_time_ms: int,
    success: bool
):
    """Log AI Tutor interaction for analytics"""
    from database import db
    
    db.execute("""
        INSERT INTO ai_tutor_interactions 
        (user_id, tier, question, answer, tokens_used, response_time_ms, success, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """, (user_id, tier, question, answer, tokens_used, response_time_ms, success))
```

**Metrics to Track**:
- Average response time (by tier)
- Most common questions (cluster with embeddings)
- Quota utilization rate (Intermediate tier)
- User satisfaction (thumbs up/down on answers)
- Conversion: Basic → Intermediate (after seeing AI Tutor prompts)

---

## Testing

### Unit Tests

```python
# tests/test_ai_tutor.py
def test_quota_basic_tier():
    tracker = QuotaTracker("user123", "basic")
    can_ask, message = tracker.can_ask_question()
    assert can_ask == False
    assert "Intermediate tier" in message

def test_quota_intermediate_tier():
    tracker = QuotaTracker("user456", "intermediate")
    # Mock usage to 49/50
    tracker.usage = 49
    can_ask, message = tracker.can_ask_question()
    assert can_ask == True
    assert "1/50" in message

def test_quota_exceeded():
    tracker = QuotaTracker("user789", "intermediate")
    tracker.usage = 50
    can_ask, message = tracker.can_ask_question()
    assert can_ask == False
    assert "Advanced tier" in message
```

### Integration Tests

```python
def test_ollama_connection():
    """Ensure OLLAMA is accessible"""
    import ollama
    models = ollama.list()
    assert "llama3.1:8b" in [m['name'] for m in models['models']]

def test_ai_tutor_response():
    """Test end-to-end AI Tutor response"""
    tutor = AITutor("test_user", "advanced")
    result = tutor.ask_question("What is machine learning?")
    assert result["success"] == True
    assert len(result["answer"]) > 50  # Meaningful response
```

---

## Future Enhancements

### Phase 2
- **Voice input**: Ask questions via speech-to-text
- **Image understanding**: Upload diagrams for explanation
- **Personalized responses**: Adapt to student's learning style
- **Feedback loop**: Thumbs up/down to improve responses

### Phase 3
- **Proactive suggestions**: AI suggests what to learn next
- **Study buddy**: AI generates quiz questions
- **Code review**: AI reviews student's code submissions
- **Multi-model support**: Switch between Llama, Mistral, CodeLlama

---

## Conclusion

The OLLAMA-powered AI Tutor provides:
- **Privacy-first**: No data sent to external APIs
- **Cost-effective**: No per-query charges
- **Tier-differentiated**: Clear value proposition for upgrades
- **Context-aware**: Understands what student is learning
- **Quota-managed**: Enforces limits for Intermediate tier

This design encourages Basic users to upgrade to Intermediate for AI assistance, and Intermediate users to upgrade to Advanced for unlimited access.
