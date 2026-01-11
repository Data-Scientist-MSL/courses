# Building a Personal Knowledge Assistant with RAG

## 🎯 Objective
Create your own "second brain" - an AI assistant that can answer questions based on your personal documents, notes, and knowledge base.

## 🛠️ Tech Stack
- **LangChain**: Document processing and chaining
- **ChromaDB**: Vector database for semantic search
- **OLLAMA**: Local LLM (Llama 3 or Mistral)
- **Sentence Transformers**: Generate embeddings

## 📚 Step-by-Step Implementation

### Step 1: Collect Your Knowledge Base

```python
import os
from pathlib import Path

# Organize your documents
knowledge_base = {
    'notes': Path('./my_notes'),
    'pdfs': Path('./research_papers'),
    'articles': Path('./saved_articles'),
    'code': Path('./projects')
}

# Supported formats: .txt, .md, .pdf, .docx, .py, .js
```

### Step 2: Load and Process Documents

```python
from langchain.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load all documents
loaders = [
    DirectoryLoader('./my_notes', glob="**/*.md", loader_cls=UnstructuredMarkdownLoader),
    DirectoryLoader('./my_notes', glob="**/*.txt", loader_cls=TextLoader),
    DirectoryLoader('./research_papers', glob="**/*.pdf", loader_cls=PyPDFLoader),
]

documents = []
for loader in loaders:
    documents.extend(loader.load())

print(f"Loaded {len(documents)} documents")

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\\n\\n", "\\n", ". ", " ", ""]
)

chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")
```

### Step 3: Create Embeddings and Vector Store

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Use local embedding model (free!)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'}  # or 'cuda' if you have GPU
)

# Create persistent vector database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# Save for later use
vectorstore.persist()
```

### Step 4: Connect to OLLAMA

```python
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# Initialize OLLAMA
llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434"
)

# Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)
```

### Step 5: Query Your Knowledge Base

```python
def ask_question(question):
    """Ask a question and get an answer with sources"""
    result = qa_chain({"query": question})
    
    print(f"Question: {question}")
    print(f"\\nAnswer: {result['result']}")
    print(f"\\nSources:")
    for i, doc in enumerate(result['source_documents'], 1):
        print(f"{i}. {doc.metadata.get('source', 'Unknown')}")
    
    return result

# Example queries
ask_question("What did I learn about transformers?")
ask_question("Summarize my notes on machine learning")
ask_question("What are my TODO items from project X?")
```

### Step 6: Build Interactive Interface

```python
import streamlit as st

st.title("🧠 Personal Knowledge Assistant")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Chat interface
user_input = st.text_input("Ask me anything from your knowledge base:")

if user_input:
    with st.spinner("Searching knowledge base..."):
        result = qa_chain({"query": user_input})
        
        # Display answer
        st.write("### Answer")
        st.write(result['result'])
        
        # Display sources
        st.write("### Sources")
        for doc in result['source_documents']:
            with st.expander(doc.metadata.get('source', 'Source')):
                st.write(doc.page_content[:500])
        
        # Add to history
        st.session_state.chat_history.append({
            'question': user_input,
            'answer': result['result']
        })

# Show chat history
if st.session_state.chat_history:
    st.write("### Chat History")
    for chat in reversed(st.session_state.chat_history[-5:]):
        st.write(f"**Q:** {chat['question']}")
        st.write(f"**A:** {chat['answer']}")
        st.divider()
```

## 🚀 Advanced Features

### 1. Auto-Update on New Documents

```python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class KnowledgeBaseWatcher(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(('.md', '.txt', '.pdf')):
            print(f"New file detected: {event.src_path}")
            # Process and add to vector store
            self.add_to_vectorstore(event.src_path)

observer = Observer()
observer.schedule(KnowledgeBaseWatcher(), path='./my_notes', recursive=True)
observer.start()
```

### 2. Semantic Search with Filters

```python
# Search with metadata filters
results = vectorstore.similarity_search(
    "machine learning concepts",
    k=5,
    filter={"type": "notes", "year": 2024}
)
```

### 3. Multi-Modal Knowledge Base

```python
# Include code snippets with syntax highlighting
from langchain.document_loaders import PythonLoader

code_docs = DirectoryLoader(
    './my_code',
    glob="**/*.py",
    loader_cls=PythonLoader
).load()
```

## 💡 Use Cases

1. **Research Assistant**: Query academic papers and notes
2. **Project Memory**: Remember decisions and design choices
3. **Learning Journal**: Review what you've learned
4. **Meeting Notes**: Find action items and discussions
5. **Code Reference**: Search through your projects

## 🎯 Best Practices

1. **Organize documents**: Use consistent folder structure
2. **Add metadata**: Include dates, tags, categories
3. **Regular updates**: Set up automatic indexing
4. **Chunk size**: Experiment with 500-1500 characters
5. **Embeddings**: Use domain-specific models if available

## 📊 Performance Optimization

```python
# Use faster retrieval
retriever = vectorstore.as_retriever(
    search_type="mmr",  # Maximal Marginal Relevance
    search_kwargs={
        "k": 5,
        "fetch_k": 20,
        "lambda_mult": 0.5
    }
)

# Cache embeddings
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()
```

## 🔒 Privacy & Security

- ✅ 100% local - no data sent to cloud
- ✅ OLLAMA runs on your machine
- ✅ Embeddings generated locally
- ✅ Full control over your data

## 📚 Resources

- **LangChain Docs**: langchain.readthedocs.io
- **ChromaDB Guide**: docs.trychroma.com
- **OLLAMA Models**: ollama.ai/library

## 💰 Cost Analysis

**Cloud Alternative (e.g., Notion AI, ChatGPT Plus):**
- $10-20/month subscription
- Limited queries
- Data on third-party servers

**This Solution:**
- $0 - Completely free
- Unlimited queries
- Full privacy and control

---

*Built with love for knowledge workers who want to augment their cognition without sacrificing privacy or paying monthly fees!* 🚀
