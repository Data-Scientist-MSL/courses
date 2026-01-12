# Progress Tracking System

## Overview

CoursePlayerApp implements a comprehensive progress tracking system that monitors student activity, calculates completion metrics, awards achievements, and provides detailed analytics. This system integrates with CoursesGTM for data synchronization and powers the Progress Dashboard UI.

---

## Data Model

### Database Schema

```sql
-- Users table (synced from CoursesGTM)
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    license_key VARCHAR(100) UNIQUE,
    tier VARCHAR(20) NOT NULL CHECK (tier IN ('basic', 'intermediate', 'advanced')),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    INDEX idx_users_email (email),
    INDEX idx_users_tier (tier)
);

-- Course enrollment and overall progress
CREATE TABLE course_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50) NOT NULL,
    
    -- Progress tracking
    enrollment_date TIMESTAMP DEFAULT NOW(),
    current_lesson VARCHAR(50),
    completion_percentage DECIMAL(5,2) DEFAULT 0.00,
    
    -- Counters
    lessons_completed INTEGER DEFAULT 0,
    total_lessons INTEGER NOT NULL,
    labs_completed INTEGER DEFAULT 0,
    total_labs INTEGER NOT NULL,
    quizzes_passed INTEGER DEFAULT 0,
    total_quizzes INTEGER NOT NULL,
    
    -- Time tracking
    total_time_spent INTEGER DEFAULT 0,  -- seconds
    last_accessed TIMESTAMP,
    
    -- Completion
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    
    -- Constraints
    UNIQUE(user_id, course_id),
    INDEX idx_course_progress_user (user_id),
    INDEX idx_course_progress_course (course_id),
    INDEX idx_course_progress_completion (user_id, completed)
);

-- Lesson-level progress
CREATE TABLE lesson_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50) NOT NULL,
    lesson_id VARCHAR(50) NOT NULL,
    
    -- Status
    started BOOLEAN DEFAULT FALSE,
    completed BOOLEAN DEFAULT FALSE,
    
    -- Time tracking
    time_spent INTEGER DEFAULT 0,  -- seconds
    video_progress DECIMAL(5,2) DEFAULT 0.00,  -- percentage watched
    
    -- Timestamps
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    last_accessed TIMESTAMP,
    
    -- Constraints
    UNIQUE(user_id, course_id, lesson_id),
    INDEX idx_lesson_progress_user_course (user_id, course_id),
    INDEX idx_lesson_progress_completion (user_id, completed)
);

-- Lab progress
CREATE TABLE lab_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50) NOT NULL,
    lab_id VARCHAR(50) NOT NULL,
    
    -- Status
    status VARCHAR(20) DEFAULT 'not_started' CHECK (
        status IN ('not_started', 'in_progress', 'completed', 'failed')
    ),
    
    -- Scoring
    score DECIMAL(5,2),
    max_score DECIMAL(5,2) DEFAULT 100.00,
    attempts INTEGER DEFAULT 0,
    
    -- Time tracking
    time_spent INTEGER DEFAULT 0,  -- seconds
    
    -- Timestamps
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Session tracking
    last_session_id VARCHAR(100),
    
    -- Constraints
    UNIQUE(user_id, course_id, lab_id),
    INDEX idx_lab_progress_user_course (user_id, course_id),
    INDEX idx_lab_progress_status (user_id, status)
);

-- Quiz progress
CREATE TABLE quiz_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50) NOT NULL,
    quiz_id VARCHAR(50) NOT NULL,
    
    -- Scoring
    score DECIMAL(5,2),
    max_score DECIMAL(5,2) DEFAULT 100.00,
    passed BOOLEAN DEFAULT FALSE,
    passing_score DECIMAL(5,2) DEFAULT 70.00,
    attempts INTEGER DEFAULT 0,
    
    -- Time tracking
    time_spent INTEGER DEFAULT 0,  -- seconds
    
    -- Answers (JSONB for flexibility)
    answers JSONB,
    
    -- Timestamps
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    
    -- Constraints
    UNIQUE(user_id, course_id, quiz_id),
    INDEX idx_quiz_progress_user_course (user_id, course_id),
    INDEX idx_quiz_progress_passed (user_id, passed)
);

-- Achievements
CREATE TABLE achievements (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    icon_url VARCHAR(255),
    category VARCHAR(50),  -- 'course', 'streak', 'speed', 'mastery', 'community'
    points INTEGER DEFAULT 0,
    rarity VARCHAR(20) CHECK (rarity IN ('common', 'rare', 'epic', 'legendary')),
    
    -- Unlock criteria (JSONB for flexibility)
    criteria JSONB NOT NULL,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- User achievements (unlocked badges)
CREATE TABLE user_achievements (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    achievement_id VARCHAR(50) REFERENCES achievements(id),
    
    -- Unlock details
    unlocked_at TIMESTAMP DEFAULT NOW(),
    progress_data JSONB,  -- What triggered the unlock
    
    -- Constraints
    UNIQUE(user_id, achievement_id),
    INDEX idx_user_achievements_user (user_id),
    INDEX idx_user_achievements_achievement (achievement_id)
);

-- Learning streaks
CREATE TABLE learning_streaks (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Current streak
    current_streak INTEGER DEFAULT 0,  -- consecutive days
    longest_streak INTEGER DEFAULT 0,  -- all-time best
    
    -- Last activity
    last_activity_date DATE,
    
    -- Streak history (dates when user was active)
    activity_dates DATE[] DEFAULT ARRAY[]::DATE[],
    
    -- Timestamps
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    UNIQUE(user_id)
);

-- Video watch events (for analytics)
CREATE TABLE video_watch_events (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50) NOT NULL,
    lesson_id VARCHAR(50) NOT NULL,
    
    -- Event details
    event_type VARCHAR(20) CHECK (
        event_type IN ('play', 'pause', 'seek', 'complete', 'speed_change')
    ),
    video_position DECIMAL(10,2),  -- seconds
    playback_speed DECIMAL(3,2) DEFAULT 1.00,
    
    -- Metadata
    timestamp TIMESTAMP DEFAULT NOW(),
    session_id VARCHAR(100),
    
    INDEX idx_video_events_user_lesson (user_id, lesson_id),
    INDEX idx_video_events_timestamp (timestamp)
);

-- Certificates
CREATE TABLE certificates (
    id VARCHAR(100) PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    course_id VARCHAR(50) NOT NULL,
    
    -- Certificate details
    certificate_type VARCHAR(20) CHECK (
        certificate_type IN ('digital', 'blockchain')
    ),
    issued_at TIMESTAMP DEFAULT NOW(),
    
    -- URLs
    pdf_url VARCHAR(255),
    verification_url VARCHAR(255),
    blockchain_tx_hash VARCHAR(100),  -- For blockchain certificates
    
    -- Metadata
    grade DECIMAL(5,2),
    completion_date DATE,
    
    INDEX idx_certificates_user (user_id)
);
```

---

## Progress Calculation

### Course Completion Percentage

```python
from typing import Dict
from datetime import datetime

class ProgressCalculator:
    """Calculate various progress metrics."""
    
    def calculate_course_completion(
        self,
        user_id: str,
        course_id: str
    ) -> Dict:
        """
        Calculate overall course completion percentage.
        
        Formula:
        - Lessons: 60% weight
        - Labs: 30% weight
        - Quizzes: 10% weight
        """
        # Get course progress
        course_prog = db.query(CourseProgress).filter(
            CourseProgress.user_id == user_id,
            CourseProgress.course_id == course_id
        ).first()
        
        if not course_prog:
            return {"completion_percentage": 0.0}
        
        # Calculate component completions
        lesson_completion = (
            course_prog.lessons_completed / course_prog.total_lessons * 100
            if course_prog.total_lessons > 0 else 0
        )
        
        lab_completion = (
            course_prog.labs_completed / course_prog.total_labs * 100
            if course_prog.total_labs > 0 else 0
        )
        
        quiz_completion = (
            course_prog.quizzes_passed / course_prog.total_quizzes * 100
            if course_prog.total_quizzes > 0 else 0
        )
        
        # Weighted average
        overall_completion = (
            lesson_completion * 0.6 +
            lab_completion * 0.3 +
            quiz_completion * 0.1
        )
        
        # Update database
        course_prog.completion_percentage = round(overall_completion, 2)
        
        # Check if completed
        if overall_completion >= 100.0 and not course_prog.completed:
            course_prog.completed = True
            course_prog.completed_at = datetime.utcnow()
            
            # Trigger achievement check
            self.check_course_completion_achievements(user_id, course_id)
        
        db.commit()
        
        return {
            "completion_percentage": round(overall_completion, 2),
            "lesson_completion": round(lesson_completion, 2),
            "lab_completion": round(lab_completion, 2),
            "quiz_completion": round(quiz_completion, 2)
        }
    
    def update_lesson_progress(
        self,
        user_id: str,
        course_id: str,
        lesson_id: str,
        completed: bool = False,
        time_spent: int = 0,
        video_progress: float = 0.0
    ):
        """Update progress for a lesson."""
        
        # Get or create lesson progress
        lesson_prog = db.query(LessonProgress).filter(
            LessonProgress.user_id == user_id,
            LessonProgress.course_id == course_id,
            LessonProgress.lesson_id == lesson_id
        ).first()
        
        if not lesson_prog:
            lesson_prog = LessonProgress(
                user_id=user_id,
                course_id=course_id,
                lesson_id=lesson_id
            )
            db.add(lesson_prog)
        
        # Update fields
        lesson_prog.time_spent += time_spent
        lesson_prog.video_progress = max(
            lesson_prog.video_progress,
            video_progress
        )
        lesson_prog.last_accessed = datetime.utcnow()
        
        if not lesson_prog.started:
            lesson_prog.started = True
            lesson_prog.started_at = datetime.utcnow()
        
        # Mark as completed if criteria met
        if completed and not lesson_prog.completed:
            lesson_prog.completed = True
            lesson_prog.completed_at = datetime.utcnow()
            
            # Update course-level counter
            course_prog = db.query(CourseProgress).filter(
                CourseProgress.user_id == user_id,
                CourseProgress.course_id == course_id
            ).first()
            
            if course_prog:
                course_prog.lessons_completed += 1
                course_prog.total_time_spent += lesson_prog.time_spent
                course_prog.current_lesson = lesson_id
                course_prog.last_accessed = datetime.utcnow()
        
        db.commit()
        
        # Recalculate overall progress
        self.calculate_course_completion(user_id, course_id)
        
        # Update streak
        self.update_learning_streak(user_id)
        
        # Check for achievements
        self.check_lesson_achievements(user_id, lesson_id)
```

---

## Achievements System

### Achievement Definitions

```yaml
# config/achievements.yaml
achievements:
  - id: first_lesson
    name: "First Steps"
    description: "Completed your first lesson"
    icon_url: "/badges/first_lesson.svg"
    category: course
    points: 50
    rarity: common
    criteria:
      type: lesson_count
      value: 1
  
  - id: first_course
    name: "Course Completion"
    description: "Completed your first course"
    icon_url: "/badges/first_course.svg"
    category: course
    points: 500
    rarity: rare
    criteria:
      type: course_count
      value: 1
  
  - id: week_streak
    name: "Consistent Learner"
    description: "7-day learning streak"
    icon_url: "/badges/week_streak.svg"
    category: streak
    points: 200
    rarity: rare
    criteria:
      type: streak_days
      value: 7
  
  - id: month_streak
    name: "Dedicated Student"
    description: "30-day learning streak"
    icon_url: "/badges/month_streak.svg"
    category: streak
    points: 1000
    rarity: epic
    criteria:
      type: streak_days
      value: 30
  
  - id: perfect_quiz
    name: "Perfect Score"
    description: "Scored 100% on a quiz"
    icon_url: "/badges/perfect.svg"
    category: mastery
    points: 150
    rarity: rare
    criteria:
      type: quiz_score
      value: 100
  
  - id: speed_learner
    name: "Speed Learner"
    description: "Completed a course in under 2 weeks"
    icon_url: "/badges/speed.svg"
    category: speed
    points: 300
    rarity: rare
    criteria:
      type: course_completion_days
      max_value: 14
  
  - id: lab_master
    name: "Lab Master"
    description: "Completed 10 labs with score > 90%"
    icon_url: "/badges/lab_master.svg"
    category: mastery
    points: 400
    rarity: epic
    criteria:
      type: lab_high_scores
      count: 10
      min_score: 90
  
  - id: all_courses
    name: "Master Graduate"
    description: "Completed all available courses"
    icon_url: "/badges/graduate.svg"
    category: course
    points: 5000
    rarity: legendary
    criteria:
      type: all_courses_completed
  
  - id: helpful_community
    name: "Community Helper"
    description: "Answered 20 forum questions"
    icon_url: "/badges/helper.svg"
    category: community
    points: 250
    rarity: rare
    criteria:
      type: forum_answers
      value: 20
  
  - id: early_bird
    name: "Early Bird"
    description: "Studied before 7 AM"
    icon_url: "/badges/early_bird.svg"
    category: streak
    points: 100
    rarity: common
    criteria:
      type: study_time
      before_hour: 7
```

### Achievement Checking

```python
class AchievementEngine:
    """Check and award achievements."""
    
    def check_lesson_achievements(self, user_id: str, lesson_id: str):
        """Check for achievements after lesson completion."""
        
        # Count total lessons completed
        total_lessons = db.query(LessonProgress).filter(
            LessonProgress.user_id == user_id,
            LessonProgress.completed == True
        ).count()
        
        # First lesson achievement
        if total_lessons == 1:
            self.unlock_achievement(user_id, "first_lesson")
    
    def check_course_completion_achievements(
        self,
        user_id: str,
        course_id: str
    ):
        """Check for achievements after course completion."""
        
        # Get course completion details
        course_prog = db.query(CourseProgress).filter(
            CourseProgress.user_id == user_id,
            CourseProgress.course_id == course_id
        ).first()
        
        # Count total courses completed
        total_courses = db.query(CourseProgress).filter(
            CourseProgress.user_id == user_id,
            CourseProgress.completed == True
        ).count()
        
        # First course achievement
        if total_courses == 1:
            self.unlock_achievement(user_id, "first_course")
        
        # Speed learner achievement
        if course_prog:
            days_taken = (
                course_prog.completed_at - course_prog.enrollment_date
            ).days
            
            if days_taken <= 14:
                self.unlock_achievement(user_id, "speed_learner")
        
        # All courses completed
        user = db.query(User).filter(User.id == user_id).first()
        available_courses = get_available_courses_for_tier(user.tier)
        
        if total_courses >= len(available_courses):
            self.unlock_achievement(user_id, "all_courses")
    
    def check_streak_achievements(self, user_id: str, streak_days: int):
        """Check for streak-based achievements."""
        
        # 7-day streak
        if streak_days >= 7:
            self.unlock_achievement(user_id, "week_streak")
        
        # 30-day streak
        if streak_days >= 30:
            self.unlock_achievement(user_id, "month_streak")
    
    def check_quiz_achievements(
        self,
        user_id: str,
        quiz_id: str,
        score: float
    ):
        """Check for quiz-related achievements."""
        
        # Perfect score
        if score >= 100.0:
            self.unlock_achievement(user_id, "perfect_quiz")
    
    def check_lab_achievements(self, user_id: str):
        """Check for lab-related achievements."""
        
        # Count high-scoring labs (> 90%)
        high_score_labs = db.query(LabProgress).filter(
            LabProgress.user_id == user_id,
            LabProgress.score >= 90.0
        ).count()
        
        if high_score_labs >= 10:
            self.unlock_achievement(user_id, "lab_master")
    
    def unlock_achievement(
        self,
        user_id: str,
        achievement_id: str,
        progress_data: Optional[Dict] = None
    ) -> bool:
        """
        Unlock an achievement for a user.
        
        Returns:
            bool: True if newly unlocked, False if already had it
        """
        # Check if already unlocked
        existing = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement_id
        ).first()
        
        if existing:
            return False  # Already unlocked
        
        # Create new unlock record
        user_achievement = UserAchievement(
            user_id=user_id,
            achievement_id=achievement_id,
            progress_data=progress_data or {},
            unlocked_at=datetime.utcnow()
        )
        
        db.add(user_achievement)
        db.commit()
        
        # Sync with CoursesGTM
        asyncio.create_task(
            coursesgtm_client.unlock_achievement(
                user_id,
                achievement_id,
                progress_data
            )
        )
        
        # Send notification to user
        asyncio.create_task(
            send_achievement_notification(user_id, achievement_id)
        )
        
        return True
```

---

## Learning Streaks

### Streak Tracking

```python
from datetime import date, timedelta

class StreakTracker:
    """Track user learning streaks."""
    
    def update_learning_streak(self, user_id: str):
        """Update user's learning streak."""
        
        today = date.today()
        
        # Get or create streak record
        streak = db.query(LearningStreak).filter(
            LearningStreak.user_id == user_id
        ).first()
        
        if not streak:
            streak = LearningStreak(
                user_id=user_id,
                current_streak=0,
                longest_streak=0,
                activity_dates=[]
            )
            db.add(streak)
        
        # Check if already logged today
        if today in streak.activity_dates:
            return  # Already counted for today
        
        # Add today to activity dates
        streak.activity_dates.append(today)
        
        # Check if yesterday was active (streak continues)
        yesterday = today - timedelta(days=1)
        
        if streak.last_activity_date == yesterday:
            # Streak continues
            streak.current_streak += 1
        else:
            # Streak broken, start new
            streak.current_streak = 1
        
        # Update longest streak
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
        
        streak.last_activity_date = today
        streak.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Check for streak achievements
        achievement_engine.check_streak_achievements(
            user_id,
            streak.current_streak
        )
    
    def get_streak_info(self, user_id: str) -> Dict:
        """Get streak information for a user."""
        
        streak = db.query(LearningStreak).filter(
            LearningStreak.user_id == user_id
        ).first()
        
        if not streak:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "is_active_today": False
            }
        
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # Check if streak is still active
        is_active = streak.last_activity_date in [today, yesterday]
        
        # If last activity was 2+ days ago, current streak is 0
        if streak.last_activity_date < yesterday:
            current_streak = 0
        else:
            current_streak = streak.current_streak
        
        return {
            "current_streak": current_streak,
            "longest_streak": streak.longest_streak,
            "is_active_today": streak.last_activity_date == today,
            "last_activity": streak.last_activity_date.isoformat()
        }
```

---

## API Endpoints

```python
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/api/progress/overview")
async def get_progress_overview(
    current_user: User = Depends(get_current_user)
):
    """Get overall progress summary for user."""
    
    # Get all enrolled courses
    courses = db.query(CourseProgress).filter(
        CourseProgress.user_id == current_user.id
    ).all()
    
    total_time = sum(c.total_time_spent for c in courses)
    completed_courses = sum(1 for c in courses if c.completed)
    
    # Get achievements
    achievements = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id
    ).count()
    
    # Get streak
    streak = streak_tracker.get_streak_info(current_user.id)
    
    return {
        "courses_enrolled": len(courses),
        "courses_completed": completed_courses,
        "total_time_minutes": total_time // 60,
        "achievements_unlocked": achievements,
        "current_streak": streak["current_streak"],
        "longest_streak": streak["longest_streak"]
    }

@router.get("/api/progress/course/{course_id}")
async def get_course_progress(
    course_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get detailed progress for a specific course."""
    
    course_prog = db.query(CourseProgress).filter(
        CourseProgress.user_id == current_user.id,
        CourseProgress.course_id == course_id
    ).first()
    
    if not course_prog:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Calculate completion
    completion = progress_calculator.calculate_course_completion(
        current_user.id,
        course_id
    )
    
    # Get lesson progress
    lessons = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.course_id == course_id
    ).all()
    
    # Get lab progress
    labs = db.query(LabProgress).filter(
        LabProgress.user_id == current_user.id,
        LabProgress.course_id == course_id
    ).all()
    
    return {
        "course_id": course_id,
        "enrollment_date": course_prog.enrollment_date.isoformat(),
        "completion_percentage": completion["completion_percentage"],
        "lessons": {
            "completed": course_prog.lessons_completed,
            "total": course_prog.total_lessons,
            "details": [
                {
                    "lesson_id": l.lesson_id,
                    "completed": l.completed,
                    "time_spent": l.time_spent
                }
                for l in lessons
            ]
        },
        "labs": {
            "completed": course_prog.labs_completed,
            "total": course_prog.total_labs,
            "average_score": sum(l.score for l in labs if l.score) / len(labs) if labs else 0,
            "details": [
                {
                    "lab_id": l.lab_id,
                    "status": l.status,
                    "score": l.score
                }
                for l in labs
            ]
        },
        "total_time_minutes": course_prog.total_time_spent // 60,
        "last_accessed": course_prog.last_accessed.isoformat() if course_prog.last_accessed else None
    }

@router.get("/api/progress/achievements")
async def get_achievements(
    current_user: User = Depends(get_current_user)
):
    """Get all achievements (unlocked and locked)."""
    
    # Get all achievements
    all_achievements = db.query(Achievement).all()
    
    # Get user's unlocked achievements
    user_achievements = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id
    ).all()
    
    unlocked_ids = {ua.achievement_id for ua in user_achievements}
    
    return {
        "total_achievements": len(all_achievements),
        "unlocked_count": len(unlocked_ids),
        "total_points": sum(
            a.points for a in all_achievements
            if a.id in unlocked_ids
        ),
        "achievements": [
            {
                "id": a.id,
                "name": a.name,
                "description": a.description,
                "icon_url": a.icon_url,
                "points": a.points,
                "rarity": a.rarity,
                "unlocked": a.id in unlocked_ids,
                "unlocked_at": next(
                    (ua.unlocked_at.isoformat() for ua in user_achievements if ua.achievement_id == a.id),
                    None
                )
            }
            for a in all_achievements
        ]
    }

@router.post("/api/progress/lesson/update")
async def update_lesson_progress_endpoint(
    request: LessonProgressUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update progress for a lesson."""
    
    progress_calculator.update_lesson_progress(
        user_id=current_user.id,
        course_id=request.course_id,
        lesson_id=request.lesson_id,
        completed=request.completed,
        time_spent=request.time_spent,
        video_progress=request.video_progress
    )
    
    return {"status": "updated"}
```

---

## Analytics Queries

### Dashboard Queries

```sql
-- User's top performing courses
SELECT 
    cp.course_id,
    c.title,
    cp.completion_percentage,
    cp.total_time_spent / 60 as time_minutes,
    AVG(lp.score) as avg_lab_score
FROM course_progress cp
LEFT JOIN labs lp ON lp.user_id = cp.user_id AND lp.course_id = cp.course_id
WHERE cp.user_id = $1
GROUP BY cp.course_id, c.title, cp.completion_percentage, cp.total_time_spent
ORDER BY cp.completion_percentage DESC;

-- Recent activity
SELECT 
    'lesson' as activity_type,
    lesson_id as item_id,
    completed_at as timestamp
FROM lesson_progress
WHERE user_id = $1 AND completed_at IS NOT NULL
UNION ALL
SELECT 
    'lab' as activity_type,
    lab_id as item_id,
    completed_at as timestamp
FROM lab_progress
WHERE user_id = $1 AND completed_at IS NOT NULL
ORDER BY timestamp DESC
LIMIT 10;

-- Learning patterns (hour of day)
SELECT 
    EXTRACT(HOUR FROM timestamp) as hour,
    COUNT(*) as activities
FROM video_watch_events
WHERE user_id = $1
  AND event_type = 'play'
  AND timestamp >= NOW() - INTERVAL '30 days'
GROUP BY hour
ORDER BY hour;
```

---

## Conclusion

The Progress Tracking system provides:

1. **Comprehensive Metrics** - Lessons, labs, quizzes, time tracking
2. **Achievement System** - Gamification with badges and points
3. **Streak Tracking** - Encourage daily learning habits
4. **Detailed Analytics** - Learning patterns and performance insights
5. **Real-time Updates** - Instant progress calculation
6. **CoursesGTM Sync** - Seamless integration with license management

This system motivates learners while providing valuable data for personalization and improvement.
