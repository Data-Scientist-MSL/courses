# CourseIngester - Content Understanding Agents

## Overview

Understanding agents perform deep semantic analysis of parsed content to extract meaning, relationships, and pedagogical insights. These agents go beyond surface-level parsing to comprehend concepts, detect relationships, identify gaps, and assess difficulty.

**Design Philosophy**: Understanding precedes organization. Only by deeply comprehending content can we intelligently structure and enhance it.

---

## 1️⃣ Semantic Analysis Agent

### Purpose
Perform deep reading and comprehension of educational content to extract concepts, topics, entities, and intent.

### Capabilities

#### **Concept Extraction**
- **Method**: NLP-based entity recognition + LLM-based analysis
- **Process**:
  1. Extract noun phrases (potential concepts)
  2. Filter technical terms using frequency and capitalization
  3. LLM validation: "Is this a key concept in this domain?"
  4. Rank by importance (frequency, position, context)
- **Example Output**: 
  - "supervised learning", "neural networks", "backpropagation", "gradient descent"

#### **Topic Modeling**
- **Traditional Method**: Latent Dirichlet Allocation (LDA)
  - Tool: gensim
  - Discovers latent topics across documents
  - Assigns topic distributions to documents
- **Modern Method**: BERTopic
  - Transformer-based topic modeling
  - Generates coherent, interpretable topics
  - Hierarchical topic structure
- **Output**: 
  ```python
  {
      "topic_id": 1,
      "label": "Neural Networks",
      "keywords": ["neural", "layer", "activation", "weights"],
      "document_count": 15,
      "representative_docs": [...]
  }
  ```

#### **Named Entity Recognition (NER)**
- **Tool**: spaCy (en_core_web_lg model)
- **Entity Types**:
  - **PERSON**: Authors, researchers, instructors
  - **ORG**: Universities, companies, research labs
  - **GPE**: Locations (for geographic content)
  - **DATE**: Important dates, timelines
  - **TECHNOLOGY**: Programming languages, frameworks, tools
  - **ALGORITHM**: ML algorithms, data structures
- **Custom Entities**: Train domain-specific NER for educational content
- **Example**: "Geoffrey Hinton (PERSON) at University of Toronto (ORG) developed deep learning (TECHNOLOGY)"

#### **Intent Classification**
- **Purpose**: Classify content type for appropriate handling
- **Categories**:
  - **Lecture**: Theoretical explanation, foundational concepts
  - **Tutorial**: Step-by-step practical guide
  - **Reference**: Documentation, API reference, quick lookup
  - **Example**: Code examples, case studies
  - **Exercise**: Practice problems, assignments
  - **Assessment**: Quizzes, exams, tests
- **Method**: LLM-based classification with few-shot prompting
- **Prompt Example**: 
  ```
  Classify this educational content:
  [Content excerpt]
  
  Is this a: Lecture, Tutorial, Reference, Example, Exercise, or Assessment?
  ```

#### **Language Complexity Analysis**
- **Readability Metrics**:
  - **Flesch-Kincaid Grade Level**: US grade level
  - **SMOG Index**: Years of education needed
  - **Coleman-Liau Index**: Grade level based on characters
  - **Automated Readability Index (ARI)**
- **Vocabulary Analysis**:
  - Unique word count
  - Average word length
  - Technical term density
- **Sentence Complexity**:
  - Average sentence length
  - Subordinate clause count
  - Passive voice usage
- **Tools**: textstat, readability libraries

### LLM Usage (OLLAMA)

#### **Model Selection**
- **Concept Extraction**: llama3.2:3b (balance speed/accuracy)
- **Intent Classification**: llama3.2:1b (simple classification)
- **Semantic Similarity**: Embeddings from sentence-transformers

#### **Prompt Templates**
```python
CONCEPT_EXTRACTION_PROMPT = """
You are an educational content analyst. Extract key concepts from this text.

Text: {content}

List 5-10 key concepts that a learner should understand from this material.
Format: one concept per line, no numbering.
"""

INTENT_CLASSIFICATION_PROMPT = """
Classify this educational content into ONE category:
- Lecture (theoretical explanation)
- Tutorial (step-by-step guide)
- Reference (documentation, lookup)
- Example (code sample, case study)
- Exercise (practice problem)
- Assessment (quiz, test)

Content: {content}

Category: """
```

### Outputs

**Semantic Analysis Result**:
```python
{
    "document_id": "lecture_03.pdf",
    "concepts": [
        {
            "term": "supervised learning",
            "importance": 0.95,
            "first_mention_page": 3,
            "frequency": 42
        },
        {
            "term": "training data",
            "importance": 0.88,
            "first_mention_page": 4,
            "frequency": 35
        }
    ],
    "topics": [
        {
            "id": 1,
            "label": "Machine Learning Fundamentals",
            "probability": 0.75,
            "keywords": ["learning", "model", "training", "prediction"]
        }
    ],
    "entities": {
        "PERSON": ["Andrew Ng", "Geoffrey Hinton"],
        "ORG": ["Stanford University", "Google Brain"],
        "TECHNOLOGY": ["TensorFlow", "PyTorch", "scikit-learn"]
    },
    "intent": "Lecture",
    "complexity": {
        "flesch_kincaid_grade": 12.5,
        "smog_index": 11.2,
        "unique_words": 1250,
        "technical_term_ratio": 0.18
    }
}
```

### Configuration
```yaml
semantic_analysis:
  llm_model: "llama3.2:3b"
  extract_concepts: true
  min_concept_frequency: 3
  topic_modeling_method: "bertopic"  # or "lda"
  num_topics: 20
  ner_model: "en_core_web_lg"
  custom_entities: ["ALGORITHM", "TECHNOLOGY"]
```

---

## 2️⃣ Relationship Mapping Agent

### Purpose
Connect concepts across documents to build a web of knowledge, identifying prerequisites, examples, and related content.

### Capabilities

#### **Prerequisite Detection**
- **Method**: Co-occurrence analysis + LLM reasoning
- **Heuristics**:
  - Temporal analysis: Concepts introduced earlier are likely prerequisites
  - Definitional dependency: "X is defined using Y" → Y prerequisite to X
  - Complexity ordering: Simpler concepts prerequisite to complex ones
- **LLM Prompt**: 
  ```
  Given two concepts: "{concept_a}" and "{concept_b}"
  
  Is there a prerequisite relationship?
  - If understanding {concept_b} requires understanding {concept_a}, respond "A→B"
  - If understanding {concept_a} requires understanding {concept_b}, respond "B→A"  
  - If neither, respond "NONE"
  ```
- **Example**: "linear regression" → "gradient descent" (must know regression to understand gradient descent)

#### **Cross-Reference Finding**
- **Purpose**: Find related content across different documents
- **Methods**:
  1. **Concept Co-occurrence**: Documents sharing concepts are related
  2. **Semantic Similarity**: Embedding-based similarity (cosine similarity > 0.7)
  3. **Citation Analysis**: Documents citing same sources are related
  4. **LLM Comparison**: "How are these two sections related?"
- **Output**: Related document pairs with relationship type

#### **Dependency Graphing**
- **Graph Structure**:
  - **Nodes**: Concepts, topics, documents
  - **Edges**: Relationships (prerequisite, example-of, elaborates, contradicts)
- **Graph Metrics**:
  - **In-degree**: How many prerequisites a concept has
  - **Out-degree**: How many concepts depend on this one
  - **PageRank**: Importance of concept in curriculum
  - **Shortest Path**: Learning path between concepts
- **Tool**: NetworkX for graph construction and analysis

#### **Similarity Scoring**
- **Document Similarity**: 
  - **Method**: TF-IDF cosine similarity or embedding cosine similarity
  - **Threshold**: > 0.7 for "highly related", 0.5-0.7 "moderately related"
- **Concept Similarity**:
  - **Method**: Word embeddings (word2vec, GloVe, BERT)
  - **Purpose**: Identify synonyms or closely related concepts
  - **Example**: "neural network" ≈ "deep learning" (similarity: 0.85)

### Outputs

**Relationship Graph**:
```python
{
    "nodes": [
        {
            "id": "concept_1",
            "label": "linear regression",
            "type": "concept",
            "importance": 0.85,
            "document_refs": ["doc_1", "doc_3", "doc_7"]
        },
        {
            "id": "concept_2",
            "label": "gradient descent",
            "type": "concept",
            "importance": 0.92,
            "document_refs": ["doc_3", "doc_5"]
        }
    ],
    "edges": [
        {
            "source": "concept_1",
            "target": "concept_2",
            "type": "prerequisite",
            "confidence": 0.88,
            "evidence": "Gradient descent is used to optimize linear regression models"
        },
        {
            "source": "doc_1",
            "target": "doc_3",
            "type": "elaborates",
            "similarity": 0.72
        }
    ],
    "statistics": {
        "total_nodes": 145,
        "total_edges": 320,
        "avg_degree": 4.4,
        "connected_components": 1
    }
}
```

### Tools & Methods
- **NetworkX**: Graph construction and analysis
- **sentence-transformers**: Semantic embeddings
- **scikit-learn**: TF-IDF, cosine similarity
- **OLLAMA**: LLM-based relationship reasoning
- **spaCy**: Syntactic dependency parsing for relationship extraction

### Configuration
```yaml
relationship_mapping:
  llm_model: "llama3.2:3b"
  similarity_threshold: 0.7
  max_edges_per_node: 20
  detect_prerequisites: true
  cross_reference_similarity: 0.6
```

---

## 3️⃣ Knowledge Graph Builder

### Purpose
Construct a comprehensive, queryable knowledge graph representing all concepts, topics, entities, and their relationships.

### Capabilities

#### **Node Extraction**
- **Node Types**:
  - **Concept**: Key ideas (e.g., "neural networks")
  - **Topic**: Broad themes (e.g., "Machine Learning")
  - **Entity**: People, organizations, technologies
  - **Document**: Source materials
  - **Example**: Code snippets, case studies
  - **Exercise**: Practice problems
- **Node Properties**:
  - Label, description
  - Type, category
  - Importance score
  - Source documents
  - Difficulty level

#### **Edge Creation**
- **Edge Types**:
  - **prerequisite**: A must be learned before B
  - **example-of**: B is an example of A
  - **part-of**: A is part of larger topic B
  - **related-to**: A and B are related (generic)
  - **elaborates**: B provides more detail on A
  - **contradicts**: A and B have conflicting information (flag for review)
  - **cites**: Document A cites source B
- **Edge Properties**:
  - Relationship type
  - Confidence score (0-1)
  - Evidence text (snippet supporting relationship)
  - Source document

#### **Graph Visualization**
- **Tools**:
  - **PyVis**: Interactive network visualization (HTML)
  - **Plotly**: Custom graph layouts
  - **Graphviz**: Static graph images
- **Features**:
  - Node coloring by type or difficulty
  - Edge thickness by confidence
  - Interactive zoom, pan, drag
  - Node tooltips (show details on hover)
  - Filter by type, difficulty, topic
- **Layouts**: Force-directed, hierarchical, circular

#### **Graph Querying**
- **Query Types**:
  - **Find prerequisites**: "What must I learn before X?"
  - **Find dependents**: "What can I learn after mastering X?"
  - **Shortest path**: "What's the learning path from A to B?"
  - **Concept neighborhood**: "What's related to X?"
  - **Topic subgraph**: "Show all concepts in topic Y"
- **Query Language**: Cypher-style or custom DSL
- **Example Queries**:
  ```python
  # Find prerequisites for "neural networks"
  query("MATCH (a)-[:prerequisite]->(b {label: 'neural networks'}) RETURN a")
  
  # Find learning path
  query("SHORTEST_PATH from 'variables' to 'deep learning'")
  
  # Find related concepts
  query("NEIGHBORS of 'gradient descent' within 2 hops")
  ```

### Graph Construction Pipeline

```python
def build_knowledge_graph(documents, semantic_analysis, relationships):
    graph = nx.DiGraph()
    
    # Add concept nodes
    for doc in documents:
        for concept in doc.concepts:
            graph.add_node(
                concept.id,
                label=concept.term,
                type="concept",
                importance=concept.importance,
                sources=[doc.id]
            )
    
    # Add relationship edges
    for rel in relationships:
        graph.add_edge(
            rel.source,
            rel.target,
            type=rel.type,
            confidence=rel.confidence,
            evidence=rel.evidence
        )
    
    # Compute centrality metrics
    pagerank = nx.pagerank(graph)
    for node, score in pagerank.items():
        graph.nodes[node]['centrality'] = score
    
    return graph
```

### Outputs

**Knowledge Graph (Serialized)**:
```json
{
    "graph_id": "ml_course_2024",
    "metadata": {
        "created": "2024-01-15",
        "num_nodes": 245,
        "num_edges": 580,
        "num_topics": 8,
        "num_concepts": 180,
        "num_documents": 42
    },
    "nodes": [
        {
            "id": "n1",
            "label": "supervised learning",
            "type": "concept",
            "properties": {
                "importance": 0.95,
                "difficulty": "intermediate",
                "sources": ["doc_1", "doc_5", "doc_12"],
                "centrality": 0.042
            }
        }
    ],
    "edges": [
        {
            "id": "e1",
            "source": "n1",
            "target": "n5",
            "type": "prerequisite",
            "properties": {
                "confidence": 0.88,
                "evidence": "Linear regression is a supervised learning technique"
            }
        }
    ],
    "visualization": {
        "html_path": "knowledge_graph.html",
        "static_image": "knowledge_graph.png"
    }
}
```

### Tools & Libraries
- **NetworkX**: Graph data structure and algorithms
- **PyVis**: Interactive visualization
- **Plotly**: Custom visualizations
- **Neo4j** (optional): Graph database for large-scale graphs
- **graph-tool** (optional): High-performance graph library

### Configuration
```yaml
knowledge_graph:
  max_nodes: 10000
  max_edges_per_node: 50
  visualization_tool: "pyvis"
  layout: "force_directed"
  export_formats: ["json", "html", "gexf"]
  compute_centrality: true
```

---

## 4️⃣ Summarization Agent

### Purpose
Generate multi-level summaries of educational content, from single sentences to comprehensive overviews.

### Capabilities

#### **Abstractive Summarization (LLM-Based)**
- **Method**: OLLAMA language model generates summaries
- **Advantages**: Natural language, coherent, customizable
- **Prompt Template**:
  ```
  Summarize the following educational content in {length} {unit}.
  Focus on key concepts and learning objectives.
  
  Content: {text}
  
  Summary:
  ```
- **Levels**:
  - **1-sentence**: TL;DR (10-20 words)
  - **Paragraph**: Brief overview (50-100 words)
  - **Page**: Detailed summary (200-300 words)

#### **Extractive Summarization**
- **Method**: Select key sentences from original text
- **Algorithms**:
  - **TextRank**: PageRank for sentences (based on similarity graph)
  - **LexRank**: Similar to TextRank with different similarity metric
  - **LSA (Latent Semantic Analysis)**: SVD-based sentence selection
- **Advantages**: Preserves original wording, factually accurate
- **Tools**: sumy, gensim

#### **Hierarchical Summarization**
- **Structure**:
  - **Section → Chapter → Document → Collection**
- **Process**:
  1. Summarize each section (paragraph)
  2. Combine section summaries into chapter summary
  3. Combine chapter summaries into document summary
  4. Combine document summaries into collection summary
- **Benefit**: Provides multi-resolution understanding

#### **Bullet-Point Generation**
- **Purpose**: Quick-scan format for rapid review
- **Method**: Extract key points as bulleted list
- **Template**:
  ```
  Key Points:
  • Main concept 1
  • Main concept 2
  • Main concept 3
  ```

#### **Different Lengths**
- **Micro (1 sentence)**: "This section introduces neural networks as computational models inspired by the brain."
- **Short (3-5 sentences / ~50 words)**: "Neural networks are computational models inspired by biological neural networks..."
- **Medium (1 paragraph / ~100 words)**: More detailed overview
- **Long (1 page / ~300 words)**: Comprehensive summary with examples

### LLM Usage (OLLAMA)

#### **Model Selection**
- **Short summaries**: llama3.2:1b (fast)
- **Medium summaries**: llama3.2:3b (balanced)
- **Long summaries**: llama3.1:8b (detailed, nuanced)

#### **Prompt Engineering**
```python
SUMMARY_PROMPTS = {
    "micro": "Summarize in ONE sentence: {text}",
    
    "short": """Summarize this educational content in 3-5 sentences.
    Content: {text}
    Summary:""",
    
    "medium": """Provide a one-paragraph summary (100 words) of this educational material.
    Focus on: key concepts, main ideas, learning objectives.
    
    Content: {text}
    
    Summary:""",
    
    "long": """Write a comprehensive summary (300 words) of this educational content.
    Include: main topics, key concepts, important details, examples, and conclusions.
    
    Content: {text}
    
    Summary:"""
}
```

### Outputs

**Multi-Level Summaries**:
```python
{
    "document_id": "ml_lecture_04.pdf",
    "summaries": {
        "micro": "This lecture covers backpropagation in neural networks.",
        
        "short": "This lecture explains backpropagation, the algorithm for training neural networks. It covers the chain rule, gradient computation, and weight updates. Examples demonstrate how errors propagate backward through network layers.",
        
        "medium": "This lecture provides a comprehensive introduction to backpropagation, the fundamental algorithm for training neural networks. We begin by reviewing the forward pass and loss computation, then introduce the chain rule of calculus as the mathematical foundation for backpropagation. The lecture demonstrates how gradients are computed for each layer, working backward from the output layer to the input layer. Practical examples show weight update calculations and common pitfalls. The session concludes with best practices for efficient implementation.",
        
        "bullet_points": [
            "Backpropagation enables training of deep neural networks",
            "Chain rule is the mathematical foundation",
            "Gradients flow backward from output to input",
            "Weight updates use computed gradients",
            "Implementation requires careful handling of numerical stability"
        ],
        
        "hierarchical": {
            "section_summaries": {
                "introduction": "Overview of backpropagation necessity...",
                "chain_rule": "Mathematical foundations using chain rule...",
                "algorithm": "Step-by-step backpropagation algorithm...",
                "examples": "Practical examples demonstrating..."
            },
            "chapter_summary": "Combined summary of all sections..."
        }
    },
    "metadata": {
        "original_length": 5000,
        "micro_length": 12,
        "short_length": 45,
        "medium_length": 98,
        "compression_ratio": 0.02
    }
}
```

### Tools & Libraries
- **OLLAMA**: LLM for abstractive summarization
- **sumy**: Extractive summarization (TextRank, LSA)
- **gensim**: Text summarization
- **transformers**: BART, T5 for summarization (if using HuggingFace)
- **nltk**: Sentence tokenization

### Configuration
```yaml
summarization:
  llm_model: "llama3.2:3b"
  default_length: "medium"
  generate_bullet_points: true
  hierarchical_summary: true
  extractive_method: "textrank"
  max_input_tokens: 4000
```

---

## 5️⃣ Question Generation Agent

### Purpose
Automatically generate study questions, quizzes, and discussion prompts from educational content.

### Capabilities

#### **Study Question Generation**
- **Question Types**:
  - **Comprehension**: "What is the purpose of backpropagation?"
  - **Application**: "How would you apply gradient descent to optimize this function?"
  - **Analysis**: "Compare and contrast supervised and unsupervised learning."
  - **Evaluation**: "Assess the effectiveness of neural networks for time series prediction."
- **Method**: LLM-based generation with constraints
- **Prompt**:
  ```
  Generate 5 study questions about this content.
  Mix of: definition, explanation, application, and comparison questions.
  
  Content: {text}
  
  Questions:
  1.
  ```

#### **FAQ Generation**
- **Purpose**: Create Frequently Asked Questions for quick reference
- **Method**: 
  1. Identify common confusion points from content
  2. Generate questions a learner might ask
  3. Provide clear, concise answers
- **Example**: 
  - Q: "What's the difference between parameters and hyperparameters?"
  - A: "Parameters are learned during training (e.g., weights). Hyperparameters are set before training (e.g., learning rate)."

#### **Quiz Generation**
- **Question Types**:
  - **Multiple Choice**: 4 options, 1 correct
  - **True/False**
  - **Fill-in-the-blank**
  - **Short Answer**
- **Components**:
  - Question text
  - Answer options (for MCQ)
  - Correct answer
  - Explanation (why this answer is correct)
  - Difficulty level
  - Related concepts
- **Distractor Generation**: Plausible wrong answers for MCQs

#### **Discussion Prompt Generation**
- **Purpose**: Encourage deeper thinking and peer discussion
- **Question Style**: Open-ended, thought-provoking
- **Examples**:
  - "How might bias in training data affect real-world AI applications?"
  - "Discuss the ethical implications of using facial recognition systems."

#### **Bloom's Taxonomy Alignment**
- **Levels** (low to high):
  1. **Remember**: "Define neural network."
  2. **Understand**: "Explain how gradient descent works."
  3. **Apply**: "Use backpropagation to train this network."
  4. **Analyze**: "Compare CNN vs. RNN architectures."
  5. **Evaluate**: "Assess which algorithm is best for this problem."
  6. **Create**: "Design a neural network architecture for image classification."
- **Distribution**: Generate questions across all levels
- **Tagging**: Each question tagged with Bloom's level

### LLM Usage (OLLAMA)

#### **Prompt Templates**
```python
MCQ_GENERATION_PROMPT = """
Generate a multiple-choice question about this content.

Content: {text}

Format:
Question: [question text]
A) [option]
B) [option]
C) [option]
D) [option]
Correct: [A/B/C/D]
Explanation: [why this is correct]
Bloom's Level: [Remember/Understand/Apply/Analyze/Evaluate/Create]
"""

DISCUSSION_PROMPT_TEMPLATE = """
Generate an open-ended discussion question about this content.
The question should encourage critical thinking and diverse viewpoints.

Content: {text}

Discussion Question:
"""
```

### Outputs

**Generated Questions**:
```python
{
    "document_id": "ml_basics.pdf",
    "questions": {
        "study_questions": [
            {
                "id": "q1",
                "question": "What is the primary purpose of a loss function in machine learning?",
                "type": "comprehension",
                "blooms_level": "Understand",
                "difficulty": "Easy",
                "related_concepts": ["loss function", "optimization"]
            },
            {
                "id": "q2",
                "question": "How would you modify the learning rate to improve convergence?",
                "type": "application",
                "blooms_level": "Apply",
                "difficulty": "Medium",
                "related_concepts": ["learning rate", "convergence", "hyperparameters"]
            }
        ],
        
        "quiz": [
            {
                "id": "quiz1",
                "type": "multiple_choice",
                "question": "Which of the following is a supervised learning algorithm?",
                "options": [
                    "K-means clustering",
                    "Linear regression",
                    "PCA",
                    "Autoencoders"
                ],
                "correct_answer": "B",
                "explanation": "Linear regression is supervised (uses labeled data). The others are unsupervised.",
                "blooms_level": "Remember",
                "difficulty": "Easy",
                "points": 1
            },
            {
                "id": "quiz2",
                "type": "true_false",
                "question": "Increasing the learning rate always improves training speed.",
                "correct_answer": false,
                "explanation": "Too high a learning rate can cause divergence and prevent convergence.",
                "blooms_level": "Understand",
                "difficulty": "Medium",
                "points": 1
            }
        ],
        
        "faq": [
            {
                "question": "What's the difference between overfitting and underfitting?",
                "answer": "Overfitting occurs when a model learns training data too well, including noise, and performs poorly on new data. Underfitting occurs when a model is too simple to capture the underlying pattern."
            }
        ],
        
        "discussion_prompts": [
            "Discuss the trade-offs between model complexity and interpretability in machine learning applications.",
            "How should we address bias in training data to ensure fair AI systems?"
        ]
    },
    
    "statistics": {
        "total_questions": 45,
        "by_blooms_level": {
            "Remember": 8,
            "Understand": 12,
            "Apply": 10,
            "Analyze": 8,
            "Evaluate": 5,
            "Create": 2
        },
        "by_difficulty": {
            "Easy": 15,
            "Medium": 20,
            "Hard": 10
        }
    }
}
```

### Tools & Libraries
- **OLLAMA**: LLM for question generation
- **transformers**: Question generation models (T5, BART)
- **nltk**: Sentence analysis
- **questgen**: Automated question generation library

### Configuration
```yaml
question_generation:
  llm_model: "llama3.2:3b"
  num_study_questions: 10
  num_quiz_questions: 20
  generate_faq: true
  generate_discussion: true
  bloom_distribution: [0.2, 0.25, 0.25, 0.15, 0.10, 0.05]  # Remember to Create
  difficulty_distribution: [0.3, 0.5, 0.2]  # Easy, Medium, Hard
```

---

## 6️⃣ Gap Identification Agent

### Purpose
Identify missing, incomplete, or inconsistent content within ingested materials.

### Capabilities

#### **Missing Concept Detection**
- **Method**: Compare concepts in materials to target curriculum or domain knowledge base
- **Process**:
  1. Extract concepts from materials (via Semantic Analysis Agent)
  2. Load reference curriculum or domain ontology
  3. Identify concepts in reference but not in materials
  4. Rank gaps by importance
- **Example**: Materials cover "linear regression" but not "logistic regression" (common prerequisite)

#### **Completeness Checking**
- **Criteria**:
  - **Concept Coverage**: Is concept defined, explained, and exemplified?
  - **Topic Coverage**: Are all aspects of topic covered (theory, practice, examples)?
  - **Depth**: Is coverage superficial or thorough?
- **Scoring**:
  - **Complete (100%)**: Definition + explanation + examples + exercises
  - **Partial (50%)**: Definition + brief explanation
  - **Minimal (25%)**: Only mentioned, not explained
  - **Missing (0%)**: Not covered
- **Method**: LLM-based assessment
  ```
  Assess completeness of coverage for concept "{concept}":
  Content: {text}
  
  Is this concept:
  - Fully explained with examples? (Complete)
  - Briefly explained? (Partial)
  - Only mentioned? (Minimal)
  - Not covered? (Missing)
  ```

#### **Inconsistency Detection**
- **Types**:
  - **Definitional**: Same term defined differently in different documents
  - **Factual**: Contradicting facts or numbers
  - **Notation**: Same concept using different notation
- **Method**: 
  1. Extract definitions/facts for same concept from multiple sources
  2. Compute semantic similarity
  3. If similarity < threshold, flag as potential inconsistency
  4. LLM verification: "Are these two statements inconsistent?"
- **Example**: 
  - Doc 1: "Learning rate should be small (0.001)"
  - Doc 2: "Use large learning rate (0.1) for fast convergence"
  - → Inconsistency flagged

#### **Missing Reference Finder**
- **Purpose**: Identify incomplete citations or missing sources
- **Detection**:
  - Claims without citations
  - "See [?]" or "TODO: add reference"
  - Dangling citations (cited but not in bibliography)
- **Method**: Regex patterns + reference parsing

#### **Coverage Analysis**
- **Purpose**: Compare materials to target curriculum
- **Input**: Target curriculum (list of topics/concepts to cover)
- **Output**: Coverage percentage, missing topics
- **Visualization**: Heat map or checklist
- **Example**:
  ```
  Target Curriculum Coverage: 78%
  
  Covered:
  ✓ Linear Regression
  ✓ Gradient Descent
  ✓ Neural Networks
  
  Missing:
  ✗ Logistic Regression
  ✗ Decision Trees
  ✗ SVM
  
  Incomplete:
  ⚠ Overfitting (mentioned but not explained)
  ```

### Outputs

**Gap Analysis Report**:
```python
{
    "analysis_date": "2024-01-15",
    "target_curriculum": "ML_Foundations",
    
    "missing_concepts": [
        {
            "concept": "logistic regression",
            "severity": "critical",
            "reason": "Fundamental supervised learning algorithm not covered",
            "suggested_action": "Add lecture or reading on logistic regression"
        },
        {
            "concept": "cross-validation",
            "severity": "warning",
            "reason": "Model evaluation technique not discussed",
            "suggested_action": "Include section on validation techniques"
        }
    ],
    
    "incomplete_coverage": [
        {
            "concept": "overfitting",
            "current_coverage": 25,  # percentage
            "gaps": [
                "No examples provided",
                "Regularization techniques not discussed",
                "No exercises on preventing overfitting"
            ],
            "severity": "warning"
        }
    ],
    
    "inconsistencies": [
        {
            "concept": "learning rate",
            "type": "recommendation_conflict",
            "sources": [
                {
                    "document": "lecture_02.pdf",
                    "statement": "Use small learning rate (0.001)",
                    "page": 15
                },
                {
                    "document": "tutorial_05.md",
                    "statement": "Large learning rate (0.1) for faster convergence",
                    "page": null
                }
            ],
            "severity": "warning",
            "resolution": "Clarify that optimal learning rate depends on problem"
        }
    ],
    
    "missing_references": [
        {
            "document": "lecture_08.pdf",
            "page": 23,
            "context": "According to [?], neural networks can approximate any function",
            "severity": "info"
        }
    ],
    
    "coverage_summary": {
        "total_concepts_target": 50,
        "concepts_covered": 39,
        "coverage_percentage": 78,
        "complete_coverage": 25,
        "partial_coverage": 14,
        "missing": 11
    },
    
    "severity_breakdown": {
        "critical": 2,
        "warning": 8,
        "info": 15
    }
}
```

### Tools & Methods
- **OLLAMA**: LLM for consistency checking
- **sentence-transformers**: Semantic similarity
- **difflib**: Text comparison
- **Regex**: Pattern matching for references

### Configuration
```yaml
gap_identification:
  llm_model: "llama3.2:3b"
  target_curriculum_path: "curricula/ml_foundations.yaml"
  completeness_threshold: 0.5
  inconsistency_threshold: 0.3  # Similarity < 0.3 → inconsistent
  severity_levels: ["critical", "warning", "info"]
```

---

## 7️⃣ Difficulty Assessor Agent

### Purpose
Rate content difficulty to enable appropriate sequencing and learner guidance.

### Capabilities

#### **Readability Scoring**
- **Metrics**:
  - **Flesch-Kincaid Grade Level**: US school grade (e.g., 12 = high school senior)
  - **SMOG Index**: Years of education required
  - **Coleman-Liau Index**: Grade level based on characters
  - **Gunning Fog Index**: Years of education for comprehension
- **Tool**: textstat library
- **Interpretation**:
  - 0-6: Elementary
  - 7-9: Middle school
  - 10-12: High school
  - 13-16: College
  - 17+: Graduate/Professional

#### **Concept Complexity Analysis**
- **Factors**:
  - **Number of Prerequisites**: More prerequisites → higher complexity
  - **Abstraction Level**: Concrete vs. abstract concepts
  - **Technical Term Density**: % of technical/domain-specific terms
  - **Conceptual Novelty**: New concept vs. combination of known concepts
- **Method**: 
  - Count prerequisites from knowledge graph
  - Measure abstraction using WordNet (abstract vs. concrete nouns)
  - Calculate technical term ratio
- **Formula**: 
  ```
  Complexity = 0.3 * prerequisite_count + 
               0.3 * abstraction_score + 
               0.2 * technical_density +
               0.2 * novelty_score
  ```

#### **Prerequisite Estimation**
- **Purpose**: Determine required background knowledge
- **Method**:
  1. Identify concepts in content
  2. Look up prerequisites in knowledge graph
  3. Aggregate all prerequisites
  4. Rank by importance
- **Output**: List of prerequisite concepts/topics
- **Example**: 
  - Content: "Convolutional Neural Networks"
  - Prerequisites: "Neural Networks", "Gradient Descent", "Linear Algebra", "Python"

#### **Tier Mapping**
- **Tiers**:
  - **Basic**: Introductory, minimal prerequisites, high readability
  - **Intermediate**: Some prerequisites, moderate complexity
  - **Advanced**: Many prerequisites, high complexity, specialized
- **Classification Method**: Decision tree or LLM-based
- **Criteria**:
  ```
  if prerequisite_count <= 2 and readability <= 12:
      tier = "Basic"
  elif prerequisite_count <= 5 and readability <= 16:
      tier = "Intermediate"
  else:
      tier = "Advanced"
  ```

### Outputs

**Difficulty Assessment**:
```python
{
    "document_id": "neural_networks_lecture.pdf",
    
    "readability": {
        "flesch_kincaid_grade": 13.5,
        "smog_index": 12.8,
        "coleman_liau": 14.2,
        "gunning_fog": 13.9,
        "average_grade_level": 13.6,
        "interpretation": "College level"
    },
    
    "concept_complexity": {
        "score": 7.5,  # out of 10
        "factors": {
            "prerequisite_count": 6,
            "abstraction_score": 0.72,
            "technical_density": 0.28,
            "novelty_score": 0.65
        },
        "interpretation": "High complexity"
    },
    
    "prerequisites": [
        {
            "concept": "Linear Algebra",
            "importance": 0.95,
            "required": true
        },
        {
            "concept": "Calculus",
            "importance": 0.88,
            "required": true
        },
        {
            "concept": "Python Programming",
            "importance": 0.75,
            "required": true
        },
        {
            "concept": "Probability Theory",
            "importance": 0.60,
            "required": false
        }
    ],
    
    "tier": "Advanced",
    "tier_confidence": 0.89,
    
    "difficulty_score": 8.2,  # out of 10
    
    "learner_guidance": "This content is suitable for learners with strong mathematical background and prior exposure to basic machine learning concepts. Recommended prerequisites: Linear Algebra, Calculus, Python."
}
```

### Tools & Libraries
- **textstat**: Readability metrics
- **nltk**: Text analysis
- **WordNet**: Concept abstraction analysis
- **NetworkX**: Prerequisite graph traversal

### Configuration
```yaml
difficulty_assessment:
  readability_metrics: ["flesch_kincaid", "smog", "coleman_liau"]
  tier_thresholds:
    basic_max_prerequisites: 2
    intermediate_max_prerequisites: 5
  complexity_weights:
    prerequisites: 0.3
    abstraction: 0.3
    technical_density: 0.2
    novelty: 0.2
```

---

## Agent Orchestration

### Sequential Processing
```
Parse → Semantic Analysis → Relationship Mapping → Knowledge Graph → 
Summarization → Question Generation → Gap Identification → Difficulty Assessment
```

### Parallel Processing
- Semantic Analysis and Summarization can run in parallel
- Question Generation and Difficulty Assessment can run in parallel
- Knowledge Graph depends on Semantic Analysis + Relationship Mapping

### State Sharing
All agents read from and write to shared state:
```python
class UnderstandingState:
    documents: List[ParsedDocument]
    concepts: List[Concept]
    topics: List[Topic]
    entities: Dict[str, List[str]]
    relationships: List[Relationship]
    knowledge_graph: nx.DiGraph
    summaries: Dict[str, Summary]
    questions: List[Question]
    gaps: GapAnalysisReport
    difficulty_scores: Dict[str, DifficultyScore]
```

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Design Specification (Not Implemented)
