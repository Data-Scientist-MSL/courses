#!/usr/bin/env python3
"""
Custom Component Example - CoursePlayerApp

This example shows how to build a custom component for CoursePlayerApp
that integrates with the feature gating system and CoursesGTM.

Example: A custom Quiz Review component with tier-based analytics.
"""

import streamlit as st
from typing import Optional, List, Dict
from abc import ABC, abstractmethod


# ============================================================================
# Base Component Pattern
# ============================================================================

class BaseComponent(ABC):
    """
    Base class for all CoursePlayerApp components.
    
    All components should:
    1. Inherit from BaseComponent
    2. Implement _render_content() method
    3. Use _has_feature() for feature gates
    4. Call render() to display
    """
    
    def __init__(self, course_id: str, resource_id: str):
        self.course_id = course_id
        self.resource_id = resource_id
        # In production, this would be the real CoursesGTM client
        self.gtm_client = self._get_gtm_client()
    
    def _get_gtm_client(self):
        """Get CoursesGTM client instance (mocked for demo)"""
        # In production: return CoursesGTMClient.get_instance()
        return MockGTMClient()
    
    def _has_feature(self, feature_name: str) -> bool:
        """Check if user has access to a feature"""
        return self.gtm_client.can_use_feature(feature_name)
    
    def _get_user_tier(self) -> str:
        """Get current user's tier"""
        return self.gtm_client.get_user_tier()
    
    def _render_upgrade_prompt(self, feature_name: str):
        """Render upgrade prompt for locked features"""
        st.info(
            f"🔒 **{feature_name}** is not available in your current tier.\n\n"
            f"Upgrade to unlock this feature."
        )
        if st.button("Upgrade Now"):
            st.session_state.page = "upgrade"
    
    def render(self):
        """Main render method - checks access then renders content"""
        if not self._check_access():
            self._render_access_denied()
            return
        
        self._render_content()
    
    def _check_access(self) -> bool:
        """Check if user can access this component/resource"""
        # Override in subclass if needed
        return True
    
    def _render_access_denied(self):
        """Render when access is denied"""
        st.error("⛔ You don't have access to this resource.")
    
    @abstractmethod
    def _render_content(self):
        """Render the actual component content - must be implemented by subclass"""
        pass


# ============================================================================
# Custom Component Example: Quiz Review
# ============================================================================

class QuizReview(BaseComponent):
    """
    Custom component for reviewing quiz performance.
    
    Tier-based features:
    - Basic: Show score only
    - Intermediate: Show detailed answers and explanations
    - Advanced: Show performance analytics and peer comparison
    
    Usage:
        review = QuizReview('data-science-101', 'quiz-1')
        review.render()
    """
    
    def __init__(self, course_id: str, quiz_id: str):
        super().__init__(course_id, quiz_id)
        self.quiz_id = quiz_id
        self.quiz_data = self._load_quiz_data()
        self.user_answers = self._load_user_answers()
    
    def _load_quiz_data(self) -> Dict:
        """Load quiz questions and correct answers"""
        # In production, fetch from API
        return {
            "title": "Pandas Fundamentals Quiz",
            "questions": [
                {
                    "id": 1,
                    "text": "What is a DataFrame?",
                    "options": ["A", "B", "C", "D"],
                    "correct": "B",
                    "explanation": "A DataFrame is a 2-dimensional labeled data structure..."
                },
                {
                    "id": 2,
                    "text": "How do you select a column?",
                    "options": ["df['col']", "df.col", "Both A and B", "None"],
                    "correct": "Both A and B",
                    "explanation": "Both bracket notation and dot notation work..."
                }
            ]
        }
    
    def _load_user_answers(self) -> Dict:
        """Load user's submitted answers"""
        # In production, fetch from API
        return {
            1: {"answer": "B", "correct": True},
            2: {"answer": "df['col']", "correct": False}
        }
    
    def _render_content(self):
        """Render quiz review based on user tier"""
        st.subheader(f"📝 {self.quiz_data['title']} - Review")
        
        # Calculate score
        total_questions = len(self.quiz_data['questions'])
        correct_count = sum(1 for ans in self.user_answers.values() if ans['correct'])
        score = (correct_count / total_questions) * 100
        
        # Always show score (all tiers)
        self._render_score_summary(score, correct_count, total_questions)
        
        # Detailed review (Intermediate+)
        if self._has_feature('quiz_analytics'):
            self._render_detailed_review()
        else:
            self._render_upgrade_prompt("Detailed Quiz Review")
        
        # Analytics (Advanced only)
        if self._get_user_tier() == 'advanced':
            self._render_analytics()
    
    def _render_score_summary(self, score: float, correct: int, total: int):
        """Render score summary - available to all tiers"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Your Score", f"{score:.0f}%")
        with col2:
            st.metric("Correct Answers", f"{correct}/{total}")
        with col3:
            if score >= 80:
                st.metric("Status", "Passed ✅")
            else:
                st.metric("Status", "Review 📚")
    
    def _render_detailed_review(self):
        """Render detailed answer review - Intermediate+ only"""
        st.markdown("### 📋 Detailed Review")
        
        for question in self.quiz_data['questions']:
            q_id = question['id']
            user_answer = self.user_answers[q_id]
            
            # Question container
            with st.container():
                # Show correctness
                if user_answer['correct']:
                    st.success(f"✅ Question {q_id}: {question['text']}")
                else:
                    st.error(f"❌ Question {q_id}: {question['text']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Your answer:** {user_answer['answer']}")
                with col2:
                    st.write(f"**Correct answer:** {question['correct']}")
                
                # Show explanation
                with st.expander("💡 Explanation"):
                    st.write(question['explanation'])
                
                st.divider()
    
    def _render_analytics(self):
        """Render performance analytics - Advanced only"""
        st.markdown("### 📊 Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Your Performance Over Time")
            # Mock chart data
            import pandas as pd
            chart_data = pd.DataFrame({
                'Attempt': [1, 2, 3, 4, 5],
                'Score': [65, 72, 78, 85, 90]
            })
            st.line_chart(chart_data.set_index('Attempt'))
        
        with col2:
            st.markdown("#### Peer Comparison")
            st.write("Your score: **90%**")
            st.write("Average score: **75%**")
            st.write("Top 10%: **95%**")
            st.progress(0.9)
            st.caption("You're in the top 25% of learners!")


# ============================================================================
# Mock GTM Client for Demo
# ============================================================================

class MockGTMClient:
    """Mock CoursesGTM client for demonstration"""
    
    def get_user_tier(self) -> str:
        # Change this to test different tiers
        return st.session_state.get('demo_tier', 'intermediate')
    
    def can_use_feature(self, feature: str) -> bool:
        tier = self.get_user_tier()
        
        # Feature availability by tier
        features = {
            'basic': ['quiz_access'],
            'intermediate': ['quiz_access', 'quiz_analytics'],
            'advanced': ['quiz_access', 'quiz_analytics', 'peer_comparison']
        }
        
        return feature in features.get(tier, [])


# ============================================================================
# Demo Application
# ============================================================================

def main():
    st.set_page_config(
        page_title="Custom Component Example",
        page_icon="🔧",
        layout="wide"
    )
    
    st.title("🔧 Custom Component Example")
    st.markdown("""
    This demo shows how to build a custom component for CoursePlayerApp
    that integrates with feature gating and tier-based access.
    """)
    
    # Tier selector for demo
    st.sidebar.header("🎯 Demo Controls")
    demo_tier = st.sidebar.selectbox(
        "Select Tier to Demo",
        ['basic', 'intermediate', 'advanced']
    )
    st.session_state.demo_tier = demo_tier
    
    st.sidebar.markdown(f"""
    **Current Tier:** {demo_tier.title()}
    
    **Features Available:**
    - Basic: Score summary only
    - Intermediate: + Detailed review
    - Advanced: + Performance analytics
    """)
    
    st.divider()
    
    # Render custom component
    review = QuizReview('data-science-101', 'quiz-1')
    review.render()
    
    # Show code
    st.divider()
    st.markdown("### 💻 Component Code")
    
    with st.expander("View QuizReview Component Code"):
        st.code('''
class QuizReview(BaseComponent):
    """Custom quiz review component with tier-based features"""
    
    def __init__(self, course_id: str, quiz_id: str):
        super().__init__(course_id, quiz_id)
        # Initialize component
    
    def _render_content(self):
        """Render based on user tier"""
        # Always show score
        self._render_score_summary()
        
        # Detailed review (Intermediate+)
        if self._has_feature('quiz_analytics'):
            self._render_detailed_review()
        else:
            self._render_upgrade_prompt("Detailed Quiz Review")
        
        # Analytics (Advanced only)
        if self._get_user_tier() == 'advanced':
            self._render_analytics()

# Usage
review = QuizReview('course-id', 'quiz-id')
review.render()
        ''', language='python')
    
    # Best practices
    st.markdown("""
    ### ✅ Best Practices for Custom Components
    
    1. **Inherit from BaseComponent** - Use the standard pattern
    2. **Use Feature Gates** - Check features with `_has_feature()`
    3. **Graceful Degradation** - Show upgrade prompts, don't hide features
    4. **Tier-Aware UI** - Adapt the interface based on tier
    5. **Document Tiers** - Clearly state what each tier includes
    6. **Test All Tiers** - Test your component with all tier levels
    7. **Performance** - Cache data fetching operations
    8. **Error Handling** - Handle API errors gracefully
    
    ### 📚 Related Documentation
    
    - [Component Specifications](../docs/courseplayerapp/COMPONENTS.md)
    - [Feature Gates](../docs/courseplayerapp/FEATURE_GATES.md)
    - [Architecture](../docs/courseplayerapp/ARCHITECTURE.md)
    """)


if __name__ == "__main__":
    main()
