# CourseTransformer - Human-in-Loop Interface

This document specifies the Streamlit-based human interface for the CourseTransformer system.

## Overview

The Human-in-Loop Interface is a Streamlit web application that enables humans to:
- Configure transformations with guiding principles
- Review and approve transformation plans
- Review and edit generated content
- Monitor real-time progress
- Download exported packages

## Application Architecture

```
Streamlit UI (Frontend)
    ↓
FastAPI Backend (Optional)
    ↓
LangGraph Orchestrator
    ↓
Agents (7 core agents)
```

## Page Structure

The application uses Streamlit's multi-page architecture:

```
coursetransformer_ui/
├── Home.py                    # Dashboard
├── pages/
│   ├── 1_Guiding_Principles.py
│   ├── 2_Ingestion.py
│   ├── 3_Analysis.py
│   ├── 4_Planning.py          # ⭐ Human Review Required
│   ├── 5_Progress.py
│   ├── 6_Content_Review.py    # ⭐ Human Review Required
│   ├── 7_Quality_Report.py
│   └── 8_Export.py
└── components/
    ├── state_manager.py
    ├── websocket_client.py
    └── ui_components.py
```

## Pages/Tabs Specification

### 1. Home Dashboard

**Purpose**: Overview of all transformations and quick actions

**Components**:
- Active transformations list (table)
- Progress indicators
- Quick start button
- Recent activity log

**Layout**:
```python
import streamlit as st

st.title("CourseTransformer Dashboard")

# Active transformations
st.header("Active Transformations")
transformations = get_active_transformations()

for t in transformations:
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    with col1:
        st.write(f"**{t['name']}**")
    with col2:
        st.progress(t['progress'] / 100)
        st.caption(f"{t['progress']}% complete")
    with col3:
        st.write(f"Status: {t['status']}")
    with col4:
        if t['awaiting_review']:
            if st.button("Review", key=f"review_{t['id']}"):
                st.switch_page(f"pages/{t['review_page']}.py")

# Start new transformation
st.header("Start New Transformation")
if st.button("➕ New Transformation", type="primary"):
    st.switch_page("pages/1_Guiding_Principles.py")
```

**Features**:
- Auto-refresh every 5 seconds
- Filter by status (in progress, awaiting review, completed)
- Search transformations by name

---

### 2. Guiding Principles Editor

**Purpose**: Configure transformation parameters and philosophies

**Components**:
- Philosophy selector
- Target year input
- Tech stack preferences
- Modern topics multi-select
- Quality standards sliders
- Preset save/load

**Layout**:
```python
st.title("Configure Guiding Principles")

# Load existing presets
st.sidebar.header("Presets")
preset = st.sidebar.selectbox(
    "Load Preset",
    ["None", "Default 2026", "R to Python", "Custom"]
)
if preset != "None":
    principles = load_preset(preset)
else:
    principles = {}

# Philosophy
st.header("Philosophy")
philosophy = st.selectbox(
    "Educational Philosophy",
    ["Augmented Human", "Self-Paced", "Project-Based", "Bootcamp Style"],
    help="Defines how AI and humans collaborate in content creation"
)

# Target year
target_year = st.number_input("Target Year", min_value=2024, max_value=2030, value=2026)

# Tech stack
st.header("Technology Stack")
primary_lang = st.selectbox("Primary Language", ["Python", "R", "Julia", "JavaScript"])
secondary_langs = st.multiselect("Secondary Languages", ["R", "Julia", "JavaScript", "Go"])

# LLM integration
llm_choice = st.selectbox("LLM Provider", ["OLLAMA (Local)", "OpenAI", "Anthropic", "Mixed"])
if llm_choice == "OLLAMA (Local)":
    st.info("✅ Privacy-first: All processing happens locally")

# Modern topics
st.header("Modern Topics to Include")
modern_topics = st.multiselect(
    "Select topics to add",
    [
        "Transformers & Attention Mechanism",
        "Large Language Models (LLMs)",
        "Retrieval Augmented Generation (RAG)",
        "MLOps (MLflow, DVC, Weights & Biases)",
        "Privacy-Preserving ML",
        "Federated Learning",
        "Docker & Containerization",
        "GitHub Actions CI/CD",
        "FastAPI for Model Deployment"
    ],
    default=["Transformers & Attention Mechanism", "Large Language Models (LLMs)", "Docker & Containerization"]
)

# Quality standards
st.header("Quality Standards")
col1, col2, col3 = st.columns(3)
with col1:
    code_pass_rate = st.slider("Code Pass Rate", 0.0, 1.0, 1.0, help="% of code that must execute successfully")
with col2:
    accuracy = st.slider("Accuracy Threshold", 0.0, 1.0, 0.95, help="Fact-checking accuracy requirement")
with col3:
    completeness = st.slider("Completeness", 0.0, 1.0, 0.90, help="% of learning objectives covered")

# Pedagogical preferences
st.header("Pedagogical Preferences")
hands_on_ratio = st.slider("Hands-on vs Theory", 0.0, 1.0, 0.8, help="0 = all theory, 1 = all hands-on")
st.caption(f"Hands-on: {hands_on_ratio*100:.0f}%, Theory: {(1-hands_on_ratio)*100:.0f}%")

quiz_frequency = st.radio("Quiz Frequency", ["per_module", "per_lesson", "end_of_course"])
project_based = st.checkbox("Include Capstone Projects", value=True)

# Save configuration
st.divider()
col1, col2 = st.columns([3, 1])
with col1:
    preset_name = st.text_input("Save as Preset", placeholder="My Custom Principles")
with col2:
    st.write("")  # Spacing
    if st.button("💾 Save Preset"):
        save_preset(preset_name, principles)
        st.success(f"Saved preset: {preset_name}")

# Start transformation
if st.button("▶️ Start Transformation", type="primary"):
    # Save principles to session state
    st.session_state['guiding_principles'] = {
        "philosophy": philosophy,
        "target_year": target_year,
        "primary_language": primary_lang,
        "secondary_languages": secondary_langs,
        "llm_integration": llm_choice,
        "modern_topics": modern_topics,
        "quality_thresholds": {
            "code_pass_rate": code_pass_rate,
            "accuracy": accuracy,
            "completeness": completeness
        },
        "pedagogical_preferences": {
            "hands_on_ratio": hands_on_ratio,
            "quiz_frequency": quiz_frequency,
            "project_based": project_based
        }
    }
    st.switch_page("pages/2_Ingestion.py")
```

**Features**:
- YAML export of principles
- Preset templates for common scenarios
- Validation of configuration
- Tooltips explaining each option

---

### 3. Ingestion Tab

**Purpose**: Upload legacy course and view extraction results

**Layout**:
```python
st.title("Course Ingestion")

# Upload options
upload_method = st.radio("Upload Method", ["Directory", "ZIP Archive", "Git Repository"])

if upload_method == "Directory":
    course_path = st.text_input("Course Directory Path", "/path/to/legacy/course")
elif upload_method == "ZIP Archive":
    uploaded_file = st.file_uploader("Upload ZIP", type=['zip'])
else:  # Git Repository
    repo_url = st.text_input("Repository URL", "https://github.com/...")
    branch = st.text_input("Branch", "main")

# File format selection
st.subheader("File Formats to Process")
formats = st.multiselect(
    "Select formats",
    ["R", "Python", "Markdown", "PDF", "HTML", "Video", "Jupyter Notebooks"],
    default=["R", "Markdown", "PDF"]
)

# Start ingestion
if st.button("🔍 Start Ingestion"):
    with st.spinner("Ingesting course content..."):
        result = run_ingestion_agent(course_path, formats)
        st.session_state['ingestion_result'] = result
    st.success("✅ Ingestion complete!")

# Preview extracted content
if 'ingestion_result' in st.session_state:
    result = st.session_state['ingestion_result']
    
    st.subheader("Extracted Course Structure")
    st.json(result['structure'])
    
    st.subheader("Extracted Concepts")
    concepts_df = pd.DataFrame(result['extracted_concepts'])
    st.dataframe(concepts_df, use_container_width=True)
    
    st.subheader("Code Inventory")
    for lang, stats in result['code_inventory'].items():
        st.metric(f"{lang} Code", f"{stats['lines']} lines in {stats['files']} files")
        with st.expander(f"{lang} Libraries"):
            st.write(stats['libraries'])
    
    # Proceed button
    if st.button("➡️ Proceed to Analysis"):
        st.switch_page("pages/3_Analysis.py")
```

---

### 4. Analysis Tab

**Purpose**: View relevance report and gap analysis

**Layout**:
```python
st.title("Content Analysis")

if 'analysis_result' not in st.session_state:
    with st.spinner("Analyzing content relevance..."):
        result = run_analysis_agent(st.session_state['ingestion_result'])
        st.session_state['analysis_result'] = result

result = st.session_state['analysis_result']

# Overall relevance
st.metric("Overall Relevance Score", f"{result['overall_relevance']}%")

# Concept analysis table
st.subheader("Concept Relevance Analysis")
concepts = pd.DataFrame(result['concept_analysis'])
concepts['status_emoji'] = concepts['status'].map({
    'timeless': '✅',
    'relevant': '⚠️',
    'outdated': '🔄',
    'obsolete': '❌'
})
st.dataframe(
    concepts[['status_emoji', 'concept', 'relevance_score', 'recommendation', 'modern_equivalent']],
    use_container_width=True
)

# Gap visualization
st.subheader("Identified Gaps")
gaps = result['missing_topics']
for gap in gaps:
    priority_color = {
        'critical': '🔴',
        'important': '🟡',
        'nice-to-have': '🟢'
    }
    st.write(f"{priority_color[gap['priority']]} **{gap['topic']}** ({gap['priority']})")
    st.caption(gap['reasoning'])
    st.caption(f"Estimated: {gap['estimated_hours']} hours")

# Technology stack comparison
st.subheader("Technology Stack Analysis")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Legacy Stack**")
    st.code("R\nRStudio\nggplot2\ndplyr")
with col2:
    st.markdown("**Modern Stack**")
    st.code("Python 3.10+\nVS Code\nplotly\npandas")

if st.button("➡️ Proceed to Planning"):
    st.switch_page("pages/4_Planning.py")
```

---

### 5. Planning Tab ⭐ (Human Review Required)

**Purpose**: Review and approve transformation plan

**Layout**:
```python
st.title("Transformation Plan Review")

if 'planning_result' not in st.session_state:
    with st.spinner("Generating transformation plan..."):
        result = run_planning_agent(
            st.session_state['analysis_result'],
            st.session_state['guiding_principles']
        )
        st.session_state['planning_result'] = result

plan = st.session_state['planning_result']

# Side-by-side comparison
st.subheader("Curriculum Structure Comparison")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Original Structure")
    st.json(st.session_state['ingestion_result']['structure'])

with col2:
    st.markdown("### Proposed Structure")
    st.json(plan['curriculum_structure'])

# Transformation summary
st.subheader("Transformation Action Summary")
summary = plan['scope_summary']
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Keep", summary['keep']['count'], f"{summary['keep']['hours']}h")
with col2:
    st.metric("Modernize", summary['modernize']['count'], f"{summary['modernize']['hours']}h")
with col3:
    st.metric("Create New", summary['create']['count'], f"{summary['create']['hours']}h")
with col4:
    st.metric("Remove", summary['remove']['count'])

# Detailed task list
st.subheader("Detailed Transformation Tasks")
tasks_df = pd.DataFrame(plan['tasks'])
st.dataframe(
    tasks_df[['task_id', 'type', 'description', 'priority', 'estimated_hours']],
    use_container_width=True
)

# Human review section
st.divider()
st.subheader("🔍 Review and Decision")

# Feedback text area
feedback = st.text_area(
    "Feedback/Comments",
    placeholder="Add any comments or requested changes...",
    height=100
)

# Approval buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✅ Approve Plan", type="primary"):
        submit_review("planning", "approved", feedback)
        st.success("Plan approved! Proceeding to modernization...")
        time.sleep(2)
        st.switch_page("pages/5_Progress.py")

with col2:
    if st.button("🔄 Needs Adjustment"):
        submit_review("planning", "needs_adjustment", feedback)
        st.warning("Sending back to planning agent with your feedback...")
        time.sleep(2)
        st.rerun()

with col3:
    if st.button("❌ Reject Plan"):
        if st.session_state.get('confirm_reject'):
            submit_review("planning", "rejected", feedback)
            st.error("Plan rejected. Transformation aborted.")
        else:
            st.session_state['confirm_reject'] = True
            st.warning("Click again to confirm rejection")
```

**Features**:
- Expandable task details
- Filter tasks by type/priority
- Export plan as PDF
- Version comparison if plan is revised

---

### 6. Progress Tab

**Purpose**: Monitor real-time transformation progress

**Layout**:
```python
st.title("Transformation Progress")

transformation_id = st.session_state.get('transformation_id')
if not transformation_id:
    st.error("No active transformation")
    st.stop()

# Auto-refresh
st.markdown("Auto-refreshing every 5 seconds...")

# Current stage
status = get_transformation_status(transformation_id)
st.header(f"Stage: {status['current_stage'].title()}")

# Progress bar
progress = status['progress_percentage'] / 100
st.progress(progress)
st.caption(f"{status['progress_percentage']}% complete")

# Timeline
st.subheader("Workflow Timeline")
stages = ["Ingestion", "Analysis", "Planning", "Modernization", "Generation", "QA", "Export"]
current_index = stages.index(status['current_stage'].title()) if status['current_stage'].title() in stages else 0

cols = st.columns(len(stages))
for i, (col, stage) in enumerate(zip(cols, stages)):
    with col:
        if i < current_index:
            st.success(f"✅ {stage}")
        elif i == current_index:
            st.info(f"⏳ {stage}")
        else:
            st.text(f"⭕ {stage}")

# Real-time activity log
st.subheader("Activity Log")
log_container = st.container()
with log_container:
    logs = get_activity_logs(transformation_id, limit=20)
    for log in logs:
        timestamp = log['timestamp']
        message = log['message']
        level = log['level']
        
        if level == 'error':
            st.error(f"[{timestamp}] {message}")
        elif level == 'warning':
            st.warning(f"[{timestamp}] {message}")
        else:
            st.text(f"[{timestamp}] {message}")

# Performance metrics
st.subheader("Performance Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("LLM Tokens Used", format_number(status['llm_token_usage']))
with col2:
    elapsed = calculate_elapsed_time(status['created_at'])
    st.metric("Elapsed Time", elapsed)
with col3:
    eta = status['estimated_completion']
    st.metric("ETA", eta)

# Control buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("⏸️ Pause Transformation"):
        pause_transformation(transformation_id)
        st.info("Transformation paused")
with col2:
    if st.button("🔄 Resume Transformation"):
        resume_transformation(transformation_id)
        st.success("Transformation resumed")

# Auto-refresh
time.sleep(5)
st.rerun()
```

**Features**:
- WebSocket integration for live updates
- Pause/resume controls
- Download logs button
- ETA estimation

---

### 7. Content Review Tab ⭐ (Human Review Required)

**Purpose**: Review and edit generated content

**Layout**:
```python
st.title("Content Review")

content = st.session_state.get('generation_output')
qa_report = st.session_state.get('qa_output')

if not content:
    st.warning("No content ready for review yet")
    st.stop()

# Quality score badge
score = qa_report['overall_score']
score_color = 'green' if score >= 85 else 'orange' if score >= 70 else 'red'
st.markdown(f"**Overall Quality Score**: <span style='color:{score_color}; font-size:24px;'>{score}%</span>", unsafe_allow_html=True)

# Content type tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Slides", "💻 Labs", "❓ Quizzes", "📈 Diagrams"])

with tab1:
    st.subheader("Generated Slides")
    slides = content['slides']
    
    for i, slide in enumerate(slides):
        with st.expander(f"Slide {i+1}: {slide['title']}", expanded=(i==0)):
            # Show slide content
            st.markdown(slide['content'])
            
            # Side-by-side: original vs generated (if modernizing)
            if slide.get('original_content'):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Original**")
                    st.code(slide['original_content'])
                with col2:
                    st.markdown("**Generated**")
                    st.code(slide['content'])
            
            # Actions
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("✅ Approve", key=f"approve_slide_{i}"):
                    approve_content_item('slide', slide['id'])
                    st.success("Approved!")
            with col2:
                if st.button("✏️ Edit", key=f"edit_slide_{i}"):
                    st.session_state[f'editing_slide_{i}'] = True
            with col3:
                if st.button("🔄 Regenerate", key=f"regen_slide_{i}"):
                    instructions = st.text_input(f"Instructions for regeneration (slide {i})")
                    regenerate_content('slide', slide['id'], instructions)
            with col4:
                if st.button("❌ Discard", key=f"discard_slide_{i}"):
                    discard_content_item('slide', slide['id'])
            
            # Inline editor (if edit clicked)
            if st.session_state.get(f'editing_slide_{i}'):
                edited_content = st.text_area(
                    "Edit content",
                    value=slide['content'],
                    height=300,
                    key=f"editor_slide_{i}"
                )
                if st.button("💾 Save", key=f"save_slide_{i}"):
                    save_edited_content('slide', slide['id'], edited_content)
                    st.session_state[f'editing_slide_{i}'] = False
                    st.success("Saved!")

with tab2:
    st.subheader("Generated Labs")
    labs = content['labs']
    
    for i, lab in enumerate(labs):
        with st.expander(f"Lab {i+1}: {lab['title']}", expanded=(i==0)):
            # Show notebook
            st.code(lab['content'], language='python')
            
            # Execution status
            exec_status = qa_report['checks']['code_execution']['details']['labs'][i]
            if exec_status['passed']:
                st.success(f"✅ Code executes successfully ({exec_status['duration_ms']}ms)")
            else:
                st.error(f"❌ Execution failed: {exec_status['error']}")
            
            # Actions (same as slides)
            # ... (similar action buttons)

with tab3:
    st.subheader("Generated Quizzes")
    quizzes = content['quizzes']
    
    for quiz in quizzes:
        st.markdown(f"**{quiz['question']}**")
        if quiz['type'] == 'multiple_choice':
            for option in quiz['options']:
                if option == quiz['correct_answer']:
                    st.success(f"✅ {option} (correct)")
                else:
                    st.text(f"   {option}")
        st.caption(f"Explanation: {quiz['explanation']}")
        st.divider()

with tab4:
    st.subheader("Generated Diagrams")
    diagrams = content['diagrams']
    
    for diagram in diagrams:
        st.markdown(f"**{diagram['title']}**")
        st.code(diagram['mermaid_code'], language='mermaid')
        # Render diagram (using streamlit-mermaid or similar)
        # st_mermaid(diagram['mermaid_code'])

# Quality issues
st.divider()
st.subheader("Quality Issues")
issues = qa_report['issues']
critical = [i for i in issues if i['severity'] == 'critical']
warnings = [i for i in issues if i['severity'] == 'warning']

if critical:
    st.error(f"🔴 {len(critical)} Critical Issues")
    for issue in critical:
        st.write(f"- {issue['description']} ({issue['location']})")

if warnings:
    st.warning(f"🟡 {len(warnings)} Warnings")
    with st.expander("View warnings"):
        for issue in warnings:
            st.write(f"- {issue['description']} ({issue['location']})")

# Batch operations
st.divider()
st.subheader("Batch Operations")
col1, col2 = st.columns(2)
with col1:
    if st.button("✅ Approve All"):
        approve_all_content()
        st.success("All content approved!")
with col2:
    if st.button("🔄 Regenerate All with Issues"):
        regenerate_all_with_issues()
        st.info("Regenerating problematic content...")

# Final review decision
st.divider()
st.subheader("Final Decision")
feedback = st.text_area("Overall Feedback")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✅ Approve All Content", type="primary"):
        submit_review("content", "approved", feedback)
        st.success("Content approved! Proceeding to export...")
        time.sleep(2)
        st.switch_page("pages/8_Export.py")
with col2:
    if st.button("✏️ Continue Editing"):
        st.info("Keep editing...")
with col3:
    if st.button("❌ Reject All"):
        submit_review("content", "rejected", feedback)
        st.error("Content rejected")
```

**Features**:
- Inline content editing with syntax highlighting
- Side-by-side original vs generated comparison
- Per-item and batch operations
- Code execution results display
- Issue highlighting

---

### 8. Quality Report Tab

**Purpose**: Detailed quality metrics and issue tracking

**Layout**: See complete specification in repository.

---

### 9. Export Tab

**Purpose**: Download and deploy transformed course

**Layout**:
```python
st.title("Export Transformed Course")

export_result = st.session_state.get('export_output')
if not export_result:
    with st.spinner("Preparing export..."):
        result = run_export_agent(st.session_state['generation_output'])
        st.session_state['export_output'] = result

# Export preview
st.subheader("Export Structure Preview")
st.code(display_directory_tree(export_result['output_path']))

# Export options
st.subheader("Export Format")
export_format = st.radio(
    "Choose export format",
    ["Full Package (CoursesGTM + CoursePlayerApp + Docker)",
     "CoursesGTM Only",
     "CoursePlayerApp Only",
     "Individual Course"]
)

# Download buttons
st.subheader("Download")
col1, col2, col3 = st.columns(3)
with col1:
    zip_file = create_zip(export_result['output_path'])
    st.download_button(
        "📦 Download Full Package",
        data=zip_file,
        file_name="transformed_course.zip",
        mime="application/zip"
    )
with col2:
    curriculum_json = export_result['coursesgtm_curriculum']
    st.download_button(
        "📄 Download curriculum.json",
        data=curriculum_json,
        file_name="curriculum.json",
        mime="application/json"
    )
with col3:
    docker_compose = export_result['docker_compose']
    st.download_button(
        "🐳 Download docker-compose.yml",
        data=docker_compose,
        file_name="docker-compose.yml"
    )

# Deployment instructions
st.subheader("Deployment Instructions")
with st.expander("Deploy to CoursesGTM"):
    st.markdown("""
    1. Copy `curriculum.json` to CoursesGTM seed directory
    2. Run `npm run seed`
    3. Verify courses appear in database
    """)

with st.expander("Deploy to CoursePlayerApp"):
    st.markdown("""
    1. Extract course content to `CoursePlayerApp/public/content/`
    2. Rebuild app: `npm run build`
    3. Deploy to hosting platform
    """)

st.success("✅ Transformation Complete!")
```

---

## WebSocket Integration

For real-time updates:

```python
import streamlit as st
from streamlit_ws import st_ws

# In Progress page
ws = st_ws.create("ws://localhost:8000/ws/transformation/{transformation_id}")

for event in ws.receive():
    if event['type'] == 'agent_completed':
        st.toast(f"✅ {event['agent']} completed!")
    elif event['type'] == 'human_review_required':
        st.info("⏸️ Waiting for your review...")
        # Switch to review page
```

---

## State Management

```python
# Shared state across pages
if 'transformation_id' not in st.session_state:
    st.session_state['transformation_id'] = None

if 'guiding_principles' not in st.session_state:
    st.session_state['guiding_principles'] = {}

# Persist state to disk
def save_session_state():
    with open(f"session_{st.session_state['transformation_id']}.json", 'w') as f:
        json.dump(dict(st.session_state), f)

def load_session_state(transformation_id):
    with open(f"session_{transformation_id}.json", 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            st.session_state[key] = value
```

---

This specification provides a complete foundation for implementing the Streamlit human interface for CourseTransformer.
