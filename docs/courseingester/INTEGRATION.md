# CourseIngester - Integration Specifications

## Overview

CourseIngester integrates with multiple systems and services to provide comprehensive functionality. This document specifies integration patterns for CourseTransformer, OLLAMA, and various external services.

**Design Philosophy**: Loose coupling, clear interfaces. Integrations should be pluggable and replaceable without affecting core functionality.

---

## Integration with CourseTransformer

### Purpose
Export enriched, organized content from CourseIngester to CourseTransformer for modernization, transformation, and interactive element generation.

### Export Format

#### **Directory Structure**
```
course_export/
├── metadata.json              # Course metadata
├── curriculum/
│   ├── structure.json         # Curriculum organization
│   ├── modules/
│   │   ├── module_01.json    # Module details
│   │   ├── module_02.json
│   │   └── ...
│   └── tracks.json           # Learning tracks
├── content/
│   ├── raw/                  # Original parsed documents
│   │   ├── lectures/
│   │   ├── tutorials/
│   │   ├── readings/
│   │   └── assessments/
│   └── processed/            # Processed content
│       ├── text/
│       ├── images/
│       ├── code/
│       └── tables/
├── knowledge/
│   ├── knowledge_graph.json  # Serialized KG
│   ├── concepts.json         # Concept definitions
│   ├── relationships.json    # Concept relationships
│   └── summaries.json        # Document summaries
├── enhancements/
│   ├── study_guides/
│   ├── flashcards/
│   ├── glossary.json
│   ├── timelines/
│   └── bibliography.json
├── rag/
│   ├── chroma_db/           # Vector database
│   ├── embeddings/
│   └── index_metadata.json
└── analytics/
    ├── difficulty_scores.json
    ├── gap_analysis.json
    └── statistics.json
```

#### **Metadata Schema**
```json
{
  "course_metadata": {
    "id": "ml_fundamentals_2024",
    "name": "Machine Learning Fundamentals",
    "version": "1.0",
    "author": "Dr. Jane Doe",
    "description": "Comprehensive introduction to machine learning",
    "created_at": "2024-01-15T10:00:00Z",
    "exported_from": "CourseIngester v1.0",
    "ingestion_mode": "standard",
    "total_documents": 45,
    "total_modules": 6,
    "estimated_duration_hours": 120
  },
  
  "source_files": {
    "total_files": 45,
    "by_type": {
      "pdf": 15,
      "video": 8,
      "notebook": 12,
      "code": 10
    },
    "upload_dates": ["2024-01-10", "2024-01-12", "2024-01-14"]
  },
  
  "processing_metadata": {
    "ingestion_date": "2024-01-15T10:00:00Z",
    "processing_time_seconds": 1800,
    "human_reviewed": true,
    "review_date": "2024-01-15T12:00:00Z"
  },
  
  "quality_metrics": {
    "parsing_success_rate": 0.96,
    "concept_extraction_confidence": 0.88,
    "knowledge_graph_completeness": 0.92,
    "duplicate_detection_precision": 0.94
  }
}
```

#### **Curriculum Structure Schema**
```json
{
  "curriculum": {
    "id": "ml_fundamentals_curriculum",
    "name": "ML Fundamentals Curriculum",
    "modules": [
      {
        "id": "mod_1",
        "number": 1,
        "name": "Python Fundamentals",
        "tier": "Basic",
        "duration_hours": 15,
        "learning_objectives": ["...", "..."],
        "prerequisites": [],
        "content_refs": {
          "lectures": ["doc_001", "doc_005"],
          "tutorials": ["doc_010", "doc_012"],
          "readings": ["doc_020"],
          "assessments": ["doc_030"]
        },
        "concepts": ["variables", "functions", "loops"],
        "difficulty_score": 3.2
      }
    ],
    "tracks": [
      {
        "id": "data_scientist",
        "name": "Data Scientist Track",
        "modules": ["mod_1", "mod_2", "mod_3"]
      }
    ],
    "learning_paths": [
      {
        "id": "linear_beginner",
        "name": "Linear Path",
        "sequence": ["mod_1", "mod_2", "mod_3", "mod_4", "mod_5", "mod_6"]
      }
    ]
  }
}
```

### Export API

```python
class CourseIngesterExporter:
    """Exports enriched content to CourseTransformer format"""
    
    def export(self, state: IngestionState, export_dir: str):
        """Export complete course package"""
        
        # Create directory structure
        self._create_directories(export_dir)
        
        # Export metadata
        self._export_metadata(state, export_dir)
        
        # Export curriculum structure
        self._export_curriculum(state, export_dir)
        
        # Export content
        self._export_content(state, export_dir)
        
        # Export knowledge graph
        self._export_knowledge(state, export_dir)
        
        # Export enhancements
        self._export_enhancements(state, export_dir)
        
        # Export RAG data
        self._export_rag(state, export_dir)
        
        # Export analytics
        self._export_analytics(state, export_dir)
        
        # Create manifest
        self._create_manifest(export_dir)
        
        return export_dir
    
    def _export_curriculum(self, state, export_dir):
        """Export curriculum structure"""
        curriculum_data = {
            'curriculum': {
                'id': state['workflow_id'],
                'modules': state['proposed_modules'],
                'tracks': state['proposed_tracks'],
                'learning_paths': state['learning_paths']
            }
        }
        
        with open(f"{export_dir}/curriculum/structure.json", 'w') as f:
            json.dump(curriculum_data, f, indent=2)
```

### CourseTransformer Import

```python
class CourseTransformerImporter:
    """Imports enriched content from CourseIngester"""
    
    def import_course(self, import_dir: str):
        """Import course package from CourseIngester"""
        
        # Load metadata
        metadata = self._load_metadata(import_dir)
        
        # Validate structure
        self._validate_structure(import_dir)
        
        # Import curriculum
        curriculum = self._import_curriculum(import_dir)
        
        # Import content
        content = self._import_content(import_dir)
        
        # Import knowledge graph
        kg = self._import_knowledge_graph(import_dir)
        
        # Import enhancements
        enhancements = self._import_enhancements(import_dir)
        
        # Import RAG data
        rag_data = self._import_rag(import_dir)
        
        return {
            'metadata': metadata,
            'curriculum': curriculum,
            'content': content,
            'knowledge': kg,
            'enhancements': enhancements,
            'rag': rag_data
        }
```

### Integration Points

**CourseIngester provides to CourseTransformer**:
- ✅ Organized curriculum structure (modules, tracks, paths)
- ✅ Parsed and cleaned content
- ✅ Knowledge graph with concept relationships
- ✅ Enriched metadata (difficulty, topics, concepts)
- ✅ Study aids (guides, flashcards, glossary)
- ✅ RAG-ready vector database

**CourseTransformer uses this to**:
- Modernize content (update code, examples)
- Transform formats (markdown → interactive)
- Generate interactive elements (quizzes, simulations)
- Create personalized learning paths
- Build LMS-compatible packages (SCORM, xAPI)

---

## Integration with OLLAMA

### Purpose
Use local LLM inference for semantic analysis, summarization, question generation, and chat functionality without requiring cloud APIs.

### Model Selection Strategy

```python
class OLLAMAModelSelector:
    """Select appropriate OLLAMA model for each task"""
    
    MODELS = {
        'lightweight': 'llama3.2:1b',    # Fast, low resource
        'medium': 'llama3.2:3b',          # Balanced
        'large': 'llama3.1:8b'            # High quality
    }
    
    TASK_MODELS = {
        'categorization': 'lightweight',
        'summarization': 'medium',
        'question_generation': 'medium',
        'study_guide_generation': 'large',
        'curriculum_design': 'large',
        'rag_chat': 'medium'
    }
    
    def select_model(self, task: str) -> str:
        """Select model for task"""
        model_size = self.TASK_MODELS.get(task, 'medium')
        return self.MODELS[model_size]
```

### OLLAMA Client

```python
import requests
import json

class OLLAMAClient:
    """Client for OLLAMA API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, model: str, prompt: str, system: str = None, 
                 temperature: float = 0.7, max_tokens: int = 1000):
        """Generate completion"""
        
        payload = {
            'model': model,
            'prompt': prompt,
            'system': system,
            'options': {
                'temperature': temperature,
                'num_predict': max_tokens
            }
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            stream=False
        )
        
        return response.json()['response']
    
    def embed(self, model: str, text: str):
        """Generate embeddings"""
        
        payload = {
            'model': model,
            'prompt': text
        }
        
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json=payload
        )
        
        return response.json()['embedding']
    
    def list_models(self):
        """List available models"""
        response = requests.get(f"{self.base_url}/api/tags")
        return response.json()['models']
```

### Usage Examples

```python
ollama = OLLAMAClient()

# Categorization (lightweight)
prompt = f"Categorize this content: {content_summary}"
category = ollama.generate(
    model="llama3.2:1b",
    prompt=prompt,
    temperature=0.3  # Low temp for factual task
)

# Summarization (medium)
prompt = f"Summarize this in 100 words: {content}"
summary = ollama.generate(
    model="llama3.2:3b",
    prompt=prompt,
    temperature=0.5
)

# Study guide generation (large)
prompt = f"Create a comprehensive study guide: {module_content}"
study_guide = ollama.generate(
    model="llama3.1:8b",
    prompt=prompt,
    temperature=0.7,
    max_tokens=2000
)
```

### Context Window Management

```python
def chunk_for_llm(text: str, max_tokens: int = 4000):
    """Chunk text to fit within LLM context window"""
    
    # Estimate tokens (rough: 1 token ≈ 4 chars)
    estimated_tokens = len(text) // 4
    
    if estimated_tokens <= max_tokens:
        return [text]
    
    # Split into chunks
    chunks = []
    chunk_size = max_tokens * 4  # Convert back to chars
    
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    
    return chunks

def process_long_document(document_text: str, task: str):
    """Process document longer than context window"""
    
    chunks = chunk_for_llm(document_text)
    results = []
    
    for chunk in chunks:
        result = ollama.generate(model="llama3.2:3b", prompt=f"{task}: {chunk}")
        results.append(result)
    
    # Combine results
    combined = combine_chunk_results(results)
    return combined
```

### Batch Processing

```python
def batch_process_with_ollama(items: List[str], task_template: str, 
                               batch_size: int = 10):
    """Process items in batches to optimize OLLAMA usage"""
    
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        
        # Combine into single prompt for efficiency
        batch_prompt = "\n\n".join([
            f"Item {j+1}: {item}"
            for j, item in enumerate(batch)
        ])
        
        prompt = f"{task_template}\n\n{batch_prompt}"
        
        result = ollama.generate(model="llama3.2:3b", prompt=prompt)
        
        # Parse batch results
        parsed = parse_batch_results(result, len(batch))
        results.extend(parsed)
    
    return results
```

### Fallback Strategy

```python
class LLMClient:
    """LLM client with fallback from OLLAMA to cloud"""
    
    def __init__(self, prefer_local=True):
        self.prefer_local = prefer_local
        self.ollama = OLLAMAClient()
    
    def generate(self, prompt: str, **kwargs):
        """Generate with fallback"""
        
        if self.prefer_local:
            try:
                return self.ollama.generate(prompt=prompt, **kwargs)
            except Exception as e:
                logger.warning(f"OLLAMA failed: {e}. Falling back to cloud.")
                return self._cloud_generate(prompt, **kwargs)
        else:
            return self._cloud_generate(prompt, **kwargs)
    
    def _cloud_generate(self, prompt, **kwargs):
        """Fallback to cloud LLM (OpenAI, Anthropic, etc.)"""
        # Implementation for cloud LLM
        pass
```

---

## Integration with External Services

### YouTube API (Video Discovery)

```python
from googleapiclient.discovery import build

class YouTubeResourceSuggester:
    """Find relevant YouTube videos"""
    
    def __init__(self, api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def search_videos(self, query: str, max_results: int = 5):
        """Search for educational videos"""
        
        request = self.youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            videoCategoryId='27',  # Education category
            maxResults=max_results,
            order='relevance',
            relevanceLanguage='en'
        )
        
        response = request.execute()
        
        videos = []
        for item in response['items']:
            videos.append({
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'video_id': item['id']['videoId'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'description': item['snippet']['description']
            })
        
        return videos
```

### arXiv API (Academic Papers)

```python
import arxiv

class ArxivResourceSuggester:
    """Find relevant academic papers"""
    
    def search_papers(self, query: str, max_results: int = 5):
        """Search arXiv for papers"""
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for result in search.results():
            papers.append({
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'abstract': result.summary,
                'url': result.entry_id,
                'pdf_url': result.pdf_url,
                'published': result.published.strftime('%Y-%m-%d'),
                'categories': result.categories
            })
        
        return papers
```

### Kaggle API (Datasets)

```python
from kaggle.api.kaggle_api_extended import KaggleApi

class KaggleDatasetSuggester:
    """Find relevant datasets on Kaggle"""
    
    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()
    
    def search_datasets(self, query: str, max_results: int = 5):
        """Search for datasets"""
        
        datasets = self.api.dataset_list(search=query)
        
        results = []
        for dataset in datasets[:max_results]:
            results.append({
                'name': dataset.title,
                'owner': dataset.ref.split('/')[0],
                'url': f"https://www.kaggle.com/{dataset.ref}",
                'size': dataset.totalBytes,
                'description': dataset.subtitle,
                'last_updated': dataset.lastUpdated
            })
        
        return results
```

### AssemblyAI (Cloud Transcription - Optional)

```python
import assemblyai as aai

class AssemblyAITranscriber:
    """Cloud-based transcription (alternative to Whisper)"""
    
    def __init__(self, api_key: str):
        aai.settings.api_key = api_key
    
    def transcribe(self, audio_file: str):
        """Transcribe audio file"""
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)
        
        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")
        
        return {
            'text': transcript.text,
            'confidence': transcript.confidence,
            'words': [
                {
                    'text': word.text,
                    'start': word.start,
                    'end': word.end,
                    'confidence': word.confidence
                }
                for word in transcript.words
            ]
        }
```

---

## Configuration Management

### Centralized Configuration

```yaml
# config/integrations.yaml

coursetransformer:
  export_format: "json"
  export_dir: "./exports"
  include_rag_db: true
  include_original_files: false

ollama:
  base_url: "http://localhost:11434"
  models:
    lightweight: "llama3.2:1b"
    medium: "llama3.2:3b"
    large: "llama3.1:8b"
  default_temperature: 0.7
  max_tokens: 1000
  timeout_seconds: 60
  prefer_local: true

external_services:
  youtube:
    enabled: true
    api_key: "${YOUTUBE_API_KEY}"
    max_results: 5
  
  arxiv:
    enabled: true
    max_results: 5
  
  kaggle:
    enabled: true
    credentials_path: "~/.kaggle/kaggle.json"
  
  assemblyai:
    enabled: false
    api_key: "${ASSEMBLYAI_API_KEY}"
    use_for_long_audio: true  # Use for audio > 2 hours

whisper:
  model_size: "medium"  # tiny, base, small, medium, large
  device: "cpu"  # or "cuda"
  use_gpu: false

tesseract:
  language: "eng"
  config: "--psm 3"  # Page segmentation mode
```

### Environment Variables

```bash
# .env file
YOUTUBE_API_KEY=your_youtube_api_key
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_key
ASSEMBLYAI_API_KEY=your_assemblyai_key
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Integration Testing

### Mock Services for Testing

```python
class MockOLLAMA:
    """Mock OLLAMA for testing"""
    
    def generate(self, model, prompt, **kwargs):
        """Return mock response"""
        return f"Mock response for: {prompt[:50]}..."
    
    def embed(self, model, text):
        """Return mock embeddings"""
        return [0.1] * 384  # Mock 384-dim embedding

class MockYouTubeAPI:
    """Mock YouTube API"""
    
    def search_videos(self, query, max_results=5):
        """Return mock video results"""
        return [
            {
                'title': f'Mock Video for {query}',
                'channel': 'Test Channel',
                'url': 'https://youtube.com/mock'
            }
        ]
```

### Integration Health Checks

```python
def check_integrations():
    """Verify all integrations are working"""
    
    results = {}
    
    # OLLAMA
    try:
        ollama = OLLAMAClient()
        models = ollama.list_models()
        results['ollama'] = 'OK' if models else 'No models available'
    except Exception as e:
        results['ollama'] = f'ERROR: {e}'
    
    # YouTube API
    try:
        youtube = YouTubeResourceSuggester(api_key=os.getenv('YOUTUBE_API_KEY'))
        videos = youtube.search_videos('test', max_results=1)
        results['youtube'] = 'OK' if videos else 'No results'
    except Exception as e:
        results['youtube'] = f'ERROR: {e}'
    
    # CourseTransformer
    try:
        export_dir = './test_export'
        # Test export
        results['coursetransformer'] = 'OK'
    except Exception as e:
        results['coursetransformer'] = f'ERROR: {e}'
    
    return results
```

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Design Specification (Not Implemented)
