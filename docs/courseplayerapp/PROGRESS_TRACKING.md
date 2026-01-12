# Progress Tracking Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Define student progress tracking system and gamification

---

## Overview

The Progress Tracking system monitors student learning activities, provides visual feedback on achievements, and motivates continued engagement through gamification. It tracks multiple metrics across videos, labs, quizzes, and simulations.

---

## Progress Metrics

### Core Metrics

#### 1. Video Progress
```python
video_metrics = {
    "videos_watched": "Count of completed videos",
    "watch_time_hours": "Total hours spent watching",
    "completion_percentage": "% of videos watched in course",
    "avg_video_completion": "Average % watched per video",
    "rewatch_count": "Videos rewatched for review"
}
```

**Completion Criteria**:
- **Not Started**: < 10 seconds watched
- **In Progress**: 10% - 89% watched
- **Completed**: ≥ 90% watched OR manually marked complete

#### 2. Lab Progress
```python
lab_metrics = {
    "labs_started": "Count of labs opened",
    "labs_completed": "Count of labs finished",
    "code_execution_count": "Times code was run",
    "validation_success_rate": "% of tests passed on first try",
    "avg_lab_completion_time": "Average time to complete labs"
}
```

**Lab Statuses**:
- **Locked**: Not yet unlocked (prerequisites not met)
- **Available**: Unlocked but not started
- **In Progress**: Started but not completed
- **Completed**: All validation tests passed
- **Reviewed**: Completed and reviewed by instructor (optional)

#### 3. Quiz/Assessment Progress
```python
quiz_metrics = {
    "quizzes_taken": "Count of quizzes attempted",
    "quizzes_passed": "Count passed (≥ 70% score)",
    "avg_quiz_score": "Average score across all quizzes",
    "best_quiz_score": "Highest score achieved",
    "attempts_per_quiz": "Average attempts before passing"
}
```

#### 4. Simulation Progress
```python
simulation_metrics = {
    "simulations_completed": "Count of simulations finished",
    "simulation_success_rate": "% of simulations passed",
    "avg_simulation_score": "Average performance score",
    "simulation_time_total": "Total time in simulations"
}
```

#### 5. Overall Course Progress
```python
course_metrics = {
    "overall_completion": "% of course completed",
    "current_module": "Which module student is on",
    "days_since_enrollment": "Days since enrolled",
    "study_time_total": "Total hours spent learning",
    "current_streak": "Consecutive days active",
    "longest_streak": "Longest streak achieved"
}
```

**Completion Calculation**:
```python
def calculate_course_completion(user_id, course_id):
    """Calculate overall course completion percentage"""
    
    # Weighted components
    weights = {
        "videos": 0.40,      # 40% weight
        "labs": 0.30,        # 30% weight
        "quizzes": 0.20,     # 20% weight
        "simulations": 0.10  # 10% weight
    }
    
    # Get completion for each component
    video_completion = get_video_completion(user_id, course_id)
    lab_completion = get_lab_completion(user_id, course_id)
    quiz_completion = get_quiz_completion(user_id, course_id)
    simulation_completion = get_simulation_completion(user_id, course_id)
    
    # Calculate weighted average
    overall = (
        video_completion * weights["videos"] +
        lab_completion * weights["labs"] +
        quiz_completion * weights["quizzes"] +
        simulation_completion * weights["simulations"]
    )
    
    return round(overall, 2)
```

---

## Data Model

### Database Schema

```sql
-- User progress tracking table
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id VARCHAR(50) NOT NULL,
    module_id VARCHAR(50),
    resource_type VARCHAR(20) NOT NULL,  -- video, lab, quiz, simulation
    resource_id VARCHAR(100) NOT NULL,
    
    -- Progress data
    status VARCHAR(20) NOT NULL,  -- not_started, in_progress, completed
    completion_percent INTEGER DEFAULT 0,
    time_spent_seconds INTEGER DEFAULT 0,
    last_position TEXT,  -- For resume functionality (JSON)
    score INTEGER,  -- For quizzes/assessments
    attempts INTEGER DEFAULT 0,
    
    -- Timestamps
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id, course_id, resource_type, resource_id),
    CHECK (completion_percent >= 0 AND completion_percent <= 100),
    CHECK (status IN ('not_started', 'in_progress', 'completed'))
);

-- Indexes for performance
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_course_id ON user_progress(course_id);
CREATE INDEX idx_user_progress_status ON user_progress(status);
CREATE INDEX idx_user_progress_updated_at ON user_progress(updated_at DESC);

-- User achievements table
CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    achievement_type VARCHAR(50) NOT NULL,  -- streak, milestone, mastery, etc.
    achievement_id VARCHAR(100) NOT NULL,
    
    -- Achievement data
    title VARCHAR(200) NOT NULL,
    description TEXT,
    icon_url VARCHAR(500),
    points INTEGER DEFAULT 0,
    
    -- Progress toward achievement
    current_progress INTEGER DEFAULT 0,
    required_progress INTEGER NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    earned_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, achievement_id)
);

-- Daily activity tracking
CREATE TABLE user_activity (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    activity_date DATE NOT NULL,
    
    -- Activity metrics
    videos_watched INTEGER DEFAULT 0,
    labs_completed INTEGER DEFAULT 0,
    quizzes_taken INTEGER DEFAULT 0,
    ai_questions_asked INTEGER DEFAULT 0,
    time_spent_seconds INTEGER DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, activity_date)
);

-- Streak tracking
CREATE TABLE user_streaks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_activity_date DATE,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id)
);
```

---

## Achievements & Gamification

### Achievement Types

#### 1. Streak Achievements
```python
streak_achievements = [
    {
        "id": "streak_3",
        "title": "🔥 Getting Started",
        "description": "Study for 3 consecutive days",
        "requirement": 3,
        "points": 10
    },
    {
        "id": "streak_7",
        "title": "🔥 Week Warrior",
        "description": "Study for 7 consecutive days",
        "requirement": 7,
        "points": 25
    },
    {
        "id": "streak_30",
        "title": "🔥 Monthly Master",
        "description": "Study for 30 consecutive days",
        "requirement": 30,
        "points": 100
    },
    {
        "id": "streak_100",
        "title": "🔥 Century Champion",
        "description": "Study for 100 consecutive days",
        "requirement": 100,
        "points": 500
    }
]
```

#### 2. Milestone Achievements
```python
milestone_achievements = [
    {
        "id": "first_video",
        "title": "🎬 First Steps",
        "description": "Watch your first video",
        "points": 5
    },
    {
        "id": "first_lab",
        "title": "⚗️ Lab Novice",
        "description": "Complete your first lab",
        "points": 10
    },
    {
        "id": "module_complete",
        "title": "📚 Module Master",
        "description": "Complete your first module",
        "points": 50
    },
    {
        "id": "course_complete",
        "title": "🎓 Course Graduate",
        "description": "Complete your first course",
        "points": 200
    },
    {
        "id": "videos_10",
        "title": "📺 Video Enthusiast",
        "description": "Watch 10 videos",
        "points": 20
    },
    {
        "id": "videos_50",
        "title": "📺 Binge Learner",
        "description": "Watch 50 videos",
        "points": 75
    },
    {
        "id": "labs_10",
        "title": "🧪 Lab Expert",
        "description": "Complete 10 labs",
        "points": 50
    }
]
```

#### 3. Mastery Achievements
```python
mastery_achievements = [
    {
        "id": "quiz_perfect",
        "title": "💯 Perfect Score",
        "description": "Score 100% on a quiz",
        "points": 30
    },
    {
        "id": "quiz_streak_5",
        "title": "📝 Quiz Master",
        "description": "Pass 5 quizzes in a row on first attempt",
        "points": 50
    },
    {
        "id": "lab_speedrun",
        "title": "⚡ Speed Coder",
        "description": "Complete a lab in under 10 minutes",
        "points": 25
    },
    {
        "id": "ai_curious",
        "title": "🤖 Curious Mind",
        "description": "Ask 20 questions to AI Tutor",
        "points": 15
    }
]
```

#### 4. Time-Based Achievements
```python
time_achievements = [
    {
        "id": "study_1hr",
        "title": "⏱️ Hour Power",
        "description": "Study for 1 hour in a single day",
        "points": 10
    },
    {
        "id": "study_10hr",
        "title": "⏱️ Dedicated Learner",
        "description": "Accumulate 10 hours of study time",
        "points": 30
    },
    {
        "id": "study_100hr",
        "title": "⏱️ Elite Scholar",
        "description": "Accumulate 100 hours of study time",
        "points": 150
    },
    {
        "id": "early_bird",
        "title": "🌅 Early Bird",
        "description": "Study before 7 AM",
        "points": 15
    },
    {
        "id": "night_owl",
        "title": "🦉 Night Owl",
        "description": "Study after 11 PM",
        "points": 15
    }
]
```

### Leaderboard System

**Privacy-Respecting Design**:
```python
leaderboard_config = {
    "opt_in": True,  # Users must opt-in to appear
    "anonymization": {
        "display_name": "username_or_anonymous",
        "show_real_name": False,
        "show_avatar": "optional"
    },
    "categories": [
        "total_points",
        "courses_completed",
        "current_streak",
        "labs_completed"
    ],
    "timeframes": [
        "weekly",
        "monthly",
        "all_time"
    ],
    "visibility": "cohort_only"  # Only show users in same course cohort
}
```

**Implementation**:
```python
# progress/leaderboard.py

class Leaderboard:
    async def get_leaderboard(
        self,
        course_id: str,
        category: str = "total_points",
        timeframe: str = "weekly",
        limit: int = 10
    ):
        """Get leaderboard rankings"""
        
        # Only include users who opted in
        query = """
        SELECT 
            u.username,
            u.avatar_url,
            SUM(ua.points) as total_points,
            COUNT(DISTINCT up.course_id) as courses_completed,
            us.current_streak,
            COUNT(CASE WHEN up.resource_type = 'lab' 
                  THEN 1 END) as labs_completed
        FROM users u
        JOIN user_achievements ua ON u.id = ua.user_id
        JOIN user_progress up ON u.id = up.user_id
        LEFT JOIN user_streaks us ON u.id = us.user_id
        WHERE u.leaderboard_opt_in = TRUE
        AND up.course_id = :course_id
        """
        
        # Add timeframe filter
        if timeframe == "weekly":
            query += "AND ua.earned_at >= NOW() - INTERVAL '7 days'"
        elif timeframe == "monthly":
            query += "AND ua.earned_at >= NOW() - INTERVAL '30 days'"
        
        query += f"""
        GROUP BY u.id, u.username, u.avatar_url, us.current_streak
        ORDER BY {category} DESC
        LIMIT :limit
        """
        
        results = await db.fetch_all(query, {"course_id": course_id, "limit": limit})
        
        return [
            {
                "rank": idx + 1,
                "username": row["username"],
                "avatar_url": row["avatar_url"],
                "score": row[category]
            }
            for idx, row in enumerate(results)
        ]
```

---

## Progress Visualization

### Dashboard Components

#### 1. Course Progress Overview
```python
def render_progress_dashboard(user_id, course_id):
    """Render main progress dashboard"""
    
    st.title("📊 Your Progress")
    
    # Overall progress
    progress = get_course_progress(user_id, course_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Course Progress",
            f"{progress['overall_completion']}%",
            delta=f"+{progress['recent_increase']}% this week"
        )
    
    with col2:
        st.metric(
            "Current Streak",
            f"{progress['current_streak']} days",
            delta=f"Record: {progress['longest_streak']}"
        )
    
    with col3:
        st.metric(
            "Total Study Time",
            f"{progress['total_hours']} hrs",
            delta=f"+{progress['hours_this_week']} this week"
        )
    
    with col4:
        st.metric(
            "Achievement Points",
            progress['total_points'],
            delta=f"+{progress['points_this_week']} this week"
        )
    
    # Progress visualization
    st.markdown("---")
    
    # Course progress bar
    st.subheader("Course Completion")
    
    # Breakdown by component
    components = get_progress_breakdown(user_id, course_id)
    
    for component in ["videos", "labs", "quizzes", "simulations"]:
        col_a, col_b = st.columns([1, 4])
        with col_a:
            st.write(f"**{component.title()}**")
        with col_b:
            st.progress(
                components[component]["completed"] / components[component]["total"],
                text=f"{components[component]['completed']}/{components[component]['total']} completed"
            )
    
    # Module progress
    st.markdown("---")
    st.subheader("Module Progress")
    
    modules = get_module_progress(user_id, course_id)
    
    for module in modules:
        with st.expander(
            f"{'✅' if module['completed'] else '⏳'} {module['name']} - {module['completion']}%",
            expanded=not module['completed']
        ):
            st.progress(module['completion'] / 100)
            
            st.write(f"**Videos**: {module['videos_completed']}/{module['videos_total']}")
            st.write(f"**Labs**: {module['labs_completed']}/{module['labs_total']}")
            st.write(f"**Quizzes**: {module['quizzes_completed']}/{module['quizzes_total']}")
```

#### 2. Study Time Analytics
```python
def render_study_analytics(user_id):
    """Render study time analytics"""
    
    st.subheader("📈 Study Analytics")
    
    # Get activity data (last 30 days)
    activity = get_daily_activity(user_id, days=30)
    
    # Chart: Daily study time
    import plotly.express as px
    
    fig = px.bar(
        activity,
        x="date",
        y="time_spent_minutes",
        title="Daily Study Time (Last 30 Days)",
        labels={"time_spent_minutes": "Minutes", "date": "Date"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Study patterns
    col1, col2 = st.columns(2)
    
    with col1:
        # Best study day
        best_day = activity.groupby("day_of_week")["time_spent_minutes"].mean()
        
        st.metric(
            "Most Productive Day",
            best_day.idxmax(),
            delta=f"{int(best_day.max())} min avg"
        )
    
    with col2:
        # Best study time
        best_hour = activity.groupby("hour_of_day")["time_spent_minutes"].mean()
        
        st.metric(
            "Peak Study Hour",
            f"{best_hour.idxmax()}:00",
            delta=f"{int(best_hour.max())} min avg"
        )
```

#### 3. Achievement Gallery
```python
def render_achievements(user_id):
    """Render user achievements"""
    
    st.subheader("🏆 Achievements")
    
    achievements = get_user_achievements(user_id)
    
    # Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Earned", len([a for a in achievements if a["is_completed"]]))
    
    with col2:
        st.metric("In Progress", len([a for a in achievements if not a["is_completed"]]))
    
    with col3:
        st.metric("Total Points", sum(a["points"] for a in achievements if a["is_completed"]))
    
    # Achievement cards
    st.markdown("---")
    
    # Filter
    filter_type = st.selectbox(
        "Filter by",
        ["All", "Earned", "In Progress", "Streak", "Milestone", "Mastery"]
    )
    
    # Grid layout
    cols = st.columns(3)
    
    for idx, achievement in enumerate(achievements):
        # Apply filter
        if filter_type != "All":
            if filter_type == "Earned" and not achievement["is_completed"]:
                continue
            if filter_type == "In Progress" and achievement["is_completed"]:
                continue
            if filter_type in ["Streak", "Milestone", "Mastery"]:
                if achievement["achievement_type"].lower() != filter_type.lower():
                    continue
        
        col = cols[idx % 3]
        
        with col:
            # Achievement card
            with st.container():
                if achievement["is_completed"]:
                    st.success(f"✅ {achievement['title']}")
                else:
                    st.info(f"⏳ {achievement['title']}")
                
                st.caption(achievement["description"])
                
                if not achievement["is_completed"]:
                    # Progress bar
                    progress = achievement["current_progress"] / achievement["required_progress"]
                    st.progress(
                        progress,
                        text=f"{achievement['current_progress']}/{achievement['required_progress']}"
                    )
                else:
                    st.caption(f"🎖️ {achievement['points']} points")
                
                st.markdown("---")
```

---

## Streak Management

```python
# progress/streak_manager.py

class StreakManager:
    async def update_streak(self, user_id: str):
        """Update user's learning streak"""
        
        today = datetime.now().date()
        
        # Get current streak data
        streak = await db.fetch_one(
            "SELECT * FROM user_streaks WHERE user_id = :user_id",
            {"user_id": user_id}
        )
        
        if not streak:
            # First time activity
            await db.execute(
                """
                INSERT INTO user_streaks (user_id, current_streak, longest_streak, last_activity_date)
                VALUES (:user_id, 1, 1, :today)
                """,
                {"user_id": user_id, "today": today}
            )
            return 1
        
        last_activity = streak["last_activity_date"]
        current_streak = streak["current_streak"]
        longest_streak = streak["longest_streak"]
        
        # Check if streak continues
        if last_activity == today:
            # Already active today
            return current_streak
        
        elif last_activity == today - timedelta(days=1):
            # Streak continues!
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
            
            await db.execute(
                """
                UPDATE user_streaks
                SET current_streak = :current_streak,
                    longest_streak = :longest_streak,
                    last_activity_date = :today,
                    updated_at = NOW()
                WHERE user_id = :user_id
                """,
                {
                    "user_id": user_id,
                    "current_streak": current_streak,
                    "longest_streak": longest_streak,
                    "today": today
                }
            )
            
            # Check for streak achievements
            await self._check_streak_achievements(user_id, current_streak)
            
            return current_streak
        
        else:
            # Streak broken
            await db.execute(
                """
                UPDATE user_streaks
                SET current_streak = 1,
                    last_activity_date = :today,
                    updated_at = NOW()
                WHERE user_id = :user_id
                """,
                {"user_id": user_id, "today": today}
            )
            
            return 1
    
    async def _check_streak_achievements(self, user_id: str, streak: int):
        """Check if user earned streak achievements"""
        
        streak_milestones = [3, 7, 14, 30, 60, 100, 365]
        
        for milestone in streak_milestones:
            if streak == milestone:
                await award_achievement(
                    user_id,
                    f"streak_{milestone}",
                    achievement_type="streak"
                )
```

---

## Progress Export

**Feature**: Allow users to export their progress data

```python
# progress/exporter.py

async def export_progress(user_id: str, course_id: str, format: str = "pdf"):
    """Export user progress report"""
    
    progress = await get_comprehensive_progress(user_id, course_id)
    
    if format == "pdf":
        # Generate PDF report
        pdf = generate_pdf_report(progress)
        return pdf
    
    elif format == "json":
        # Export as JSON
        return json.dumps(progress, indent=2)
    
    elif format == "csv":
        # Export as CSV
        return convert_to_csv(progress)

def generate_pdf_report(progress: dict) -> bytes:
    """Generate PDF progress report"""
    
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    
    # Create PDF with:
    # - Course completion summary
    # - Module breakdown
    # - Study time analytics
    # - Achievement list
    # - Certificates earned
    
    # ... PDF generation code ...
    
    return pdf_bytes
```

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [Feature Gating](./FEATURE_GATING.md)
- [UI/UX Design](./UI_UX_DESIGN.md)
- [Certificate Display](./CERTIFICATE_DISPLAY.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
