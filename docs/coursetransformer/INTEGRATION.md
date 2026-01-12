# CourseTransformer - Integration Specification

This document specifies how CourseTransformer integrates with external systems.

## Integration Overview

CourseTransformer integrates with:
1. **CoursesGTM** - Curriculum database and management system
2. **CoursePlayerApp** - Course delivery platform
3. **OLLAMA** - Local LLM provider
4. **Knowledge Base (RAG)** - Semantic search and fact-checking

## 1. CoursesGTM Integration

### Purpose
Export transformed courses to CoursesGTM database schema for management and access control.

### Schema Mapping

**Curriculum JSON Structure**:
```json
{
  "curriculum_id": "modern_ds_2026",
  "curriculum_name": "Modern Data Science & AI 2026",
  "version": "2.0.0",
  "tracks": [
    {
      "track_id": "foundations",
      "track_name": "Foundational Skills",
      "courses": [
        {
          "course_id": "01_modern_dev_environment",
          "course_name": "Modern Development Environment",
          "tier": "basic",
          "duration_hours": 6,
          "prerequisites": ["00_philosophy"],
          "description": "Set up a modern Python data science environment",
          "tags": ["python", "tools", "git", "docker"],
          "price_usd": 0,  # Basic tier is free
          "modules": [...]
        }
      ]
    }
  ]
}
```

**Tiers JSON**:
```json
{
  "tiers": [
    {
      "tier_id": "basic",
      "tier_name": "Basic",
      "price_monthly": 0,
      "features": ["Core courses", "Community access"],
      "course_count": 12
    },
    {
      "tier_id": "intermediate",
      "tier_name": "Intermediate",
      "price_monthly": 29,
      "features": ["All Basic", "Advanced courses", "Projects"],
      "course_count": 18
    },
    {
      "tier_id": "advanced",
      "tier_name": "Advanced",
      "price_monthly": 99,
      "features": ["All Intermediate", "Expert courses", "1-on-1 mentoring"],
      "course_count": 24
    }
  ]
}
```

### Export Agent Implementation

```python
def format_for_coursesgtm(approved_content: dict, curriculum_structure: dict) -> dict:
    """Format content for CoursesGTM"""
    output = {
        "curriculum": curriculum_structure,
        "tiers": generate_tier_structure(curriculum_structure),
        "metadata": generate_course_metadata(approved_content)
    }
    return output

def generate_tier_structure(curriculum: dict) -> dict:
    """Generate tiers.json from curriculum"""
    tiers = {"basic": [], "intermediate": [], "advanced": []}
    
    for track in curriculum["tracks"]:
        for course in track["courses"]:
            tier = course["tier"]
            tiers[tier].append(course["course_id"])
    
    return {
        "tiers": [
            {"tier_id": tier, "course_ids": course_list}
            for tier, course_list in tiers.items()
        ]
    }
```

### Validation

```python
import jsonschema

COURSESGTM_SCHEMA = {
    "type": "object",
    "required": ["curriculum_id", "curriculum_name", "tracks"],
    "properties": {
        "curriculum_id": {"type": "string"},
        "tracks": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["track_id", "courses"],
                "properties": {
                    "courses": {
                        "type": "array",
                        "items": {
                            "required": ["course_id", "tier", "duration_hours"],
                            "properties": {
                                "tier": {"enum": ["basic", "intermediate", "advanced"]}
                            }
                        }
                    }
                }
            }
        }
    }
}

def validate_coursesgtm_export(data: dict) -> bool:
    try:
        jsonschema.validate(instance=data, schema=COURSESGTM_SCHEMA)
        return True
    except jsonschema.ValidationError as e:
        print(f"Validation error: {e}")
        return False
```

---

## 2. CoursePlayerApp Integration

### Purpose
Package course content for delivery through CoursePlayerApp.

### Directory Structure

```
courses-v2/
├── curriculum.json                    # Course catalog
├── 00_Philosophy/
│   ├── manifest.json                  # Course manifest
│   ├── 01_Augmented_Human/
│   │   ├── slides/
│   │   │   ├── 01_ai_as_tool.html    # Converted from Marp
│   │   │   └── 01_ai_as_tool.pdf     # Printable version
│   │   ├── labs/
│   │   │   └── 01_intro_lab.ipynb
│   │   ├── quizzes/
│   │   │   └── quiz_01.json
│   │   └── assets/
│   │       ├── images/
│   │       └── datasets/
│   └── README.md
├── 01_Modern_Dev_Environment/
│   └── ...
└── assets/
    ├── global_stylesheets/
    ├── common_images/
    └── shared_datasets/
```

### Manifest Format

```json
{
  "course_id": "00_philosophy",
  "course_name": "Data Science Philosophy & Ethics",
  "version": "1.0.0",
  "tier": "basic",
  "modules": [
    {
      "module_id": "01_augmented_human",
      "module_name": "Augmented Human Approach",
      "lessons": [
        {
          "lesson_id": "01_ai_as_tool",
          "lesson_name": "AI as Tool, Not Replacement",
          "type": "lecture",
          "slides": "slides/01_ai_as_tool.html",
          "duration_minutes": 15,
          "learning_objectives": [
            "Understand augmented human philosophy",
            "Distinguish AI assistance from AI replacement"
          ]
        }
      ]
    }
  ],
  "total_duration_hours": 2,
  "prerequisites": [],
  "tags": ["philosophy", "ethics", "ai"],
  "authors": ["CourseTransformer"],
  "created_at": "2026-01-12T00:00:00Z"
}
```

### Content Conversion

```python
def convert_marp_to_html(marp_file: str) -> str:
    """Convert Marp markdown to HTML slides"""
    import subprocess
    
    output_file = marp_file.replace('.md', '.html')
    subprocess.run([
        'marp',
        marp_file,
        '--html',
        '--output', output_file
    ])
    return output_file

def package_for_courseplayerapp(content: dict, output_dir: str):
    """Package content for CoursePlayerApp"""
    for course in content['courses']:
        course_dir = Path(output_dir) / course['course_id']
        course_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert slides
        for slide in course.get('slides', []):
            if slide.endswith('.md'):
                convert_marp_to_html(slide)
        
        # Copy assets
        copy_assets(course.get('assets', []), course_dir / 'assets')
        
        # Generate manifest
        manifest = generate_manifest(course)
        with open(course_dir / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
```

---

## 3. OLLAMA Integration

### Purpose
Use OLLAMA as the local, privacy-first LLM provider.

### Model Selection Strategy

```python
MODEL_MAPPING = {
    "ingestion": "llama2:7b",      # Lightweight for extraction
    "analysis": "llama2:13b",       # Medium for reasoning
    "planning": "mixtral:8x7b",     # Heavy for complex planning
    "modernization": "codellama:13b",  # Specialized for code
    "generation": "mixtral:8x7b",   # Heavy for content creation
    "qa": "llama2:7b",              # Lightweight for checking
}

class OLLAMAClient:
    """Client for OLLAMA API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, prompt: str, agent_type: str) -> str:
        """Generate response using appropriate model"""
        model = MODEL_MAPPING.get(agent_type, "llama2:7b")
        
        import requests
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        
        return response.json()["response"]
    
    async def generate_async(self, prompt: str, agent_type: str) -> str:
        """Async generation"""
        import aiohttp
        model = MODEL_MAPPING.get(agent_type, "llama2:7b")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt}
            ) as resp:
                data = await resp.json()
                return data["response"]
```

### Context Window Management

```python
def manage_context_window(text: str, max_tokens: int = 4096) -> str:
    """Truncate text to fit in context window"""
    # Simple truncation (improve with smart chunking)
    estimated_tokens = len(text.split()) * 1.3  # Rough estimate
    if estimated_tokens > max_tokens:
        words = text.split()
        target_words = int(max_tokens / 1.3)
        return ' '.join(words[:target_words])
    return text
```

### Caching Strategy

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_llm_call(prompt_hash: str, model: str) -> str:
    """Cache LLM responses"""
    # Actual call would be made here
    return get_from_cache_or_generate(prompt_hash, model)

def generate_with_cache(prompt: str, agent_type: str) -> str:
    """Generate with caching"""
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    return cached_llm_call(prompt_hash, agent_type)
```

---

## 4. Knowledge Base (RAG) Integration

### Purpose
Provide semantic search and fact-checking capabilities using vector database.

### Architecture

```
Knowledge Base
├── Vector Store (ChromaDB)
│   ├── Course Content Embeddings
│   ├── Modern Best Practices
│   └── Reference Documentation
├── Embedding Model (sentence-transformers)
└── Query Interface
```

### Implementation

```python
import chromadb
from chromadb.config import Settings

class KnowledgeBase:
    """RAG system for CourseTransformer"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection(
            name="course_knowledge",
            metadata={"description": "Course content and best practices"}
        )
    
    def add_documents(self, documents: List[str], metadatas: List[dict]):
        """Add documents to knowledge base"""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
    
    def query(self, query_text: str, n_results: int = 5) -> List[dict]:
        """Query knowledge base"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return [
            {
                "document": doc,
                "metadata": meta,
                "distance": dist
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    
    def fact_check(self, claim: str) -> dict:
        """Fact-check a claim against knowledge base"""
        results = self.query(claim, n_results=3)
        
        # Use LLM to compare claim against retrieved docs
        context = "\n".join([r["document"] for r in results])
        prompt = f"""Fact-check this claim:
        
        Claim: {claim}
        
        Reference information:
        {context}
        
        Is the claim accurate? Provide verification."""
        
        # Call LLM (OLLAMA)
        verification = ollama_client.generate(prompt, "qa")
        
        return {
            "claim": claim,
            "verification": verification,
            "sources": results
        }
```

### Seeding Knowledge Base

```python
def seed_knowledge_base():
    """Seed KB with modern best practices"""
    kb = KnowledgeBase()
    
    documents = [
        "In 2026, Transformers are the foundation of modern NLP...",
        "MLOps involves model versioning with tools like MLflow and DVC...",
        "Docker containers ensure reproducibility in data science...",
        # ... more documents
    ]
    
    metadatas = [
        {"source": "Modern AI Practices", "year": 2026, "topic": "transformers"},
        {"source": "MLOps Guide", "year": 2026, "topic": "mlops"},
        {"source": "DevOps for DS", "year": 2026, "topic": "docker"},
    ]
    
    kb.add_documents(documents, metadatas)
```

---

## Integration Testing

```python
def test_coursesgtm_integration():
    """Test export to CoursesGTM"""
    content = {
        "curriculum_id": "test_curriculum",
        "tracks": [...]
    }
    
    formatted = format_for_coursesgtm(content, {})
    assert validate_coursesgtm_export(formatted)

def test_ollama_integration():
    """Test OLLAMA connection"""
    client = OLLAMAClient()
    response = client.generate("Test prompt", "analysis")
    assert len(response) > 0

def test_knowledge_base_integration():
    """Test RAG system"""
    kb = KnowledgeBase(persist_directory=":memory:")
    kb.add_documents(["Test document"], [{"source": "test"}])
    results = kb.query("Test query")
    assert len(results) > 0
```

---

This integration specification ensures CourseTransformer works seamlessly with all required external systems.
