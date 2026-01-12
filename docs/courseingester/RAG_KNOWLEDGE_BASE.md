# CourseIngester - RAG Knowledge Base & NotebookLM Features

## Overview

The RAG (Retrieval-Augmented Generation) knowledge base enables NotebookLM-style interaction with ingested course materials. Users can chat with their sources, ask questions, and receive cited answers drawn from the content, creating an interactive learning companion.

**Design Philosophy**: Transform static content into a conversational learning experience. Every answer is grounded in source materials with full attribution.

---

## Core RAG System

### Vector Database: ChromaDB

#### **Why ChromaDB?**
- **Lightweight**: Embedded database, no separate server required
- **Python-Native**: Seamless integration with Python applications
- **Flexible**: Supports metadata filtering, multi-modal embeddings
- **Open Source**: Free, community-driven
- **Persistent**: Data survives application restarts

#### **Architecture**
```python
import chromadb
from chromadb.config import Settings

# Initialize persistent client
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

# Create collection
collection = client.create_collection(
    name="course_materials",
    metadata={"description": "Ingested course content"}
)
```

#### **Collections**
- **Primary Collection**: `course_materials` - All course content
- **Enhancement Collections**:
  - `study_guides` - Generated study guides
  - `flashcards` - Flashcard content
  - `glossary` - Technical terms and definitions
- **Metadata Collections**:
  - `concepts` - Extracted concepts
  - `summaries` - Document summaries

#### **Storage Structure**
```
chroma_db/
├── course_materials/
│   ├── embeddings.parquet
│   ├── metadata.parquet
│   └── documents.parquet
├── study_guides/
├── flashcards/
└── glossary/
```

---

### Embedding Models

#### **Primary Model: sentence-transformers**
```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
embeddings = model.encode([
    "Neural networks are computational models...",
    "Backpropagation is an algorithm for training..."
])
```

#### **Model Options**

| Model | Dimensions | Speed | Quality | Use Case |
|-------|-----------|-------|---------|----------|
| `all-MiniLM-L6-v2` | 384 | Fast | Good | Default, balanced |
| `all-mpnet-base-v2` | 768 | Medium | Excellent | High accuracy |
| `paraphrase-MiniLM-L3-v2` | 384 | Very Fast | Fair | Quick prototyping |
| `multi-qa-MiniLM-L6-cos-v1` | 384 | Fast | Good (Q&A) | Question answering |

#### **OpenAI Embeddings (Optional)**
```python
import openai

# Requires API key
embeddings = openai.Embedding.create(
    input=["Your text here"],
    model="text-embedding-ada-002"
)
```

**Trade-offs**:
- **Local (sentence-transformers)**: Free, private, offline
- **OpenAI**: Higher quality, requires API key, costs money

---

### Chunking Strategy

#### **Why Chunking?**
- **Context Window Limits**: LLMs have token limits (e.g., 4K, 8K, 32K)
- **Retrieval Precision**: Smaller chunks = more precise retrieval
- **Embedding Quality**: Embeddings work best on coherent, focused text

#### **Chunking Methods**

##### **1. Semantic Chunking** (Recommended)
- **Method**: Split by natural boundaries (sections, paragraphs)
- **Implementation**:
  ```python
  def semantic_chunk(document):
      chunks = []
      for section in document.sections:
          if len(section.text) > max_chunk_size:
              # Further split by paragraphs
              chunks.extend(split_by_paragraphs(section.text))
          else:
              chunks.append({
                  'text': section.text,
                  'metadata': {
                      'section': section.title,
                      'page': section.page
                  }
              })
      return chunks
  ```
- **Advantages**: Preserves semantic coherence, natural boundaries
- **Disadvantages**: Variable chunk sizes

##### **2. Fixed-Size Chunking with Overlap**
- **Method**: Split into fixed-size chunks (e.g., 500 tokens) with overlap
- **Implementation**:
  ```python
  def fixed_chunk_with_overlap(text, chunk_size=500, overlap=50):
      tokens = tokenize(text)
      chunks = []
      for i in range(0, len(tokens), chunk_size - overlap):
          chunk_tokens = tokens[i:i+chunk_size]
          chunks.append(detokenize(chunk_tokens))
      return chunks
  ```
- **Advantages**: Consistent chunk sizes, overlap preserves context
- **Disadvantages**: May split mid-sentence, mid-concept

##### **3. Recursive Character Splitting** (LangChain)
- **Method**: Attempt to split on paragraph, then sentence, then word boundaries
- **Implementation**:
  ```python
  from langchain.text_splitter import RecursiveCharacterTextSplitter
  
  splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000,
      chunk_overlap=200,
      separators=["\n\n", "\n", ". ", " ", ""]
  )
  chunks = splitter.split_text(document_text)
  ```
- **Advantages**: Balances semantic coherence and size consistency

##### **4. Document Structure Chunking**
- **Method**: Use document structure (headings, sections, code blocks)
- **Best For**: Structured documents (LaTeX, Markdown, DOCX with styles)

#### **Recommended Configuration**
```yaml
chunking:
  method: "semantic"  # semantic, fixed, recursive, structure
  max_chunk_size: 1000  # tokens
  min_chunk_size: 100  # tokens
  overlap: 200  # tokens (for fixed/recursive)
  respect_boundaries: true  # Don't split mid-sentence
  preserve_code_blocks: true
```

#### **Chunk Metadata**
```python
chunk_metadata = {
    'document_id': 'lecture_03.pdf',
    'document_title': 'Neural Networks Lecture',
    'section': 'Backpropagation',
    'page': 15,
    'chunk_index': 3,
    'total_chunks': 45,
    'type': 'lecture',  # lecture, lab, reading, etc.
    'difficulty': 'intermediate',
    'concepts': ['backpropagation', 'gradient descent', 'chain rule'],
    'source_file': 'uploads/lecture_03.pdf'
}
```

---

### Retrieval Strategies

#### **1. Semantic Search** (Primary)
- **Method**: Cosine similarity between query embedding and chunk embeddings
- **Process**:
  1. Embed user query
  2. Compute cosine similarity with all chunk embeddings
  3. Return top-k most similar chunks
- **Code**:
  ```python
  def semantic_search(query, k=5):
      query_embedding = embedding_model.encode([query])
      results = collection.query(
          query_embeddings=query_embedding,
          n_results=k,
          include=['documents', 'metadatas', 'distances']
      )
      return results
  ```
- **Advantages**: Finds semantically similar content, not just keyword matches
- **Example**:
  - Query: "How do neural networks learn?"
  - Retrieves chunks about backpropagation, gradient descent, training

#### **2. Hybrid Search** (Semantic + Keyword)
- **Method**: Combine semantic similarity with keyword matching
- **Implementation**:
  ```python
  def hybrid_search(query, k=5):
      # Semantic search
      semantic_results = semantic_search(query, k=k*2)
      
      # Keyword search (BM25)
      keyword_results = bm25_search(query, k=k*2)
      
      # Merge and re-rank
      combined = merge_results(semantic_results, keyword_results)
      reranked = rerank(combined, query)
      
      return reranked[:k]
  ```
- **Advantages**: Captures both meaning and specific terms
- **Best For**: Technical queries with specific terminology

#### **3. Metadata Filtering**
- **Method**: Pre-filter by metadata before semantic search
- **Use Cases**:
  - "Search only lecture notes" → `type='lecture'`
  - "Search intermediate content" → `difficulty='intermediate'`
  - "Search module 3" → `module_id='mod_3'`
- **Code**:
  ```python
  results = collection.query(
      query_embeddings=query_embedding,
      n_results=k,
      where={"type": "lecture", "difficulty": "intermediate"}
  )
  ```

#### **4. Re-ranking**
- **Purpose**: Improve relevance of retrieved chunks
- **Methods**:
  - **Cross-Encoder**: Fine-tuned model for relevance scoring
  - **LLM Re-ranking**: Use LLM to score relevance
  - **Diversity Re-ranking**: Ensure diverse results (not all from same doc)
- **Implementation**:
  ```python
  from sentence_transformers import CrossEncoder
  
  reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
  
  def rerank(query, candidates):
      pairs = [[query, candidate] for candidate in candidates]
      scores = reranker.predict(pairs)
      ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
      return [candidate for candidate, score in ranked]
  ```

#### **Recommended Strategy**
```yaml
retrieval:
  primary_method: "hybrid"  # semantic, hybrid, keyword
  top_k: 5
  enable_metadata_filtering: true
  enable_reranking: true
  reranker_model: "cross-encoder/ms-marco-MiniLM-L-6-v2"
  diversity_penalty: 0.3  # Penalize multiple chunks from same doc
```

---

## Chat with Sources (NotebookLM Style)

### Interface: Streamlit Chat UI

#### **Chat Interface Features**
```python
import streamlit as st

st.title("💬 Chat with Your Course Materials")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show sources for assistant messages
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source['title']}** (Page {source['page']})")
                    st.markdown(f"> {source['snippet']}")

# User input
if prompt := st.chat_input("Ask a question about your materials..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response
    response, sources = generate_response(prompt)
    
    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "sources": sources
    })
```

#### **UI Elements**
- **Chat History**: Scrollable conversation log
- **User Input**: Text input at bottom
- **Source Citations**: Expandable sections showing source snippets
- **Suggested Questions**: Pre-generated questions for exploration
- **Clear Chat**: Reset conversation
- **Export Chat**: Download conversation as Markdown/PDF

---

### Capabilities

#### **1. Ask Questions About Ingested Materials**
- **Example Questions**:
  - "What is backpropagation?"
  - "How do I implement a neural network in Python?"
  - "What are the main topics covered in module 3?"
  - "Explain the difference between supervised and unsupervised learning"

#### **2. Multi-Document Synthesis**
- **Capability**: Synthesize information from multiple sources
- **Example**:
  - Query: "What are the pros and cons of neural networks?"
  - Answer synthesizes from:
    - Lecture notes (pros: universal approximation, learns features)
    - Tutorial (cons: requires lots of data, computationally expensive)
    - Article (pros/cons: interpretability challenges)
- **Implementation**:
  ```python
  def multi_doc_synthesis(query):
      # Retrieve from multiple documents
      results = retrieve(query, k=10)
      
      # Group by document
      by_doc = group_by_document(results)
      
      # Generate synthesis
      prompt = f"""
      Question: {query}
      
      Information from multiple sources:
      {format_sources(by_doc)}
      
      Synthesize a comprehensive answer that:
      1. Integrates information from all sources
      2. Highlights agreements and disagreements
      3. Cites each source
      """
      
      return llm_generate(prompt)
  ```

#### **3. Citation Tracking**
- **Requirement**: Every answer must cite source documents
- **Citation Format**:
  ```
  "Neural networks use backpropagation for training (Source: Lecture 3, 
  page 15). This involves computing gradients using the chain rule 
  (Source: Tutorial 2, section 2.3)."
  ```
- **Implementation**:
  ```python
  def generate_with_citations(query, retrieved_chunks):
      context = "\n\n".join([
          f"[Source {i+1}: {chunk['metadata']['title']}, page {chunk['metadata']['page']}]\n{chunk['text']}"
          for i, chunk in enumerate(retrieved_chunks)
      ])
      
      prompt = f"""
      Answer this question using ONLY the provided sources. 
      Cite sources inline using format: (Source: [title], page [num])
      
      Question: {query}
      
      Sources:
      {context}
      
      Answer:
      """
      
      return llm_generate(prompt)
  ```

#### **4. Follow-up Questions**
- **Capability**: Maintain conversation context for follow-ups
- **Example**:
  ```
  User: "What is backpropagation?"
  AI: "Backpropagation is an algorithm for training neural networks... (Source: Lecture 3)"
  
  User: "Can you explain it with an example?"
  AI: "Sure! Here's an example from the materials... (Source: Tutorial 2)"
  
  User: "How is it different from forward propagation?"
  AI: "While forward propagation computes outputs... (Source: Lecture 3, page 12)"
  ```
- **Implementation**: 
  - Store conversation history
  - Use history to understand context
  - Reformulate query based on history

#### **5. Clarification Requests**
- **Capability**: AI asks for clarification when query is ambiguous
- **Example**:
  ```
  User: "Tell me about networks"
  AI: "I found information about several topics:
       1. Neural Networks (machine learning)
       2. Computer Networks (networking course)
       Which would you like to know about?"
  
  User: "Neural networks"
  AI: "Neural networks are computational models... (Source: Lecture 1)"
  ```
- **Implementation**:
  ```python
  def detect_ambiguity(query, results):
      # Cluster results by topic
      topics = cluster_by_topic(results)
      
      if len(topics) > 1:
          return {
              'ambiguous': True,
              'topics': topics,
              'clarification': f"I found {len(topics)} topics related to '{query}'. Which did you mean?"
          }
      return {'ambiguous': False}
  ```

---

### LLM Integration (OLLAMA)

#### **Model Selection**
```yaml
rag_chat:
  default_model: "llama3.2:3b"  # Balanced speed/quality
  large_model: "llama3.1:8b"  # For complex synthesis
  use_large_for_synthesis: true
```

#### **Context Building**
```python
def build_context(query, retrieved_chunks, conversation_history):
    # Conversation context (last 3 turns)
    history_context = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in conversation_history[-3:]
    ])
    
    # Retrieved chunks context
    sources_context = "\n\n".join([
        f"[Source {i+1}: {chunk['metadata']['title']}, "
        f"page {chunk['metadata']['page']}]\n{chunk['text']}"
        for i, chunk in enumerate(retrieved_chunks)
    ])
    
    # System prompt
    system_prompt = """
    You are a helpful AI assistant for a course on machine learning.
    Answer questions using ONLY the provided source materials.
    Always cite your sources using the format: (Source: [title], page [num])
    If the answer isn't in the sources, say "I don't find that information in the materials."
    Be concise but thorough.
    """
    
    # User prompt
    user_prompt = f"""
    Previous conversation:
    {history_context}
    
    Current question: {query}
    
    Available sources:
    {sources_context}
    
    Please answer the question using the sources above.
    """
    
    return system_prompt, user_prompt
```

#### **Answer Generation**
```python
def generate_answer(query, conversation_history=[]):
    # Retrieve relevant chunks
    retrieved = retrieve(query, k=5)
    
    # Build context
    system_prompt, user_prompt = build_context(
        query, retrieved, conversation_history
    )
    
    # Generate with OLLAMA
    response = ollama.generate(
        model="llama3.2:3b",
        system=system_prompt,
        prompt=user_prompt,
        options={
            'temperature': 0.3,  # Low temperature for factual accuracy
            'top_p': 0.9,
            'num_ctx': 4096  # Context window size
        }
    )
    
    # Extract citations
    citations = extract_citations(response, retrieved)
    
    return {
        'answer': response['response'],
        'sources': citations,
        'retrieved_chunks': retrieved
    }
```

#### **Source Attribution**
```python
def extract_citations(response_text, retrieved_chunks):
    citations = []
    
    # Regex to find citations in response
    citation_pattern = r'\(Source: ([^,]+), page (\d+)\)'
    matches = re.findall(citation_pattern, response_text)
    
    for title, page in matches:
        # Find matching chunk
        for chunk in retrieved_chunks:
            if (chunk['metadata']['title'] == title and 
                chunk['metadata']['page'] == int(page)):
                citations.append({
                    'title': title,
                    'page': int(page),
                    'snippet': chunk['text'][:200] + '...',
                    'document_id': chunk['metadata']['document_id']
                })
                break
    
    return citations
```

---

### Example Interactions

#### **Example 1: Concept Explanation**
```
User: "What are the main concepts in machine learning covered in these materials?"

AI: "Based on the materials, the main machine learning concepts are:

1. **Supervised Learning** - Training models with labeled data to make predictions. 
   This includes regression and classification tasks. (Source: ML Basics Lecture, page 5)

2. **Unsupervised Learning** - Finding patterns in unlabeled data through clustering 
   and dimensionality reduction. (Source: ML Basics Lecture, page 12)

3. **Neural Networks** - Computational models inspired by biological neurons, capable 
   of learning complex patterns. (Source: Neural Networks Lecture, page 3)

4. **Deep Learning** - A subset of machine learning using multi-layer neural networks 
   to learn hierarchical representations. (Source: Deep Learning Module, page 1)

5. **Backpropagation** - The algorithm for training neural networks by computing 
   gradients through the chain rule. (Source: Neural Networks Lecture, page 15)

Would you like me to explain any of these concepts in more detail?"

📚 Sources (expandable):
- ML Basics Lecture (pages 5, 12)
- Neural Networks Lecture (pages 3, 15)
- Deep Learning Module (page 1)
```

#### **Example 2: Implementation Question**
```
User: "How does the professor explain neural networks?"

AI: "The professor uses several approaches to explain neural networks:

1. **Biological Analogy**: Neural networks are compared to biological neurons in the brain, 
   with artificial neurons mimicking the behavior of real neurons. (Source: Neural Networks 
   Lecture, page 3)

2. **Mathematical Foundation**: They're described as functions that compute weighted sums 
   of inputs and apply activation functions. The mathematical formulation is: 
   y = f(Σ(w_i * x_i) + b). (Source: Neural Networks Lecture, page 5)

3. **Visual Representation**: The lecture includes diagrams showing layers of interconnected 
   nodes, illustrating how information flows from input to output. (Source: Neural Networks 
   Lecture, page 4, Figure 1)

4. **Practical Example**: A step-by-step Python implementation is provided using NumPy to 
   build a simple 2-layer network. (Source: Neural Networks Tutorial, section 2.1)

The professor emphasizes that neural networks are 'universal function approximators' 
capable of learning any continuous function given sufficient data and neurons. 
(Source: Neural Networks Lecture, page 8)"

📚 Sources:
- Neural Networks Lecture (pages 3-8)
- Neural Networks Tutorial (section 2.1)
```

#### **Example 3: Comparison Question**
```
User: "What's the difference between supervised and unsupervised learning?"

AI: "The materials explain the key differences as:

**Supervised Learning:**
- Uses **labeled data** where both inputs and correct outputs are provided during training
- Goal is to learn a mapping from inputs to outputs to make predictions on new data
- Examples include classification (predicting categories) and regression (predicting 
  continuous values)
- Common algorithms: Linear Regression, Logistic Regression, Neural Networks
(Source: ML Basics Lecture, pages 5-7)

**Unsupervised Learning:**
- Uses **unlabeled data** where only inputs are provided, without corresponding outputs
- Goal is to discover hidden patterns, structures, or relationships in the data
- Examples include clustering (grouping similar items) and dimensionality reduction 
  (reducing number of features)
- Common algorithms: K-Means, PCA, Autoencoders
(Source: ML Basics Lecture, pages 12-14)

The professor notes that supervised learning is like learning with a teacher who provides 
correct answers, while unsupervised learning is like learning by finding patterns on your 
own. (Source: ML Basics Lecture, page 14)"

📚 Sources:
- ML Basics Lecture (pages 5-7, 12-14)
```

#### **Example 4: Follow-up Context**
```
User: "What is backpropagation?"

AI: "Backpropagation is an algorithm for training neural networks by efficiently computing 
gradients of the loss function with respect to the network's weights. It works by:

1. Computing the output of the network (forward pass)
2. Calculating the error between prediction and actual value
3. Propagating this error backward through the network layer by layer
4. Using the chain rule from calculus to compute gradients for each weight
5. Updating weights using these gradients to minimize the error

(Source: Neural Networks Lecture, pages 15-18)"

User: "Can you show me the mathematical formula?"

AI: "Yes! The key formula for backpropagation is based on the chain rule. For a weight w 
connecting neurons in adjacent layers:

∂L/∂w = ∂L/∂a * ∂a/∂z * ∂z/∂w

Where:
- L is the loss function
- a is the activation of the next layer
- z is the weighted sum (before activation)
- w is the weight we're updating

For the output layer:
∂L/∂w_output = (predicted - actual) * x

For hidden layers:
∂L/∂w_hidden = ∂L/∂a_next * activation_derivative(z) * x

(Source: Neural Networks Lecture, page 16, Equations 3.1-3.3)

The tutorial also provides a Python implementation of these formulas if you'd like to see 
the code. (Source: Neural Networks Tutorial, section 3.2)"

User: "Yes, show me the code"

AI: "Here's the Python implementation from the tutorial:

```python
def backpropagation(X, y, weights, activations):
    # Output layer gradient
    output_error = activations[-1] - y
    output_delta = output_error * sigmoid_derivative(activations[-1])
    
    # Hidden layer gradient (example for 1 hidden layer)
    hidden_error = output_delta.dot(weights['output'].T)
    hidden_delta = hidden_error * sigmoid_derivative(activations[0])
    
    # Update weights
    weights['output'] -= learning_rate * activations[0].T.dot(output_delta)
    weights['hidden'] -= learning_rate * X.T.dot(hidden_delta)
    
    return weights
```

This code shows how gradients are computed for both output and hidden layers, then used 
to update weights. The sigmoid_derivative function computes the derivative of the activation 
function. (Source: Neural Networks Tutorial, section 3.2, Code Listing 3.1)"
```

---

### Advanced Features

#### **Suggested Questions**
Generate questions users might want to ask:
```python
def generate_suggested_questions(document_summaries):
    prompt = f"""
    Based on these course materials, generate 5 questions a learner might ask:
    
    Materials: {document_summaries}
    
    Generate questions like:
    - "What is [concept]?"
    - "How do I [task]?"
    - "What's the difference between [A] and [B]?"
    - "Why do we use [technique]?"
    """
    
    return llm_generate(prompt)
```

Display in UI:
```python
st.subheader("💡 Suggested Questions")
for question in suggested_questions:
    if st.button(question):
        # Automatically ask this question
        handle_query(question)
```

#### **Chat History Export**
```python
def export_chat_history(messages, format='markdown'):
    if format == 'markdown':
        output = "# Chat History\n\n"
        for msg in messages:
            output += f"**{msg['role'].title()}**: {msg['content']}\n\n"
            if 'sources' in msg:
                output += "**Sources:**\n"
                for source in msg['sources']:
                    output += f"- {source['title']}, page {source['page']}\n"
                output += "\n"
        return output
    
    elif format == 'json':
        return json.dumps(messages, indent=2)
```

#### **Conversation Persistence**
```python
# Save conversation to database
def save_conversation(session_id, messages):
    db.execute("""
        INSERT INTO conversations (session_id, messages, created_at)
        VALUES (?, ?, ?)
    """, (session_id, json.dumps(messages), datetime.now()))

# Load conversation
def load_conversation(session_id):
    result = db.execute("""
        SELECT messages FROM conversations WHERE session_id = ?
    """, (session_id,)).fetchone()
    return json.loads(result[0]) if result else []
```

---

## System Integration

### Indexing Pipeline
```python
def index_document(parsed_document):
    # 1. Chunk document
    chunks = chunk_document(parsed_document)
    
    # 2. Generate embeddings
    texts = [chunk['text'] for chunk in chunks]
    embeddings = embedding_model.encode(texts)
    
    # 3. Prepare metadata
    metadatas = [chunk['metadata'] for chunk in chunks]
    
    # 4. Add to ChromaDB
    collection.add(
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
        ids=[f"{parsed_document.id}_chunk_{i}" for i in range(len(chunks))]
    )
    
    print(f"Indexed {len(chunks)} chunks from {parsed_document.filename}")
```

### Query Pipeline
```
User Query → Embedding → Retrieval (ChromaDB) → Re-ranking → 
Context Building → LLM Generation → Citation Extraction → Response
```

### Performance Optimization
```yaml
performance:
  batch_embedding_size: 32  # Embed multiple chunks at once
  cache_embeddings: true  # Cache frequently accessed embeddings
  max_context_chunks: 5  # Limit chunks sent to LLM
  enable_caching: true  # Cache LLM responses for common queries
  async_indexing: true  # Index new documents asynchronously
```

---

## Configuration

### Complete RAG Configuration
```yaml
rag_system:
  # Vector Database
  vector_db:
    type: "chromadb"
    persist_directory: "./chroma_db"
    collection_name: "course_materials"
  
  # Embedding Model
  embedding:
    model: "all-MiniLM-L6-v2"  # or "all-mpnet-base-v2"
    device: "cpu"  # or "cuda"
    batch_size: 32
  
  # Chunking
  chunking:
    method: "semantic"
    max_chunk_size: 1000
    min_chunk_size: 100
    overlap: 200
  
  # Retrieval
  retrieval:
    strategy: "hybrid"  # semantic, hybrid, keyword
    top_k: 5
    enable_reranking: true
    reranker_model: "cross-encoder/ms-marco-MiniLM-L-6-v2"
  
  # LLM
  llm:
    provider: "ollama"
    model: "llama3.2:3b"
    temperature: 0.3
    max_tokens: 1000
    context_window: 4096
  
  # Chat
  chat:
    enable_history: true
    history_length: 10  # Number of turns to keep
    enable_citations: true
    citation_format: "(Source: {title}, page {page})"
    enable_suggested_questions: true
```

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Design Specification (Not Implemented)
