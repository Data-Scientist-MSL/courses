# 🤖 AI Instructor Guide - OLLAMA Integration

This guide explains how to use OLLAMA as your personal AI tutor for data science learning.

---

## 🎯 Overview

OLLAMA enables running large language models locally on your machine, providing:
- **Privacy**: All processing happens locally
- **Zero cost**: No API fees
- **Always available**: 24/7 access without rate limits
- **Customizable**: Use any open-source LLM

---

## 🚀 Quick Start

### 1. Install OLLAMA

**Mac/Linux**:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows**:
Download from [ollama.ai/download](https://ollama.ai/download)

**Docker** (included in docker-compose):
```bash
docker-compose up -d ollama
```

### 2. Download Models

```bash
# General tutoring (recommended first)
ollama pull llama3

# Code assistance
ollama pull codellama

# Fast responses
ollama pull mistral

# Lightweight option
ollama pull phi3
```

### 3. Test Installation

```bash
# Interactive chat
ollama run llama3

# API test
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Explain gradient descent in simple terms."
}'
```

---

## 🧠 Available Models

### Llama 3 (8B) - General Purpose ⭐
- **Size**: 4.7GB
- **Best for**: General tutoring, explanations, Q&A
- **Speed**: Moderate
- **Quality**: Excellent

**Use cases**:
- Concept explanations
- Study help
- Project brainstorming

**Example**:
```bash
ollama run llama3 "Explain the bias-variance tradeoff"
```

---

### CodeLlama (13B) - Code Expert 💻
- **Size**: 7.3GB  
- **Best for**: Code generation, debugging, review
- **Speed**: Slower but accurate
- **Quality**: Superior for code

**Use cases**:
- Code completion
- Bug finding
- Code explanation

**Example**:
```bash
ollama run codellama "Write a Python function to implement k-means clustering"
```

---

### Mistral (7B) - Fast Inference ⚡
- **Size**: 4.1GB
- **Best for**: Quick answers, simple tasks
- **Speed**: Fast
- **Quality**: Good

**Use cases**:
- Quick questions
- Simple explanations
- Resource-constrained environments

**Example**:
```bash
ollama run mistral "What is a neural network?"
```

---

### Phi-3 (3.8B) - Lightweight 🪶
- **Size**: 2.3GB
- **Best for**: Low-resource devices
- **Speed**: Very fast
- **Quality**: Decent

**Use cases**:
- Laptops with limited RAM
- Quick lookups
- Basic tutoring

---

## 📚 Using OLLAMA in Learning

### 1. Concept Clarification

```python
import requests

def ask_tutor(question, model="llama3"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": f"As a data science tutor, explain: {question}",
        "stream": False
    })
    return response.json()['response']

# Usage
explanation = ask_tutor("What is backpropagation?")
print(explanation)
```

### 2. Code Review

```python
def review_code(code, model="codellama"):
    prompt = f"""Review this code and suggest improvements:

{code}

Provide:
1. Code quality assessment
2. Potential bugs
3. Performance improvements
4. Best practices
"""
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']

# Usage
my_code = '''
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model
'''
feedback = review_code(my_code)
```

### 3. Lab Assistance

```python
def get_hint(lab_name, stuck_on, model="llama3"):
    prompt = f"""I'm working on {lab_name} and stuck on: {stuck_on}

Provide a hint without giving the full solution."""
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']

# Usage
hint = get_hint(
    "Transformer Architecture Lab",
    "Understanding multi-head attention dimensions"
)
```

### 4. Quiz Generation

```python
def generate_quiz(topic, num_questions=5, model="llama3"):
    prompt = f"""Create {num_questions} multiple choice questions about {topic}.

Format each question as:
Q: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [correct letter]
Explanation: [why this is correct]
"""
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']

# Usage
quiz = generate_quiz("Convolutional Neural Networks", 3)
```

---

## 🎓 Lecture Generation

### Generate Slides

```python
# See: 03_AI_Instructor_System/lecture_generator/generate_slides.py

def generate_lecture_slides(topic, level="intermediate", format="markdown"):
    prompt = f"""Create a comprehensive lecture on {topic} for {level} level.

Include:
1. Learning objectives (3-5)
2. Key concepts with explanations
3. Visual diagram descriptions
4. Code examples
5. Practice exercises
6. Summary

Format: {format}
"""
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']

# Usage
slides = generate_lecture_slides("Transformer Architecture", "intermediate")
```

### Create Diagrams

```python
# Generate Mermaid diagram code
def generate_diagram(concept, diagram_type="flowchart"):
    prompt = f"""Create a {diagram_type} diagram for {concept} in Mermaid syntax.

Return only the Mermaid code, starting with ```mermaid
"""
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']

# Usage
diagram = generate_diagram("RAG Pipeline", "flowchart")
```

---

## 🔧 Advanced Usage

### Streaming Responses

```python
def stream_response(prompt, model="llama3"):
    """Stream response word by word"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt},
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            import json
            chunk = json.loads(line)
            if 'response' in chunk:
                print(chunk['response'], end='', flush=True)
                
stream_response("Explain transformers")
```

### Custom System Prompts

```python
def ask_with_context(question, context, model="llama3"):
    """Ask question with specific context"""
    full_prompt = f"""Context: {context}

Question: {question}

Provide a detailed answer based on the context."""
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": full_prompt,
        "stream": False
    })
    return response.json()['response']

# Usage
context = "You are a patient tutor helping beginners learn machine learning."
answer = ask_with_context("What is overfitting?", context)
```

### RAG Integration

```python
from langchain.llms import Ollama
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# Setup
llm = Ollama(model="llama3", base_url="http://localhost:11434")
embeddings = HuggingFaceEmbeddings()

# Create knowledge base
vectorstore = Chroma.from_documents(
    documents=course_documents,
    embedding=embeddings
)

# Create QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Ask questions
result = qa_chain("How do I implement attention mechanism?")
print(result['result'])
```

---

## 🎯 Best Practices

### 1. Model Selection
- **Quick questions**: Use Mistral or Phi-3
- **Deep explanations**: Use Llama 3
- **Code tasks**: Use CodeLlama
- **Low RAM**: Use Phi-3

### 2. Prompt Engineering

**Good prompts**:
```
"Explain gradient descent step by step with a simple example"
"Debug this code and explain the error: [code]"
"Compare and contrast CNNs vs RNNs for time series"
```

**Poor prompts**:
```
"Tell me about ML"  # Too vague
"Code"  # No context
```

### 3. Context Management
- Keep conversation focused
- Provide relevant context
- Break complex questions into parts

### 4. Resource Management
```bash
# Check running models
ollama ps

# Stop a model to free RAM
ollama stop llama3

# List downloaded models
ollama list
```

---

## 🐛 Troubleshooting

### Model Won't Download
```bash
# Check disk space
df -h

# Try smaller model
ollama pull phi3

# Resume interrupted download
ollama pull llama3
```

### Out of Memory
```bash
# Use smaller model
ollama pull phi3

# Or quantized version
ollama pull llama3:8b-instruct-q4_0
```

### Slow Responses
```bash
# Use faster model
ollama pull mistral

# Enable GPU (if available)
# OLLAMA automatically uses GPU when available

# Check GPU usage
nvidia-smi  # For NVIDIA GPUs
```

### Connection Errors
```bash
# Check if OLLAMA is running
curl http://localhost:11434/api/tags

# Restart OLLAMA
ollama serve

# Check firewall settings
```

---

## 📊 Performance Optimization

### GPU Acceleration
OLLAMA automatically uses GPU when available. Check with:
```bash
ollama run llama3
# Look for "loaded model on GPU" message
```

### CPU Optimization
```bash
# Set thread count
export OLLAMA_NUM_THREADS=8

# Restart OLLAMA
ollama serve
```

### Memory Management
```bash
# Set context window size (lower = less RAM)
ollama run llama3 --ctx-size 2048

# Use quantized models
ollama pull llama3:8b-instruct-q4_0  # 4-bit quantization
```

---

## 🔗 Integration with Streamlit App

The Streamlit app includes built-in OLLAMA integration:

```python
# In streamlit_app/pages/04_ai_tutor.py
import streamlit as st
import requests

def chat_with_tutor(message):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": st.session_state.get("selected_model", "llama3"),
        "prompt": message,
        "stream": True
    })
    
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            yield chunk['response']

# UI
st.title("🤖 AI Tutor")
message = st.chat_input("Ask me anything about data science...")
if message:
    for chunk in chat_with_tutor(message):
        st.write(chunk, end='')
```

---

## 📚 Additional Resources

- [OLLAMA Documentation](https://github.com/ollama/ollama)
- [Model Library](https://ollama.ai/library)
- [LangChain Integration](https://python.langchain.com/docs/integrations/llms/ollama)
- [Community Models](https://ollama.ai/library)

---

## ✅ Checklist

- [ ] OLLAMA installed
- [ ] At least one model downloaded
- [ ] Test API connection
- [ ] Try code generation
- [ ] Integrate with learning workflow
- [ ] Experiment with different models
- [ ] Set up RAG for course content

---

**Last Updated**: January 2026  
**Version**: 2.0.0
