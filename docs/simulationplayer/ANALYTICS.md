# SimulationPlayer Analytics & Tracking

This document specifies the analytics system for tracking simulation performance, user engagement, and learning outcomes.

---

## Tracked Metrics

### 1. Completion Metrics

#### Scenario Completion Rate
```python
completion_rate = (scenarios_completed / scenarios_started) * 100
```

**Tracked Data**:
- Scenarios started
- Scenarios completed
- Scenarios abandoned
- Abandonment points (which step users quit)

#### Step Completion Rate
```python
step_completion_rate = (steps_completed / steps_attempted) * 100
```

**Per Step**:
- Attempts before success
- Time to complete
- Users who skipped
- Users who abandoned

#### Time Metrics
- **Average Time to Complete**: Mean completion time
- **Median Time**: 50th percentile (more robust to outliers)
- **95th Percentile**: Identify struggling users
- **Time per Step**: Track which steps take longest

### 2. Performance Metrics

#### Attempts Per Step
```python
@dataclass
class StepPerformance:
    step_id: str
    avg_attempts: float
    median_attempts: int
    max_attempts: int
    first_try_success_rate: float  # % who succeed on first try
```

#### Hint Usage
- **Hints Requested**: Count per step
- **Hint Level Distribution**: Which hint levels used most
- **Hint Effectiveness**: Success rate after hints

#### Error Patterns
```python
@dataclass
class ErrorPattern:
    step_id: str
    error_type: str  # e.g., 'missing_flag', 'wrong_order'
    frequency: int
    recovery_rate: float  # % who recover successfully
```

### 3. Engagement Metrics

#### AI Assistant Usage
- **Questions Asked**: Total questions per scenario
- **Question Topics**: Categorize questions
- **Response Satisfaction**: Track follow-up questions

#### Session Metrics
- **Session Duration**: Total time spent
- **Active Time**: Actual interaction time (excludes idle)
- **Pause/Resume**: How often users save and return
- **Checkpoint Usage**: Frequency of manual saves

#### Interaction Patterns
```python
@dataclass
class UserInteraction:
    user_id: str
    scenario_id: str
    interactions: list[dict]  # All actions with timestamps
    idle_periods: list[timedelta]
    peak_activity_time: datetime  # When most active
```

### 4. Learning Metrics

#### Improvement Over Time
```python
def calculate_improvement(user_id: str) -> dict:
    scenarios = get_user_scenarios(user_id, order_by='completion_date')
    
    return {
        'avg_attempts_trend': regression(scenarios, metric='avg_attempts'),
        'time_trend': regression(scenarios, metric='completion_time'),
        'hint_usage_trend': regression(scenarios, metric='hints_used'),
        'accuracy_trend': regression(scenarios, metric='accuracy')
    }
```

#### Common Mistakes Database
```python
@dataclass
class CommonMistake:
    mistake_pattern: str
    frequency: int
    contexts: list[str]  # Which scenarios/steps
    typical_corrections: list[str]
    user_demographics: dict  # Skill level, background
```

#### Skill Progression
```python
@dataclass
class SkillProgression:
    user_id: str
    skill_area: str  # 'docker', 'git', 'sql', etc.
    current_level: str  # 'beginner', 'intermediate', 'advanced'
    scenarios_completed: list[str]
    proficiency_score: float  # 0-100
    recommended_next: list[str]
```

---

## Analytics Data Model

### Event Schema
```python
@dataclass
class SimulationEvent:
    event_id: str
    user_id: str
    scenario_id: str
    step_id: str
    event_type: str  # 'start', 'action', 'validation', 'hint', 'complete'
    timestamp: datetime
    data: dict  # Event-specific data
    
    # Context
    user_tier: str
    session_id: str
    device_type: str
```

### Event Types

#### 1. Scenario Events
```python
{
    'event_type': 'scenario_start',
    'data': {
        'scenario_id': 'docker-first-container',
        'user_tier': 'intermediate',
        'user_skill_level': 'beginner'
    }
}

{
    'event_type': 'scenario_complete',
    'data': {
        'scenario_id': 'docker-first-container',
        'total_time': 847,  # seconds
        'total_attempts': 12,
        'hints_used': 3,
        'accuracy': 85.7
    }
}
```

#### 2. Step Events
```python
{
    'event_type': 'step_start',
    'data': {
        'step_id': 'pull_nginx',
        'step_number': 1
    }
}

{
    'event_type': 'step_attempt',
    'data': {
        'step_id': 'pull_nginx',
        'attempt_number': 2,
        'action': 'docker pull nginx',
        'success': True,
        'validation_time_ms': 245
    }
}
```

#### 3. Assistance Events
```python
{
    'event_type': 'hint_requested',
    'data': {
        'step_id': 'run_nginx',
        'hint_level': 2,
        'time_since_step_start': 127  # seconds
    }
}

{
    'event_type': 'ai_question',
    'data': {
        'question': 'What does -d flag do?',
        'response_length': 156,
        'response_time_ms': 1234
    }
}
```

---

## Analytics Storage

### Database Schema

```sql
-- Scenarios table
CREATE TABLE scenarios (
    scenario_id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255),
    difficulty VARCHAR(20),
    estimated_time INT
);

-- User attempts table
CREATE TABLE scenario_attempts (
    attempt_id UUID PRIMARY KEY,
    user_id VARCHAR(100),
    scenario_id VARCHAR(100),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status VARCHAR(20),  -- 'completed', 'abandoned', 'in_progress'
    total_attempts INT,
    hints_used INT,
    accuracy FLOAT,
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

-- Step performance table
CREATE TABLE step_performance (
    id UUID PRIMARY KEY,
    attempt_id UUID,
    step_id VARCHAR(100),
    attempts INT,
    time_spent INT,
    hints_used INT,
    success BOOLEAN,
    FOREIGN KEY (attempt_id) REFERENCES scenario_attempts(attempt_id)
);

-- Events table (time-series)
CREATE TABLE simulation_events (
    event_id UUID PRIMARY KEY,
    user_id VARCHAR(100),
    scenario_id VARCHAR(100),
    step_id VARCHAR(100),
    event_type VARCHAR(50),
    event_data JSONB,
    timestamp TIMESTAMP,
    INDEX idx_user_time (user_id, timestamp),
    INDEX idx_scenario_time (scenario_id, timestamp)
);

-- Mistakes table
CREATE TABLE common_mistakes (
    mistake_id UUID PRIMARY KEY,
    step_id VARCHAR(100),
    mistake_pattern VARCHAR(255),
    frequency INT,
    last_seen TIMESTAMP
);
```

---

## Analytics Dashboard

### For Course Creators

#### 1. Scenario Overview
```
┌─────────────────────────────────────────────────┐
│  Scenario: Docker First Container              │
├─────────────────────────────────────────────────┤
│  📊 Completion Rate: 78%                        │
│  ⏱️ Avg Time: 14m 32s (target: 15m)            │
│  💪 Avg Attempts: 2.3 per step                  │
│  💡 Avg Hints: 1.8                              │
│                                                  │
│  📈 Difficulty Score: 6.2/10 (Good)             │
│  👥 Total Attempts: 1,243                       │
│  ✅ Completions: 970                            │
│  ❌ Abandonments: 273                           │
└─────────────────────────────────────────────────┘
```

#### 2. Step-by-Step Breakdown
```
┌──────────────┬─────────┬──────────┬─────────┬───────────┐
│ Step         │ Compl.% │ Avg Time │ Attempts│ Abandon % │
├──────────────┼─────────┼──────────┼─────────┼───────────┤
│ 1. Pull      │   95%   │  1m 23s  │   1.2   │    5%     │
│ 2. Run       │   82%   │  3m 45s  │   2.8   │   18%     │ ⚠️
│ 3. Inspect   │   96%   │  0m 54s  │   1.1   │    4%     │
│ 4. Exec      │   89%   │  2m 12s  │   1.9   │   11%     │
│ 5. Cleanup   │   98%   │  1m 06s  │   1.0   │    2%     │
└──────────────┴─────────┴──────────┴─────────┴───────────┘
```

#### 3. Common Mistakes Heatmap
```
Top 5 Mistakes in "Run Container" step:

1. Missing -d flag (38% of attempts)
   → Suggestion: Emphasize detached mode in guidance

2. Wrong port syntax (22% of attempts)
   → Suggestion: Add example of -p 8080:80

3. Forgot port mapping (15% of attempts)
   → Suggestion: Clearer hint about ports

4. Wrong flag order (12% of attempts)
   → Suggestion: Accept variations

5. Typo in image name (8% of attempts)
   → Suggestion: Auto-suggest corrections
```

#### 4. Hint Effectiveness
```
Hint Usage & Success Rates:

Level 1 (Concept hint):
  - Used by: 42% of users
  - Success after: 65%

Level 2 (Structure hint):
  - Used by: 28% of users
  - Success after: 85%

Level 3 (Solution hint):
  - Used by: 15% of users
  - Success after: 98%

💡 Recommendation: Level 2 hints are most effective
```

### For Learners

#### Personal Progress Dashboard
```
┌─────────────────────────────────────────────────┐
│  Your Learning Journey                          │
├─────────────────────────────────────────────────┤
│  🏆 Badges Earned: 8                            │
│  ⭐ Total Points: 1,250                         │
│  📚 Scenarios Completed: 12                     │
│  ⏱️ Total Time: 4h 32m                          │
│                                                  │
│  Your Strengths:                                │
│  ✅ Docker (85% accuracy)                       │
│  ✅ Git (92% accuracy)                          │
│                                                  │
│  Areas to Improve:                              │
│  📈 SQL (64% accuracy)                          │
│  💡 Recommendation: Try "SQL Joins Advanced"    │
│                                                  │
│  Recent Progress:                               │
│  📊 [████████░░] +15% this week                 │
└─────────────────────────────────────────────────┘
```

---

## Adaptive Difficulty System

### Difficulty Calculation
```python
def calculate_difficulty_score(scenario_stats: dict) -> float:
    """
    Returns difficulty score 0-10 based on user performance
    """
    weights = {
        'avg_attempts': 0.3,
        'avg_time_ratio': 0.2,  # actual / estimated
        'hint_usage_rate': 0.2,
        'abandonment_rate': 0.3
    }
    
    # Normalize metrics to 0-10 scale
    attempts_score = min(scenario_stats['avg_attempts'] * 2, 10)
    time_score = min(scenario_stats['avg_time_ratio'] * 10, 10)
    hint_score = scenario_stats['hint_usage_rate'] * 10
    abandon_score = scenario_stats['abandonment_rate'] * 10
    
    difficulty = (
        attempts_score * weights['avg_attempts'] +
        time_score * weights['avg_time_ratio'] +
        hint_score * weights['hint_usage_rate'] +
        abandon_score * weights['abandonment_rate']
    )
    
    return difficulty
```

### Dynamic Recommendations
```python
class AdaptiveRecommender:
    def recommend_next_scenario(self, user_id: str) -> list[str]:
        user_stats = self.get_user_stats(user_id)
        
        # If user struggling (high attempts, many hints)
        if user_stats['avg_attempts'] > 3 or user_stats['hint_usage'] > 2:
            return self._recommend_easier_scenarios(user_id)
        
        # If user excelling (low attempts, no hints, fast completion)
        if user_stats['avg_attempts'] < 1.5 and user_stats['hint_usage'] < 0.5:
            return self._recommend_harder_scenarios(user_id)
        
        # Normal progression
        return self._recommend_next_in_path(user_id)
```

### Hint Timing Adaptation
```python
class AdaptiveHintManager:
    def should_offer_hint(self, user_context: dict, step_context: dict) -> bool:
        # Personalize based on user history
        user_skill = self.get_user_skill_level(user_context['user_id'])
        
        if user_skill == 'beginner':
            offer_after_attempts = 2
            offer_after_time = 60  # 1 minute
        elif user_skill == 'intermediate':
            offer_after_attempts = 3
            offer_after_time = 120  # 2 minutes
        else:  # advanced
            offer_after_attempts = 5
            offer_after_time = 180  # 3 minutes
        
        return (
            user_context['attempts'] >= offer_after_attempts or
            user_context['time_on_step'] >= offer_after_time
        )
```

---

## Analytics API

### Querying Analytics

```python
class AnalyticsAPI:
    def get_scenario_stats(self, scenario_id: str, 
                          start_date: datetime = None, 
                          end_date: datetime = None) -> dict:
        """Get aggregated stats for a scenario"""
        
        return {
            'completion_rate': 0.78,
            'avg_time_seconds': 872,
            'avg_attempts_per_step': 2.3,
            'avg_hints_used': 1.8,
            'abandonment_rate': 0.22,
            'total_attempts': 1243,
            'step_breakdown': [...]
        }
    
    def get_user_progress(self, user_id: str) -> dict:
        """Get user's overall progress"""
        
        return {
            'scenarios_completed': 12,
            'total_points': 1250,
            'badges_earned': ['Docker Novice', 'Git Apprentice', ...],
            'skill_levels': {
                'docker': 85,
                'git': 92,
                'sql': 64
            },
            'recommended_scenarios': [...]
        }
    
    def get_common_mistakes(self, step_id: str, limit: int = 10) -> list:
        """Get most common mistakes for a step"""
        
        return [
            {
                'pattern': '^docker run nginx$',
                'frequency': 472,
                'description': 'Missing -d flag',
                'suggestion': 'Emphasize detached mode'
            },
            ...
        ]
```

---

## Reporting & Insights

### Automated Reports

#### Weekly Scenario Report
```
Subject: Scenario Performance Report - Week of Jan 8-14

Scenario: Docker First Container

Highlights:
✅ Completion rate up 5% (78% → 83%)
⚠️ Step 2 abandonment still high (18%)
💡 Hint 2 effectiveness increased to 88%

Action Items:
1. Revise Step 2 guidance (emphasize -d flag)
2. Add visual diagram for port mapping
3. Create video walkthrough for struggling users

Detailed Stats:
- 287 new attempts this week
- 238 completions
- Avg time: 14m 32s (target: 15m)
```

### A/B Testing Support

```python
class ABTestManager:
    def create_test(self, scenario_id: str, variant_a: dict, variant_b: dict):
        """Create A/B test for scenario variations"""
        
        test = {
            'test_id': uuid.uuid4(),
            'scenario_id': scenario_id,
            'variants': {
                'A': variant_a,  # e.g., original hints
                'B': variant_b   # e.g., revised hints
            },
            'metric': 'completion_rate',
            'start_date': datetime.now()
        }
        
        return test
    
    def get_test_results(self, test_id: str) -> dict:
        """Get A/B test results"""
        
        return {
            'variant_a': {
                'completion_rate': 0.78,
                'sample_size': 623
            },
            'variant_b': {
                'completion_rate': 0.84,  # 6% improvement
                'sample_size': 620
            },
            'confidence': 0.95,
            'winner': 'B'
        }
```

---

## Privacy & Ethics

### Data Collection Principles

1. **Transparency**: Users know what's tracked
2. **Consent**: Opt-in for detailed analytics
3. **Anonymization**: Personal data anonymized
4. **Security**: Analytics data encrypted
5. **Retention**: Data deleted after 2 years

### Anonymization
```python
def anonymize_event(event: SimulationEvent) -> SimulationEvent:
    """Remove PII from events"""
    
    event.user_id = hashlib.sha256(event.user_id.encode()).hexdigest()
    event.data = {k: v for k, v in event.data.items() 
                  if k not in ['email', 'name', 'ip_address']}
    
    return event
```

---

## Implementation Example

```python
class AnalyticsEngine:
    def __init__(self):
        self.db = connect_to_analytics_db()
        self.event_queue = []
    
    def track_event(self, event: SimulationEvent):
        """Track a simulation event"""
        
        # Anonymize
        event = anonymize_event(event)
        
        # Queue for batch insert
        self.event_queue.append(event)
        
        # Flush queue if full
        if len(self.event_queue) >= 100:
            self.flush_events()
    
    def flush_events(self):
        """Batch insert events to database"""
        
        self.db.bulk_insert('simulation_events', self.event_queue)
        self.event_queue = []
    
    def generate_insights(self, scenario_id: str) -> dict:
        """Generate actionable insights"""
        
        stats = self.get_scenario_stats(scenario_id)
        
        insights = []
        
        # High abandonment
        for step in stats['step_breakdown']:
            if step['abandonment_rate'] > 0.15:
                insights.append({
                    'type': 'high_abandonment',
                    'step': step['step_id'],
                    'recommendation': f"Revise guidance for {step['title']}"
                })
        
        # Ineffective hints
        for step in stats['step_breakdown']:
            if step['hint_effectiveness'] < 0.70:
                insights.append({
                    'type': 'ineffective_hints',
                    'step': step['step_id'],
                    'recommendation': f"Improve hint progression for {step['title']}"
                })
        
        return {
            'scenario_id': scenario_id,
            'insights': insights,
            'overall_health': self._calculate_health_score(stats)
        }
```

---

This comprehensive analytics system enables data-driven improvements to scenarios, personalized learning experiences, and measurable learning outcomes.
