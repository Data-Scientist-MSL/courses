# CourseIngester - Organization Agents

## Overview

Organization agents take deeply understood content and structure it into a logical, pedagogically sound curriculum. These agents categorize materials, design curriculum architecture, detect duplicates, and optimize learning sequences.

**Design Philosophy**: Organization follows understanding. Only after comprehending content semantically can we structure it effectively for learning.

---

## 1️⃣ Content Categorizer Agent

### Purpose
Group materials by topic, type, difficulty, and other dimensions to create an organized content library.

### Capabilities

#### **Topic-Based Categorization**
- **Method**: Multi-label classification based on content analysis
- **Sources**:
  - Extracted concepts (from Semantic Analysis Agent)
  - Topics (from Topic Modeling)
  - Document intent (Lecture, Tutorial, etc.)
- **Categories**: Hierarchical taxonomy
  ```
  Machine Learning
  ├── Supervised Learning
  │   ├── Regression
  │   ├── Classification
  │   └── Ensemble Methods
  ├── Unsupervised Learning
  │   ├── Clustering
  │   └── Dimensionality Reduction
  └── Deep Learning
      ├── Neural Networks
      ├── CNN
      └── RNN
  ```
- **LLM Prompt**:
  ```
  Categorize this content into one or more topics from the taxonomy:
  
  Content: {summary}
  
  Taxonomy: {taxonomy_tree}
  
  Primary Category:
  Secondary Categories:
  Justification:
  ```

#### **Type Classification**
- **Content Types**:
  - **Lecture**: Theoretical explanation, foundational concepts
  - **Lab/Tutorial**: Hands-on, step-by-step practical exercise
  - **Reading**: Supplementary text, articles, documentation
  - **Reference**: Quick lookup, cheat sheets, API docs
  - **Example**: Code samples, case studies, worked examples
  - **Exercise**: Practice problems, assignments (without solutions)
  - **Solution**: Answer keys, solution walkthroughs
  - **Assessment**: Quizzes, exams, graded assignments
  - **Video**: Recorded lectures, demonstrations
  - **Interactive**: Jupyter notebooks, interactive demos
- **Method**: Rule-based + LLM classification
- **Rules**:
  - Contains code + step-by-step instructions → Tutorial
  - Video file + transcript → Video Lecture
  - Many problems + answers → Assessment
- **LLM Fallback**: For ambiguous cases

#### **Auto-Tagging**
- **Tag Types**:
  - **Skill Tags**: "data-analysis", "visualization", "model-training"
  - **Tool Tags**: "Python", "TensorFlow", "Pandas", "R"
  - **Format Tags**: "code", "slides", "video", "text"
  - **Audience Tags**: "beginner", "intermediate", "advanced"
  - **Learning Outcome Tags**: "understand-concepts", "apply-techniques", "evaluate-models"
- **Tag Sources**:
  - Extracted entities (technologies, tools)
  - Difficulty tier (from Difficulty Assessor)
  - File type (from Parser)
  - Bloom's taxonomy level (from Question Generator)
- **Tag Cloud**: Generate tag frequency visualization

#### **Folder Organization**
- **Strategy**: Hybrid hierarchical + flat structure
- **Top-Level Organization**: By Track or Module
- **Mid-Level**: By Topic
- **Low-Level**: By Type
- **Example Structure**:
  ```
  ML_Course/
  ├── 01_Foundations/
  │   ├── lectures/
  │   │   ├── 01_intro_to_ml.pdf
  │   │   └── 02_supervised_learning.pdf
  │   ├── labs/
  │   │   └── lab_01_linear_regression.ipynb
  │   ├── readings/
  │   └── assessments/
  ├── 02_Advanced_Topics/
  └── resources/
      ├── references/
      └── datasets/
  ```
- **Naming Convention**: `##_descriptive_name.ext` (numbered for sequence)

### LLM Usage (OLLAMA)

#### **Model Selection**
- **Categorization**: llama3.2:1b (lightweight, fast classification)
- **Rationale Generation**: llama3.2:3b (explain categorization decisions)

#### **Prompt Template**
```python
CATEGORIZATION_PROMPT = """
You are an educational content organizer. Categorize this material.

Content Summary: {summary}
Content Type: {file_type}
Key Concepts: {concepts}

Assign:
1. Primary Topic (choose one from taxonomy)
2. Secondary Topics (choose 0-3)
3. Content Type (Lecture/Tutorial/Reading/Reference/Example/Exercise/Assessment)
4. Difficulty (Basic/Intermediate/Advanced)
5. Tags (3-5 relevant tags)
6. Suggested Folder Path

Taxonomy: {taxonomy}

Output format:
Primary Topic: 
Secondary Topics:
Content Type:
Difficulty:
Tags:
Folder Path:
Rationale:
"""
```

### Outputs

**Categorization Result**:
```python
{
    "document_id": "neural_networks_intro.pdf",
    "categorization": {
        "primary_topic": "Deep Learning > Neural Networks",
        "secondary_topics": [
            "Supervised Learning",
            "Optimization"
        ],
        "content_type": "Lecture",
        "difficulty": "Intermediate",
        "tier": "Intermediate",
        
        "tags": [
            "neural-networks",
            "backpropagation",
            "deep-learning",
            "python",
            "tensorflow",
            "theory"
        ],
        
        "folder_path": "02_Deep_Learning/lectures/",
        "suggested_filename": "01_neural_networks_intro.pdf",
        
        "rationale": "This is a lecture covering theoretical foundations of neural networks. It includes mathematical explanations of backpropagation and requires understanding of calculus and linear algebra (intermediate level). Primary focus is deep learning with secondary focus on supervised learning and optimization techniques.",
        
        "confidence": 0.92
    },
    
    "metadata": {
        "categorized_at": "2024-01-15T10:30:00Z",
        "categorizer_version": "1.0",
        "llm_model": "llama3.2:1b"
    }
}
```

### Tools & Libraries
- **OLLAMA**: LLM for intelligent categorization
- **scikit-learn**: Multi-label classification (if using ML approach)
- **pathlib**: File path manipulation

### Configuration
```yaml
content_categorizer:
  llm_model: "llama3.2:1b"
  taxonomy_path: "config/content_taxonomy.yaml"
  enable_auto_tagging: true
  max_tags_per_document: 5
  min_confidence: 0.7
  folder_naming_convention: "numbered"  # or "descriptive"
```

---

## 2️⃣ Curriculum Architect Agent

### Purpose
Design a coherent curriculum structure from ingested materials, creating modules, tracks, and learning paths based on pedagogical principles.

### Capabilities

#### **Module Design**
- **Definition**: A module is a cohesive unit covering a specific topic or skill
- **Components**:
  - **Learning Objectives**: What learners will achieve
  - **Content**: Lectures, readings, examples
  - **Activities**: Labs, exercises
  - **Assessments**: Quizzes, assignments
  - **Duration**: Estimated time to complete
- **Grouping Strategy**:
  1. Start with topic categories (from Categorizer)
  2. Group related content by concept similarity
  3. Ensure each module has balanced content (theory + practice)
  4. Aim for 4-8 modules per course (optimal cognitive chunking)
- **LLM Prompt**:
  ```
  Design modules from these materials:
  
  Materials: {material_summaries}
  Topics: {topics}
  
  Create 5-7 cohesive modules. For each module:
  - Module name
  - Learning objectives (3-5)
  - Contents (list of materials)
  - Estimated duration (hours)
  - Prerequisites (from other modules)
  ```

#### **Learning Path Creation**
- **Definition**: Suggested sequence for learners to follow
- **Paths**:
  - **Linear Path**: Sequential, prerequisite-driven
  - **Branching Paths**: Multiple routes (e.g., theory-heavy vs. practice-heavy)
  - **Self-Directed Path**: Learner chooses based on interests
- **Path Design Factors**:
  - Prerequisites (from Knowledge Graph)
  - Difficulty progression (gradual increase)
  - Concept scaffolding (build on previous knowledge)
  - Learning goals (certification, job role, project completion)
- **Example**:
  ```
  Linear Path (Beginner):
  Module 1: Python Basics → 
  Module 2: Data Structures → 
  Module 3: Pandas & NumPy →
  Module 4: Data Visualization →
  Module 5: Machine Learning Intro
  
  Fast-Track Path (Experienced Programmers):
  Module 1: Python Basics (optional review) →
  Module 3: Pandas & NumPy →
  Module 5: Machine Learning Intro →
  Module 6: Advanced ML
  ```

#### **Track Building**
- **Definition**: A track is a thematic grouping of modules (like a major)
- **Track Types**:
  - **Role-Based**: Data Analyst Track, ML Engineer Track, Data Scientist Track
  - **Technology-Based**: Python Track, R Track, Cloud ML Track
  - **Application-Based**: Computer Vision Track, NLP Track, Time Series Track
- **Track Structure**:
  - Core modules (required for all tracks)
  - Track-specific modules
  - Elective modules
- **Example**:
  ```
  Data Scientist Track:
  Core (Required):
    - Python Fundamentals
    - Statistics Basics
    - Machine Learning Foundations
  
  Track-Specific:
    - Advanced Statistics
    - Deep Learning
    - ML Deployment
  
  Electives (Choose 2):
    - Natural Language Processing
    - Computer Vision
    - Time Series Analysis
  ```

#### **Tier Distribution**
- **Tiers**: Basic, Intermediate, Advanced
- **Distribution Strategy**:
  - **Pyramid**: Many basic, fewer intermediate, few advanced
  - **Even**: Equal distribution across tiers
  - **Inverted**: Advanced-focused (for experienced learners)
- **Assignment**:
  - Based on difficulty scores (from Difficulty Assessor)
  - Based on prerequisite count
  - Manual override allowed
- **Recommended Distribution** (Pyramid):
  - Basic: 40%
  - Intermediate: 35%
  - Advanced: 25%

### LLM Usage (OLLAMA)

#### **Model Selection**
- **Curriculum Design**: llama3.1:8b (complex reasoning, pedagogical knowledge)
- **Learning Objectives**: llama3.2:3b (structured generation)

#### **Pedagogical Prompting**
```python
CURRICULUM_DESIGN_PROMPT = """
You are an expert instructional designer. Design a curriculum from these materials.

Materials Summary:
{materials}

Topics Covered:
{topics}

Concept Relationships:
{knowledge_graph_summary}

Design a curriculum with:
1. 5-7 cohesive modules
2. Clear learning progression (prerequisites)
3. Balanced theory and practice
4. Estimated time commitments
5. Learning objectives for each module

For each module, specify:
- Module Number and Name
- Learning Objectives (3-5, using Bloom's taxonomy verbs)
- Contents (which materials belong here)
- Prerequisites (which modules must be completed first)
- Estimated Duration (hours)
- Tier (Basic/Intermediate/Advanced)

Format as structured output.
"""

LEARNING_OBJECTIVES_PROMPT = """
Generate 3-5 learning objectives for this module.

Module Topic: {module_name}
Module Contents: {content_summary}

Use Bloom's taxonomy verbs (understand, apply, analyze, evaluate, create).
Format: "Upon completion, learners will be able to [verb] [outcome]."

Learning Objectives:
1.
2.
3.
"""
```

### Outputs

**Curriculum Structure**:
```python
{
    "curriculum_id": "ml_fundamentals_v1",
    "created_at": "2024-01-15",
    "total_modules": 6,
    
    "tracks": [
        {
            "track_id": "data_scientist",
            "name": "Data Scientist Track",
            "description": "Comprehensive track covering statistics, ML, and deployment",
            "duration_hours": 120,
            "difficulty": "Intermediate to Advanced",
            "modules": ["mod_1", "mod_2", "mod_3", "mod_4", "mod_5", "mod_6"]
        }
    ],
    
    "modules": [
        {
            "module_id": "mod_1",
            "number": 1,
            "name": "Python Fundamentals",
            "description": "Introduction to Python programming for data science",
            "tier": "Basic",
            
            "learning_objectives": [
                "Understand Python syntax and data types",
                "Apply control flow and functions to solve problems",
                "Create Python scripts for data manipulation",
                "Analyze errors and debug Python code"
            ],
            
            "contents": {
                "lectures": ["python_intro.pdf", "functions_lecture.pdf"],
                "tutorials": ["python_basics_lab.ipynb", "data_types_tutorial.md"],
                "readings": ["python_style_guide.pdf"],
                "assessments": ["python_quiz_1.md"]
            },
            
            "prerequisites": [],
            "duration_hours": 15,
            "estimated_difficulty": 3.2,
            
            "sequence_in_track": 1
        },
        
        {
            "module_id": "mod_2",
            "number": 2,
            "name": "Data Analysis with Pandas",
            "description": "Learn to manipulate and analyze data using Pandas library",
            "tier": "Intermediate",
            
            "learning_objectives": [
                "Understand Pandas DataFrame structure and operations",
                "Apply data cleaning and transformation techniques",
                "Analyze datasets to extract insights",
                "Visualize data using Pandas plotting capabilities"
            ],
            
            "contents": {
                "lectures": ["pandas_intro.pdf", "data_cleaning.pdf"],
                "tutorials": ["pandas_lab_1.ipynb", "data_analysis_tutorial.ipynb"],
                "readings": ["pandas_best_practices.md"],
                "assessments": ["pandas_assignment.ipynb"]
            },
            
            "prerequisites": ["mod_1"],
            "duration_hours": 20,
            "estimated_difficulty": 5.5,
            
            "sequence_in_track": 2
        }
        
        // ... more modules
    ],
    
    "learning_paths": [
        {
            "path_id": "linear_beginner",
            "name": "Linear Path (Beginner-Friendly)",
            "description": "Sequential learning with gradual difficulty increase",
            "module_sequence": ["mod_1", "mod_2", "mod_3", "mod_4", "mod_5", "mod_6"],
            "estimated_duration_hours": 120,
            "target_audience": "Beginners with no prior programming experience"
        },
        {
            "path_id": "fast_track",
            "name": "Fast Track (Experienced Programmers)",
            "description": "Accelerated path skipping basics",
            "module_sequence": ["mod_1_optional", "mod_3", "mod_4", "mod_5", "mod_6"],
            "estimated_duration_hours": 80,
            "target_audience": "Learners with Python programming experience"
        }
    ],
    
    "tier_distribution": {
        "Basic": {"count": 2, "percentage": 33},
        "Intermediate": {"count": 3, "percentage": 50},
        "Advanced": {"count": 1, "percentage": 17}
    },
    
    "metadata": {
        "total_materials": 45,
        "total_duration_hours": 120,
        "pedagogical_approach": "Constructivist, practice-based",
        "design_rationale": "Curriculum designed with gradual progression from basic Python to advanced ML concepts. Each module builds on previous knowledge with balanced theory and hands-on practice."
    }
}
```

### Tools & Libraries
- **OLLAMA**: LLM for curriculum design
- **NetworkX**: Analyze prerequisite dependencies
- **pandas**: Organize and analyze material metadata

### Configuration
```yaml
curriculum_architect:
  llm_model: "llama3.1:8b"
  target_modules: 6
  tier_distribution: [0.4, 0.35, 0.25]  # Basic, Intermediate, Advanced
  module_duration_hours: [10, 30]  # Min, max
  enable_multiple_paths: true
  use_bloom_taxonomy: true
```

---

## 3️⃣ Duplicate Detector Agent

### Purpose
Identify redundant or overlapping content to avoid repetition and enable merging or selective inclusion.

### Capabilities

#### **Semantic Similarity Calculation**
- **Method**: Compare document embeddings using cosine similarity
- **Process**:
  1. Generate embeddings for each document (via sentence-transformers)
  2. Compute pairwise cosine similarity
  3. Flag pairs with similarity > threshold (e.g., 0.85)
- **Granularity Levels**:
  - **Document-level**: Entire documents compared
  - **Section-level**: Individual sections compared
  - **Paragraph-level**: Fine-grained comparison
- **Similarity Threshold**:
  - 0.95-1.0: Near-identical (likely duplicates)
  - 0.85-0.95: Very similar (check manually)
  - 0.70-0.85: Related but distinct

#### **Duplicate Detection**
- **Exact Duplicates**:
  - Same file hash (MD5, SHA-256)
  - Same content, different filename
- **Near Duplicates**:
  - Minor edits (typo fixes, reformatting)
  - Same content, different format (PDF vs. DOCX of same lecture)
  - Similarity > 0.95
- **Partial Duplicates**:
  - Same section appears in multiple documents
  - Overlapping content (e.g., introduction repeated)
  - Similarity 0.85-0.95

#### **Version Identification**
- **Version Indicators**:
  - Filenames: `lecture_v1.pdf`, `lecture_v2.pdf`
  - Metadata: Modification dates
  - Content: "Revised version", "Updated 2024"
- **Version Comparison**:
  - Identify which version is latest
  - Highlight changes between versions (diff)
  - Recommend keeping latest, archiving old
- **Tools**: difflib for text comparison

#### **Merge Suggestions**
- **Criteria for Merging**:
  - Content overlap > 80%
  - One document is subset of another
  - Complementary content (merge adds value)
- **Merge Strategies**:
  - **Keep Best**: Choose higher quality version
  - **Combine**: Merge unique content from both
  - **Keep Both**: If different perspectives/approaches
- **LLM Analysis**:
  ```
  Compare these two documents:
  
  Document A: {summary_a}
  Document B: {summary_b}
  Similarity: {similarity_score}
  
  Recommendation:
  - Are they duplicates? (Yes/No)
  - Should they be merged? (Yes/No)
  - If merged, which to keep or how to combine?
  ```

### Outputs

**Duplicate Detection Report**:
```python
{
    "detection_date": "2024-01-15",
    "total_documents": 45,
    "duplicates_found": 8,
    
    "exact_duplicates": [
        {
            "group_id": "dup_1",
            "documents": [
                {"id": "doc_12", "filename": "intro_ml.pdf", "hash": "abc123"},
                {"id": "doc_28", "filename": "ml_introduction.pdf", "hash": "abc123"}
            ],
            "similarity": 1.0,
            "recommendation": "Keep doc_12 (original upload), delete doc_28",
            "action": "delete_duplicate"
        }
    ],
    
    "near_duplicates": [
        {
            "group_id": "dup_2",
            "documents": [
                {"id": "doc_5", "filename": "linear_regression.pdf"},
                {"id": "doc_18", "filename": "regression_updated.pdf"}
            ],
            "similarity": 0.92,
            "differences": "doc_18 has additional examples on page 8-10",
            "recommendation": "Keep doc_18 (newer, more complete), archive doc_5",
            "action": "keep_newer",
            "rationale": "doc_18 appears to be an updated version with added examples"
        }
    ],
    
    "partial_duplicates": [
        {
            "group_id": "dup_3",
            "documents": [
                {"id": "doc_3", "filename": "ml_overview.pdf"},
                {"id": "doc_7", "filename": "supervised_learning.pdf"}
            ],
            "similarity": 0.78,
            "overlap": "Introduction section (pages 1-3) is identical",
            "recommendation": "Keep both (different focus), note overlap",
            "action": "keep_both_note_overlap"
        }
    ],
    
    "version_groups": [
        {
            "group_id": "ver_1",
            "base_name": "python_tutorial",
            "versions": [
                {"id": "doc_10", "filename": "python_tutorial_v1.pdf", "date": "2023-05-10"},
                {"id": "doc_15", "filename": "python_tutorial_v2.pdf", "date": "2023-08-22"},
                {"id": "doc_22", "filename": "python_tutorial_v3.pdf", "date": "2024-01-05"}
            ],
            "recommendation": "Keep v3 (latest), archive v1 and v2",
            "changes": {
                "v1_to_v2": "Added section on list comprehensions",
                "v2_to_v3": "Updated for Python 3.12, added type hints examples"
            }
        }
    ],
    
    "merge_suggestions": [
        {
            "merge_id": "merge_1",
            "documents": [
                {"id": "doc_8", "filename": "pandas_basics.md"},
                {"id": "doc_14", "filename": "pandas_advanced.md"}
            ],
            "similarity": 0.65,
            "recommendation": "Do not merge - distinct topics (basics vs. advanced)",
            "action": "keep_separate"
        }
    ],
    
    "summary": {
        "total_duplicates": 8,
        "exact": 2,
        "near": 3,
        "partial": 3,
        "space_saved_mb": 45.3,  # If duplicates removed
        "action_breakdown": {
            "delete": 2,
            "archive": 4,
            "keep_both": 2
        }
    }
}
```

### Tools & Libraries
- **sentence-transformers**: Document embeddings
- **scikit-learn**: Cosine similarity
- **hashlib**: File hashing (MD5, SHA-256)
- **difflib**: Text comparison for versions
- **OLLAMA**: LLM for merge recommendations

### Configuration
```yaml
duplicate_detector:
  similarity_threshold: 0.85
  exact_duplicate_action: "auto_delete"  # or "flag_for_review"
  near_duplicate_action: "flag_for_review"
  version_detection: true
  compute_diff: true
  embedding_model: "all-MiniLM-L6-v2"
```

---

## 4️⃣ Sequence Optimizer Agent

### Purpose
Determine the optimal learning sequence based on prerequisites, difficulty progression, and pedagogical principles.

### Capabilities

#### **Topological Sort by Prerequisites**
- **Method**: Directed Acyclic Graph (DAG) topological sort
- **Process**:
  1. Build prerequisite graph (from Knowledge Graph)
  2. Verify no cycles (circular dependencies)
  3. Perform topological sort
  4. Generate valid learning sequences
- **Algorithm**: Kahn's algorithm or DFS-based topological sort
- **Tool**: NetworkX (`nx.topological_sort()`)
- **Example**:
  ```
  Graph: A → B → D
         A → C → D
  
  Valid Sequences:
  - A, B, C, D
  - A, C, B, D
  ```
- **Constraint**: All prerequisites must appear before dependent concepts

#### **Difficulty Progression**
- **Principle**: Gradual difficulty increase (scaffolding)
- **Method**:
  1. Assign difficulty scores (from Difficulty Assessor)
  2. Sort by difficulty (ascending)
  3. Adjust for prerequisite constraints
  4. Smooth progression (avoid sudden jumps)
- **Ideal Curve**: Exponential or logarithmic increase
- **Detection of Jumps**:
  ```python
  if difficulty[i+1] - difficulty[i] > threshold:
      flag_as_steep_jump()
  ```
- **Mitigation**: Insert intermediary content or flag for human review

#### **Pacing Estimation**
- **Learning Time Estimation**:
  - Based on content length (pages, words, video duration)
  - Adjusted by difficulty (harder content takes longer)
  - Adjusted by type (labs take longer than lectures)
- **Formula**:
  ```
  time = base_time * difficulty_multiplier * type_multiplier
  
  Example:
  20-page lecture, difficulty 7/10, type=lecture
  time = 20 pages * 3 min/page * 1.4 (difficulty) * 1.0 (lecture) = 84 min
  ```
- **Pacing Goals**:
  - Even distribution (each week similar time commitment)
  - Build-up (start slow, increase later)
  - Custom (user-defined)

#### **Alternate Path Generation**
- **Rationale**: Different learners have different preferences
- **Path Types**:
  - **Theory-First**: Lectures → Examples → Labs → Assessments
  - **Practice-First**: Examples → Labs → Lectures → Assessments
  - **Interleaved**: Lecture → Example → Lab → Lecture → Example → Lab
  - **Self-Paced**: Learner chooses order (with prerequisites enforced)
- **Learning Styles**:
  - **Visual Learners**: Prioritize videos, diagrams
  - **Hands-On Learners**: Prioritize labs, exercises
  - **Readers**: Prioritize text, documentation
- **Generation Method**: 
  - Maintain prerequisite constraints
  - Reorder non-dependent content by preference

### Outputs

**Optimized Sequence**:
```python
{
    "sequence_id": "optimal_linear_v1",
    "optimization_date": "2024-01-15",
    
    "primary_sequence": [
        {
            "position": 1,
            "module_id": "mod_1",
            "module_name": "Python Fundamentals",
            "difficulty": 3.2,
            "estimated_hours": 15,
            "week": 1,
            "prerequisites": [],
            "rationale": "Foundation for all subsequent modules"
        },
        {
            "position": 2,
            "module_id": "mod_2",
            "module_name": "Data Structures",
            "difficulty": 4.5,
            "estimated_hours": 18,
            "week": 2,
            "prerequisites": ["mod_1"],
            "rationale": "Builds on Python basics, required for data analysis"
        },
        {
            "position": 3,
            "module_id": "mod_3",
            "module_name": "Pandas for Data Analysis",
            "difficulty": 5.8,
            "estimated_hours": 20,
            "week": 3-4,
            "prerequisites": ["mod_1", "mod_2"],
            "rationale": "Practical application of Python and data structures"
        }
        // ... more modules
    ],
    
    "difficulty_progression": {
        "start_difficulty": 3.2,
        "end_difficulty": 8.5,
        "average_increase_per_module": 0.88,
        "steep_jumps": [
            {
                "from_module": "mod_4",
                "to_module": "mod_5",
                "jump": 2.3,
                "warning": "Significant difficulty increase, consider intermediary content"
            }
        ],
        "progression_quality": "Good"
    },
    
    "pacing": {
        "total_duration_hours": 120,
        "total_weeks": 12,
        "avg_hours_per_week": 10,
        "week_breakdown": [
            {"week": 1, "modules": ["mod_1"], "hours": 15},
            {"week": 2, "modules": ["mod_2"], "hours": 18},
            {"week": 3-4, "modules": ["mod_3"], "hours": 20}
            // ...
        ],
        "pacing_style": "Even"
    },
    
    "alternate_paths": [
        {
            "path_id": "theory_first",
            "name": "Theory-First Path",
            "description": "Lectures before labs for each topic",
            "sequence": [
                {"position": 1, "type": "lecture", "id": "lec_1"},
                {"position": 2, "type": "lecture", "id": "lec_2"},
                {"position": 3, "type": "lab", "id": "lab_1"},
                {"position": 4, "type": "lecture", "id": "lec_3"},
                {"position": 5, "type": "lab", "id": "lab_2"}
            ],
            "target_learners": "Visual learners, those preferring conceptual understanding first"
        },
        {
            "path_id": "practice_first",
            "name": "Practice-First Path",
            "description": "Labs before lectures for experiential learning",
            "sequence": [
                {"position": 1, "type": "lab", "id": "lab_1"},
                {"position": 2, "type": "lecture", "id": "lec_1"},
                {"position": 3, "type": "lab", "id": "lab_2"},
                {"position": 4, "type": "lecture", "id": "lec_2"}
            ],
            "target_learners": "Hands-on learners, experienced programmers"
        }
    ],
    
    "prerequisite_graph": {
        "nodes": ["mod_1", "mod_2", "mod_3", "mod_4", "mod_5"],
        "edges": [
            {"from": "mod_1", "to": "mod_2"},
            {"from": "mod_1", "to": "mod_3"},
            {"from": "mod_2", "to": "mod_3"},
            {"from": "mod_3", "to": "mod_4"},
            {"from": "mod_3", "to": "mod_5"}
        ],
        "critical_path": ["mod_1", "mod_2", "mod_3", "mod_5"],
        "parallel_options": [
            {"concurrent": ["mod_4", "mod_5"], "after": "mod_3"}
        ]
    },
    
    "validation": {
        "prerequisites_satisfied": true,
        "no_circular_dependencies": true,
        "difficulty_progression_smooth": false,
        "warnings": [
            "Steep difficulty jump between mod_4 and mod_5"
        ]
    }
}
```

### Tools & Libraries
- **NetworkX**: Topological sort, graph analysis
- **numpy**: Numerical operations for pacing calculations
- **matplotlib**: Visualize difficulty progression

### Configuration
```yaml
sequence_optimizer:
  optimization_method: "topological_sort"
  difficulty_jump_threshold: 1.5
  pacing_style: "even"  # even, buildup, custom
  target_hours_per_week: 10
  enable_alternate_paths: true
  smooth_difficulty_curve: true
```

---

## Organization Workflow

### Pipeline
```
Parse & Understand → Categorize → Design Curriculum → Detect Duplicates → 
Optimize Sequence → Human Review → Export Structure
```

### Human-in-Loop Integration
- **Review Point**: After Curriculum Architect proposes structure
- **Human Actions**:
  - Approve, reject, or edit proposed modules
  - Drag-drop reorganize content
  - Override categorization
  - Provide feedback for re-organization
- **Feedback Loop**: If rejected, agents re-organize with human feedback

### State Management
```python
class OrganizationState:
    categorized_content: Dict[str, Category]
    proposed_curriculum: CurriculumStructure
    duplicates: DuplicateReport
    optimized_sequence: Sequence
    human_approved: bool
    human_feedback: str
```

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Design Specification (Not Implemented)
