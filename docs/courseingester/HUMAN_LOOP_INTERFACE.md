# CourseIngester - Human-in-Loop Interface Design

## Overview

The human-in-loop interface is a Streamlit-based web application that enables users to upload content, review AI-generated organization, interact with materials via chat, and export enriched curriculum. The interface balances automation with human oversight at critical decision points.

**Design Philosophy**: Automate the tedious, consult humans for judgment. The AI handles parsing, analysis, and initial organization. Humans review, approve, and refine the final structure.

---

## Application Structure

### Technology Stack
- **Framework**: Streamlit
- **Layout**: Multi-page app with sidebar navigation
- **State Management**: Streamlit session state
- **Styling**: Custom CSS for enhanced UX
- **Components**: Streamlit native + custom components (drag-drop, graph visualization)

### Navigation
```python
# app.py - Main entry point
import streamlit as st

st.set_page_config(
    page_title="CourseIngester",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["📤 Upload", "📄 Content Viewer", "🕸️ Knowledge Graph", 
     "💬 Chat with Sources", "📋 Organization Review", 
     "📖 Study Guides", "⚠️ Gap Analysis", "📦 Export"]
)

# Route to selected page
if page == "📤 Upload":
    show_upload_page()
elif page == "📄 Content Viewer":
    show_content_viewer()
# ... etc
```

---

## 1. Upload Interface

### Features

#### **Drag-Drop File Upload**
```python
import streamlit as st

st.title("📤 Upload Course Materials")

st.markdown("""
Upload your course materials in any format. Supported types:
- 📄 Documents: PDF, DOCX, PPTX, MD, TEX
- 🎥 Videos: MP4, AVI, MOV, MKV
- 🎵 Audio: MP3, WAV, M4A
- 💻 Code: ZIP, GIT repos, Jupyter notebooks
- 🌐 Web: URLs to scrape
""")

# File uploader (multiple files)
uploaded_files = st.file_uploader(
    "Drop files here or click to browse",
    accept_multiple_files=True,
    type=['pdf', 'docx', 'pptx', 'md', 'tex', 'mp4', 'avi', 'mov', 
          'mp3', 'wav', 'zip', 'ipynb', 'tar', 'gz']
)

# URL input
url_input = st.text_input("Or enter a URL to scrape")

# Folder upload (via ZIP or directory path)
folder_path = st.text_input("Or enter path to local folder")
```

#### **Upload History**
```python
st.subheader("📜 Upload History")

# Display previous uploads
history = load_upload_history()

for upload_session in history:
    with st.expander(f"📅 {upload_session['date']} - {upload_session['file_count']} files"):
        st.write(f"**Status**: {upload_session['status']}")
        st.write(f"**Files**: {', '.join(upload_session['filenames'])}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"View Details", key=f"view_{upload_session['id']}"):
                show_upload_details(upload_session['id'])
        with col2:
            if st.button(f"Delete", key=f"delete_{upload_session['id']}"):
                delete_upload(upload_session['id'])
```

#### **Batch Operations**
```python
# Show current processing status
if st.session_state.get('processing', False):
    st.info("⏳ Processing files...")
    
    # Progress bar
    progress = st.progress(0)
    status_text = st.empty()
    
    for i, file in enumerate(st.session_state.files):
        progress.progress((i + 1) / len(st.session_state.files))
        status_text.text(f"Processing {file.name}...")
    
    # Control buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⏸️ Pause"):
            pause_processing()
    with col2:
        if st.button("❌ Cancel"):
            cancel_processing()
```

#### **File Type Detection**
```python
def detect_file_type(file):
    """Auto-detect file type and show appropriate icon"""
    ext = file.name.split('.')[-1].lower()
    
    icons = {
        'pdf': '📄', 'docx': '📝', 'pptx': '📊',
        'mp4': '🎥', 'mp3': '🎵', 'zip': '📦',
        'ipynb': '📓', 'py': '🐍', 'md': '📋'
    }
    
    return icons.get(ext, '📁')

# Display uploaded files with icons
for file in uploaded_files:
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.write(detect_file_type(file))
    with col2:
        st.write(file.name)
    with col3:
        st.write(f"{file.size / 1024:.1f} KB")
```

#### **Ingestion Mode Selection**
```python
st.subheader("⚙️ Ingestion Settings")

mode = st.radio(
    "Select ingestion mode:",
    ["Quick", "Standard (Recommended)", "Deep"],
    index=1
)

st.info({
    "Quick": "Parse only, minimal analysis (5-10 min)",
    "Standard (Recommended)": "Full understanding, organization, basic enhancements (20-30 min)",
    "Deep": "Complete NotebookLM features, comprehensive analysis (45-60 min)"
}[mode])

# Advanced options (collapsible)
with st.expander("🔧 Advanced Options"):
    enable_ocr = st.checkbox("Enable OCR for scanned PDFs", value=True)
    extract_images = st.checkbox("Extract images from documents", value=True)
    enable_transcription = st.checkbox("Transcribe videos/audio", value=True)
    enable_code_analysis = st.checkbox("Analyze code repositories", value=True)
```

---

## 2. Content Viewer

### Features

#### **Browse Parsed Documents**
```python
st.title("📄 Content Viewer")

# Sidebar filters
st.sidebar.subheader("🔍 Filters")
filter_type = st.sidebar.multiselect(
    "Content Type",
    ["Lecture", "Tutorial", "Reading", "Example", "Exercise", "Assessment"]
)
filter_difficulty = st.sidebar.multiselect(
    "Difficulty",
    ["Basic", "Intermediate", "Advanced"]
)
filter_topic = st.sidebar.multiselect(
    "Topic",
    get_unique_topics()
)

# Search bar
search_query = st.text_input("🔎 Search content", placeholder="Enter keywords...")

# Display documents
documents = get_filtered_documents(filter_type, filter_difficulty, filter_topic, search_query)

for doc in documents:
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {doc['title']}")
            st.caption(f"{doc['type']} | {doc['difficulty']} | {doc['topics']}")
        
        with col2:
            if st.button("👁️ View", key=f"view_{doc['id']}"):
                st.session_state.selected_doc = doc['id']
        
        # Preview
        with st.expander("📖 Preview"):
            st.markdown(doc['summary'][:500] + "...")
```

#### **Side-by-Side View**
```python
if st.session_state.get('selected_doc'):
    doc = get_document(st.session_state.selected_doc)
    
    st.subheader(f"📄 {doc['title']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Original")
        if doc['type'] == 'pdf':
            st.image(doc['preview_image'])
        else:
            st.code(doc['original_text'], language=doc.get('language', 'text'))
    
    with col2:
        st.markdown("#### Parsed")
        st.markdown(doc['parsed_text'])
        
        # Show extracted metadata
        with st.expander("ℹ️ Metadata"):
            st.json(doc['metadata'])
```

#### **Preview Images, Tables, Code**
```python
# Image preview
if doc['images']:
    st.subheader("🖼️ Extracted Images")
    cols = st.columns(3)
    for i, img in enumerate(doc['images']):
        with cols[i % 3]:
            st.image(img['path'], caption=img['caption'])

# Table preview
if doc['tables']:
    st.subheader("📊 Extracted Tables")
    for i, table in enumerate(doc['tables']):
        st.caption(f"Table {i+1}: {table['caption']}")
        st.dataframe(table['data'])

# Code preview
if doc['code_snippets']:
    st.subheader("💻 Code Snippets")
    for i, snippet in enumerate(doc['code_snippets']):
        st.caption(f"Code {i+1} ({snippet['language']})")
        st.code(snippet['code'], language=snippet['language'])
```

#### **Edit Metadata**
```python
with st.form("edit_metadata"):
    st.subheader("✏️ Edit Metadata")
    
    new_title = st.text_input("Title", value=doc['title'])
    new_type = st.selectbox("Type", ["Lecture", "Tutorial", "Reading", "Example"], 
                            index=["Lecture", "Tutorial", "Reading", "Example"].index(doc['type']))
    new_difficulty = st.selectbox("Difficulty", ["Basic", "Intermediate", "Advanced"],
                                  index=["Basic", "Intermediate", "Advanced"].index(doc['difficulty']))
    new_tags = st.text_input("Tags (comma-separated)", value=", ".join(doc['tags']))
    
    submitted = st.form_submit_button("💾 Save Changes")
    if submitted:
        update_document_metadata(doc['id'], {
            'title': new_title,
            'type': new_type,
            'difficulty': new_difficulty,
            'tags': [t.strip() for t in new_tags.split(',')]
        })
        st.success("✅ Metadata updated!")
```

#### **Delete/Merge Documents**
```python
col1, col2 = st.columns(2)

with col1:
    if st.button("🗑️ Delete Document"):
        if st.checkbox(f"Confirm deletion of '{doc['title']}'"):
            delete_document(doc['id'])
            st.success("✅ Document deleted")

with col2:
    merge_with = st.selectbox("Merge with", ["None"] + [d['title'] for d in get_all_documents()])
    if st.button("🔀 Merge") and merge_with != "None":
        merge_documents(doc['id'], merge_with)
        st.success("✅ Documents merged")
```

---

## 3. Knowledge Graph Viewer

### Features

#### **Interactive Graph Visualization**
```python
import streamlit.components.v1 as components
from pyvis.network import Network

st.title("🕸️ Knowledge Graph")

# Create PyVis network
net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")

# Load knowledge graph
kg = load_knowledge_graph()

# Add nodes
for node in kg['nodes']:
    net.add_node(
        node['id'],
        label=node['label'],
        color=get_color_by_type(node['type']),
        size=node['importance'] * 20,
        title=f"Type: {node['type']}\nImportance: {node['importance']}"
    )

# Add edges
for edge in kg['edges']:
    net.add_edge(
        edge['source'],
        edge['target'],
        label=edge['type'],
        color=get_color_by_relationship(edge['type']),
        width=edge['confidence'] * 5
    )

# Render
net.show("kg.html")
components.html(open("kg.html").read(), height=600)
```

#### **Node Details on Hover**
```python
# PyVis automatically shows node titles on hover
# Custom info panel
if st.session_state.get('selected_node'):
    node = get_node(st.session_state.selected_node)
    
    with st.sidebar:
        st.subheader(f"📍 {node['label']}")
        st.write(f"**Type**: {node['type']}")
        st.write(f"**Importance**: {node['importance']:.2f}")
        
        st.markdown("**Related Documents**:")
        for doc_id in node['document_refs']:
            doc = get_document(doc_id)
            st.markdown(f"- [{doc['title']}]({doc['url']})")
        
        st.markdown("**Connections**:")
        for edge in get_edges(node['id']):
            st.markdown(f"- {edge['type']}: {edge['target_label']}")
```

#### **Filter by Type**
```python
st.sidebar.subheader("🎨 Display Options")

node_types = st.sidebar.multiselect(
    "Show Node Types",
    ["Concept", "Topic", "Entity", "Document"],
    default=["Concept", "Topic"]
)

edge_types = st.sidebar.multiselect(
    "Show Relationship Types",
    ["prerequisite", "example-of", "part-of", "related-to"],
    default=["prerequisite", "part-of"]
)

# Rebuild graph with filters
filtered_kg = filter_knowledge_graph(kg, node_types, edge_types)
render_graph(filtered_kg)
```

#### **Path Finding**
```python
st.sidebar.subheader("🛤️ Find Learning Path")

start_concept = st.sidebar.selectbox("From", get_all_concepts())
end_concept = st.sidebar.selectbox("To", get_all_concepts())

if st.sidebar.button("Find Path"):
    path = find_shortest_path(kg, start_concept, end_concept)
    
    st.success(f"Found learning path with {len(path)-1} steps:")
    for i, node in enumerate(path):
        st.write(f"{i+1}. {node['label']}")
    
    # Highlight path in graph
    highlight_path(net, path)
```

#### **Export Graph**
```python
st.sidebar.subheader("📥 Export")

export_format = st.sidebar.selectbox("Format", ["PNG", "JSON", "GEXF"])

if st.sidebar.button("Export Graph"):
    if export_format == "PNG":
        export_graph_image(kg)
        st.sidebar.download_button("Download PNG", data=open("kg.png", "rb"), file_name="knowledge_graph.png")
    elif export_format == "JSON":
        st.sidebar.download_button("Download JSON", data=json.dumps(kg), file_name="knowledge_graph.json")
    elif export_format == "GEXF":
        export_graph_gexf(kg)
        st.sidebar.download_button("Download GEXF", data=open("kg.gexf", "rb"), file_name="knowledge_graph.gexf")
```

---

## 4. Chat with Sources (NotebookLM Style)

### Features

#### **Chat Interface**
```python
st.title("💬 Chat with Your Course Materials")

st.markdown("Ask questions about your course materials and get answers with source citations.")

# Display chat history
for message in st.session_state.get('messages', []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources for assistant messages
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 View Sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source['title']}** (Page {source['page']})")
                    st.markdown(f"> {source['snippet']}")
                    if st.button(f"Open {source['title']}", key=f"open_{source['doc_id']}"):
                        open_document(source['doc_id'], source['page'])

# Chat input
if prompt := st.chat_input("Ask a question about your materials..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    with st.spinner("Searching materials and generating answer..."):
        response = generate_rag_response(prompt, st.session_state.messages)
    
    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response['answer'],
        "sources": response['sources']
    })
    
    st.rerun()
```

#### **Suggested Questions**
```python
if len(st.session_state.get('messages', [])) == 0:
    st.subheader("💡 Try asking:")
    
    suggestions = [
        "What are the main topics covered in this course?",
        "Explain backpropagation in simple terms",
        "What are the prerequisites for neural networks?",
        "Show me examples of linear regression code",
        "What's the difference between supervised and unsupervised learning?"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, key=f"suggest_{suggestion}"):
            # Auto-submit this question
            st.session_state.auto_question = suggestion
            st.rerun()
```

#### **Save Chat History**
```python
st.sidebar.subheader("💾 Chat History")

if st.sidebar.button("Save Conversation"):
    # Export as Markdown
    md_content = export_chat_to_markdown(st.session_state.messages)
    st.sidebar.download_button(
        "Download as Markdown",
        data=md_content,
        file_name="chat_history.md",
        mime="text/markdown"
    )

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
```

---

## 5. Organization Review Tab ⭐ (Human Review Required)

### Features

#### **View Proposed Curriculum Structure**
```python
st.title("📋 Organization Review")

st.info("👤 **Human Review Required**: Review the AI-proposed curriculum structure and approve or provide feedback.")

curriculum = load_proposed_curriculum()

st.markdown(f"""
**Curriculum**: {curriculum['name']}  
**Total Modules**: {curriculum['total_modules']}  
**Estimated Duration**: {curriculum['total_hours']} hours
""")

# Overview metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Documents", curriculum['total_documents'])
with col2:
    st.metric("Modules", curriculum['total_modules'])
with col3:
    st.metric("Basic", curriculum['tier_distribution']['Basic'])
with col4:
    st.metric("Advanced", curriculum['tier_distribution']['Advanced'])
```

#### **Tree View: Tracks → Modules → Courses → Lessons**
```python
import streamlit_tree_select as sts

# Build tree structure
tree = []
for track in curriculum['tracks']:
    track_node = {
        'label': f"🎯 {track['name']}",
        'value': track['track_id'],
        'children': []
    }
    
    for module_id in track['modules']:
        module = get_module(module_id)
        module_node = {
            'label': f"📦 Module {module['number']}: {module['name']}",
            'value': module['module_id'],
            'children': []
        }
        
        for content_type in ['lectures', 'tutorials', 'readings', 'assessments']:
            if module['contents'][content_type]:
                type_node = {
                    'label': f"📁 {content_type.title()} ({len(module['contents'][content_type])})",
                    'value': f"{module['module_id']}_{content_type}",
                    'children': [
                        {
                            'label': f"📄 {item}",
                            'value': item
                        }
                        for item in module['contents'][content_type]
                    ]
                }
                module_node['children'].append(type_node)
        
        track_node['children'].append(module_node)
    
    tree.append(track_node)

# Render tree
selected = sts.tree_select(tree, check_model='leaf')
```

#### **Drag-Drop Reorganization**
```python
# Note: Streamlit doesn't natively support drag-drop for complex structures
# Use streamlit-sortables or custom JavaScript component

from streamlit_sortables import sort_items

st.subheader("📦 Module Sequence")
st.caption("Drag to reorder modules")

module_items = [
    f"Module {m['number']}: {m['name']}"
    for m in curriculum['modules']
]

sorted_modules = sort_items(module_items)

if sorted_modules != module_items:
    st.success("✅ Module order updated!")
    update_module_sequence(sorted_modules)
```

#### **Edit Module Names/Descriptions**
```python
st.subheader("✏️ Edit Module")

selected_module = st.selectbox(
    "Select module to edit",
    [f"Module {m['number']}: {m['name']}" for m in curriculum['modules']]
)

if selected_module:
    module = get_module_by_name(selected_module)
    
    with st.form("edit_module"):
        new_name = st.text_input("Module Name", value=module['name'])
        new_description = st.text_area("Description", value=module['description'])
        new_duration = st.number_input("Duration (hours)", value=module['duration_hours'])
        
        if st.form_submit_button("💾 Save"):
            update_module(module['module_id'], {
                'name': new_name,
                'description': new_description,
                'duration_hours': new_duration
            })
            st.success("✅ Module updated!")
```

#### **View Categorization Rationale**
```python
with st.expander("🤔 Why did the AI group these materials?"):
    rationale = get_categorization_rationale(module['module_id'])
    
    st.markdown(f"**Rationale**: {rationale['explanation']}")
    
    st.markdown("**Grouping Factors**:")
    for factor in rationale['factors']:
        st.markdown(f"- {factor['name']}: {factor['value']:.2f}")
    
    st.markdown("**Shared Concepts**:")
    st.write(", ".join(rationale['shared_concepts']))
```

#### **Approve/Reject Organization**
```python
st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Approve Organization", type="primary", use_container_width=True):
        approve_curriculum(curriculum['curriculum_id'])
        st.success("🎉 Curriculum approved! Proceeding to enhancement phase...")
        st.balloons()

with col2:
    if st.button("❌ Reject & Provide Feedback", type="secondary", use_container_width=True):
        st.session_state.show_feedback_form = True
```

#### **Provide Feedback for Re-organization**
```python
if st.session_state.get('show_feedback_form', False):
    st.subheader("📝 Feedback for Re-organization")
    
    with st.form("feedback"):
        feedback = st.text_area(
            "What would you like to change?",
            placeholder="Example: Module 3 should come before Module 2 because..."
        )
        
        specific_changes = st.multiselect(
            "Specific issues:",
            ["Module sequence wrong", "Module names unclear", "Missing content", 
             "Duplicated content", "Difficulty progression too steep", "Other"]
        )
        
        if st.form_submit_button("🔄 Request Re-organization"):
            request_reorganization(curriculum['curriculum_id'], {
                'feedback': feedback,
                'issues': specific_changes
            })
            st.info("🔄 Re-organizing with your feedback... This may take a few minutes.")
```

---

## 6. Study Guide Viewer

### Features

```python
st.title("📖 Study Guides")

module = st.selectbox("Select module", get_all_modules())

if module:
    study_guide = load_study_guide(module['module_id'])
    
    # Display study guide (Markdown rendered)
    st.markdown(study_guide['content'])
    
    # Edit/enhance section
    if st.button("✏️ Edit Study Guide"):
        edited_content = st.text_area(
            "Edit content",
            value=study_guide['content'],
            height=400
        )
        if st.button("💾 Save"):
            save_study_guide(module['module_id'], edited_content)
            st.success("✅ Study guide updated!")
    
    # Flashcards viewer
    st.subheader("🗃️ Flashcards")
    flashcards = load_flashcards(module['module_id'])
    
    if flashcards:
        card_idx = st.slider("Card", 1, len(flashcards), 1)
        card = flashcards[card_idx - 1]
        
        # Flip card interface
        if st.session_state.get(f'show_answer_{card_idx}', False):
            st.info(f"**Answer**: {card['back']}")
            if st.button("🔄 Flip to Question"):
                st.session_state[f'show_answer_{card_idx}'] = False
                st.rerun()
        else:
            st.success(f"**Question**: {card['front']}")
            if st.button("🔄 Flip to Answer"):
                st.session_state[f'show_answer_{card_idx}'] = True
                st.rerun()
```

---

## 7. Gap Analysis Dashboard

### Features

```python
st.title("⚠️ Gap Analysis")

gap_report = load_gap_analysis()

# Severity breakdown
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Critical Gaps", gap_report['severity_breakdown']['critical'], delta_color="inverse")
with col2:
    st.metric("Warnings", gap_report['severity_breakdown']['warning'])
with col3:
    st.metric("Info", gap_report['severity_breakdown']['info'])

# Missing concepts
st.subheader("🔴 Missing Concepts")
for gap in gap_report['missing_concepts']:
    with st.expander(f"{gap['concept']} ({gap['severity'].upper()})"):
        st.write(gap['reason'])
        st.info(f"**Suggested Action**: {gap['suggested_action']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Will Address", key=f"address_{gap['concept']}"):
                mark_gap(gap['concept'], 'will_address')
        with col2:
            if st.button("✔️ Acceptable", key=f"accept_{gap['concept']}"):
                mark_gap(gap['concept'], 'acceptable')
```

---

## 8. Export Settings

### Features

```python
st.title("📦 Export")

st.subheader("📋 Export Options")

# Select what to export
export_structure = st.checkbox("Curriculum Structure", value=True)
export_enhancements = st.checkbox("Study Guides & Flashcards", value=True)
export_rag = st.checkbox("RAG Knowledge Base", value=True)
export_original = st.checkbox("Original Files", value=False)

# Set metadata
st.subheader("ℹ️ Metadata")
course_name = st.text_input("Course Name", value="Machine Learning Fundamentals")
author = st.text_input("Author", value="Dr. Jane Doe")
version = st.text_input("Version", value="1.0")

# Preview export structure
if st.button("👁️ Preview Export"):
    structure = generate_export_preview(
        export_structure, export_enhancements, export_rag, export_original
    )
    st.code(structure, language="")

# Export buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📤 Export to CourseTransformer", type="primary", use_container_width=True):
        export_to_transformer(course_name, author, version)
        st.success("✅ Exported to CourseTransformer!")

with col2:
    if st.button("💾 Download ZIP Backup", use_container_width=True):
        zip_data = create_backup_zip()
        st.download_button(
            "Download ZIP",
            data=zip_data,
            file_name=f"{course_name}_backup.zip",
            mime="application/zip"
        )
```

---

## UI/UX Enhancements

### Custom Styling
```python
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        border-radius: 8px;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)
```

### Loading Indicators
```python
with st.spinner("Processing..."):
    time.sleep(2)  # Long operation
st.success("Done!")
```

### Tooltips & Help Text
```python
st.text_input(
    "Learning Rate",
    value=0.01,
    help="Controls the step size during optimization. Typical values: 0.001 - 0.1"
)
```

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Design Specification (Not Implemented)
