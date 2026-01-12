# AI Tutor Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Define AI-powered learning assistant using OLLAMA

---

## Overview

The AI Tutor provides context-aware, intelligent learning assistance to help students understand concepts, debug code, and improve their learning outcomes. Access is tier-gated with quota management for Intermediate users and unlimited access for Advanced users.

---

## Tier-Based Access

| Tier | Access | Quota | Features |
|------|--------|-------|----------|
| **Basic** | ❌ Locked | 0 questions | None - upgrade required |
| **Intermediate** | ✅ Enabled | 50 questions/month | Context-aware Q&A, code debugging, concept clarification |
| **Advanced** | ✅ Enabled | ♾️ Unlimited | All Intermediate features + priority responses + advanced analysis |

---

## AI Tutor Features

### 1. Context-Aware Q&A

The AI Tutor understands the student's current learning context:
- **Current Course**: Which course they're taking
- **Current Module**: Which module they're in
- **Current Video**: Timestamp of where they are in the video
- **Recent Labs**: Which labs they've completed or are working on
- **Progress**: Their overall progress and performance

**Example Interaction**:
```
Student: "I don't understand what gradient descent means"

AI Tutor (with context):
"Based on where you are in the Machine Learning course (Module 3, Video 2 at 5:32), 
gradient descent is an optimization algorithm we use to minimize the cost function. 

In the example Prof. Ng just showed, imagine you're on a hill and want to reach 
the lowest point. Gradient descent works by:
1. Looking at the slope where you are
2. Taking a step in the direction that goes downhill
3. Repeating until you reach the bottom

Would you like me to explain the mathematical formula, or show you a code example?"
```

### 2. Code Explanation and Debugging

**Features**:
- Explain code line-by-line
- Identify bugs and suggest fixes
- Improve code quality (style, performance)
- Suggest alternative approaches
- Explain error messages

**Example**:
```python
# Student's code with bug
def calculate_mean(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Bug: ZeroDivisionError if empty list

# Student asks: "Why does this crash with empty list?"

# AI Tutor response:
"""
Great question! Your function crashes because of a ZeroDivisionError when the 
input list is empty. Here's why:

Line 5: `return total / len(numbers)`
- If `numbers` is an empty list, `len(numbers)` returns 0
- Dividing by 0 causes a ZeroDivisionError

**Fix Option 1 (Defensive Programming)**:
```python
def calculate_mean(numbers):
    if not numbers:  # Check if list is empty
        return 0  # or raise ValueError("Cannot calculate mean of empty list")
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

**Fix Option 2 (Using Built-ins)**:
```python
from statistics import mean

def calculate_mean(numbers):
    return mean(numbers) if numbers else 0
```

The built-in `mean()` function handles edge cases better. Which approach would 
you prefer to use?
"""
```

### 3. Concept Clarification

**Capabilities**:
- Simplify complex topics
- Provide analogies and examples
- Link to related concepts
- Suggest prerequisite knowledge
- Recommend further reading

**Example**:
```
Student: "What's the difference between supervised and unsupervised learning?"

AI Tutor:
"Great question! Let me explain with a simple analogy:

**Supervised Learning** = Learning with a teacher
- You have labeled data (inputs with correct answers)
- Algorithm learns from examples
- Example: Email spam filter (you label emails as spam/not spam, it learns patterns)

**Unsupervised Learning** = Learning by discovering patterns yourself
- No labeled data (no correct answers provided)
- Algorithm finds hidden patterns
- Example: Customer segmentation (group customers by behavior without pre-defined categories)

In your current course (Module 2), you just learned about supervised learning with 
linear regression. In Module 5, you'll explore unsupervised learning with clustering.

Would you like specific examples from the course materials?"
```

### 4. Practice Problem Generation

**Features**:
- Generate practice problems based on current topic
- Adjust difficulty based on student's progress
- Provide step-by-step solutions
- Create variations of course exercises

**Example**:
```
Student: "Can you give me a practice problem for linear regression?"

AI Tutor:
"Sure! Here's a practice problem based on what you just learned:

**Problem**: Housing Price Prediction

You have data on 5 houses with their sizes and prices:
- House 1: 1000 sq ft, $200,000
- House 2: 1500 sq ft, $280,000
- House 3: 1200 sq ft, $240,000
- House 4: 1800 sq ft, $340,000
- House 5: 1100 sq ft, $220,000

**Task**:
1. Implement linear regression to predict house prices based on size
2. Predict the price of a 1400 sq ft house
3. Calculate the R² score

**Hints**:
- Use sklearn.linear_model.LinearRegression
- Remember to reshape your data (X.reshape(-1, 1))
- The answer should be around $260,000-$270,000

Try it in your lab environment, then ask me if you need help!
"""
```

### 5. Study Tips and Learning Strategies

**Features**:
- Personalized study recommendations
- Time management advice
- Learning technique suggestions
- Prerequisite identification
- Next steps guidance

**Example**:
```
Student: "I'm struggling with this module. Any tips?"

AI Tutor (analyzes progress):
"I can see you've watched 60% of Module 3 videos but haven't completed any labs yet. 
Here are some strategies:

**Immediate Actions**:
1. Pause video watching and try Lab 3.1 - hands-on practice will help concepts stick
2. Review Module 2 if gradient descent still feels unclear (foundation for Module 3)
3. Use the 2x speed less - retention improves at 1.25x-1.5x for complex topics

**Study Techniques**:
- Active Recall: After each video, write down 3 key points without looking
- Spaced Repetition: Review yesterday's material before starting today's
- Feynman Technique: Explain concepts in simple terms (try explaining to me!)

**Next Steps**:
1. Complete Lab 3.1 (25 min)
2. Watch remaining Module 3 videos
3. Take the quiz (aim for 80%+)

Would you like me to generate practice questions for gradient descent to reinforce 
your understanding?"
```

---

## OLLAMA Implementation

### Technology Stack

**Model Options**:
```yaml
ai_models:
  primary: "llama3:70b"  # Best quality, slower
  fallback: "llama3:13b"  # Faster, good quality
  code_specialized: "codellama:34b"  # For code-heavy questions
  
  model_selection_logic:
    - code_question: "codellama:34b"
    - complex_concept: "llama3:70b"
    - simple_question: "llama3:13b"
```

**Infrastructure**:
```yaml
deployment:
  platform: "Docker container with GPU"
  gpu: "NVIDIA A100 or T4"
  ram: "64GB"
  storage: "500GB SSD (for models)"
  
  scaling:
    min_instances: 2
    max_instances: 10
    scale_on: "queue_depth > 5"
```

### Implementation

```python
# ai_tutor/tutor.py

import ollama
from datetime import datetime
from typing import Optional

class AITutor:
    def __init__(self, user_tier: str, user_id: str):
        self.tier = user_tier
        self.user_id = user_id
        self.quota_manager = QuotaManager()
        self.context_builder = ContextBuilder()
        
        # Model selection based on tier
        if tier == "advanced":
            self.model = "llama3:70b"  # Best model for unlimited users
        else:
            self.model = "llama3:13b"  # Faster model for quota users
    
    async def ask_question(
        self,
        question: str,
        context: Optional[dict] = None
    ) -> dict:
        """
        Process a student question
        
        Args:
            question: Student's question
            context: Learning context (course, module, video, etc.)
        
        Returns:
            {
                "answer": "AI response",
                "quota_remaining": 45,
                "response_time_ms": 1234
            }
        """
        start_time = datetime.now()
        
        # Check quota
        quota_check = await self.quota_manager.check_quota(
            self.user_id,
            self.tier
        )
        
        if not quota_check["allowed"]:
            return {
                "error": "Quota exceeded",
                "quota_remaining": 0,
                "message": "Upgrade to Advanced for unlimited AI Tutor access",
                "reset_date": quota_check["reset_date"]
            }
        
        # Build context-aware prompt
        prompt = await self.context_builder.build_prompt(
            question=question,
            user_id=self.user_id,
            context=context
        )
        
        # Call OLLAMA
        response = await ollama.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": 0.7,  # Balance creativity and accuracy
                "top_p": 0.9,
                "top_k": 40,
                "num_predict": 500  # Max tokens
            }
        )
        
        answer = response["response"]
        
        # Record usage
        await self.quota_manager.use_quota(self.user_id, self.tier)
        
        # Log interaction
        await self._log_interaction(
            question=question,
            answer=answer,
            context=context,
            response_time=(datetime.now() - start_time).total_seconds()
        )
        
        # Get updated quota
        quota_info = await self.quota_manager.get_quota_info(
            self.user_id,
            self.tier
        )
        
        return {
            "answer": answer,
            "quota_remaining": quota_info["remaining"],
            "response_time_ms": int((datetime.now() - start_time).total_seconds() * 1000),
            "model_used": self.model
        }
    
    async def explain_code(
        self,
        code: str,
        language: str = "python"
    ) -> str:
        """Explain code snippet"""
        
        prompt = f"""
        You are an expert programming tutor. Explain this {language} code 
        in simple terms for a student learning to program.
        
        Code:
        ```{language}
        {code}
        ```
        
        Provide:
        1. What the code does (high-level)
        2. Line-by-line explanation
        3. Any important concepts or patterns
        4. Potential improvements or issues
        """
        
        return await self.ask_question(prompt)
    
    async def debug_code(
        self,
        code: str,
        error_message: str,
        language: str = "python"
    ) -> dict:
        """Help debug code with error"""
        
        prompt = f"""
        A student's {language} code has an error. Help them fix it.
        
        Code:
        ```{language}
        {code}
        ```
        
        Error:
        {error_message}
        
        Provide:
        1. Explanation of what's wrong
        2. Why the error occurs
        3. How to fix it (with corrected code)
        4. How to prevent similar errors
        """
        
        return await self.ask_question(prompt)
    
    async def generate_practice_problem(
        self,
        topic: str,
        difficulty: str = "medium"
    ) -> dict:
        """Generate a practice problem"""
        
        prompt = f"""
        Generate a {difficulty} difficulty practice problem for the topic: {topic}
        
        Include:
        1. Problem statement (clear and concise)
        2. Sample input/output (if applicable)
        3. Hints (2-3 progressive hints)
        4. Solution approach (high-level steps)
        
        Make it educational and engaging!
        """
        
        return await self.ask_question(prompt)
```

### Context Builder

```python
# ai_tutor/context_builder.py

class ContextBuilder:
    """Build context-aware prompts for AI Tutor"""
    
    async def build_prompt(
        self,
        question: str,
        user_id: str,
        context: Optional[dict] = None
    ) -> str:
        """
        Build a prompt with full learning context
        
        Context includes:
        - Current course/module/lesson
        - User's progress
        - Recent activities
        - Related content
        """
        
        # Get user's learning context
        user_context = await self._get_user_context(user_id)
        
        # Get relevant course content
        course_context = await self._get_course_context(context) if context else None
        
        # Build comprehensive prompt
        prompt = f"""
You are an expert AI tutor for EdGuide, helping students learn {user_context['course_name']}.

**Student Context**:
- Current Course: {user_context['course_name']}
- Current Module: {user_context['module_name']}
- Current Lesson: {user_context['lesson_name']}
- Video Position: {user_context.get('video_timestamp', 'N/A')}
- Progress: {user_context['completion_percent']}% complete
- Recent Topics: {', '.join(user_context['recent_topics'])}

**Relevant Course Material**:
{course_context if course_context else "No specific course material loaded"}

**Student's Question**:
{question}

**Your Task**:
Provide a helpful, clear, and educational answer. Consider:
1. The student's current learning context
2. Their progress level
3. Related concepts they've already learned
4. Upcoming topics they'll need this for

Keep explanations clear and use examples from the course when possible.
"""
        
        return prompt
    
    async def _get_user_context(self, user_id: str) -> dict:
        """Get user's current learning context"""
        
        # Query database for user's current state
        progress = await db.fetch_one(
            """
            SELECT 
                c.name as course_name,
                m.name as module_name,
                l.name as lesson_name,
                up.completion_percent,
                up.current_video_timestamp
            FROM user_progress up
            JOIN courses c ON up.course_id = c.id
            JOIN modules m ON up.module_id = m.id
            JOIN lessons l ON up.lesson_id = l.id
            WHERE up.user_id = :user_id
            AND up.status = 'in_progress'
            ORDER BY up.updated_at DESC
            LIMIT 1
            """,
            {"user_id": user_id}
        )
        
        # Get recent topics
        recent_topics = await self._get_recent_topics(user_id)
        
        return {
            "course_name": progress["course_name"],
            "module_name": progress["module_name"],
            "lesson_name": progress["lesson_name"],
            "completion_percent": progress["completion_percent"],
            "video_timestamp": progress.get("current_video_timestamp"),
            "recent_topics": recent_topics
        }
    
    async def _get_course_context(self, context: dict) -> str:
        """Get relevant course material for context"""
        
        # Retrieve relevant lesson content, transcript snippets, etc.
        # This helps AI give answers grounded in course material
        
        course_material = await db.fetch_one(
            """
            SELECT content, transcript
            FROM lessons
            WHERE id = :lesson_id
            """,
            {"lesson_id": context.get("lesson_id")}
        )
        
        return course_material.get("content", "") if course_material else ""
```

---

## Quota Management

### Quota System

```python
# ai_tutor/quota_tracker.py

class QuotaManager:
    """Manage AI Tutor usage quotas"""
    
    def __init__(self):
        self.redis = redis_client
        self.db = database
    
    async def check_quota(self, user_id: str, tier: str) -> dict:
        """Check if user can ask a question"""
        
        if tier == "advanced":
            return {"allowed": True, "remaining": "unlimited"}
        
        if tier == "intermediate":
            used = await self._get_usage_count(user_id)
            limit = 50
            
            if used >= limit:
                reset_date = self._get_next_month_start()
                return {
                    "allowed": False,
                    "remaining": 0,
                    "reset_date": reset_date.isoformat()
                }
            
            return {
                "allowed": True,
                "remaining": limit - used
            }
        
        # Basic tier
        return {
            "allowed": False,
            "remaining": 0,
            "message": "AI Tutor not available in Basic tier"
        }
    
    async def use_quota(self, user_id: str, tier: str):
        """Record a question asked"""
        
        if tier == "advanced":
            return  # No quota for Advanced
        
        # Increment usage counter in Redis
        month_key = f"ai_tutor_quota:{user_id}:{datetime.now().strftime('%Y-%m')}"
        self.redis.incr(month_key)
        self.redis.expire(month_key, timedelta(days=60))
        
        # Log in database
        await self.db.execute(
            """
            INSERT INTO ai_tutor_usage 
                (user_id, used_at, tier, month)
            VALUES 
                (:user_id, NOW(), :tier, :month)
            """,
            {
                "user_id": user_id,
                "tier": tier,
                "month": datetime.now().strftime('%Y-%m')
            }
        )
    
    async def get_quota_info(self, user_id: str, tier: str) -> dict:
        """Get detailed quota information"""
        
        if tier == "advanced":
            return {
                "total": "unlimited",
                "used": await self._get_usage_count(user_id),
                "remaining": "unlimited",
                "reset_date": None
            }
        
        used = await self._get_usage_count(user_id)
        total = 50
        
        return {
            "total": total,
            "used": used,
            "remaining": max(0, total - used),
            "reset_date": self._get_next_month_start().isoformat()
        }
    
    async def _get_usage_count(self, user_id: str) -> int:
        """Get usage count for current month"""
        
        month_key = f"ai_tutor_quota:{user_id}:{datetime.now().strftime('%Y-%m')}"
        count = self.redis.get(month_key)
        
        return int(count) if count else 0
    
    def _get_next_month_start(self) -> datetime:
        """Get first day of next month"""
        
        today = datetime.now()
        if today.month == 12:
            return datetime(today.year + 1, 1, 1)
        else:
            return datetime(today.year, today.month + 1, 1)
```

---

## UI Components

### AI Tutor Chat Interface

```python
# ui/components/ai_tutor_chat.py

import streamlit as st

def render_ai_tutor_chat(user_tier: str, user_id: str, context: dict):
    """Render AI Tutor chat interface"""
    
    st.subheader("🤖 AI Tutor")
    
    # Check access
    if user_tier == "basic":
        st.warning("🔒 AI Tutor is locked in Basic tier")
        st.info("⬆️ Upgrade to Intermediate for 50 questions/month")
        st.button("Upgrade Now", type="primary")
        return
    
    # Get quota info
    tutor = AITutor(user_tier, user_id)
    quota_info = await tutor.quota_manager.get_quota_info(user_id, user_tier)
    
    # Display quota
    if user_tier == "intermediate":
        col1, col2 = st.columns([3, 1])
        with col1:
            st.metric(
                "Questions Remaining",
                f"{quota_info['remaining']}/{quota_info['total']}"
            )
        with col2:
            if quota_info['remaining'] < 10:
                st.warning("⚡ Low")
    else:  # advanced
        st.metric("Questions", "Unlimited ♾️")
    
    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"**You**: {message['content']}")
            else:
                st.markdown(f"**🤖 AI Tutor**: {message['content']}")
            st.markdown("---")
    
    # Input area
    question = st.text_area(
        "Ask a question",
        placeholder="e.g., Can you explain gradient descent?",
        key="ai_question_input"
    )
    
    col_a, col_b, col_c = st.columns([2, 1, 1])
    
    with col_a:
        ask_button = st.button("🚀 Ask", type="primary", use_container_width=True)
    
    with col_b:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col_c:
        # Quick actions
        with st.popover("💡 Examples"):
            if st.button("Explain current topic"):
                question = "Can you explain the current topic in simple terms?"
                ask_button = True
            
            if st.button("Generate practice problem"):
                question = "Give me a practice problem for this topic"
                ask_button = True
            
            if st.button("Debug my code"):
                question = "Help me debug the code I'm working on"
                ask_button = True
    
    # Process question
    if ask_button and question:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })
        
        # Get AI response
        with st.spinner("🤔 Thinking..."):
            response = await tutor.ask_question(question, context)
        
        if "error" in response:
            st.error(response["message"])
        else:
            # Add AI response
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response["answer"]
            })
            
            # Show response time
            st.caption(f"⚡ Response time: {response['response_time_ms']}ms")
        
        st.rerun()
```

---

## Analytics & Improvement

### Track AI Tutor Performance

```python
# analytics/ai_tutor_analytics.py

async def track_ai_interaction(
    user_id: str,
    question: str,
    answer: str,
    context: dict,
    response_time: float
):
    """Track AI Tutor interaction for analytics"""
    
    await db.execute(
        """
        INSERT INTO ai_tutor_interactions
            (user_id, question, answer, context, response_time_ms, created_at)
        VALUES
            (:user_id, :question, :answer, :context, :response_time, NOW())
        """,
        {
            "user_id": user_id,
            "question": question,
            "answer": answer,
            "context": json.dumps(context),
            "response_time": response_time * 1000
        }
    )

# Metrics to track:
metrics = {
    "usage": {
        "questions_per_user": "Average questions asked per user",
        "quota_utilization": "% of quota used by Intermediate users",
        "peak_usage_times": "When students ask most questions"
    },
    "performance": {
        "avg_response_time": "Average time to generate answer",
        "model_accuracy": "Quality of answers (rated by students)",
        "follow_up_rate": "% of questions leading to follow-ups"
    },
    "topics": {
        "most_asked_topics": "Which topics generate most questions",
        "difficult_concepts": "Concepts students struggle with",
        "question_categories": "Types of questions (concept/code/practice)"
    }
}
```

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [Feature Gating](./FEATURE_GATING.md)
- [UI/UX Design](./UI_UX_DESIGN.md)
- [Progress Tracking](./PROGRESS_TRACKING.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
