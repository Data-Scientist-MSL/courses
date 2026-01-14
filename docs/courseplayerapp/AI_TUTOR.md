# CoursePlayerApp AI Tutor Specification

## Overview

The AI Tutor is an intelligent learning assistant powered by OLLAMA (local large language models) that provides context-aware Q&A, code explanations, concept clarification, and personalized learning support. This feature is tier-gated with quota management for Intermediate users and unlimited access for Advanced users.

## Feature Availability by Tier

| Tier | Access | Quota | Features |
|------|--------|-------|----------|
| **Basic** | ❌ Locked | N/A | Upgrade CTA shown |
| **Intermediate** | ✅ Enabled | 50 questions/month | Context-aware Q&A, code help |
| **Advanced** | ✅ Enabled | ∞ Unlimited | All features + priority responses |

---

## AI Tutor Capabilities

### 1. Context-Aware Q&A

The AI Tutor knows:
- **Current course**: Which course the user is taking
- **Current module**: Which module/section they're in
- **Video timestamp**: Where they paused the video
- **Code context**: Code they're working on in labs
- **Previous questions**: Conversation history (session-scoped)

**Example Interaction**:
```
User (watching video at 5:23): "What did he mean by gradient descent?"

AI Tutor: "Based on where you are in the video (5:23 - 'Optimization Algorithms'), 
gradient descent is an iterative optimization algorithm used to minimize the cost 
function in machine learning models. The instructor just explained that it works by:
1. Starting with random parameter values
2. Computing the gradient (slope) of the cost function
3. Taking small steps in the direction that reduces the cost
4. Repeating until convergence

Would you like me to explain the math behind it or show you a code example?"
```

### 2. Code Explanation and Debugging

**Capabilities**:
- Explain what code does line-by-line
- Debug errors and suggest fixes
- Suggest optimizations and best practices
- Compare different implementation approaches

**Example Interaction**:
```python
User: "Why is this code giving me a KeyError?"
Code:
    data = {'name': 'Alice', 'age': 30}
    print(data['email'])

AI Tutor: "You're getting a KeyError because the dictionary 'data' doesn't have 
a key called 'email'. It only has 'name' and 'age'.

To fix this, you have a few options:

1. Use .get() method (safe):
   print(data.get('email', 'Not provided'))
   
2. Check if key exists:
   if 'email' in data:
       print(data['email'])
   else:
       print('Email not found')

3. Use try-except:
   try:
       print(data['email'])
   except KeyError:
       print('Email not in data')

Which approach would you like to use?"
```

### 3. Concept Clarification

Explain complex concepts in simpler terms with examples.

**Example Interaction**:
```
User: "What's the difference between supervised and unsupervised learning?"

AI Tutor: "Great question! Let me break it down:

**Supervised Learning**: You have labeled data (input + correct output)
- Example: Teaching a kid to identify fruits by showing them labeled pictures
  ('This is an apple', 'This is a banana')
- Algorithms: Linear Regression, Decision Trees, Neural Networks
- Use case: Predicting house prices, email spam detection

**Unsupervised Learning**: You have unlabeled data (input only, no correct answers)
- Example: Giving a kid a box of mixed toys and asking them to organize by similarity
- Algorithms: K-Means Clustering, PCA, Autoencoders
- Use case: Customer segmentation, anomaly detection

In the course you're taking (Machine Learning Fundamentals - Module 2), you'll 
explore supervised learning first, then move to unsupervised in Module 5.

Want me to show you a code example of each?"
```

### 4. Practice Problem Generation

Create custom exercises based on the current topic.

**Example Interaction**:
```
User: "Can you give me a practice problem on loops?"

AI Tutor: "Sure! Here's a problem matching your current skill level:

**Problem**: Write a function that takes a list of numbers and returns 
a new list with only the even numbers.

Example:
Input: [1, 2, 3, 4, 5, 6]
Output: [2, 4, 6]

Hints:
- Use a for loop to iterate through the list
- Use the modulo operator (%) to check if a number is even
- Append even numbers to a new list

Try solving it, then paste your code and I'll review it!"
```

### 5. Study Tips and Learning Strategies

Provide personalized learning advice.

**Example Interaction**:
```
User: "I'm struggling to remember all these algorithms. Any tips?"

AI Tutor: "I can see you're in Module 4 (Classification Algorithms). Here are 
some strategies that work well:

1. **Create a Comparison Table**: Make a table comparing:
   - Algorithm name
   - How it works (one sentence)
   - Pros and cons
   - When to use it

2. **Hands-On Practice**: The best way to remember is by implementing. 
   Complete the labs in this module - you have 3 labs remaining.

3. **Teach Someone**: Explain each algorithm to a friend (or write it down 
   as if teaching). This reveals gaps in understanding.

4. **Use Mnemonics**: 
   - KNN = "Keep Nearest Neighbors"
   - SVM = "Support Vectors are Margins"

5. **Spaced Repetition**: Review this material again in 1 day, 3 days, and 7 days.

Your progress shows you've completed 73% of this module - you're doing great! 
Keep going. 🎯
```

---

## Implementation: OLLAMA Integration

### OLLAMA Setup

**Installation**:
```bash
# Install OLLAMA on server
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3:70b       # General Q&A (70B for better quality)
ollama pull codellama:34b    # Code-specific tasks
ollama pull mistral:7b       # Faster responses (fallback)
```

**Model Selection Strategy**:
- **General questions**: Llama 3 70B
- **Code explanations**: CodeLlama 34B
- **Simple questions**: Mistral 7B (faster)
- **Tier-based priority**:
  - Advanced users: Always use best model (70B)
  - Intermediate users: Use 70B for complex questions, 7B for simple ones

### Python Client

```python
# courseplayerapp/ai_tutor/tutor.py

import httpx
from typing import Optional, List, Dict
from datetime import datetime

class AITutor:
    """AI-powered learning assistant using OLLAMA."""
    
    def __init__(
        self,
        user_id: str,
        user_tier: str,
        ollama_base_url: str = "http://localhost:11434"
    ):
        self.user_id = user_id
        self.user_tier = user_tier
        self.ollama_base_url = ollama_base_url
        self.conversation_history: List[Dict] = []
        
        # Select model based on tier
        self.model = self._select_model()
    
    def _select_model(self) -> str:
        """Select OLLAMA model based on user tier."""
        if self.user_tier == "advanced":
            return "llama3:70b"  # Best quality for Advanced users
        else:
            return "llama3:70b"  # Intermediate users get same quality, just limited quota
    
    async def ask_question(
        self,
        question: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Ask the AI Tutor a question with context.
        
        Args:
            question: User's question
            context: {
                "course_id": str,
                "module_id": str,
                "video_id": str,
                "video_timestamp": int,  # seconds
                "code_snippet": str,  # optional
                "lab_id": str  # optional
            }
        
        Returns:
            AI Tutor's response
        """
        # Check quota before processing
        quota_manager = QuotaManager(self.user_id, self.user_tier)
        if not quota_manager.can_ask():
            raise QuotaExceededError(
                f"Monthly quota exceeded. "
                f"Upgrade to Advanced for unlimited AI Tutor access."
            )
        
        # Build context-aware prompt
        prompt = self._build_prompt(question, context)
        
        # Call OLLAMA
        response = await self._call_ollama(prompt)
        
        # Update quota
        quota_manager.use_quota()
        
        # Store in conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": response,
            "context": context
        })
        
        # Log for analytics
        self._log_interaction(question, response, context)
        
        return response
    
    def _build_prompt(self, question: str, context: Optional[Dict]) -> str:
        """
        Build context-aware prompt for OLLAMA.
        
        Includes:
        - System instructions (role as tutor)
        - Course/module context
        - Conversation history
        - User's question
        """
        system_prompt = """You are an expert AI Tutor for EdGuide, an elite learning platform. 
Your role is to help students understand concepts, debug code, and succeed in their courses.

Guidelines:
- Be encouraging and supportive
- Explain concepts clearly with examples
- Ask follow-up questions to check understanding
- Suggest hands-on practice when appropriate
- If you don't know something, admit it and suggest resources
- Keep responses concise but thorough (2-4 paragraphs)
- Use code examples when relevant
- Reference the course material when possible
"""
        
        # Add context information
        context_str = ""
        if context:
            course_info = self._get_course_info(context.get("course_id"))
            module_info = self._get_module_info(context.get("module_id"))
            
            context_str = f"""
**Current Context**:
- Course: {course_info.get('title', 'Unknown')}
- Module: {module_info.get('title', 'Unknown')}
- Topic: {module_info.get('topic', 'Unknown')}
"""
            
            if context.get("video_timestamp"):
                minutes = context["video_timestamp"] // 60
                seconds = context["video_timestamp"] % 60
                context_str += f"- Video Position: {minutes}:{seconds:02d}\n"
            
            if context.get("code_snippet"):
                context_str += f"\n**User's Code**:\n```python\n{context['code_snippet']}\n```\n"
        
        # Add conversation history (last 3 exchanges)
        history_str = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-3:]
            history_str = "\n**Previous Conversation**:\n"
            for entry in recent_history:
                history_str += f"Q: {entry['question']}\nA: {entry['answer']}\n\n"
        
        # Combine all parts
        full_prompt = f"{system_prompt}\n\n{context_str}\n{history_str}\n**Student's Question**: {question}\n\n**Your Response**:"
        
        return full_prompt
    
    async def _call_ollama(self, prompt: str) -> str:
        """Call OLLAMA API to generate response."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 1000
                    }
                }
            )
            
            result = response.json()
            return result["response"]
    
    def _get_course_info(self, course_id: Optional[str]) -> Dict:
        """Fetch course metadata from database."""
        if not course_id:
            return {}
        
        # Query database for course info
        course = db.query(
            "SELECT title, description, instructor FROM courses WHERE id = %s",
            (course_id,)
        )
        return course or {}
    
    def _get_module_info(self, module_id: Optional[str]) -> Dict:
        """Fetch module metadata from database."""
        if not module_id:
            return {}
        
        module = db.query(
            "SELECT title, topic, description FROM modules WHERE id = %s",
            (module_id,)
        )
        return module or {}
    
    def _log_interaction(
        self,
        question: str,
        answer: str,
        context: Optional[Dict]
    ):
        """Log AI Tutor interaction for analytics."""
        analytics.track(
            user_id=self.user_id,
            event="ai_tutor_question",
            properties={
                "question_length": len(question),
                "answer_length": len(answer),
                "has_code_context": bool(context and context.get("code_snippet")),
                "course_id": context.get("course_id") if context else None,
                "model_used": self.model,
                "tier": self.user_tier
            }
        )
```

---

## Quota Management

### Quota Tracker

```python
# courseplayerapp/ai_tutor/quota_tracker.py

import redis
from datetime import datetime, timezone
from calendar import monthrange

class QuotaManager:
    """Manage AI Tutor usage quotas."""
    
    QUOTAS = {
        "basic": 0,          # Locked
        "intermediate": 50,  # 50 questions/month
        "advanced": float('inf')  # Unlimited
    }
    
    def __init__(self, user_id: str, tier: str):
        self.user_id = user_id
        self.tier = tier
        self.quota_limit = self.QUOTAS.get(tier, 0)
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
    
    def can_ask(self) -> bool:
        """Check if user can ask another question."""
        if self.tier == "basic":
            return False
        if self.tier == "advanced":
            return True
        
        # Intermediate tier - check quota
        return self.get_remaining() > 0
    
    def get_usage(self) -> int:
        """Get number of questions used this month."""
        cache_key = self._get_cache_key()
        usage = self.redis.get(cache_key)
        return int(usage) if usage else 0
    
    def get_remaining(self) -> int:
        """Get remaining questions this month."""
        if self.tier == "advanced":
            return float('inf')
        
        return max(0, self.quota_limit - self.get_usage())
    
    def use_quota(self, amount: int = 1):
        """Increment usage counter."""
        if self.tier == "advanced":
            return  # No quota to track
        
        cache_key = self._get_cache_key()
        self.redis.incr(cache_key, amount)
        
        # Set expiration to end of month
        if self.redis.ttl(cache_key) == -1:  # No expiration set
            expire_at = self._get_end_of_month_timestamp()
            self.redis.expireat(cache_key, expire_at)
    
    def _get_cache_key(self) -> str:
        """Generate Redis cache key for current month."""
        year_month = datetime.now(timezone.utc).strftime("%Y-%m")
        return f"ai_tutor_quota:{self.user_id}:{year_month}"
    
    def _get_end_of_month_timestamp(self) -> int:
        """Get Unix timestamp for end of current month."""
        now = datetime.now(timezone.utc)
        last_day = monthrange(now.year, now.month)[1]
        end_of_month = datetime(now.year, now.month, last_day, 23, 59, 59, tzinfo=timezone.utc)
        return int(end_of_month.timestamp())
    
    def get_usage_history(self) -> List[Dict]:
        """Get historical usage data (last 6 months)."""
        history = []
        now = datetime.now(timezone.utc)
        
        for months_ago in range(6):
            month_date = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
            month_date = month_date.replace(month=month_date.month - months_ago)
            
            cache_key = f"ai_tutor_quota:{self.user_id}:{month_date.strftime('%Y-%m')}"
            usage = self.redis.get(cache_key)
            
            history.append({
                "month": month_date.strftime("%B %Y"),
                "used": int(usage) if usage else 0,
                "limit": self.quota_limit
            })
        
        return history


class QuotaExceededError(Exception):
    """Raised when user exceeds AI Tutor quota."""
    pass
```

---

## UI Components

### Chat Interface (Streamlit)

```python
# courseplayerapp/ui/components/ai_tutor_chat.py

import streamlit as st
import asyncio
from courseplayerapp.ai_tutor.tutor import AITutor, QuotaManager, QuotaExceededError

def render_ai_tutor_chat(user_tier: str):
    """Render AI Tutor chat interface with tier checking."""
    
    # Check tier access
    if user_tier == "basic":
        st.info("🔒 **AI Tutor is Locked**")
        st.markdown("""
        Unlock your AI-powered learning assistant:
        - 📚 Get instant answers to your questions
        - 💻 Debug code and get explanations
        - 🎯 Receive personalized study tips
        - ✨ Generate practice problems
        """)
        st.button("💎 Upgrade to Intermediate (50 Q/month) - $247", on_click=redirect_to_upgrade)
        return
    
    # Initialize quota manager
    quota = QuotaManager(st.session_state.user_id, user_tier)
    
    # Display quota status
    st.subheader("AI Tutor 🤖")
    
    if user_tier == "intermediate":
        remaining = quota.get_remaining()
        used = quota.get_usage()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(used / 50, text=f"{used}/50 questions used this month")
        with col2:
            if remaining < 10:
                st.error(f"{remaining} left")
            else:
                st.success(f"{remaining} left")
        
        if remaining < 10:
            st.warning(f"⚠️ Only {remaining} questions remaining this month")
            st.info("💎 Upgrade to Advanced for **unlimited** AI Tutor access")
    
    elif user_tier == "advanced":
        st.success("✅ **Unlimited AI Tutor Access**")
    
    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.chat_message("user").markdown(message["content"])
            else:
                st.chat_message("assistant").markdown(message["content"])
    
    # Input area
    user_question = st.chat_input("Ask me anything about this course...")
    
    if user_question:
        # Check quota
        if not quota.can_ask():
            st.error("❌ Monthly quota exceeded. Upgrade to Advanced for unlimited access.")
            st.button("💎 Upgrade Now", on_click=redirect_to_upgrade)
            return
        
        # Add user message to chat
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })
        
        # Show thinking indicator
        with st.spinner("🤔 Thinking..."):
            # Initialize AI Tutor
            tutor = AITutor(
                user_id=st.session_state.user_id,
                user_tier=user_tier
            )
            
            # Get current context
            context = {
                "course_id": st.session_state.get("current_course"),
                "module_id": st.session_state.get("current_module"),
                "video_id": st.session_state.get("current_video"),
                "video_timestamp": st.session_state.get("video_position", 0),
                "code_snippet": st.session_state.get("current_code")
            }
            
            try:
                # Get answer
                answer = asyncio.run(tutor.ask_question(user_question, context))
                
                # Add AI response to chat
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })
                
            except QuotaExceededError as e:
                st.error(f"❌ {str(e)}")
                st.button("💎 Upgrade to Advanced", on_click=redirect_to_upgrade)
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # Rerun to show new messages
        st.rerun()
    
    # Helpful prompts
    with st.expander("💡 Need help getting started?"):
        st.markdown("""
        **Try asking:**
        - "Explain this concept in simpler terms"
        - "What's the difference between X and Y?"
        - "Can you debug this code?"
        - "Give me a practice problem on [topic]"
        - "What should I focus on in this module?"
        - "How does this relate to real-world applications?"
        """)
        
        if st.button("Ask: 'Summarize this module'"):
            # Populate chat input (would need custom component in real implementation)
            pass
```

### Quota Usage Dashboard

```python
def render_quota_usage_dashboard(user_tier: str):
    """Display AI Tutor usage analytics (for user)."""
    
    if user_tier == "basic":
        st.info("AI Tutor analytics available for Intermediate and Advanced tiers")
        return
    
    quota = QuotaManager(st.session_state.user_id, user_tier)
    
    st.subheader("AI Tutor Usage")
    
    # Current month stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions This Month", quota.get_usage())
    with col2:
        if user_tier == "intermediate":
            st.metric("Remaining", quota.get_remaining())
        else:
            st.metric("Remaining", "∞ Unlimited")
    with col3:
        st.metric("Tier", user_tier.capitalize())
    
    # Historical usage chart
    if user_tier == "intermediate":
        history = quota.get_usage_history()
        
        chart_data = {
            "Month": [h["month"] for h in history],
            "Used": [h["used"] for h in history],
            "Limit": [h["limit"] for h in history]
        }
        
        st.line_chart(chart_data, x="Month", y=["Used", "Limit"])
```

---

## Response Time Optimization

### Caching Common Questions

```python
# Cache frequently asked questions
import hashlib

class CachedAITutor(AITutor):
    """AI Tutor with response caching for common questions."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_ttl = 86400  # 24 hours
    
    async def ask_question(self, question: str, context: Optional[Dict] = None) -> str:
        # Check cache first
        cache_key = self._generate_cache_key(question, context)
        cached_response = self.redis.get(cache_key)
        
        if cached_response:
            return cached_response.decode('utf-8')
        
        # If not cached, generate new response
        response = await super().ask_question(question, context)
        
        # Cache the response
        self.redis.setex(cache_key, self.cache_ttl, response)
        
        return response
    
    def _generate_cache_key(self, question: str, context: Optional[Dict]) -> str:
        """Generate cache key from question and context."""
        key_data = f"{question}:{context.get('course_id') if context else ''}"
        return f"ai_tutor_cache:{hashlib.md5(key_data.encode()).hexdigest()}"
```

### Priority Queue for Advanced Users

```python
# Advanced users get faster responses via priority queue
class PriorityAITutor(AITutor):
    """AI Tutor with priority queue for Advanced tier."""
    
    async def ask_question(self, question: str, context: Optional[Dict] = None) -> str:
        if self.user_tier == "advanced":
            # Use dedicated GPU server for Advanced users
            self.ollama_base_url = "http://gpu-priority.internal:11434"
        
        return await super().ask_question(question, context)
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: EdGuide AI Team  
**Platform**: EdGuide (gai-observe.online)
