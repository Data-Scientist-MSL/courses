# CourseIngester - Specialist Parser Agents

## Overview

Parser agents are specialized components responsible for extracting structured content from diverse file formats. Each parser is an expert in a specific format family, employing format-specific tools and techniques to maximize extraction quality.

**Design Pattern**: Each parser implements a standard interface:
```python
class ParserAgent:
    def can_handle(self, file_path: str) -> bool:
        """Check if this parser can handle the file"""
        pass
    
    def parse(self, file_path: str) -> ParsedDocument:
        """Parse file and return structured document"""
        pass
    
    def extract_metadata(self, file_path: str) -> Dict:
        """Extract file metadata"""
        pass
```

---

## 1️⃣ PDF Parser Agent

### Purpose
Extract content from PDF files, handling both native (searchable) PDFs and scanned (image-based) PDFs with OCR.

### Capabilities

#### **Native PDF Text Extraction**
- **Primary Tool**: pdfplumber (more accurate than PyPDF2)
- **Fallback Tool**: PyPDF2 (for compatibility)
- **Features**:
  - Text extraction with position information (x, y coordinates)
  - Font information (size, family, weight)
  - Reading order detection
  - Hyperlink extraction

#### **OCR for Scanned PDFs**
- **Detection**: Identify scanned PDFs (low text/page ratio)
- **Primary OCR**: Tesseract OCR (open-source, multi-language)
- **Advanced OCR**: EasyOCR (deep learning-based, higher accuracy)
- **Pre-processing**: 
  - Image deskewing (correct rotation)
  - Contrast enhancement
  - Noise reduction
  - Binarization (black/white conversion)

#### **Layout Analysis**
- **Column Detection**: Identify multi-column layouts
- **Section Detection**: Detect headers, paragraphs, footers
- **Reading Order**: Determine correct text sequence
- **Margin Detection**: Exclude headers/footers from main content

#### **Table Extraction**
- **Primary Tool**: tabula-py (table-specific extraction)
- **Fallback**: pdfplumber tables
- **Features**:
  - Preserve table structure (rows, columns, cells)
  - Detect merged cells
  - Export to pandas DataFrame
  - Handle spanning cells

#### **Image Extraction**
- **Tool**: pdf2image + PIL
- **Features**:
  - Extract embedded images (JPEG, PNG)
  - Preserve image resolution
  - Extract image captions (nearby text)
  - Filter out decorative elements (logos, backgrounds)

#### **Metadata Extraction**
- **Standard Metadata**:
  - Title, author, subject, keywords
  - Creation date, modification date
  - Producer (software that created PDF)
  - Page count
- **Custom Metadata**: XMP metadata parsing
- **Table of Contents**: Extract bookmarks/outline

### Inputs
- **Formats**: `.pdf`
- **Size Limit**: 500 MB per file
- **Page Limit**: 5,000 pages (performance consideration)

### Outputs

**Structured Document**:
```python
{
    "type": "pdf",
    "filename": "ml_textbook.pdf",
    "metadata": {
        "title": "Introduction to Machine Learning",
        "author": "Jane Doe",
        "pages": 450,
        "creation_date": "2023-05-10",
        "is_scanned": False
    },
    "content": {
        "text": "Full extracted text...",
        "sections": [
            {
                "title": "Chapter 1: Supervised Learning",
                "page_start": 12,
                "page_end": 45,
                "text": "...",
                "subsections": [...]
            }
        ],
        "tables": [
            {
                "page": 25,
                "caption": "Comparison of Algorithms",
                "data": [[...], [...]]  # pandas-compatible
            }
        ],
        "images": [
            {
                "page": 30,
                "path": "extracted_images/image_p30_1.png",
                "caption": "Neural Network Architecture"
            }
        ]
    }
}
```

### Tools & Libraries
- **pdfplumber**: Advanced PDF parsing
- **PyPDF2**: PDF manipulation and fallback
- **Tesseract OCR**: Text recognition
- **EasyOCR**: Deep learning OCR
- **pdf2image**: PDF to image conversion
- **tabula-py**: Table extraction
- **PyMuPDF (fitz)**: Fast PDF rendering
- **Pillow (PIL)**: Image processing

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Multi-column layouts** | Use pdfplumber layout analysis to detect columns, sort by (column, y-position) |
| **Scanned quality** | Pre-process images (deskew, enhance contrast) before OCR |
| **Complex tables** | Try tabula-py first, fall back to pdfplumber, manual extraction as last resort |
| **Mathematical equations** | Extract as images, use LaTeX OCR (e.g., Mathpix) for conversion |
| **Encrypted PDFs** | Detect encryption, prompt user for password |
| **Large files** | Process page-by-page, stream results instead of loading all at once |
| **Different encodings** | Try UTF-8, fall back to Latin-1, detect encoding automatically |

### Configuration Options
```yaml
pdf_parser:
  ocr_threshold: 0.3  # Trigger OCR if text ratio < 30%
  ocr_language: "eng+fra+spa"  # Multi-language OCR
  extract_images: true
  extract_tables: true
  max_pages: 5000
  use_advanced_ocr: false  # Use EasyOCR (slower, more accurate)
```

---

## 2️⃣ Video Analysis Agent

### Purpose
Extract content from video lectures and tutorials, including audio transcription, visual analysis, and timestamp mapping.

### Capabilities

#### **Audio Transcription**
- **Primary Tool**: Whisper (OpenAI's speech-to-text model)
  - Supports 99 languages
  - Automatic language detection
  - Punctuation and capitalization
  - Timestamp alignment (word-level)
- **Cloud Alternative**: AssemblyAI API (optional, for higher accuracy)
- **Features**:
  - Multiple model sizes (tiny, base, small, medium, large)
  - GPU acceleration support
  - Batch processing

#### **Speaker Diarization**
- **Tool**: pyannote.audio
- **Features**:
  - Identify number of speakers
  - Label speaker segments (Speaker 1, Speaker 2, etc.)
  - Attribute transcript to speakers
  - Detect overlapping speech
- **Use Cases**: Panel discussions, Q&A sessions, interviews

#### **Scene Detection**
- **Tool**: scenedetect (PySceneDetect)
- **Methods**:
  - Content-based detection (visual changes)
  - Threshold-based detection (fade to black)
- **Purpose**: Identify topic changes, chapter boundaries

#### **Slide Extraction**
- **Method**: Frame differencing to detect static slides
- **Process**:
  1. Sample frames at regular intervals (e.g., every 2 seconds)
  2. Compute frame similarity (SSIM, perceptual hash)
  3. Extract unique slides (discard duplicates)
  4. OCR extracted slides for text content
- **Tools**: OpenCV for frame extraction, ImageHash for deduplication

#### **Timestamp Mapping**
- **Content → Time Mapping**:
  - Map transcribed sentences to video timestamps
  - Create chapter markers at scene changes
  - Tag code snippets with timestamps
- **Output**: Timestamped transcript with clickable links

#### **Visual Analysis**
- **Code Snippet Detection**:
  - Detect code on screen (monospace font, syntax highlighting)
  - Extract code via OCR
  - Syntax highlighting preservation
- **Diagram Detection**:
  - Identify diagrams, flowcharts, graphs
  - Extract as high-resolution images
  - Caption extraction from nearby text/speech

### Inputs
- **Formats**: `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`
- **Size Limit**: 10 GB per video
- **Duration Limit**: 8 hours (performance consideration)
- **Resolution**: Any (higher resolution improves slide extraction)

### Outputs

**Structured Video Content**:
```python
{
    "type": "video",
    "filename": "python_tutorial.mp4",
    "metadata": {
        "duration_seconds": 3600,
        "resolution": "1920x1080",
        "fps": 30,
        "codec": "h264",
        "audio_language": "en"
    },
    "transcript": {
        "language": "en",
        "segments": [
            {
                "start": 0.0,
                "end": 5.2,
                "text": "Welcome to this Python tutorial.",
                "speaker": "Speaker 1",
                "confidence": 0.95
            },
            # ... more segments
        ],
        "full_text": "Welcome to this Python tutorial. ..."
    },
    "scenes": [
        {
            "start": 0.0,
            "end": 120.5,
            "title": "Introduction"  # from transcript analysis
        },
        # ... more scenes
    ],
    "slides": [
        {
            "timestamp": 15.0,
            "image_path": "extracted_slides/slide_001.png",
            "text": "Course Outline\n- Basics\n- Functions\n- OOP"
        },
        # ... more slides
    ],
    "code_snippets": [
        {
            "timestamp": 450.0,
            "code": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)",
            "language": "python"
        }
    ]
}
```

### Tools & Libraries
- **Whisper**: Speech-to-text transcription
- **pyannote.audio**: Speaker diarization
- **OpenCV (cv2)**: Video frame extraction and analysis
- **scenedetect**: Scene change detection
- **moviepy**: Video manipulation
- **pydub**: Audio extraction and processing
- **ImageHash**: Image deduplication
- **pytesseract**: OCR for slides

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Poor audio quality** | Noise reduction (pydub), multiple Whisper passes, use larger model |
| **Overlapping speakers** | pyannote.audio handles this; mark as "overlap" in transcript |
| **Handwritten slides** | Use EasyOCR (better for handwriting) instead of Tesseract |
| **Fast speech** | Whisper handles well; confidence scores indicate quality |
| **Screen recording with webcam** | Detect webcam area, crop to content area for slide extraction |
| **Large video files** | Stream processing, extract audio separately, process in chunks |
| **Accents/dialects** | Whisper is robust; try language-specific models if issues persist |

### Configuration Options
```yaml
video_parser:
  whisper_model: "medium"  # tiny, base, small, medium, large
  enable_diarization: true
  extract_slides: true
  slide_interval_seconds: 2
  scene_threshold: 30  # Sensitivity for scene detection
  max_duration_hours: 8
  use_gpu: true
```

---

## 3️⃣ Document Parser Agent

### Purpose
Extract structured content from office documents (Word, PowerPoint) and markup formats (Markdown, LaTeX, RTF).

### Capabilities

#### **DOCX Parsing (Microsoft Word)**
- **Tool**: python-docx
- **Features**:
  - Extract paragraphs with style information
  - Parse headings (H1-H6) for document structure
  - Extract tables (preserve cells, rows, columns)
  - Extract images (embedded and linked)
  - Comments and tracked changes
  - Lists (numbered, bulleted) with nesting
  - Text formatting (bold, italic, underline)

#### **PPTX Parsing (Microsoft PowerPoint)**
- **Tool**: python-pptx
- **Features**:
  - Extract slides with layouts
  - Parse text boxes, titles, bullet points
  - Extract images from slides
  - Speaker notes extraction
  - Slide numbers and sequence
  - Shapes and diagrams (limited)
  - Slide transitions metadata

#### **Markdown Parsing**
- **Tool**: markdown, mistune (Python Markdown parsers)
- **Features**:
  - Parse headings, paragraphs, lists
  - Code blocks (with language tags)
  - Links and images
  - Tables (GitHub-flavored Markdown)
  - Blockquotes
  - Horizontal rules
  - Inline code and formatting

#### **LaTeX Parsing**
- **Tool**: pylatexenc, TexSoup
- **Features**:
  - Extract document structure (\section, \subsection)
  - Parse mathematical equations (convert to MathML or images)
  - Bibliography (\cite, \bibitem)
  - Figures and tables
  - Custom commands and environments
  - Unicode conversion (LaTeX symbols to Unicode)

#### **RTF Parsing**
- **Tool**: striprtf, pyth (RTF to plain text)
- **Features**:
  - Text extraction with basic formatting
  - Convert to plain text or HTML
  - Limited structure preservation

### Inputs
- **Formats**: `.docx`, `.pptx`, `.md`, `.tex`, `.rtf`, `.odt` (via conversion)
- **Size Limit**: 100 MB per file

### Outputs

**Structured Document (DOCX)**:
```python
{
    "type": "docx",
    "filename": "course_syllabus.docx",
    "metadata": {
        "title": "CS 101 Syllabus",
        "author": "Prof. Smith",
        "created": "2023-08-15",
        "modified": "2024-01-10"
    },
    "content": {
        "text": "Full text content...",
        "structure": [
            {
                "type": "heading",
                "level": 1,
                "text": "Course Overview"
            },
            {
                "type": "paragraph",
                "text": "This course introduces...",
                "formatting": ["bold"]
            },
            {
                "type": "table",
                "rows": 5,
                "cols": 3,
                "data": [[...], [...]]
            }
        ],
        "images": [...],
        "tables": [...]
    }
}
```

**Structured Presentation (PPTX)**:
```python
{
    "type": "pptx",
    "filename": "lecture_01.pptx",
    "slides": [
        {
            "slide_number": 1,
            "layout": "Title Slide",
            "title": "Introduction to Python",
            "content": "Lecture 1\nProf. Johnson",
            "notes": "Start with enthusiasm...",
            "images": [...]
        },
        # ... more slides
    ]
}
```

### Tools & Libraries
- **python-docx**: DOCX parsing
- **python-pptx**: PPTX parsing
- **markdown**: Markdown parsing
- **mistune**: Fast Markdown parser
- **pylatexenc**: LaTeX to Unicode conversion
- **TexSoup**: LaTeX parsing
- **striprtf**: RTF parsing
- **odfpy**: ODF (OpenDocument) format parsing

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Complex formatting** | Extract semantic structure (headings), ignore decorative formatting |
| **Equation parsing (LaTeX)** | Convert to MathML or render as images for preservation |
| **Nested structures (lists)** | Recursive parsing to preserve hierarchy |
| **Embedded objects** | Extract OLE objects, convert to images if possible |
| **Version compatibility** | Use python-docx/pptx (handles modern formats), convert legacy (.doc, .ppt) via LibreOffice |
| **Macros/VBA** | Ignore macros (security risk), extract text content only |

### Configuration Options
```yaml
document_parser:
  preserve_formatting: false  # Extract plain text vs. rich text
  extract_images: true
  extract_tables: true
  convert_equations: true  # LaTeX equations to images
  max_file_size_mb: 100
```

---

## 4️⃣ Code Repository Parser Agent

### Purpose
Analyze code repositories (Git repos, code folders) to extract structure, dependencies, documentation, and key modules.

### Capabilities

#### **Directory Structure Analysis**
- **Tool**: os.walk, pathlib
- **Features**:
  - Tree view generation (folder hierarchy)
  - Identify main entry points (main.py, index.js, app.py)
  - Classify file types (source, test, config, docs)
  - Detect common project structures (MVC, monorepo, microservices)

#### **Dependency Extraction**
- **Python**: requirements.txt, setup.py, Pipfile, pyproject.toml
- **JavaScript**: package.json, yarn.lock
- **Ruby**: Gemfile
- **Java**: pom.xml, build.gradle
- **Go**: go.mod
- **Rust**: Cargo.toml
- **Features**:
  - List all dependencies with versions
  - Identify direct vs. transitive dependencies
  - Detect outdated dependencies (via version comparison)

#### **README Parsing**
- **Locate**: README.md, README.txt, README.rst
- **Extract**:
  - Project description
  - Setup instructions
  - Usage examples
  - API documentation
  - Contributing guidelines
  - License information

#### **Code Structure Analysis**
- **Python**: Use `ast` module to parse without execution
  - Classes, functions, methods
  - Docstrings
  - Imports (internal and external)
- **Multi-language**: tree-sitter for robust parsing
  - Supports 40+ languages
  - Syntax-aware parsing
  - Query language for code patterns

#### **Documentation Extraction**
- **Docstrings**: Python (PEP 257), JavaScript (JSDoc)
- **Comments**: Inline comments, block comments
- **Markdown docs**: In `docs/` folder
- **API specs**: OpenAPI, Swagger files

#### **License Detection**
- **File**: LICENSE, LICENSE.txt, COPYING
- **Parsing**: Identify license type (MIT, GPL, Apache, etc.)
- **Tool**: licensee, scancode-toolkit

### Inputs
- **Git Repository**: URL or local path
- **Code Folder**: Local directory
- **Size Limit**: 1 GB (code only, excludes .git)
- **File Count Limit**: 50,000 files

### Outputs

**Repository Structure**:
```python
{
    "type": "code_repository",
    "path": "/path/to/repo",
    "metadata": {
        "name": "my-ml-project",
        "language": "Python",
        "framework": "Flask",
        "license": "MIT",
        "total_files": 1234,
        "lines_of_code": 45000
    },
    "structure": {
        "tree": "my-ml-project/\n├── src/\n│   ├── models/\n│   ├── utils/\n...",
        "entry_points": ["src/main.py", "app.py"]
    },
    "dependencies": {
        "runtime": [
            {"name": "numpy", "version": "1.24.0"},
            {"name": "pandas", "version": "2.0.0"}
        ],
        "dev": [
            {"name": "pytest", "version": "7.3.0"}
        ]
    },
    "documentation": {
        "readme": "# My ML Project\n...",
        "setup_instructions": "pip install -r requirements.txt",
        "usage_examples": "python main.py --input data.csv"
    },
    "modules": [
        {
            "file": "src/models/classifier.py",
            "classes": ["LogisticClassifier", "SVMClassifier"],
            "functions": ["train_model", "evaluate"],
            "docstrings": {...}
        }
    ]
}
```

### Tools & Libraries
- **GitPython**: Git repository interaction
- **ast**: Python Abstract Syntax Tree parsing
- **tree-sitter**: Multi-language parsing
- **pathlib**: Path manipulation
- **toml**: TOML parsing (for pyproject.toml, Cargo.toml)
- **PyYAML**: YAML parsing
- **pipreqs**: Automatic requirements.txt generation
- **licensee**: License detection

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Multi-language repos** | Use tree-sitter for cross-language parsing |
| **Monorepos** | Detect multiple projects, parse each independently |
| **Binary files** | Skip binary files, focus on source code |
| **Generated code** | Detect common patterns (build/, dist/), exclude from analysis |
| **Large repos** | Sample files (analyze subset), focus on main modules |
| **Missing docs** | Infer from code structure, generate basic README |

### Configuration Options
```yaml
code_parser:
  analyze_tests: false  # Include test files in analysis
  extract_docstrings: true
  max_file_size_mb: 10  # Skip files larger than this
  excluded_dirs: ["node_modules", "venv", ".git", "dist"]
  max_files: 50000
```

---

## 5️⃣ Audio Transcription Agent

### Purpose
Transcribe audio lectures, podcasts, and interviews with speaker identification and timestamping.

### Capabilities

#### **Speech-to-Text**
- **Primary Tool**: Whisper (OpenAI)
  - State-of-the-art accuracy
  - 99 language support
  - Robust to accents, noise
  - Multiple model sizes (speed vs. accuracy trade-off)
- **Cloud Alternative**: AssemblyAI, Google Speech-to-Text (optional)

#### **Speaker Diarization**
- **Tool**: pyannote.audio
- **Features**:
  - Automatic speaker counting
  - Speaker segment labeling
  - Overlapping speech detection
  - Speaker embeddings for identification

#### **Audio Enhancement**
- **Noise Reduction**: noisereduce library
- **Volume Normalization**: pydub
- **Format Conversion**: Convert any audio format to WAV for processing
- **Silence Removal**: Trim silent segments

#### **Timestamp Generation**
- **Word-level timestamps**: Whisper provides word timings
- **Sentence timestamps**: Aggregate words into sentences
- **Chapter markers**: Based on silence duration or speaker changes

#### **Language Detection**
- **Automatic**: Whisper auto-detects language
- **Manual Override**: User can specify language
- **Multi-language**: Handle code-switching (multiple languages in one audio)

### Inputs
- **Formats**: `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`, `.aac`, `.wma`
- **Size Limit**: 500 MB per file
- **Duration Limit**: 8 hours
- **Sample Rate**: Any (converted to 16kHz for Whisper)

### Outputs

**Transcribed Audio**:
```python
{
    "type": "audio",
    "filename": "podcast_episode_42.mp3",
    "metadata": {
        "duration_seconds": 2700,
        "format": "mp3",
        "sample_rate": 44100,
        "language": "en",
        "num_speakers": 2
    },
    "transcript": {
        "language": "en",
        "segments": [
            {
                "start": 0.0,
                "end": 4.5,
                "text": "Welcome to the data science podcast.",
                "speaker": "Host",
                "confidence": 0.97
            },
            {
                "start": 4.8,
                "end": 12.3,
                "text": "Today we're discussing neural networks.",
                "speaker": "Host",
                "confidence": 0.95
            },
            # ... more segments
        ],
        "full_text": "Welcome to the data science podcast. ...",
        "word_timestamps": [
            {"word": "Welcome", "start": 0.0, "end": 0.5},
            # ... more words
        ]
    },
    "speakers": [
        {"id": "Speaker 1", "label": "Host", "total_time": 1500},
        {"id": "Speaker 2", "label": "Guest", "total_time": 1200}
    ]
}
```

### Tools & Libraries
- **Whisper**: Speech recognition
- **pyannote.audio**: Speaker diarization
- **pydub**: Audio manipulation
- **librosa**: Audio analysis
- **noisereduce**: Noise reduction
- **SpeechRecognition**: Alternative transcription (Google, CMU Sphinx)

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Accents** | Whisper is trained on diverse data; use language-specific models |
| **Background noise** | Pre-process with noise reduction (noisereduce) |
| **Multiple speakers** | pyannote.audio for diarization, label speakers in transcript |
| **Low quality audio** | Audio enhancement, use larger Whisper model |
| **Long files** | Process in chunks (30-minute segments), stitch results |
| **Music/sound effects** | Detect non-speech segments, mark as [music] or [sound effect] |

### Configuration Options
```yaml
audio_parser:
  whisper_model: "medium"
  enable_diarization: true
  noise_reduction: true
  language: "auto"  # or specify: "en", "es", "fr", etc.
  max_duration_hours: 8
  use_gpu: true
```

---

## 6️⃣ Web Scraper Agent

### Purpose
Extract educational content from web pages, blogs, online documentation, and course websites.

### Capabilities

#### **HTML Content Extraction**
- **Tool**: BeautifulSoup4
- **Features**:
  - Parse HTML structure
  - Extract text, links, images
  - Navigate DOM tree
  - Handle malformed HTML

#### **Article Extraction**
- **Tool**: newspaper3k
- **Features**:
  - Identify main content (remove ads, navigation, sidebars)
  - Extract article title, author, publish date
  - Extract article images
  - Download and parse entire article
  - Multi-page article handling

#### **Link Crawling**
- **Strategy**: Breadth-first or depth-first crawling
- **Features**:
  - Follow related links (same domain)
  - Respect robots.txt
  - Configurable depth limit
  - URL deduplication

#### **Image Downloading**
- **Features**:
  - Download inline images
  - Preserve image filenames
  - Handle relative and absolute URLs
  - Image format conversion

#### **Metadata Extraction**
- **Open Graph Tags**: og:title, og:description, og:image
- **Twitter Card Tags**: twitter:title, twitter:description
- **Schema.org**: Structured data (Article, Course, etc.)
- **Standard Meta Tags**: description, keywords, author

#### **Dynamic Content Handling**
- **Tool**: Selenium (for JavaScript-heavy sites)
- **Features**:
  - Wait for JavaScript to load
  - Scroll to load lazy content
  - Click buttons/links programmatically
  - Handle pop-ups

### Inputs
- **Input**: URLs (single or list)
- **Depth**: Crawl depth (0 = single page, 1 = page + links, etc.)
- **Max Pages**: Limit crawled pages (default: 100)

### Outputs

**Scraped Web Content**:
```python
{
    "type": "webpage",
    "url": "https://example.com/ml-tutorial",
    "metadata": {
        "title": "Introduction to Machine Learning",
        "author": "John Doe",
        "publish_date": "2023-09-15",
        "description": "A comprehensive guide to ML basics",
        "language": "en"
    },
    "content": {
        "text": "Machine learning is a subset of artificial intelligence...",
        "html": "<article><h1>Introduction to ML</h1>...",
        "images": [
            {
                "url": "https://example.com/images/ml_diagram.png",
                "alt": "ML workflow diagram",
                "local_path": "downloaded_images/ml_diagram.png"
            }
        ],
        "links": [
            {"text": "Next lesson", "url": "https://example.com/ml-tutorial-2"}
        ]
    },
    "related_pages": [
        "https://example.com/ml-tutorial-2",
        "https://example.com/ml-tutorial-3"
    ]
}
```

### Tools & Libraries
- **BeautifulSoup4**: HTML parsing
- **newspaper3k**: Article extraction
- **requests**: HTTP client
- **Selenium**: Browser automation for dynamic content
- **lxml**: Fast XML/HTML parsing
- **html2text**: Convert HTML to Markdown
- **trafilatura**: Web scraping and text extraction

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Dynamic JavaScript content** | Use Selenium with headless browser (Chrome, Firefox) |
| **Paywalls** | Detect paywall, notify user (cannot bypass) |
| **Rate limiting** | Respect robots.txt, add delays between requests (politeness) |
| **Anti-scraping measures** | Rotate user agents, use sessions, add random delays |
| **Infinite scroll** | Selenium: scroll to bottom, wait for new content to load |
| **CAPTCHAs** | Cannot automate; notify user to manually download |
| **Different encodings** | Detect charset from headers or meta tags, decode properly |

### Configuration Options
```yaml
web_scraper:
  max_pages: 100
  crawl_depth: 1
  download_images: true
  use_selenium: false  # Enable for JavaScript sites
  politeness_delay_seconds: 1
  user_agent: "Mozilla/5.0 (CourseIngester Bot)"
  respect_robots_txt: true
  timeout_seconds: 30
```

---

## 7️⃣ Archive Extractor Agent

### Purpose
Extract and organize files from compressed archives, handling nested archives and various compression formats.

### Capabilities

#### **ZIP Extraction**
- **Tool**: zipfile (built-in)
- **Features**:
  - Extract all files
  - Preserve directory structure
  - Handle password-protected archives (with password)
  - Detect ZIP bombs (malicious archives)

#### **RAR Extraction**
- **Tool**: rarfile
- **Features**:
  - Extract RAR archives (requires UnRAR binary)
  - Multi-volume RAR support
  - Password-protected archives

#### **TAR/GZ Extraction**
- **Tool**: tarfile (built-in)
- **Formats**: .tar, .tar.gz, .tar.bz2, .tar.xz
- **Features**:
  - Compressed TAR archives
  - Preserve file permissions
  - Handle symbolic links

#### **Automatic File Organization**
- **Flat extraction**: Extract to single folder
- **Structured extraction**: Preserve archive directory structure
- **Categorization**: Group by file type after extraction

#### **Recursive Extraction**
- **Nested archives**: Detect archives within archives
- **Auto-extract**: Recursively extract nested archives
- **Depth limit**: Prevent infinite recursion

### Inputs
- **Formats**: `.zip`, `.rar`, `.tar`, `.gz`, `.bz2`, `.xz`, `.7z`
- **Size Limit**: 5 GB per archive
- **Nesting Limit**: 5 levels deep

### Outputs

**Extracted Archive**:
```python
{
    "type": "archive",
    "filename": "course_materials.zip",
    "metadata": {
        "compressed_size_mb": 250,
        "uncompressed_size_mb": 800,
        "file_count": 1500,
        "format": "zip",
        "is_encrypted": False
    },
    "extraction": {
        "path": "extracted/course_materials/",
        "files_extracted": 1500,
        "nested_archives": [
            "lectures/week1.zip",
            "labs/lab3.tar.gz"
        ],
        "structure": {
            "lectures/": 120,
            "labs/": 45,
            "readings/": 80,
            "videos/": 12
        }
    },
    "contents": [
        # List of ParsedDocument from contained files
    ]
}
```

### Tools & Libraries
- **zipfile**: ZIP extraction (built-in)
- **rarfile**: RAR extraction
- **tarfile**: TAR extraction (built-in)
- **py7zr**: 7-Zip extraction
- **patool**: Unified interface for all archive types

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Password-protected archives** | Prompt user for password, retry with password |
| **Archive bombs (zip bombs)** | Check compressed vs. uncompressed ratio, abort if > 100x |
| **Nested structures** | Track recursion depth, stop at configurable limit |
| **Corrupted archives** | Try to extract partial content, log errors |
| **Path traversal attacks** | Sanitize extracted paths, prevent writing outside target dir |
| **Large archives** | Stream extraction, process files incrementally |

### Configuration Options
```yaml
archive_parser:
  max_size_mb: 5000
  max_recursion_depth: 5
  detect_bombs: true
  bomb_ratio_threshold: 100
  preserve_structure: true
  auto_extract_nested: true
```

---

## 8️⃣ Notebook Parser Agent

### Purpose
Parse Jupyter notebooks to extract code cells, markdown documentation, outputs, and dependencies.

### Capabilities

#### **Code Cell Extraction**
- **Tool**: nbformat
- **Features**:
  - Extract code cells with source code
  - Preserve cell execution order
  - Extract cell metadata (execution count)
  - Language detection (Python, R, Julia, etc.)

#### **Markdown Cell Extraction**
- **Features**:
  - Extract markdown cells as documentation
  - Parse markdown content (headings, lists, etc.)
  - Identify section headers

#### **Cell Output Parsing**
- **Output Types**:
  - Text output (stdout, stderr)
  - Rich output (HTML, LaTeX, images)
  - Error tracebacks
  - Execution results
- **Features**:
  - Extract plots/visualizations as images
  - Capture data tables

#### **Dependency Identification**
- **Import Analysis**: Parse `import` statements in code cells
- **Magic Commands**: Extract `!pip install` or `%conda install`
- **Requirements**: Generate requirements.txt from imports

#### **Execution Order Analysis**
- **Execution Count**: Track cell execution order
- **Out-of-order Execution**: Detect cells run out of sequence
- **Non-executed Cells**: Identify cells never run

#### **Notebook Conversion**
- **Tool**: nbconvert
- **Formats**: HTML, PDF, Markdown, Python script
- **Features**: Export notebook to static formats

### Inputs
- **Format**: `.ipynb`
- **Size Limit**: 50 MB per notebook
- **Cell Limit**: 1,000 cells

### Outputs

**Parsed Notebook**:
```python
{
    "type": "jupyter_notebook",
    "filename": "data_analysis.ipynb",
    "metadata": {
        "kernel": "python3",
        "language": "Python",
        "notebook_version": "4.5",
        "total_cells": 45,
        "code_cells": 30,
        "markdown_cells": 15
    },
    "cells": [
        {
            "type": "markdown",
            "source": "# Data Analysis Tutorial\n\n...",
            "rendered_html": "<h1>Data Analysis Tutorial</h1>..."
        },
        {
            "type": "code",
            "source": "import pandas as pd\nimport numpy as np",
            "execution_count": 1,
            "outputs": [],
            "language": "python"
        },
        {
            "type": "code",
            "source": "df = pd.read_csv('data.csv')\ndf.head()",
            "execution_count": 2,
            "outputs": [
                {
                    "type": "execute_result",
                    "data": {"text/html": "<table>...</table>"}
                }
            ]
        }
    ],
    "dependencies": [
        {"name": "pandas", "import_type": "library"},
        {"name": "numpy", "import_type": "library"},
        {"name": "matplotlib", "import_type": "library"}
    ],
    "execution_analysis": {
        "all_cells_executed": True,
        "out_of_order": False,
        "max_execution_count": 30
    }
}
```

### Tools & Libraries
- **nbformat**: Read and write notebook files
- **nbconvert**: Convert notebooks to other formats
- **ast**: Analyze Python code in cells
- **IPython**: For rendering outputs

### Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **Out-of-order execution** | Track execution counts, warn about non-sequential execution |
| **Missing outputs** | Detect cells without outputs, mark as "not run" |
| **Large outputs** | Truncate large outputs, save full output separately |
| **Cell dependencies** | Analyze variable usage across cells to detect dependencies |
| **Different kernels** | Support Python, R, Julia; kernel-specific parsing |
| **Version compatibility** | Use nbformat for compatibility across notebook versions |

### Configuration Options
```yaml
notebook_parser:
  extract_outputs: true
  max_output_size_kb: 1000
  render_markdown: true
  analyze_execution_order: true
  extract_plots: true
```

---

## Parser Orchestration

### Multi-Parser Workflow

```python
def route_to_parser(file_path: str) -> ParserAgent:
    """Route file to appropriate parser based on extension and content."""
    ext = get_extension(file_path)
    
    parser_map = {
        '.pdf': PDFParser,
        '.mp4': VideoParser,
        '.docx': DocumentParser,
        '.py': CodeParser,
        '.mp3': AudioParser,
        '.html': WebScraper,
        '.zip': ArchiveExtractor,
        '.ipynb': NotebookParser
    }
    
    return parser_map.get(ext, GenericParser)()
```

### Parallel Processing
- Process multiple files simultaneously using multiprocessing
- Resource pooling (limit concurrent heavy parsers like video)
- Progress tracking for batch operations

### Error Handling
- Failed parsers don't block workflow
- Detailed error logging
- Retry mechanism for transient failures
- Fallback to generic text extraction

---

**Document Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Design Specification (Not Implemented)
