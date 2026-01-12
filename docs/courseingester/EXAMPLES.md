# CourseIngester - Example Use Cases

## Overview

This document provides detailed walkthroughs of four realistic use cases demonstrating how CourseIngester handles different types of educational content ingestion scenarios.

---

## Example 1: Ingest Legacy Course from ZIP

### Scenario
An instructor has a legacy R-based statistics course stored in a ZIP archive containing PDFs, R scripts, datasets, and video lectures. They want to modernize it and make it more accessible to students.

### Input Materials
```
statistics_course_legacy.zip (850 MB)
├── lectures/
│   ├── week1_intro_to_r.pdf (12 MB)
│   ├── week2_data_structures.pdf (8 MB)
│   ├── week3_statistical_tests.pdf (15 MB)
│   ├── week4_regression.pdf (20 MB)
│   └── week5_visualization.pdf (18 MB)
├── videos/
│   ├── lecture_01_introduction.mp4 (250 MB)
│   ├── lecture_02_data_types.mp4 (220 MB)
│   └── lecture_03_hypothesis_testing.mp4 (300 MB)
├── code/
│   ├── week1_basics.R
│   ├── week2_dataframes.R
│   ├── week3_tests.R
│   ├── week4_linear_regression.R
│   └── week5_ggplot.R
├── datasets/
│   ├── iris.csv
│   ├── mtcars.csv
│   └── diabetes.csv
└── syllabus.docx
```

### Workflow

#### **Step 1: Upload**
```python
# User uploads ZIP file via Streamlit UI
uploaded_file = "statistics_course_legacy.zip"
ingestion_mode = "standard"  # Full understanding, smart organization

# System initiates workflow
workflow_id = initiate_ingestion(uploaded_file, ingestion_mode)
```

#### **Step 2: Archive Extraction**
```
⏳ Processing... Extracting archive
✅ Extracted 45 files from archive
   - 5 PDF lectures
   - 3 MP4 videos
   - 5 R scripts
   - 3 CSV datasets
   - 1 DOCX syllabus
   - 28 miscellaneous files (images, data)
```

#### **Step 3: Parallel Parsing**
```
⏳ Parsing documents in parallel...

📄 PDF Parser (5 files):
  ✅ week1_intro_to_r.pdf → 45 pages, 12,000 words
  ✅ week2_data_structures.pdf → 32 pages, 8,500 words
  ✅ week3_statistical_tests.pdf → 58 pages, 15,000 words
  ✅ week4_regression.pdf → 72 pages, 18,000 words
  ✅ week5_visualization.pdf → 65 pages, 16,000 words

🎥 Video Parser (3 files):
  ⏳ Transcribing with Whisper...
  ✅ lecture_01_introduction.mp4 → 45 min, transcript with timestamps
  ✅ lecture_02_data_types.mp4 → 38 min, transcript + extracted slides (15 slides)
  ✅ lecture_03_hypothesis_testing.mp4 → 52 min, transcript + code snippets detected

💻 Code Parser (5 files):
  ✅ Parsed R scripts → functions, dependencies, comments extracted

📝 Document Parser (1 file):
  ✅ syllabus.docx → Course outline, grading policy, schedule
```

#### **Step 4: Semantic Analysis**
```
⏳ Analyzing content semantically...

Extracted Concepts (78 total):
  - R programming (importance: 0.95)
  - Statistical testing (importance: 0.92)
  - Linear regression (importance: 0.88)
  - Data visualization (importance: 0.85)
  - Hypothesis testing (importance: 0.87)
  - ggplot2 (importance: 0.78)
  - p-values (importance: 0.76)
  - ...

Identified Topics (5 main topics):
  1. R Programming Basics (25% of content)
  2. Descriptive Statistics (18%)
  3. Inferential Statistics (22%)
  4. Regression Analysis (20%)
  5. Data Visualization (15%)

Named Entities:
  - People: Ronald Fisher, Karl Pearson, John Tukey
  - Technologies: R, ggplot2, dplyr, tidyr
  - Datasets: Iris, mtcars, diamonds

Content Type Classification:
  - Lectures: 8 documents (PDFs + video transcripts)
  - Code Examples: 5 R scripts
  - Datasets: 3 CSV files
  - Reference: 1 syllabus
```

#### **Step 5: Knowledge Graph Construction**
```
⏳ Building knowledge graph...

✅ Created 145 nodes:
   - 78 Concepts
   - 45 Documents
   - 17 Examples
   - 5 Topics

✅ Created 312 edges:
   - 89 prerequisite relationships
   - 125 example-of relationships
   - 67 part-of relationships
   - 31 related-to relationships

Key Prerequisites Detected:
  - "R basics" → "data frames" → "data manipulation" → "visualization"
  - "descriptive statistics" → "inferential statistics" → "hypothesis testing"
  - "correlation" → "simple regression" → "multiple regression"
```

#### **Step 6: Organization**
```
⏳ Organizing into curriculum...

Proposed Structure:

📚 Course: Introduction to Statistics with R
   Duration: 60 hours

🎯 Track 1: Core Statistics Track (Recommended)
   
   📦 Module 1: R Programming Foundations (Basic)
      Duration: 12 hours
      Contents:
        - Lecture: week1_intro_to_r.pdf
        - Video: lecture_01_introduction.mp4
        - Lab: week1_basics.R
        - Dataset: iris.csv
      Learning Objectives:
        - Understand R syntax and data types
        - Create vectors, matrices, and data frames
        - Use basic R functions for data manipulation
   
   📦 Module 2: Data Structures and Manipulation (Basic)
      Duration: 10 hours
      Contents:
        - Lecture: week2_data_structures.pdf
        - Video: lecture_02_data_types.mp4
        - Lab: week2_dataframes.R
        - Dataset: mtcars.csv
      Prerequisites: Module 1
   
   📦 Module 3: Descriptive Statistics (Intermediate)
      Duration: 8 hours
      Contents:
        - Selected sections from week3_statistical_tests.pdf
      Prerequisites: Module 2
   
   📦 Module 4: Hypothesis Testing (Intermediate)
      Duration: 12 hours
      Contents:
        - Lecture: week3_statistical_tests.pdf
        - Video: lecture_03_hypothesis_testing.mp4
        - Lab: week3_tests.R
      Prerequisites: Module 3
   
   📦 Module 5: Regression Analysis (Advanced)
      Duration: 10 hours
      Contents:
        - Lecture: week4_regression.pdf
        - Lab: week4_linear_regression.R
        - Dataset: diabetes.csv
      Prerequisites: Module 4
   
   📦 Module 6: Data Visualization (Intermediate)
      Duration: 8 hours
      Contents:
        - Lecture: week5_visualization.pdf
        - Lab: week5_ggplot.R
      Prerequisites: Module 2

Tier Distribution:
  - Basic: 2 modules (33%)
  - Intermediate: 3 modules (50%)
  - Advanced: 1 module (17%)

Duplicates Detected:
  ⚠️ Introduction to R appears in both week1_intro_to_r.pdf (pages 1-10) 
      and lecture_01_introduction.mp4 transcript (0:00-12:30)
  → Recommendation: Keep both (different modalities), note overlap
```

#### **Step 7: Human Review**
```
👤 Human Review Required

Organization Review Dashboard:
  ✅ Structure looks good
  ✏️ Minor edit: Rename "Module 3" to "Exploratory Data Analysis"
  ✏️ Feedback: Module 6 should be optional/elective, not required
  
✅ Approved with changes
```

#### **Step 8: Enhancement Generation**
```
⏳ Generating study aids...

📖 Study Guides (6 modules):
  ✅ Module 1: R Programming Foundations
     - Key points: 15
     - Examples: 8 code snippets
     - Practice problems: 12 (4 easy, 5 medium, 3 hard)
  
🗃️ Flashcards (180 cards total):
  ✅ R Basics: 45 cards
  ✅ Statistical Tests: 52 cards
  ✅ Regression: 38 cards
  ✅ Visualization: 25 cards
  ✅ Concepts: 20 cards

📚 Glossary (124 terms):
  - ANOVA: Analysis of variance, a statistical test...
  - correlation: A measure of association between...
  - ggplot2: An R package for data visualization...
  - p-value: The probability of observing...
  - regression: A statistical method for modeling...

📅 Timeline:
  History of Statistics:
    1900 - Pearson develops chi-square test
    1908 - Student's t-test published
    1925 - Fisher introduces ANOVA
    1993 - R language created
    2005 - ggplot2 released

📄 Bibliography (28 references):
  Organized by type and cited throughout materials
```

#### **Step 9: RAG Indexing**
```
⏳ Indexing for chat interface...

✅ Chunked 45 documents into 892 chunks
✅ Generated embeddings (all-MiniLM-L6-v2)
✅ Indexed in ChromaDB
✅ RAG system ready

Chat Interface Available:
  - Ask questions about R programming
  - Query statistical concepts
  - Request code examples
  - All answers with source citations
```

#### **Step 10: Export**
```
✅ Export Complete

Package: statistics_with_r_v1.zip (920 MB)

Contents:
  ✅ 6 modules with learning objectives
  ✅ 45 source documents (organized)
  ✅ Knowledge graph (145 nodes, 312 edges)
  ✅ 6 study guides
  ✅ 180 flashcards (Anki format)
  ✅ Glossary (124 terms)
  ✅ Timeline
  ✅ ChromaDB vector database
  ✅ Metadata and analytics

Ready for CourseTransformer:
  → Modernize R code for latest R version
  → Generate interactive visualizations
  → Create auto-graded exercises
  → Build LMS-compatible package
```

### Outcomes
- ✅ Legacy course transformed into structured curriculum
- ✅ 6 well-organized modules with clear progression
- ✅ Comprehensive study aids generated
- ✅ Chat interface for interactive Q&A
- ✅ Ready for modernization pipeline

---

## Example 2: Ingest Book (PDF) for Course Creation

### Scenario
An instructor has a 500-page machine learning textbook (PDF) and wants to create a course from it. The book is text-heavy with equations, diagrams, and code examples.

### Input Materials
```
ml_textbook.pdf (28 MB, 500 pages)
- Chapter 1: Introduction to Machine Learning (25 pages)
- Chapter 2: Supervised Learning (65 pages)
- Chapter 3: Neural Networks (80 pages)
- Chapter 4: Deep Learning (95 pages)
- Chapter 5: Unsupervised Learning (55 pages)
- Chapter 6: Reinforcement Learning (70 pages)
- Chapter 7: Advanced Topics (60 pages)
- Appendices: Mathematical Background (50 pages)
```

### Workflow

#### **Step 1: Upload & Parse**
```
📄 Parsing PDF (Deep Mode selected)

⏳ Extracting content...
  ✅ 500 pages processed
  ✅ 125,000 words extracted
  ✅ 87 diagrams extracted
  ✅ 45 code examples extracted
  ✅ 234 equations detected (LaTeX)
  ✅ 18 tables extracted
  ✅ Table of contents parsed
```

#### **Step 2: Understanding**
```
Semantic Analysis:
  - 342 concepts identified
  - 15 main topics
  - Difficulty: Advanced (Flesch-Kincaid Grade: 15.2)

Key Concepts (top 20):
  1. supervised learning (0.98)
  2. neural networks (0.97)
  3. gradient descent (0.95)
  4. backpropagation (0.94)
  5. deep learning (0.93)
  ...

Knowledge Graph:
  - 342 concept nodes
  - 789 relationships
  - 156 prerequisite chains
  - 28 foundational concepts (no prerequisites)

Chapter Summaries Generated:
  ✅ All 7 chapters + appendices
  ✅ Multi-level: 1-sentence, paragraph, page
```

#### **Step 3: Organization**
```
Proposed Structure:

📚 Course: Machine Learning Fundamentals
   Based on: ML Textbook by Author
   Duration: 120 hours

🎯 Track 1: Complete ML Track
   
   📦 Module 1: Introduction & Foundations (Basic)
      From: Chapter 1 + Appendix A (Math Background)
      Duration: 15 hours
      28 concepts, 12 code examples
   
   📦 Module 2: Supervised Learning Basics (Intermediate)
      From: Chapter 2 (pages 26-65)
      Duration: 18 hours
      45 concepts, 18 code examples
   
   📦 Module 3: Neural Network Fundamentals (Intermediate)
      From: Chapter 3
      Duration: 22 hours
      58 concepts, 25 code examples
   
   📦 Module 4: Deep Learning (Advanced)
      From: Chapter 4
      Duration: 25 hours
      67 concepts, 32 code examples
   
   📦 Module 5: Unsupervised Learning (Intermediate)
      From: Chapter 5
      Duration: 18 hours
      42 concepts, 15 code examples
   
   📦 Module 6: Reinforcement Learning (Advanced)
      From: Chapter 6
      Duration: 22 hours
      52 concepts, 20 code examples

Alternative Track: Project-Based
   (Same modules, different sequence emphasizing hands-on projects)
```

#### **Step 4: Enhancement**
```
📖 Study Guides:
  ✅ 6 comprehensive guides (avg. 8 pages each)
  ✅ Key equations highlighted
  ✅ Concept maps for each chapter
  ✅ Code walkthroughs

🗃️ Flashcards:
  ✅ 450+ cards generated
  ✅ Definitions, equations, concepts
  ✅ Spaced repetition ready

📚 Glossary:
  ✅ 342 terms defined
  ✅ Cross-referenced
  ✅ Searchable

Gap Analysis:
  ⚠️ Practical datasets not included → Suggest Kaggle datasets
  ⚠️ No exercises → Generate practice problems (120 problems created)
```

#### **Step 5: Chat Interaction**
```
User: "Explain backpropagation in simple terms"

AI: "Backpropagation is the algorithm neural networks use to learn. Here's how 
it works:

1. **Forward Pass**: Input data flows through the network to produce a prediction
2. **Error Calculation**: Compare prediction to actual answer
3. **Backward Pass**: Calculate how much each neuron contributed to the error
4. **Weight Update**: Adjust each connection to reduce error

The key insight is using the chain rule from calculus to efficiently compute 
gradients layer by layer, starting from the output and working backward to the 
input.

(Source: ML Textbook, Chapter 3, pages 145-152)

The textbook provides this helpful analogy: 'Think of backpropagation like 
assigning credit (or blame) to each player on a team after a game. Each player's 
contribution is assessed based on how their actions affected the final score.'
(Source: ML Textbook, Chapter 3, page 146)"

📚 Sources:
  - ML Textbook, Chapter 3: Neural Networks (pages 145-152)
  - ML Textbook, Chapter 3: Backpropagation Algorithm (pages 148-150)
```

### Export
```
✅ Exported to CourseTransformer

Course Package Includes:
  - 6 modules with 120 hours of content
  - 342 concepts mapped in knowledge graph
  - 450+ flashcards
  - Comprehensive glossary
  - 120 practice problems (AI-generated)
  - RAG-powered Q&A system
  - Study guides for all chapters

Ready for:
  - Interactive quiz generation
  - Video lecture creation
  - Code playground integration
  - LMS deployment
```

---

## Example 3: Ingest YouTube Playlist

### Scenario
A creator has published a 20-video tutorial series on YouTube about data science. They want to convert it into a structured course with transcripts, slides, and study materials.

### Input
```
YouTube Playlist URL:
https://youtube.com/playlist?list=ABC123...

Videos (20 total, 18 hours):
  1. Introduction to Data Science (45 min)
  2. Python Setup and Basics (38 min)
  3. NumPy Fundamentals (52 min)
  4. Pandas for Data Analysis (1h 5min)
  ...
  20. Final Project Walkthrough (1h 15min)
```

### Workflow

#### **Step 1: Video Download & Processing**
```
⏳ Downloading 20 videos from YouTube...
✅ Downloaded (4.2 GB total)

⏳ Processing videos in parallel...

🎥 Video Analysis (per video):
  ✅ Audio extraction
  ✅ Transcription (Whisper)
  ✅ Slide extraction (detected static frames)
  ✅ Code snippet detection (OCR on code shown on screen)
  ✅ Scene detection (topic changes)

Results:
  ✅ 20 transcripts (avg. 12,000 words each)
  ✅ 342 slides extracted (deduplicated)
  ✅ 89 code snippets detected
  ✅ 127 scene markers (topic changes)
```

#### **Step 2: Understanding**
```
Transcript Analysis:
  - Topics: Python, NumPy, Pandas, Matplotlib, Scikit-learn, ML
  - 156 concepts extracted
  - Speaker: Single instructor (consistent voice)

Content Mapping:
  Video 1 (Intro) → Overview concepts (no code)
  Video 2 (Python) → 12 code examples, setup instructions
  Video 3 (NumPy) → Arrays, operations, broadcasting
  ...

Duplicate Detection:
  ⚠️ Introduction to Python repeated in Videos 2 and 10
  ⚠️ Matplotlib basics covered in Videos 8 and 15
  → Combined into single sections
```

#### **Step 3: Organization**
```
Proposed Structure:

📚 Course: Data Science with Python
   Format: Video-based course
   Duration: 18 hours (20 videos)

🎯 Learning Path:

📦 Module 1: Python Foundations (3 videos, 2.5 hours)
   - Video 1: Introduction
   - Video 2: Python Setup
   - Video 3: Python Basics
   Extracted: 28 slides, 15 code snippets

📦 Module 2: Data Manipulation (4 videos, 4 hours)
   - Video 4: NumPy Fundamentals
   - Video 5: Advanced NumPy
   - Video 6: Pandas Introduction
   - Video 7: Pandas Advanced
   Extracted: 67 slides, 32 code snippets

📦 Module 3: Visualization (3 videos, 2.5 hours)
   - Video 8: Matplotlib Basics
   - Video 9: Seaborn
   - Video 10: Advanced Plots
   Extracted: 45 slides, 18 code snippets

📦 Module 4: Machine Learning (6 videos, 6 hours)
   - Videos 11-16: ML topics
   Extracted: 98 slides, 45 code snippets

📦 Module 5: Final Project (4 videos, 3 hours)
   - Videos 17-20: Project walkthrough
   Extracted: 52 slides, 28 code snippets
```

#### **Step 4: Enhancement**
```
Study Guides:
  ✅ Generated from video transcripts
  ✅ Timestamped links to video sections
  ✅ Code examples from videos

Flashcards:
  ✅ 280 cards from video content
  ✅ Include video timestamps

Glossary:
  ✅ 156 terms from transcripts
  ✅ Linked to video explanations

Combined Study Guide:
  Unified guide synthesizing all 20 videos
  Chapter for each module
  Cross-references between videos
```

### Export
```
Course Package:
  ✅ 20 video transcripts (timestamped)
  ✅ 342 slides (organized by topic)
  ✅ 89 code snippets (executable)
  ✅ 5 modules with clear progression
  ✅ Study guides with video timestamps
  ✅ 280 flashcards
  ✅ Comprehensive glossary
  ✅ Timeline of topics covered

Ready for:
  - Video platform integration
  - Interactive coding exercises
  - Auto-generated quizzes
```

---

## Example 4: Iterative Multi-Source Ingestion

### Scenario
An instructor is building a course incrementally, adding materials over multiple days from different sources.

### Timeline

#### **Day 1: Initial Upload (PDFs)**
```
Upload: 5 PDF lecture slides
⏳ Processing...
✅ Parsed, analyzed, organized
📊 Current State:
   - 5 documents
   - 78 concepts
   - Preliminary structure: 2 modules
```

#### **Day 3: Add YouTube Lectures**
```
Upload: 8 YouTube videos
⏳ Processing...
✅ Transcribed, integrated with existing content

📊 Updated State:
   - 13 documents (5 PDFs + 8 videos)
   - 156 concepts (78 new)
   - Updated structure: 4 modules
   
🔗 Connections Detected:
   - Video 2 elaborates on PDF Lecture 1
   - Video 5 provides examples for PDF Lecture 3
```

#### **Day 5: Add GitHub Repository**
```
Upload: GitHub repo (ML course code)
⏳ Processing...
✅ Code analyzed, linked to lectures

📊 Updated State:
   - 13 + 1 repository (52 code files)
   - 187 concepts
   - Updated structure: 5 modules (added code labs)
   
🔗 Connections:
   - linear_regression.py implements concepts from Video 4
   - neural_network.ipynb matches PDF Lecture 5
```

#### **Day 7: Add Supplementary Articles**
```
Upload: 10 web articles (URLs)
⏳ Scraping and processing...
✅ Articles integrated

📊 Final State:
   - 76 documents total
   - 245 concepts
   - Knowledge graph: 567 relationships
   - Final structure: 6 modules

🎯 Unified Curriculum:
   All materials connected via knowledge graph
   Optimal learning sequence determined
   Duplicate content merged
   Gaps identified (none critical)
```

### Continuous Updates
```
Knowledge Graph Evolution:

Day 1: [78 nodes, 120 edges]
  Basic concept network

Day 3: [156 nodes, 298 edges]
  Videos add elaboration relationships
  Cross-modal connections (PDF ↔ Video)

Day 5: [187 nodes, 421 edges]
  Code examples link to concepts
  Implementation relationships added

Day 7: [245 nodes, 567 edges]
  Articles provide context
  External references added
  Complete concept coverage
```

### Export
```
Final Course Package:

Comprehensive ML Course
  ✅ 6 modules, 120 hours
  ✅ Multi-format content:
      - 5 PDF lectures
      - 8 video lectures
      - 52 code examples
      - 10 reading articles
  ✅ Fully connected knowledge graph
  ✅ No critical gaps
  ✅ Study aids for all modules
  ✅ RAG system with all sources

Benefit of Iterative Approach:
  - Organic content collection
  - Continuous refinement
  - Multi-modal learning
  - Comprehensive coverage
```

---

## Success Metrics (All Examples)

| Metric | Example 1 | Example 2 | Example 3 | Example 4 |
|--------|-----------|-----------|-----------|-----------|
| **Input Files** | 45 | 1 | 20 | 76 |
| **Parsing Success** | 96% | 100% | 100% | 97% |
| **Concepts Extracted** | 78 | 342 | 156 | 245 |
| **Modules Created** | 6 | 6 | 5 | 6 |
| **Processing Time** | 28 min | 42 min | 3.5 hours | 1.5 hours (total) |
| **Human Review Time** | 15 min | 20 min | 12 min | 25 min |
| **Study Aids Generated** | ✅ All | ✅ All | ✅ All | ✅ All |
| **RAG Ready** | ✅ | ✅ | ✅ | ✅ |

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Design Specification (Not Implemented)
