# SimulationPlayer UI Design

This document specifies the Streamlit-based user interface for SimulationPlayer, including component layouts, interactions, and visual design.

---

## Design Principles

1. **Clarity**: Clear visual hierarchy and obvious actions
2. **Feedback**: Immediate, visible feedback for all actions
3. **Progress**: Always show current position and progress
4. **Encouragement**: Positive, motivating messaging
5. **Accessibility**: Readable fonts, good contrast, keyboard navigation
6. **Responsiveness**: Works on desktop and tablet (mobile view-only)

---

## Main Simulation Viewer

### Layout Overview

```
┌──────────────────────────────────────────────────────────────────┐
│  🎮 Interactive Lab Simulation                    [↻ Reset] [⏸]  │
├──────────────────────────────────────────────────────────────────┤
│  [Progress: ████████░░░░░░ 60% (3/5 steps)]  ⏱️ 12m 34s         │
├──────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌─────────────────────────────────────┐  ┌─────────────────────┐│
│  │  📝 Step 3 of 5: Run Container      │  │  💡 Hints           ││
│  │                                      │  │  ▼ Click for hint   ││
│  │  Objective:                          │  │                     ││
│  │  Start NGINX in detached mode        │  │  🤖 AI Assistant    ││
│  │                                      │  │  Ask a question...  ││
│  │  💬 AI Guidance:                     │  │  ┌───────────────┐  ││
│  │  Now let's start the container.      │  │  │ Q: What's -d? │  ││
│  │  Use the -d flag to run it in the    │  │  │ A: The -d flag│  ││
│  │  background so your terminal stays   │  │  │ runs detached │  ││
│  │  available for other commands.       │  │  └───────────────┘  ││
│  │                                      │  │                     ││
│  │  💻 Terminal                         │  │  📊 Your Progress   ││
│  │  ┌──────────────────────────────┐   │  │  ⏱️ Time: 5m 23s   ││
│  │  │ $ docker pull nginx          │   │  │  💪 Attempts: 2     ││
│  │  │ Status: Downloaded           │   │  │  💡 Hints: 1        ││
│  │  │ $ docker run                 │   │  │  ✅ Accuracy: 85%   ││
│  │  │                              │   │  │                     ││
│  │  └──────────────────────────────┘   │  │  🏆 Badges          ││
│  │  [▶️ Execute] [💡 Hint] [❓ Help]    │  │  ⭐ Git Beginner    ││
│  │                                      │  └─────────────────────┘│
│  │  Output:                             │                         │
│  │  ┌──────────────────────────────┐   │                         │
│  │  │ (pending execution...)       │   │                         │
│  │  └──────────────────────────────┘   │                         │
│  │                                      │                         │
│  └─────────────────────────────────────┘                         │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. Header Bar

**Location**: Top of page

**Components**:
```python
def render_header():
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.title("🎮 " + scenario.title)
    
    with col2:
        if st.button("↻ Reset Scenario"):
            reset_scenario()
    
    with col3:
        if st.button("⏸ Save & Exit"):
            save_checkpoint()
```

**Features**:
- Scenario title with icon
- Reset button (with confirmation modal)
- Save & Exit button (creates checkpoint)

**Visual Design**:
- Background: Light blue (#E3F2FD)
- Title: 24px, bold
- Buttons: Outlined, 14px

---

### 2. Progress Indicator

**Location**: Below header

**Components**:
```python
def render_progress():
    col1, col2 = st.columns([4, 1])
    
    with col1:
        progress_pct = (current_step / total_steps)
        st.progress(progress_pct)
        st.caption(f"Step {current_step} of {total_steps} ({int(progress_pct*100)}%)")
    
    with col2:
        elapsed = datetime.now() - start_time
        st.metric("Time", format_duration(elapsed))
```

**Features**:
- Visual progress bar
- Step counter (e.g., "3/5 steps")
- Percentage complete
- Elapsed time
- Estimated time remaining (optional)

**Visual Design**:
- Progress bar: Green gradient (#4CAF50 to #8BC34A)
- Height: 20px
- Border radius: 10px
- Animated on progress

---

### 3. Step Panel (Main Content)

**Location**: Left side, 70% width

#### 3.1 Step Header

```python
def render_step_header(step):
    st.subheader(f"📝 Step {step.number} of {total_steps}: {step.title}")
    
    with st.expander("ℹ️ Step Details", expanded=True):
        st.markdown(f"**Objective**: {step.objective}")
        if step.description:
            st.markdown(step.description)
```

**Features**:
- Step number and title
- Expandable details section
- Clear objective statement

#### 3.2 AI Guidance Section

```python
def render_ai_guidance(guidance_text):
    st.markdown("### 💬 AI Guidance")
    st.info(guidance_text)  # Blue info box
```

**Features**:
- AI-generated contextual guidance
- Displayed in info box (light blue background)
- Markdown formatting support
- Updates dynamically based on context

**Visual Design**:
- Background: #E3F2FD (light blue)
- Border-left: 4px solid #2196F3
- Padding: 16px
- Icon: 💬 or 🤖

#### 3.3 Environment UI (Terminal Example)

```python
def render_terminal_environment():
    st.markdown("### 💻 Terminal")
    
    # Command history
    history_container = st.container()
    with history_container:
        for entry in command_history:
            st.code(f"$ {entry.command}", language="bash")
            if entry.output:
                if entry.success:
                    st.success(entry.output)
                else:
                    st.error(entry.output)
    
    # Command input
    command = st.text_input(
        "Command:",
        key="terminal_cmd",
        placeholder="$ Enter your command here..."
    )
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        execute_btn = st.button("▶️ Execute", type="primary")
    with col2:
        hint_btn = st.button("💡 Hint")
    with col3:
        help_btn = st.button("❓ Ask Question")
    
    # Execute command
    if execute_btn and command:
        result = execute_command(command)
        display_result(result)
```

**Features**:
- Command history (scrollable)
- Current command input
- Execute button (primary action)
- Hint button (secondary action)
- Help/question button

**Visual Design**:
- Terminal font: 'Fira Code', 'Courier New', monospace
- Background: #1E1E1E (dark theme)
- Text color: #D4D4D4 (light gray)
- Prompt: #4EC9B0 (cyan)
- Border radius: 8px

#### 3.4 Feedback Display

```python
def display_result(result):
    if result.is_valid:
        st.success(f"""
        ✅ **Correct!**
        
        {result.success_message}
        """)
        
        if result.is_final_step:
            st.balloons()
            show_completion_modal()
        else:
            if st.button("➡️ Next Step"):
                advance_to_next_step()
    else:
        st.error(f"""
        ❌ **Not quite right**
        
        {result.error_message}
        
        💡 **Suggestion**: {result.suggestion}
        """)
        
        # Show retry button
        if st.button("🔄 Try Again"):
            clear_input()
```

**Visual Design**:
- Success: Green box (#4CAF50 background, white text)
- Error: Red box (#F44336 background, white text)
- Warning: Yellow box (#FFC107 background, dark text)
- Animations: Balloons on scenario completion

---

### 4. Sidebar Panels

**Location**: Right side, 30% width

#### 4.1 Hint Panel (Collapsible)

```python
def render_hint_panel():
    with st.expander("💡 Hints", expanded=False):
        st.write(f"**Hints used: {hints_used}/3**")
        
        # Show used hints
        for i, hint in enumerate(used_hints):
            st.info(f"**Level {i+1}**: {hint.text}")
        
        # Offer next hint
        if hints_used < 3:
            next_level = hints_used + 1
            if st.button(f"Show Level {next_level} Hint"):
                show_hint(next_level)
        else:
            st.warning("All hints used")
        
        # Hint impact warning
        if hints_used == 0:
            st.caption("💭 Using hints may reduce your score")
```

**Features**:
- Collapsible expander
- Shows hint count
- Display previously used hints
- Button to reveal next hint
- Warning about score impact
- Progressive disclosure (level 1, 2, 3)

**Visual Design**:
- Collapsed by default
- Hint levels color-coded:
  - Level 1: Blue (#2196F3)
  - Level 2: Orange (#FF9800)
  - Level 3: Red (#F44336)

#### 4.2 AI Assistant Chat (Collapsible)

```python
def render_ai_assistant():
    with st.expander("🤖 AI Assistant", expanded=False):
        # Chat history
        chat_container = st.container()
        with chat_container:
            for msg in chat_history:
                if msg.role == "user":
                    st.markdown(f"**You**: {msg.content}")
                else:
                    st.info(f"**AI**: {msg.content}")
        
        # Question input
        question = st.text_input(
            "Ask a question:",
            key="ai_question",
            placeholder="e.g., What does the -d flag do?"
        )
        
        if st.button("Send"):
            answer = get_ai_answer(question)
            chat_history.append({"role": "user", "content": question})
            chat_history.append({"role": "assistant", "content": answer})
            st.rerun()
```

**Features**:
- Chat-style interface
- Message history
- Text input for questions
- Context-aware responses
- Scrollable history

**Visual Design**:
- User messages: Right-aligned, blue bubble
- AI messages: Left-aligned, gray bubble
- Avatar icons (👤 for user, 🤖 for AI)

#### 4.3 Stats Panel

```python
def render_stats_panel():
    st.subheader("📊 Your Progress")
    
    # Time spent
    st.metric(
        "⏱️ Time on Step",
        format_duration(step_time),
        delta=None
    )
    
    # Attempts
    st.metric(
        "💪 Attempts",
        attempts,
        delta=None
    )
    
    # Hints used
    st.metric(
        "💡 Hints Used",
        hints_used,
        delta=None
    )
    
    # Accuracy
    accuracy = calculate_accuracy(attempts, hints_used)
    st.metric(
        "✅ Accuracy",
        f"{accuracy}%",
        delta=None
    )
    
    # Progress chart (optional)
    if show_chart:
        st.line_chart(step_progress_data)
```

**Features**:
- Real-time metrics
- Time tracking
- Attempt counter
- Hint usage
- Accuracy score
- Optional progress visualization

**Visual Design**:
- Metrics: Large numbers (24px), labels (12px)
- Icons: Emoji or Font Awesome
- Background: Light gray (#F5F5F5)

#### 4.4 Badges Section

```python
def render_badges():
    st.subheader("🏆 Badges")
    
    for badge in earned_badges:
        st.success(f"⭐ {badge.name}")
        st.caption(badge.description)
    
    if unearned_badges:
        with st.expander("🔒 Locked Badges"):
            for badge in unearned_badges:
                st.write(f"🔒 {badge.name}")
                st.caption(f"Unlock by: {badge.requirement}")
```

---

## Environment-Specific UIs

### Terminal Simulator

Already shown above. Key features:
- Command input
- Command history
- Colored output
- Monospace font

### Code Editor

```python
def render_code_editor():
    from streamlit_monaco import st_monaco
    
    st.subheader("💻 Code Editor")
    
    # File tabs (if multiple files)
    if len(files) > 1:
        selected_file = st.tabs([f.name for f in files])
    
    # Monaco editor
    edited_code = st_monaco(
        value=current_file.content,
        height=400,
        language=current_file.language,
        theme="vs-dark",
        options={
            'fontSize': 14,
            'minimap': {'enabled': True},
            'scrollBeyondLastLine': False,
            'lineNumbers': 'on',
            'wordWrap': 'on'
        }
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Run Code"):
            result = execute_code(edited_code)
            display_output(result)
    with col2:
        if st.button("🔍 Check Solution"):
            validation = validate_code(edited_code)
            display_validation(validation)
    with col3:
        if st.button("📊 Show Diff"):
            show_diff(original_code, edited_code)
```

### Infrastructure Builder

```python
def render_infrastructure_builder():
    from streamlit_agraph import agraph, Node, Edge
    
    st.subheader("🏗️ Infrastructure Designer")
    
    # Component palette (sidebar)
    with st.sidebar:
        st.subheader("🧩 Components")
        component_type = st.selectbox(
            "Add Component",
            ["EC2 Instance", "S3 Bucket", "RDS Database", "Load Balancer"]
        )
        if st.button("➕ Add to Canvas"):
            add_component(component_type)
    
    # Canvas
    nodes = [
        Node(id=c.id, label=c.name, image=c.icon)
        for c in components
    ]
    edges = [
        Edge(source=conn.from_id, target=conn.to_id)
        for conn in connections
    ]
    
    selected = agraph(nodes=nodes, edges=edges)
    
    # Configuration panel
    if selected:
        st.subheader("⚙️ Configure Component")
        # Component-specific config form
        show_component_config(selected)
```

### Database Query Simulator

```python
def render_database_query():
    st.subheader("💾 SQL Query Editor")
    
    # Schema viewer
    with st.expander("📋 Database Schema"):
        for table in schema.tables:
            st.write(f"**{table.name}**")
            st.dataframe(table.sample_data.head())
    
    # SQL editor
    query = st.text_area(
        "SQL Query:",
        height=150,
        placeholder="SELECT * FROM customers WHERE..."
    )
    
    # Execute button
    if st.button("▶️ Execute Query"):
        result = execute_query(query)
        
        # Results
        st.success(f"Query executed in {result.time_ms}ms")
        st.dataframe(result.data)
        
        # Query plan
        with st.expander("📊 Query Plan"):
            st.code(result.explain_plan)
```

---

## Completion Modal

```python
def show_completion_modal():
    st.balloons()
    
    st.success(f"""
    # 🎉 Congratulations!
    
    You've completed **{scenario.title}**!
    
    ## Your Stats:
    - ⏱️ Time: {total_time}
    - 💪 Total Attempts: {total_attempts}
    - 💡 Hints Used: {total_hints}
    - ✅ Accuracy: {accuracy}%
    
    ## What You Learned:
    {format_learning_objectives(scenario.learning_objectives)}
    
    ## Badge Earned:
    🏆 **{scenario.completion.badge}** (+{scenario.completion.points} points)
    """)
    
    # Next steps
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Retry Scenario"):
            reset_scenario()
    with col2:
        if scenario.completion.next_scenario:
            if st.button(f"➡️ Next: {next_scenario_title}"):
                load_scenario(scenario.completion.next_scenario)
    
    # Certificate download
    if st.button("📜 Download Certificate"):
        generate_certificate()
```

---

## Responsive Design

### Desktop (>1200px)
- Two-column layout (70% main, 30% sidebar)
- All panels visible
- Large terminal/editor

### Tablet (768px - 1200px)
- Single column layout
- Collapsible sidebar
- Compact stats

### Mobile (<768px)
- View-only mode
- No interactive execution
- Tutorial walkthrough only

---

## Color Palette

### Primary Colors
- **Primary**: #2196F3 (Blue)
- **Secondary**: #4CAF50 (Green)
- **Accent**: #FF9800 (Orange)

### Status Colors
- **Success**: #4CAF50 (Green)
- **Error**: #F44336 (Red)
- **Warning**: #FFC107 (Yellow)
- **Info**: #2196F3 (Blue)

### Neutral Colors
- **Background**: #FAFAFA (Light Gray)
- **Surface**: #FFFFFF (White)
- **Border**: #E0E0E0 (Gray)
- **Text Primary**: #212121 (Dark Gray)
- **Text Secondary**: #757575 (Medium Gray)

---

## Typography

### Fonts
- **Headings**: 'Inter', 'Helvetica Neue', sans-serif
- **Body**: 'Inter', sans-serif
- **Code**: 'Fira Code', 'Courier New', monospace

### Sizes
- **H1**: 32px, bold
- **H2**: 24px, bold
- **H3**: 20px, semibold
- **Body**: 16px, regular
- **Caption**: 12px, regular
- **Code**: 14px, regular

---

## Animations

### Progress Bar
```css
@keyframes progress {
    0% { width: 0%; }
    100% { width: var(--progress); }
}
```

### Success Celebration
- Streamlit balloons
- Confetti (custom component)
- Badge animation (scale + fade-in)

### Loading States
- Spinner for command execution
- Skeleton screens for slow loads
- Progress indicators

---

## Accessibility

### Keyboard Navigation
- Tab through all interactive elements
- Enter to submit
- Escape to close modals
- Arrow keys for history navigation

### Screen Reader Support
- ARIA labels on all buttons
- Alt text for images/icons
- Semantic HTML structure
- Focus indicators

### Color Contrast
- WCAG AA compliance (4.5:1 for normal text)
- WCAG AAA for important actions (7:1)

---

## Implementation Example

```python
import streamlit as st
from streamlit_monaco import st_monaco
from datetime import datetime

class SimulationPlayerUI:
    def __init__(self, scenario):
        self.scenario = scenario
        self.current_step = 0
        self.start_time = datetime.now()
    
    def render(self):
        # Header
        self.render_header()
        
        # Progress
        self.render_progress()
        
        # Main content
        col1, col2 = st.columns([7, 3])
        
        with col1:
            self.render_step_panel()
        
        with col2:
            self.render_sidebar()
    
    def render_header(self):
        st.title(f"🎮 {self.scenario.title}")
        
        col1, col2 = st.columns([5, 1])
        with col2:
            if st.button("↻ Reset"):
                self.reset()
    
    def render_progress(self):
        progress = (self.current_step + 1) / len(self.scenario.steps)
        st.progress(progress)
        st.caption(f"Step {self.current_step + 1} of {len(self.scenario.steps)}")
    
    def render_step_panel(self):
        step = self.scenario.steps[self.current_step]
        
        st.subheader(f"📝 {step.title}")
        st.info(f"**Objective**: {step.objective}")
        
        # AI Guidance
        guidance = self.get_ai_guidance(step)
        st.markdown("### 💬 AI Guidance")
        st.info(guidance)
        
        # Environment UI
        self.render_environment(step)
    
    def render_sidebar(self):
        # Hints
        with st.expander("💡 Hints"):
            self.render_hints()
        
        # AI Assistant
        with st.expander("🤖 AI Assistant"):
            self.render_ai_assistant()
        
        # Stats
        st.subheader("📊 Stats")
        self.render_stats()
    
    def render_environment(self, step):
        if self.scenario.environment.type == "terminal":
            self.render_terminal()
        elif self.scenario.environment.type == "code_editor":
            self.render_code_editor()
        # ... other types

if __name__ == "__main__":
    scenario = load_scenario("docker-first-container")
    ui = SimulationPlayerUI(scenario)
    ui.render()
```

---

## Testing UI Components

### Visual Regression Testing
- Screenshot comparisons
- Cross-browser testing
- Responsive breakpoint testing

### Usability Testing
- Task completion rates
- Time to complete steps
- Error recovery success
- Hint usage patterns

### A/B Testing Opportunities
- Hint presentation style
- Feedback message tone
- Progress indicator design
- Color schemes

---

This UI design creates an engaging, supportive learning environment that guides users through hands-on practice while maintaining clarity and providing intelligent assistance when needed.
