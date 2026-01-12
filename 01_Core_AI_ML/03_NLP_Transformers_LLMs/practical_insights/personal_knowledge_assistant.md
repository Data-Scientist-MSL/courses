# Building a Personal Knowledge Assistant with RAG

## 🎯 Project Overview

Build your own AI-powered "second brain" that:
- Stores and indexes your notes, papers, and learning materials
- Answers questions using your personal knowledge base
- Runs locally with OLLAMA (privacy-first)
- Uses RAG (Retrieval-Augmented Generation) for accurate responses

## 🧠 What is RAG?

**Retrieval-Augmented Generation** combines:
1. **Retrieval**: Find relevant documents from your knowledge base
2. **Augmentation**: Add retrieved context to the prompt
3. **Generation**: LLM generates answer based on your documents

**Advantages**:
- No hallucinations (answers based on your data)
- Always up-to-date (add new documents anytime)
- Transparent (see which documents were used)
- Privacy-preserving (runs locally)

## 🏗️ Architecture

```
Your Documents → Chunking → Embeddings → Vector DB (Chroma)
                                              ↓
User Question → Embedding → Similarity Search → Top K Documents
                                                       ↓
                                            LLM (OLLAMA + Context)
                                                       ↓
                                                    Answer
```

## 🛠️ Implementation

### Step 1: Install Dependencies

```bash
pip install langchain chromadb sentence-transformers pypdf
```

### Step 2: Prepare Your Documents

```python
import os
from pathlib import Path
from langchain.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PDFLoader,
    UnstructuredMarkdownLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load documents from your knowledge base
def load_documents(directory="./my_knowledge"):
    """Load all documents from directory"""
    loaders = {
        '.txt': TextLoader,
        '.md': UnstructuredMarkdownLoader,
        '.pdf': PDFLoader,
    }
    
    documents = []
    
    for ext, loader_class in loaders.items():
        loader = DirectoryLoader(
            directory,
            glob=f"**/*{ext}",
            loader_cls=loader_class
        )
        documents.extend(loader.load())
    
    print(f"Loaded {len(documents)} documents")
    return documents

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

documents = load_documents()
texts = text_splitter.split_documents(documents)
print(f"Created {len(texts)} chunks")
```

### Step 3: Create Vector Database

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Vector database created!")
```

### Step 4: Set up OLLAMA LLM

```python
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# Initialize OLLAMA
llm = Ollama(
    model="llama3",
    base_url="http://localhost:11434"
)

# Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
    ),
    return_source_documents=True
)
```

### Step 5: Query Your Knowledge Base

```python
def ask_question(question):
    """Ask a question about your documents"""
    result = qa_chain({"query": question})
    
    print(f"Question: {question}")
    print(f"\nAnswer: {result['result']}")
    print("\nSources:")
    for i, doc in enumerate(result['source_documents'], 1):
        print(f"  {i}. {doc.metadata.get('source', 'Unknown')}")
    
    return result

# Usage
ask_question("What did I learn about transformers?")
ask_question("Summarize my notes on machine learning")
ask_question("What are the key concepts in deep learning?")
```

## 🎨 Complete Application

```python
"""
Personal Knowledge Assistant - Complete Implementation
"""

import os
from pathlib import Path
from langchain.document_loaders import DirectoryLoader, TextLoader, PDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.chains import RetrievalQA


class KnowledgeAssistant:
    def __init__(self, knowledge_dir, db_dir="./chroma_db"):
        self.knowledge_dir = knowledge_dir
        self.db_dir = db_dir
        self.vectorstore = None
        self.qa_chain = None
        
    def load_and_index(self):
        """Load documents and create vector database"""
        print("Loading documents...")
        
        # Load documents
        loader = DirectoryLoader(
            self.knowledge_dir,
            glob="**/*.md",
            loader_cls=TextLoader
        )
        documents = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        print(f"Loaded {len(documents)} documents, created {len(texts)} chunks")
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory=self.db_dir
        )
        
        print("Vector database created!")
        
    def setup_qa_chain(self, model="llama3"):
        """Set up question-answering chain"""
        llm = Ollama(model=model, base_url="http://localhost:11434")
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        
        print(f"QA chain ready with {model}!")
    
    def ask(self, question):
        """Ask a question"""
        if not self.qa_chain:
            raise ValueError("QA chain not set up. Call setup_qa_chain() first.")
        
        result = self.qa_chain({"query": question})
        
        return {
            'answer': result['result'],
            'sources': [doc.metadata.get('source') for doc in result['source_documents']]
        }
    
    def interactive(self):
        """Interactive chat loop"""
        print("\n🧠 Personal Knowledge Assistant")
        print("Ask questions about your documents. Type 'quit' to exit.\n")
        
        while True:
            question = input("You: ")
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            result = self.ask(question)
            print(f"\nAssistant: {result['answer']}")
            print(f"\nSources: {', '.join(result['sources'])}\n")


# Usage
if __name__ == "__main__":
    # Initialize assistant
    assistant = KnowledgeAssistant(
        knowledge_dir="./my_notes"  # Directory with your notes
    )
    
    # Load and index documents (do this once)
    assistant.load_and_index()
    
    # Setup QA chain
    assistant.setup_qa_chain(model="llama3")
    
    # Interactive mode
    assistant.interactive()
```

## 📚 What to Store

Great documents to add to your knowledge base:
- 📝 **Course notes**: Lectures, summaries
- 📄 **Papers**: Research papers you've read
- 📖 **Books**: Highlights and summaries
- 💡 **Ideas**: Project ideas, brainstorms
- 🔗 **Links**: Annotated bookmarks
- 📊 **Data**: Dataset descriptions, results

## 🎯 Use Cases

1. **Study Assistant**
   - "What did I learn about gradient descent?"
   - "Summarize my deep learning notes"

2. **Research Helper**
   - "Which papers discuss attention mechanisms?"
   - "What are the key findings from [author]?"

3. **Project Reference**
   - "How did I implement feature engineering last time?"
   - "What datasets are good for sentiment analysis?"

4. **Writing Aid**
   - "Find my notes on transformers for this blog post"
   - "What examples can I use for explaining CNNs?"

## 🚀 Enhancements

### 1. Add More Document Types

```python
# Add support for .docx, .html, etc.
from langchain.document_loaders import Docx2txtLoader, UnstructuredHTMLLoader
```

### 2. Improve Retrieval

```python
# Use hybrid search (semantic + keyword)
from langchain.retrievers import BM25Retriever, EnsembleRetriever

# Combine dense and sparse retrieval
```

### 3. Add Memory

```python
# Remember conversation context
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
```

### 4. Web Interface

```python
# Create Streamlit app
import streamlit as st

st.title("🧠 Personal Knowledge Assistant")
question = st.text_input("Ask a question:")

if question:
    result = assistant.ask(question)
    st.write(result['answer'])
    st.write("Sources:", result['sources'])
```

## 💡 Tips

1. **Organize documents**: Use clear filenames and folder structure
2. **Keep updated**: Regularly add new notes and papers
3. **Quality over quantity**: Well-written notes work better
4. **Experiment with chunking**: Try different chunk sizes
5. **Use metadata**: Add tags, dates, categories to documents

## 🔒 Privacy Benefits

- ✅ All processing happens locally
- ✅ No data sent to external APIs
- ✅ Full control over your knowledge
- ✅ Works offline (after setup)

## 📖 Next Steps

1. Create your knowledge directory
2. Add your first documents
3. Run the implementation
4. Ask questions and iterate
5. Expand with more document types

---

**This is the power of augmented intelligence!** 🚀

Your "second brain" that:
- Never forgets
- Finds connections you might miss
- Answers instantly
- Protects your privacy
