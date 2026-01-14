# AI Tutor Specification

## Overview

The CoursePlayerApp AI Tutor is an OLLAMA-powered intelligent assistant that provides context-aware educational support to students. The system enforces strict quota management based on subscription tier and maintains educational integrity by guiding students rather than providing complete solutions.

---

## AI Tutor Goals

1. **Educational Guidance**: Help students understand concepts, don't solve problems for them
2. **Context Awareness**: Understand current course, module, and topic
3. **Quota Enforcement**: Strict tier-based usage limits
4. **Conversational Quality**: Natural, patient, encouraging responses
5. **Safety**: Appropriate, respectful, educational content only

---

## Tier-Based Access & Quotas

| Tier | Enabled | Monthly Quota | Priority | History | Cost Impact |
|------|---------|---------------|----------|---------|-------------|
| **Basic** | ❌ No | 0 | N/A | N/A | Feature locked |
| **Intermediate** | ✅ Yes | 50 questions | Standard | ❌ No | Moderate usage |
| **Advanced** | ✅ Yes | Unlimited (-1) | ⚡ Yes | ✅ Yes | Premium feature |

### Quota Reset Logic
- **Reset Frequency**: Monthly (on subscription anniversary)
- **Mid-Tier Upgrade**: If user upgrades from Intermediate → Advanced, quota becomes unlimited immediately
- **Downgrade Behavior**: If user downgrades Advanced → Intermediate, quota applies starting next billing cycle

---

## OLLAMA Integration

### Model Selection

**Primary Model**: `llama3.1:8b`
- **Pros**: Balanced size, good reasoning, fast inference
- **Cons**: Requires ~6GB VRAM
- **Alternative**: `llama3.1:7b` for resource-constrained environments

**Fallback Models**:
- `mistral:7b-instruct` - Alternative for speed
- `phi-3:medium` - Smaller footprint

### OLLAMA Setup

**Installation**:
```bash
# Install OLLAMA
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Verify
ollama run llama3.1:8b "Hello, test"
```

**Configuration** (`config/ollama.yaml`):
```yaml
model: "llama3.1:8b"
temperature: 0.7
max_tokens: 500
timeout: 30
host: "http://localhost:11434"
```

---

## AI Tutor Features

### Core Capabilities

1. **Concept Explanation**
   - Simplify complex topics
   - Use analogies and examples
   - Break down into digestible parts

2. **Question Answering**
   - Answer "What is...?" questions
   - Clarify confusion: "I don't understand..."
   - Provide context: "Why is this important?"

3. **Hint Generation**
   - Give clues without full solutions
   - Socratic questioning: "What happens if...?"
   - Guide toward discovery

4. **Resource Suggestions**
   - Recommend related videos
   - Point to relevant documentation
   - Suggest practice exercises

5. **Code Assistance** (Limited)
   - Explain code logic
   - Debug conceptual errors
   - **Not allowed**: Write complete solutions

### Conversational Behavior

**Tone**:
- Friendly and encouraging
- Patient and non-judgmental
- Professional yet approachable

**Response Style**:
- Clear and concise
- Use formatting (bold, code blocks)
- Provide examples when helpful
- Ask follow-up questions to ensure understanding

**Educational Guardrails**:
- Never give complete homework/lab solutions
- Guide with questions, not direct answers
- Encourage critical thinking
- Suggest trying before revealing

---

## Implementation

### AI Tutor Class

```python
# components/ai_tutor.py
import ollama
import streamlit as st
from datetime import datetime
from utils.feature_flags import get_tier_config
from utils.database import (
    get_ai_usage, 
    increment_ai_usage, 
    save_conversation,
    get_conversation_history
)

class AITutor:
    """OLLAMA-powered AI Tutor with quota management"""
    
    def __init__(self):
        self.user_id = st.session_state.get('user_id')
        self.tier = st.session_state.get('tier', 'basic').lower()
        self.config = get_tier_config(self.tier)
        self.quota = self.config['ai_tutor_quota']
        self.enabled = self.config['ai_tutor_enabled']
        self.priority = self.config.get('ai_tutor_priority', False)
        self.save_history = self.config.get('ai_tutor_history', False)
        
        # Load usage
        self.usage = get_ai_usage(self.user_id) if self.enabled else 0
    
    def can_ask_question(self) -> tuple[bool, str]:
        """Check if user can ask a question"""
        
        if not self.enabled:
            return False, "🔒 AI Tutor is available in Intermediate tier ($247). Upgrade to unlock!"
        
        # Unlimited quota
        if self.quota == -1:
            return True, "✅ Unlimited questions remaining"
        
        # Check quota
        if self.usage >= self.quota:
            return False, f"❌ You've used all {self.quota} questions this month. Upgrade to Advanced for unlimited!"
        
        remaining = self.quota - self.usage
        return True, f"💬 {remaining}/{self.quota} questions remaining this month"
    
    def ask_question(self, question: str, context: dict = None) -> str:
        """Ask a question to the AI Tutor"""
        
        # Check if can ask
        can_ask, message = self.can_ask_question()
        
        if not can_ask:
            return message
        
        # Build context
        if context is None:
            context = self._get_current_context()
        
        # Build prompt
        prompt = self._build_prompt(question, context)
        
        # Call OLLAMA
        try:
            response = self._call_ollama(prompt)
            
            # Increment usage (unless unlimited)
            if self.quota != -1:
                increment_ai_usage(self.user_id)
                self.usage += 1
            
            # Save conversation (if enabled)
            if self.save_history:
                save_conversation(
                    user_id=self.user_id,
                    question=question,
                    response=response,
                    context=context,
                    timestamp=datetime.now()
                )
            
            return response
        
        except Exception as e:
            st.error(f"❌ Error communicating with AI Tutor: {str(e)}")
            return "I'm having trouble right now. Please try again in a moment."
    
    def _get_current_context(self) -> dict:
        """Get current learning context from session"""
        return {
            'course_id': st.session_state.get('current_course_id', 'unknown'),
            'course_title': st.session_state.get('current_course_title', 'Unknown Course'),
            'module_id': st.session_state.get('current_module_id', 'unknown'),
            'module_name': st.session_state.get('current_module_name', 'Unknown Module'),
            'topic': st.session_state.get('current_topic', 'General'),
            'video_title': st.session_state.get('current_video_title', None)
        }
    
    def _build_prompt(self, question: str, context: dict) -> str:
        """Build educational prompt for OLLAMA"""
        
        system_instruction = """You are a helpful AI tutor for GAI-Observe Academy. Your role is to:

1. Guide students toward understanding, not give direct answers
2. Use the Socratic method: ask questions to help students think
3. Provide hints and explanations, not complete solutions
4. Be encouraging and patient
5. Use examples and analogies when helpful
6. Keep responses concise (2-3 paragraphs max)

IMPORTANT RULES:
- Never write complete code solutions for labs or assignments
- Never give direct answers to quiz/exam questions
- If asked for a solution, provide hints and guidance instead
- Encourage students to try first, then help them debug

Educational Philosophy: "Guide, don't tell."
"""
        
        context_str = f"""
Current Context:
- Course: {context['course_title']} ({context['course_id']})
- Module: {context['module_name']} ({context['module_id']})
- Topic: {context['topic']}
"""
        
        if context.get('video_title'):
            context_str += f"- Current Video: {context['video_title']}\n"
        
        full_prompt = f"""{system_instruction}

{context_str}

Student Question: {question}

Provide a helpful, educational response that guides the student toward understanding:
"""
        
        return full_prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """Call OLLAMA API"""
        
        # OLLAMA configuration
        model = "llama3.1:8b"
        
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            options={
                'temperature': 0.7,
                'num_predict': 500,  # Max tokens
            }
        )
        
        return response['message']['content']
    
    def get_quota_info(self) -> dict:
        """Get current quota information"""
        return {
            'enabled': self.enabled,
            'quota': self.quota,
            'usage': self.usage,
            'remaining': self.quota - self.usage if self.quota != -1 else -1,
            'unlimited': self.quota == -1,
            'tier': self.tier
        }
    
    def get_conversation_history(self, limit: int = 10) -> list:
        """Get past conversations (Advanced tier only)"""
        if not self.save_history:
            return []
        
        return get_conversation_history(self.user_id, limit=limit)
```

---

## UI Components

### AI Tutor Sidebar

```python
# components/ai_tutor_ui.py
import streamlit as st
from components.ai_tutor import AITutor

def render_ai_tutor_sidebar():
    """Render AI Tutor in sidebar"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🤖 AI Tutor")
    
    # Initialize AI Tutor
    if 'ai_tutor' not in st.session_state:
        st.session_state.ai_tutor = AITutor()
    
    tutor = st.session_state.ai_tutor
    
    # Check if enabled
    can_ask, message = tutor.can_ask_question()
    
    # Display quota status
    quota_info = tutor.get_quota_info()
    
    if quota_info['enabled']:
        if quota_info['unlimited']:
            st.sidebar.success("✅ Unlimited questions")
        else:
            remaining = quota_info['remaining']
            total = quota_info['quota']
            
            # Progress bar
            progress = (total - remaining) / total
            st.sidebar.progress(progress)
            st.sidebar.caption(f"{remaining}/{total} questions remaining")
            
            # Warning if running low
            if remaining <= 5:
                st.sidebar.warning(f"⚠️ Only {remaining} questions left!")
    else:
        st.sidebar.info("🔒 AI Tutor available in Intermediate tier")
        if st.sidebar.button("Upgrade to Intermediate"):
            st.switch_page("pages/7_⚙️_Settings.py")
        return
    
    # Chat interface
    st.sidebar.markdown("---")
    
    # Question input
    question = st.sidebar.text_area(
        "Ask me anything about the course:",
        placeholder="e.g., Can you explain gradient descent?",
        height=100,
        key="ai_tutor_question"
    )
    
    # Ask button
    if st.sidebar.button("🚀 Ask AI Tutor", type="primary", disabled=not can_ask):
        if question.strip():
            with st.sidebar.spinner("🤔 Thinking..."):
                response = tutor.ask_question(question)
            
            # Display response
            st.sidebar.markdown("**AI Tutor:**")
            st.sidebar.info(response)
            
            # Clear input
            st.session_state.ai_tutor_question = ""
        else:
            st.sidebar.warning("Please enter a question first.")
    
    # Status message
    if not can_ask:
        st.sidebar.error(message)
    
    # Conversation history (Advanced tier only)
    if quota_info.get('save_history'):
        render_conversation_history(tutor)


def render_conversation_history(tutor: AITutor):
    """Render conversation history (Advanced tier)"""
    
    st.sidebar.markdown("---")
    
    with st.sidebar.expander("📜 Conversation History"):
        history = tutor.get_conversation_history(limit=5)
        
        if not history:
            st.write("No previous conversations yet.")
        else:
            for i, conv in enumerate(history):
                st.markdown(f"**Q{i+1}:** {conv['question'][:50]}...")
                st.caption(f"{conv['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                
                if st.button(f"View", key=f"view_conv_{i}"):
                    st.markdown(f"**Question:** {conv['question']}")
                    st.markdown(f"**Answer:** {conv['response']}")
```

### Standalone AI Tutor Page

```python
# pages/8_🤖_AI_Tutor.py (Optional dedicated page)
import streamlit as st
from components.ai_tutor import AITutor

st.set_page_config(page_title="AI Tutor", page_icon="🤖")

st.title("🤖 AI Tutor")
st.write("Your intelligent learning companion")

# Initialize
if 'ai_tutor' not in st.session_state:
    st.session_state.ai_tutor = AITutor()

tutor = st.session_state.ai_tutor

# Quota display
quota_info = tutor.get_quota_info()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tier", quota_info['tier'].title())

with col2:
    if quota_info['unlimited']:
        st.metric("Questions", "Unlimited")
    else:
        st.metric("Remaining", quota_info['remaining'])

with col3:
    st.metric("Total Used", quota_info['usage'])

st.markdown("---")

# Main chat interface
st.subheader("Ask Me Anything")

question = st.text_area(
    "Type your question:",
    placeholder="e.g., What is the difference between supervised and unsupervised learning?",
    height=150
)

if st.button("🚀 Ask", type="primary"):
    if question.strip():
        can_ask, message = tutor.can_ask_question()
        
        if can_ask:
            with st.spinner("🤔 Let me think..."):
                response = tutor.ask_question(question)
            
            st.success("**AI Tutor Response:**")
            st.markdown(response)
        else:
            st.error(message)
    else:
        st.warning("Please enter a question.")

# Conversation history
if quota_info.get('save_history'):
    st.markdown("---")
    st.subheader("📜 Recent Conversations")
    
    history = tutor.get_conversation_history(limit=10)
    
    for i, conv in enumerate(history):
        with st.expander(f"Q: {conv['question'][:80]}..."):
            st.markdown(f"**Asked:** {conv['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            st.markdown(f"**Question:** {conv['question']}")
            st.markdown(f"**Answer:** {conv['response']}")
```

---

## Database Schema

### AI Tutor Usage Table

```sql
CREATE TABLE ai_tutor_usage (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    month VARCHAR(7) NOT NULL,  -- Format: "2026-01"
    usage_count INTEGER DEFAULT 0,
    last_reset DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, month)
);

-- Indexes
CREATE INDEX idx_ai_usage_user_month ON ai_tutor_usage(user_id, month);
```

### Conversation History Table (Advanced Tier)

```sql
CREATE TABLE ai_tutor_conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    course_id VARCHAR(100),
    module_id VARCHAR(100),
    question TEXT NOT NULL,
    response TEXT NOT NULL,
    context JSONB,
    timestamp TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_conversations_user(user_id),
    INDEX idx_conversations_timestamp(timestamp DESC)
);
```

---

## Quota Management Functions

```python
# utils/database.py
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_current_month() -> str:
    """Get current month in YYYY-MM format"""
    return datetime.now().strftime("%Y-%m")

def get_ai_usage(user_id: str) -> int:
    """Get AI Tutor usage for current month"""
    month = get_current_month()
    
    result = db.query(
        """
        SELECT usage_count 
        FROM ai_tutor_usage 
        WHERE user_id = %s AND month = %s
        """,
        (user_id, month)
    )
    
    if result:
        return result[0]['usage_count']
    else:
        # Initialize for new month
        db.execute(
            """
            INSERT INTO ai_tutor_usage (user_id, month, usage_count, last_reset)
            VALUES (%s, %s, 0, CURRENT_DATE)
            """,
            (user_id, month)
        )
        return 0

def increment_ai_usage(user_id: str):
    """Increment AI Tutor usage count"""
    month = get_current_month()
    
    db.execute(
        """
        INSERT INTO ai_tutor_usage (user_id, month, usage_count, last_reset)
        VALUES (%s, %s, 1, CURRENT_DATE)
        ON CONFLICT (user_id, month)
        DO UPDATE SET 
            usage_count = ai_tutor_usage.usage_count + 1,
            updated_at = NOW()
        """,
        (user_id, month)
    )

def reset_ai_quota(user_id: str):
    """Reset AI Tutor quota (called on tier upgrade to Advanced)"""
    # No action needed - Advanced tier has unlimited quota (-1)
    # Usage tracking continues for analytics
    pass

def save_conversation(user_id: str, question: str, response: str, 
                     context: dict, timestamp: datetime):
    """Save conversation (Advanced tier only)"""
    db.execute(
        """
        INSERT INTO ai_tutor_conversations 
        (user_id, course_id, module_id, question, response, context, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            context.get('course_id'),
            context.get('module_id'),
            question,
            response,
            json.dumps(context),
            timestamp
        )
    )

def get_conversation_history(user_id: str, limit: int = 10) -> list:
    """Get conversation history"""
    results = db.query(
        """
        SELECT question, response, timestamp, context
        FROM ai_tutor_conversations
        WHERE user_id = %s
        ORDER BY timestamp DESC
        LIMIT %s
        """,
        (user_id, limit)
    )
    
    return results
```

---

## Safety & Content Moderation

### Input Filtering

```python
def is_appropriate_question(question: str) -> tuple[bool, str]:
    """Check if question is appropriate"""
    
    # Banned patterns
    inappropriate_patterns = [
        r'hack',
        r'cheat',
        r'write.*complete.*code',
        r'solve.*for.*me',
        r'give.*answer'
    ]
    
    question_lower = question.lower()
    
    for pattern in inappropriate_patterns:
        if re.search(pattern, question_lower):
            return False, "Please rephrase your question. I'm here to guide, not solve problems for you."
    
    return True, ""
```

### Response Validation

```python
def validate_response(response: str) -> str:
    """Validate AI response doesn't contain inappropriate content"""
    
    # Check for complete code solutions
    if response.count('```') > 2:  # Multiple code blocks
        # Log for review
        log_potential_solution_leak(response)
    
    return response
```

---

## Analytics & Monitoring

### Metrics to Track

```python
# AI Tutor Analytics
{
    "total_questions_asked": 12500,
    "questions_by_tier": {
        "intermediate": 8200,
        "advanced": 4300
    },
    "average_questions_per_user": {
        "intermediate": 23,
        "advanced": 87
    },
    "quota_exhaustion_rate": "34%",  # % of Intermediate users hitting limit
    "top_topics": [
        {"topic": "Machine Learning", "count": 3200},
        {"topic": "Neural Networks", "count": 2800},
        {"topic": "Data Preprocessing", "count": 1900}
    ],
    "average_response_time": "2.3s",
    "user_satisfaction": 4.6  # /5 based on feedback
}
```

---

## Testing

### Unit Tests

```python
def test_quota_enforcement():
    tutor = AITutor(tier='intermediate', user_id='test_user')
    
    # Simulate 50 questions
    for i in range(50):
        can_ask, _ = tutor.can_ask_question()
        assert can_ask == True
        tutor.ask_question(f"Question {i}")
    
    # 51st question should fail
    can_ask, message = tutor.can_ask_question()
    assert can_ask == False
    assert "used all" in message

def test_unlimited_quota():
    tutor = AITutor(tier='advanced', user_id='test_user')
    
    # Should always be able to ask
    for i in range(100):
        can_ask, _ = tutor.can_ask_question()
        assert can_ask == True
```

---

## Future Enhancements

### Phase 2
- **Voice Input**: Ask questions via voice
- **Multi-turn Conversations**: Remember context across questions
- **Code Review**: AI reviews student code and provides feedback
- **Personalized Learning**: Adapt explanations to user's level

### Phase 3
- **Collaborative Learning**: Group Q&A sessions
- **Tutor Analytics Dashboard**: Show learning patterns
- **Custom Models**: Fine-tuned on course content
- **Video Explanations**: AI generates video responses

---

## Conclusion

The AI Tutor provides intelligent, context-aware educational assistance with strict quota management and a focus on guiding students toward understanding rather than providing direct solutions. The implementation leverages OLLAMA for local, cost-effective AI inference while maintaining high educational quality.

