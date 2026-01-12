# UI Components Specification

## Overview

This document specifies all major UI components for CoursePlayerApp. Each component is designed to be modular, reusable, accessible, and tier-aware.

---

## 1. Video Player Component

### Purpose
Deliver high-quality video streaming with adaptive bitrate, playback controls, and tier-gated download functionality.

### Technical Stack
- **Player Library**: Video.js or Plyr.js
- **Streaming Protocol**: HLS (HTTP Live Streaming)
- **Format**: H.264 video, AAC audio
- **Container**: MP4 segments

### Features

#### Core Playback
- ✅ Play/Pause toggle
- ✅ Seek bar with preview thumbnails
- ✅ Volume control with mute toggle
- ✅ Current time / Total duration display
- ✅ Fullscreen mode
- ✅ Picture-in-Picture (PiP) mode

#### Advanced Features
- ✅ Playback speed control (0.25x, 0.5x, 0.75x, 1x, 1.25x, 1.5x, 1.75x, 2x)
- ✅ Quality selection (based on tier):
  - Basic: Auto, 720p
  - Intermediate: Auto, 720p, 1080p
  - Advanced: Auto, 720p, 1080p, 4K
- ✅ Closed captions/subtitles (multiple languages)
- ✅ Auto-generated transcript display (synchronized)
- ✅ Bookmarks (save position, resume later)
- ✅ Notes (timestamp-tagged annotations)
- ✅ Download button (tier-gated)

#### Keyboard Shortcuts
```
Space       - Play/Pause
←/→         - Seek backward/forward 5s
↑/↓         - Volume up/down
F           - Fullscreen toggle
M           - Mute toggle
C           - Captions toggle
K           - Play/Pause (YouTube-style)
J/L         - Seek backward/forward 10s
0-9         - Jump to 0%, 10%, ..., 90%
</>         - Decrease/increase playback speed
```

### Component Interface

```typescript
interface VideoPlayerProps {
  videoUrl: string;                    // HLS manifest URL
  title: string;                       // Lesson title
  lessonId: string;                    // Unique lesson identifier
  courseId: string;                    // Course identifier
  userTier: 'basic' | 'intermediate' | 'advanced';
  
  // Optional features
  transcriptUrl?: string;              // VTT transcript file
  thumbnailsUrl?: string;              // VTT thumbnails for seek preview
  bookmarks?: Bookmark[];              // Previously saved bookmarks
  notes?: Note[];                      // Previously saved notes
  startTime?: number;                  // Resume from this position (seconds)
  
  // Callbacks
  onProgress?: (time: number) => void; // Called every 5 seconds
  onComplete?: () => void;             // Called when video ends
  onBookmarkAdd?: (bookmark: Bookmark) => void;
  onNoteAdd?: (note: Note) => void;
  onDownloadRequest?: () => void;      // Triggered when download clicked
}

interface Bookmark {
  id: string;
  timestamp: number;                   // Seconds
  label?: string;                      // Optional user label
  createdAt: Date;
}

interface Note {
  id: string;
  timestamp: number;                   // Seconds
  content: string;                     // Markdown supported
  createdAt: Date;
}
```

### Implementation Example (React)

```tsx
import React, { useRef, useEffect, useState } from 'react';
import Plyr from 'plyr-react';
import 'plyr-react/plyr.css';

const VideoPlayer: React.FC<VideoPlayerProps> = ({
  videoUrl,
  title,
  lessonId,
  userTier,
  transcriptUrl,
  startTime = 0,
  onProgress,
  onComplete,
  onDownloadRequest
}) => {
  const playerRef = useRef<Plyr>(null);
  const [showDownloadButton, setShowDownloadButton] = useState(false);
  
  useEffect(() => {
    // Check if download is allowed for tier
    const downloadAllowed = ['intermediate', 'advanced'].includes(userTier);
    setShowDownloadButton(downloadAllowed);
  }, [userTier]);
  
  // Configure quality options based on tier
  const getQualityOptions = () => {
    switch (userTier) {
      case 'basic':
        return { default: 720, options: [720] };
      case 'intermediate':
        return { default: 1080, options: [720, 1080] };
      case 'advanced':
        return { default: 1080, options: [720, 1080, 2160] };
      default:
        return { default: 720, options: [720] };
    }
  };
  
  const plyrOptions = {
    controls: [
      'play-large',
      'play',
      'progress',
      'current-time',
      'duration',
      'mute',
      'volume',
      'captions',
      'settings',
      'pip',
      'airplay',
      'fullscreen'
    ],
    settings: ['captions', 'quality', 'speed'],
    quality: getQualityOptions(),
    speed: { selected: 1, options: [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2] },
    keyboard: { focused: true, global: true },
    tooltips: { controls: true, seek: true },
    captions: { active: false, update: true },
  };
  
  const handleTimeUpdate = (event: Plyr.PlyrEvent) => {
    const currentTime = event.detail.plyr.currentTime;
    if (onProgress && currentTime % 5 === 0) {
      onProgress(currentTime);
    }
  };
  
  const handleEnded = () => {
    if (onComplete) {
      onComplete();
    }
  };
  
  const handleDownload = () => {
    if (onDownloadRequest) {
      onDownloadRequest();
    }
  };
  
  return (
    <div className="video-player-container">
      <div className="video-header">
        <h2>{title}</h2>
        {showDownloadButton && (
          <button onClick={handleDownload} className="download-btn">
            ⬇️ Download Video
          </button>
        )}
        {!showDownloadButton && userTier === 'basic' && (
          <button className="upgrade-btn" disabled>
            🔒 Download (Upgrade to unlock)
          </button>
        )}
      </div>
      
      <Plyr
        ref={playerRef}
        source={{
          type: 'video',
          sources: [{ src: videoUrl, type: 'application/x-mpegURL' }],
          tracks: transcriptUrl ? [{
            kind: 'captions',
            label: 'English',
            srclang: 'en',
            src: transcriptUrl,
            default: true
          }] : []
        }}
        options={plyrOptions}
        onTimeUpdate={handleTimeUpdate}
        onEnded={handleEnded}
      />
      
      <div className="video-info">
        <p className="keyboard-hint">
          💡 Tip: Press <kbd>K</kbd> to play/pause, <kbd>←</kbd>/<kbd>→</kbd> to seek
        </p>
      </div>
    </div>
  );
};

export default VideoPlayer;
```

### UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  Lesson 1: Introduction to Data Science  [⬇️ Download] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                    [Video Frame]                        │
│                                                         │
│                        [▶]                              │
│                                                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ [⏮] [⏯] [⏭]  ▓▓▓▓▓▓▓▓░░░░░░░░░░  12:34 / 45:00       │
│                                                         │
│ [🔊] [━━━━━━━━━━] [CC] [⚙️] [⛶] [⬜]                  │
│                                                         │
│ Speed: 1x ▼  Quality: 1080p ▼  Captions: English ▼    │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Slides Viewer Component

### Purpose
Display course slides with navigation, zoom, search, and tier-gated download functionality.

### Technical Stack
- **PDF Rendering**: PDF.js (Mozilla)
- **Alternative**: react-pdf for React apps
- **Format**: PDF files (with PPTX source for Advanced tier)

### Features

#### Core Viewing
- ✅ Page navigation (prev/next, jump to page)
- ✅ Page indicator (current/total)
- ✅ Zoom in/out (50% - 200%)
- ✅ Fit to width / Fit to page
- ✅ Fullscreen mode
- ✅ Thumbnails sidebar

#### Advanced Features
- ✅ Search within slides
- ✅ Text selection and copy
- ✅ Slide notes (if embedded in PDF)
- ✅ Download button (tier-gated):
  - Basic: ❌ No download
  - Intermediate: ✅ PDF download
  - Advanced: ✅ PDF + PPTX download
- ✅ Print functionality (respects tier permissions)

### Component Interface

```typescript
interface SlidesViewerProps {
  pdfUrl: string;                      // PDF file URL
  pptxUrl?: string;                    // PowerPoint URL (Advanced tier only)
  title: string;                       // Slide deck title
  lessonId: string;                    // Lesson identifier
  userTier: 'basic' | 'intermediate' | 'advanced';
  
  // Optional
  currentPage?: number;                // Start at this page
  
  // Callbacks
  onPageChange?: (page: number) => void;
  onDownloadPDF?: () => void;
  onDownloadPPTX?: () => void;
}
```

### Implementation Example (React)

```tsx
import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

// Configure PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const SlidesViewer: React.FC<SlidesViewerProps> = ({
  pdfUrl,
  pptxUrl,
  title,
  userTier,
  currentPage = 1,
  onPageChange,
  onDownloadPDF,
  onDownloadPPTX
}) => {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState(currentPage);
  const [scale, setScale] = useState(1.0);
  const [searchText, setSearchText] = useState('');
  
  const canDownloadPDF = ['intermediate', 'advanced'].includes(userTier);
  const canDownloadPPTX = userTier === 'advanced';
  
  const handleDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };
  
  const goToPrevPage = () => {
    const newPage = Math.max(1, pageNumber - 1);
    setPageNumber(newPage);
    if (onPageChange) onPageChange(newPage);
  };
  
  const goToNextPage = () => {
    const newPage = Math.min(numPages, pageNumber + 1);
    setPageNumber(newPage);
    if (onPageChange) onPageChange(newPage);
  };
  
  const zoomIn = () => setScale(Math.min(2.0, scale + 0.1));
  const zoomOut = () => setScale(Math.max(0.5, scale - 0.1));
  
  return (
    <div className="slides-viewer">
      <div className="slides-toolbar">
        <div className="toolbar-left">
          <h3>{title}</h3>
        </div>
        
        <div className="toolbar-center">
          <button onClick={goToPrevPage} disabled={pageNumber <= 1}>
            ← Previous
          </button>
          <span className="page-indicator">
            Page {pageNumber} of {numPages}
          </span>
          <button onClick={goToNextPage} disabled={pageNumber >= numPages}>
            Next →
          </button>
        </div>
        
        <div className="toolbar-right">
          <button onClick={zoomOut}>-</button>
          <span>{Math.round(scale * 100)}%</span>
          <button onClick={zoomIn}>+</button>
          
          {canDownloadPDF && (
            <button onClick={onDownloadPDF} className="download-btn">
              ⬇️ PDF
            </button>
          )}
          
          {canDownloadPPTX && pptxUrl && (
            <button onClick={onDownloadPPTX} className="download-btn">
              ⬇️ PPTX
            </button>
          )}
          
          {!canDownloadPDF && (
            <button className="upgrade-btn" disabled>
              🔒 Download (Upgrade)
            </button>
          )}
        </div>
      </div>
      
      <div className="slides-content">
        <Document
          file={pdfUrl}
          onLoadSuccess={handleDocumentLoadSuccess}
          loading={<div>Loading slides...</div>}
        >
          <Page
            pageNumber={pageNumber}
            scale={scale}
            renderTextLayer={true}
            renderAnnotationLayer={true}
          />
        </Document>
      </div>
      
      <div className="slides-search">
        <input
          type="text"
          placeholder="Search in slides..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        />
      </div>
    </div>
  );
};

export default SlidesViewer;
```

### UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  Data Science Fundamentals - Lecture 1                 │
│  [← Prev]  Page 5 of 25  [Next →]  [-] 100% [+]       │
│  [⬇️ PDF] [⬇️ PPTX] [🖨️] [⛶]                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌───────────────────────────────────────────┐        │
│   │                                           │        │
│   │         Slide Content Here                │        │
│   │                                           │        │
│   │   • Data Science Overview                 │        │
│   │   • Tools and Technologies                │        │
│   │   • Getting Started                       │        │
│   │                                           │        │
│   └───────────────────────────────────────────┘        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Search: [___________________________] 🔍              │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Lab Runner Component

### Purpose
Provide an interactive coding environment for hands-on exercises, with view-only mode for Basic tier and full interactivity for higher tiers.

### Technical Stack
- **Notebook**: JupyterLab embedded (iframe or custom integration)
- **Code Editor**: Monaco Editor (VS Code engine) or CodeMirror
- **Terminal**: xterm.js
- **Backend**: JupyterHub or custom execution environment

### Features

#### Core Features
- ✅ Code cell editing (tier-gated: interactive vs view-only)
- ✅ Code execution (tier-gated)
- ✅ Output display (stdout, stderr, images, plots)
- ✅ Markdown cells for instructions
- ✅ Syntax highlighting (Python, R, SQL)
- ✅ Auto-completion (if interactive mode)

#### Advanced Features
- ✅ Terminal access (tier-gated):
  - Basic: ❌ No terminal
  - Intermediate: ✅ Limited commands
  - Advanced: ✅ Full shell access
- ✅ File browser (view/upload/download files)
- ✅ Save/checkpoint functionality
- ✅ Reset to original state
- ✅ Progress indicator (cells completed)
- ✅ Launch SimulationPlayer button (for complex scenarios)

#### Tier-Specific Modes

**Basic Tier - View-Only Mode**:
- Pre-executed notebook (all outputs visible)
- Cannot edit cells
- Cannot run code
- Can read instructions and explanations
- Upgrade prompt overlays interactive sections

**Intermediate Tier - Interactive Mode**:
- Edit and execute code
- 100 lab hours/month quota
- Save checkpoints
- Limited terminal (safe commands)
- Cannot create custom scenarios

**Advanced Tier - Full Access**:
- Unlimited lab hours
- Full terminal access
- Custom scenario creation
- GPU access (for ML workloads)
- Persistent environments

### Component Interface

```typescript
interface LabRunnerProps {
  labId: string;                       // Lab identifier
  courseId: string;                    // Course identifier
  notebookUrl: string;                 // Jupyter notebook JSON URL
  userTier: 'basic' | 'intermediate' | 'advanced';
  
  // Optional
  checkpointData?: any;                // Resume from checkpoint
  simulationPlayerId?: string;         // If lab has advanced simulation
  
  // Callbacks
  onSaveCheckpoint?: (data: any) => void;
  onComplete?: (results: LabResults) => void;
  onLaunchSimulation?: () => void;
}

interface LabResults {
  cellsCompleted: number;
  totalCells: number;
  timeSpent: number;                   // Seconds
  score?: number;                      // If auto-graded
}
```

### Implementation Example

```tsx
import React, { useState, useEffect } from 'react';
import MonacoEditor from '@monaco-editor/react';

const LabRunner: React.FC<LabRunnerProps> = ({
  labId,
  notebookUrl,
  userTier,
  simulationPlayerId,
  onComplete,
  onLaunchSimulation
}) => {
  const [notebook, setNotebook] = useState<any>(null);
  const [currentCell, setCurrentCell] = useState(0);
  const [isViewOnly, setIsViewOnly] = useState(userTier === 'basic');
  
  useEffect(() => {
    // Load notebook
    fetch(notebookUrl)
      .then(res => res.json())
      .then(data => setNotebook(data));
  }, [notebookUrl]);
  
  const handleRunCell = async (cellIndex: number) => {
    if (isViewOnly) {
      alert('Upgrade to Intermediate to run code interactively!');
      return;
    }
    
    // Execute cell via backend API
    const code = notebook.cells[cellIndex].source.join('');
    
    try {
      const response = await fetch('/api/lab/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ labId, code })
      });
      
      const result = await response.json();
      // Update cell output
      const updatedNotebook = { ...notebook };
      updatedNotebook.cells[cellIndex].outputs = result.outputs;
      setNotebook(updatedNotebook);
    } catch (error) {
      console.error('Execution failed:', error);
    }
  };
  
  if (!notebook) {
    return <div>Loading lab...</div>;
  }
  
  return (
    <div className="lab-runner">
      {isViewOnly && (
        <div className="view-only-banner">
          ℹ️ This is a view-only preview. 
          <button className="upgrade-btn">
            Upgrade to Intermediate for interactive labs
          </button>
        </div>
      )}
      
      <div className="lab-header">
        <h2>{notebook.metadata.title || 'Lab Exercise'}</h2>
        <div className="lab-actions">
          {!isViewOnly && (
            <>
              <button onClick={() => {}}>Save Checkpoint</button>
              <button onClick={() => {}}>Reset Lab</button>
            </>
          )}
          {simulationPlayerId && (
            <button onClick={onLaunchSimulation} className="launch-sim-btn">
              🚀 Launch Simulation
            </button>
          )}
        </div>
      </div>
      
      <div className="lab-content">
        {notebook.cells.map((cell: any, index: number) => (
          <div key={index} className={`cell cell-${cell.cell_type}`}>
            {cell.cell_type === 'markdown' ? (
              <div className="markdown-cell">
                {/* Render markdown */}
                {cell.source.join('')}
              </div>
            ) : (
              <div className="code-cell">
                <MonacoEditor
                  height="200px"
                  language={cell.metadata.language || 'python'}
                  value={cell.source.join('')}
                  options={{
                    readOnly: isViewOnly,
                    minimap: { enabled: false },
                    fontSize: 14
                  }}
                />
                
                {!isViewOnly && (
                  <button 
                    onClick={() => handleRunCell(index)}
                    className="run-cell-btn"
                  >
                    ▶ Run
                  </button>
                )}
                
                {cell.outputs && cell.outputs.length > 0 && (
                  <div className="cell-output">
                    {/* Render outputs */}
                    <pre>{JSON.stringify(cell.outputs, null, 2)}</pre>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default LabRunner;
```

### UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  Lab 3: Data Manipulation with Pandas                  │
│  [💾 Save] [🔄 Reset] [🚀 Launch Simulation]           │
├─────────────────────────────────────────────────────────┤
│  ℹ️ View-only mode. Upgrade for interactive coding.    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📝 Introduction                                        │
│  In this lab, you'll learn to manipulate data using... │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  💻 Code Cell 1                                         │
│  1 | import pandas as pd                               │
│  2 | df = pd.read_csv('data.csv')                      │
│  3 | df.head()                                         │
│                                            [▶ Run]      │
│  ─────────────────────────────────────────────────────  │
│  Output:                                                │
│       name  age  city                                   │
│  0    Alice  25   NYC                                   │
│  1    Bob    30   LA                                    │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  Progress: 2/8 cells completed  [▓▓░░░░░░] 25%         │
└─────────────────────────────────────────────────────────┘
```

---

## 4. AI Tutor Component

### Purpose
Provide context-aware AI assistance for learning, with quota management for tier-based access.

### Technical Stack
- **LLM**: OLLAMA (Llama 2 or CodeLlama)
- **UI**: Chat interface (ChatGPT-style)
- **Backend**: FastAPI with streaming responses

### Features

#### Core Features
- ✅ Chat interface (messages, input, send)
- ✅ Context-aware (knows current lesson, course)
- ✅ Quota display (questions remaining)
- ✅ Conversation history (per course)
- ✅ Code syntax highlighting in responses
- ✅ Citation of course materials
- ✅ Streaming responses (word-by-word)

#### Question Types Supported
- Concept clarification ("What is a p-value?")
- Code debugging ("Why is my code failing?")
- Code explanation ("What does this function do?")
- Practice problems ("Give me a similar problem to solve")
- Resource recommendations ("Where can I learn more?")

#### Tier-Specific Access
- **Basic**: ❌ Not available
- **Intermediate**: ✅ 50 questions/month
- **Advanced**: ✅ Unlimited questions

### Component Interface

```typescript
interface AITutorProps {
  userTier: 'basic' | 'intermediate' | 'advanced';
  courseId: string;                    // For context
  lessonId: string;                    // For context
  lessonContent?: string;              // Current lesson content for context
  
  // Optional
  conversationHistory?: Message[];    // Load previous conversation
  
  // Callbacks
  onQuotaExceeded?: () => void;
  onMessageSent?: (message: Message) => void;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  citations?: string[];                // Referenced course materials
}
```

### Implementation Example

```tsx
import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

const AITutor: React.FC<AITutorProps> = ({
  userTier,
  courseId,
  lessonId,
  lessonContent,
  onQuotaExceeded
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [quota, setQuota] = useState({ used: 0, limit: 0, remaining: 0 });
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const canUseAITutor = ['intermediate', 'advanced'].includes(userTier);
  
  useEffect(() => {
    // Fetch quota on mount
    fetchQuota();
  }, []);
  
  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  const fetchQuota = async () => {
    const response = await fetch(`/api/ai-tutor/quota`);
    const data = await response.json();
    setQuota(data);
  };
  
  const sendMessage = async () => {
    if (!inputText.trim() || !canUseAITutor) return;
    
    // Check quota
    if (quota.remaining === 0 && userTier === 'intermediate') {
      if (onQuotaExceeded) onQuotaExceeded();
      return;
    }
    
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    
    try {
      // Call AI API with context
      const response = await fetch('/api/ai-tutor/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: inputText,
          courseId,
          lessonId,
          context: lessonContent,
          history: messages
        })
      });
      
      const data = await response.json();
      
      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        citations: data.citations
      };
      
      setMessages(prev => [...prev, assistantMessage]);
      
      // Update quota
      fetchQuota();
    } catch (error) {
      console.error('AI Tutor error:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  if (!canUseAITutor) {
    return (
      <div className="ai-tutor-locked">
        <div className="lock-icon">🤖</div>
        <h3>AI Tutor</h3>
        <p>Get instant answers to your questions!</p>
        <ul>
          <li>✓ Context-aware assistance</li>
          <li>✓ Code debugging help</li>
          <li>✓ Concept clarification</li>
        </ul>
        <button className="upgrade-btn">
          Unlock with Intermediate Tier →
        </button>
      </div>
    );
  }
  
  return (
    <div className="ai-tutor">
      <div className="ai-tutor-header">
        <h3>🤖 AI Tutor</h3>
        <div className="quota-indicator">
          {quota.limit === -1 ? (
            <span>✨ Unlimited</span>
          ) : (
            <span>{quota.remaining}/{quota.limit} questions left</span>
          )}
        </div>
      </div>
      
      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <p>👋 Hi! I'm your AI tutor. Ask me anything about this lesson!</p>
            <div className="example-questions">
              <p>Try asking:</p>
              <button onClick={() => setInputText("Can you explain this concept?")}>
                Can you explain this concept?
              </button>
              <button onClick={() => setInputText("Why is my code not working?")}>
                Why is my code not working?
              </button>
            </div>
          </div>
        )}
        
        {messages.map((message) => (
          <div key={message.id} className={`message message-${message.role}`}>
            <div className="message-avatar">
              {message.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-content">
              <ReactMarkdown
                components={{
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || '');
                    return !inline && match ? (
                      <SyntaxHighlighter language={match[1]} PreTag="div">
                        {String(children).replace(/\n$/, '')}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  }
                }}
              >
                {message.content}
              </ReactMarkdown>
              
              {message.citations && message.citations.length > 0 && (
                <div className="citations">
                  <small>📚 References: {message.citations.join(', ')}</small>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message message-assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <div className="input-container">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask a question..."
          disabled={isLoading}
        />
        <button onClick={sendMessage} disabled={isLoading || !inputText.trim()}>
          Send ↗
        </button>
      </div>
    </div>
  );
};

export default AITutor;
```

### UI Layout

```
┌─────────────────────────────────────────┐
│  🤖 AI Tutor       [45/50 questions]   │
├─────────────────────────────────────────┤
│                                         │
│  👋 Hi! I'm your AI tutor.             │
│  Ask me anything about this lesson!     │
│                                         │
│  Try asking:                            │
│  [Can you explain this concept?]        │
│  [Why is my code not working?]          │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  👤 What is a p-value?                  │
│                                         │
│  🤖 A p-value is a measure of the       │
│  probability that an observed           │
│  difference could have occurred just by │
│  random chance...                       │
│  📚 Reference: Lesson 3, Slide 12       │
│                                         │
│  ─────────────────────────────────────  │
│                                         │
│  [Ask a question...___________] [Send] │
└─────────────────────────────────────────┘
```

---

## 5. Progress Dashboard Component

### Purpose
Display comprehensive learning analytics, achievements, and progress tracking.

### Features

#### Overview Section
- ✅ Overall progress percentage
- ✅ Courses enrolled / completed
- ✅ Total time spent learning
- ✅ Current learning streak

#### Course Progress
- ✅ List of active courses
- ✅ Progress bar for each course
- ✅ Lessons completed / total
- ✅ Labs completed / total
- ✅ Quizzes passed

#### Achievements
- ✅ Badges earned
- ✅ Milestones reached
- ✅ Locked achievements (preview)

#### Analytics (Advanced tier only)
- ✅ Learning pace graph
- ✅ Time distribution by course
- ✅ Performance trends
- ✅ Skills assessment

### Component Interface

```typescript
interface ProgressDashboardProps {
  userId: string;
  userTier: 'basic' | 'intermediate' | 'advanced';
}

interface ProgressData {
  overallProgress: number;             // 0-100
  coursesEnrolled: number;
  coursesCompleted: number;
  totalTimeSpent: number;              // Minutes
  learningStreak: number;              // Days
  
  courses: CourseProgress[];
  achievements: Achievement[];
  certificates: Certificate[];
}

interface CourseProgress {
  courseId: string;
  courseName: string;
  progressPercentage: number;
  lessonsCompleted: number;
  totalLessons: number;
  labsCompleted: number;
  totalLabs: number;
  lastAccessed: Date;
}

interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlocked: boolean;
  unlockedAt?: Date;
}
```

### UI Layout

```
┌───────────────────────────────────────────────────────────┐
│  My Learning Progress                                     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Overall Progress      [▓▓▓▓▓▓░░░░] 45%             │ │
│  │ Courses Completed:    2 of 5                        │ │
│  │ Total Time:           24h 30m                       │ │
│  │ Learning Streak:      🔥 7 days                     │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  Active Courses                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Data Science 101                                    │ │
│  │ [▓▓▓▓▓▓▓▓▓░░░░] 65%  12/20 lessons  3/5 labs      │ │
│  │ Last accessed: 2 hours ago                          │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  │ Machine Learning                                    │ │
│  │ [▓▓▓░░░░░░░░░░] 25%  5/20 lessons  0/8 labs        │ │
│  │ Last accessed: Yesterday                            │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  Achievements Unlocked (8/20)                             │
│  🏆 🎯 ⭐ 🚀 📚 💡 🔥 ✨                               │
│                                                           │
│  Certificates Earned (1)                                  │
│  📜 Data Scientist's Toolbox - Issued Jan 2024           │
└───────────────────────────────────────────────────────────┘
```

---

## 6. Course Catalog Component

### Purpose
Browse and discover courses with filtering, search, and tier-based access indicators.

### Features

- ✅ Grid/list view toggle
- ✅ Search bar (title, description, tags)
- ✅ Filters:
  - Topic (Data Science, ML, Statistics, etc.)
  - Difficulty (Beginner, Intermediate, Advanced)
  - Tier access (My Tier, All)
- ✅ Course cards showing:
  - Thumbnail image
  - Title
  - Duration estimate
  - Prerequisites
  - Tier requirement
  - Lock icon if above user's tier
- ✅ Sort by: Newest, Most Popular, Duration

### Component Interface

```typescript
interface CourseCatalogProps {
  userTier: 'basic' | 'intermediate' | 'advanced';
  onCourseSelect: (courseId: string) => void;
  onUpgradeClick: (requiredTier: string) => void;
}

interface Course {
  id: string;
  title: string;
  description: string;
  thumbnailUrl: string;
  duration: string;                    // "6h 30m"
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  requiredTier: 'basic' | 'intermediate' | 'advanced';
  topics: string[];
  prerequisites: string[];
  enrolled: boolean;
  progress?: number;                   // If enrolled
}
```

### UI Layout

```
┌───────────────────────────────────────────────────────────┐
│  Course Catalog                                           │
│  [Search: _______________] [🔍]  [⊞ Grid] [≡ List]       │
│  Filter: [Topic ▼] [Difficulty ▼] [My Tier ▼]           │
│  Sort: [Newest ▼]                                         │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│  │ [Image]  │ │ [Image]  │ │ [Image]  │                 │
│  │          │ │          │ │  🔒      │                 │
│  │ Course 1 │ │ Course 2 │ │ Course 3 │                 │
│  │ 4h 30m   │ │ 6h 15m   │ │ 8h 00m   │                 │
│  │ Beginner │ │ Intermed.│ │ Advanced │                 │
│  │          │ │          │ │ Requires │                 │
│  │ [Start]  │ │[Continue]│ │ Advanced │                 │
│  │          │ │          │ │ [Upgrade]│                 │
│  └──────────┘ └──────────┘ └──────────┘                 │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## Accessibility Checklist for All Components

### Keyboard Navigation
- ✅ All interactive elements tabbable
- ✅ Logical tab order
- ✅ Visible focus indicators
- ✅ Escape key closes modals/overlays
- ✅ Arrow keys for navigation where appropriate

### Screen Reader Support
- ✅ ARIA labels for all controls
- ✅ ARIA live regions for dynamic content
- ✅ Semantic HTML (nav, main, article, etc.)
- ✅ Alt text for images
- ✅ Form labels properly associated

### Visual Accessibility
- ✅ Color contrast ratio ≥ 4.5:1
- ✅ No reliance on color alone
- ✅ Text resizable to 200%
- ✅ Focus indicators visible
- ✅ Clear error messages

### Media Accessibility
- ✅ Captions for videos
- ✅ Transcripts available
- ✅ Audio controls labeled
- ✅ Pause/stop controls for auto-playing content

---

## Conclusion

These six components form the core UI of CoursePlayerApp:

1. **Video Player** - Adaptive streaming with tier-gated downloads
2. **Slides Viewer** - PDF/PPTX viewing with tier-gated downloads
3. **Lab Runner** - Interactive coding with view-only mode for Basic
4. **AI Tutor** - Context-aware assistance with quota management
5. **Progress Dashboard** - Comprehensive learning analytics
6. **Course Catalog** - Browse and discover with access indicators

All components are designed with:
- **Tier awareness** - Feature gating built-in
- **Accessibility** - WCAG 2.1 AA compliance
- **Performance** - Optimized rendering and loading
- **Modularity** - Reusable across the platform
