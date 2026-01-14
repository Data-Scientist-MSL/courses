# CoursePlayerApp Video Player Specification

## Overview

The video player is a central component of the EdGuide learning experience, providing adaptive HLS streaming, tier-based download capabilities, and rich playback features. This document specifies the complete video player architecture, delivery system, and user experience.

## Video Player Features

### Core Playback Features

#### HLS Adaptive Streaming
- **Protocol**: HTTP Live Streaming (HLS)
- **Adaptive Bitrate**: Automatically adjusts quality based on network conditions
- **Qualities Available**:
  - 360p (Low) - 500 Kbps
  - 720p (Medium) - 2 Mbps
  - 1080p (High) - 5 Mbps
- **Format**: H.264 video codec, AAC audio codec
- **Segment Duration**: 6 seconds per segment
- **Buffer**: 30 seconds ahead

#### Playback Speed Control
- **Speeds Available**: 0.25x, 0.5x, 0.75x, 1x (Normal), 1.25x, 1.5x, 1.75x, 2x
- **Keyboard Shortcut**: `<` (slower), `>` (faster)
- **Persistence**: User preference saved per course
- **Visual Indicator**: Display current speed (e.g., "1.5x")

#### Subtitles and Captions
- **Format**: WebVTT (Web Video Text Tracks)
- **Languages**: English (default), Spanish, French, Mandarin (auto-generated)
- **Customization**:
  - Font size (small, medium, large)
  - Background opacity (0-100%)
  - Font color (white, yellow, cyan)
- **Keyboard Shortcut**: `C` (toggle captions)
- **Auto-Load**: User preference remembered

#### Chapter Markers
- **Navigation**: Jump to specific topics within video
- **Display**: Timeline scrubber shows chapter boundaries
- **UI**: Hover over timeline shows chapter title
- **Format**: JSON metadata
  ```json
  {
    "chapters": [
      {"time": 0, "title": "Introduction"},
      {"time": 120, "title": "Core Concepts"},
      {"time": 300, "title": "Hands-On Example"},
      {"time": 540, "title": "Summary"}
    ]
  }
  ```
- **Skip**: Click chapter in sidebar to jump

#### Bookmark & Resume Functionality
- **Auto-Save**: Progress saved every 10 seconds
- **Resume Prompt**: "Resume from 5:23 or start from beginning?"
- **Bookmarks**: User can manually bookmark important timestamps
- **Persistence**: Stored in PostgreSQL user_progress table
- **Cross-Device**: Resume from any device

#### Picture-in-Picture Mode
- **Activation**: Button in player controls or keyboard shortcut `P`
- **Browser Support**: Chrome, Edge, Safari, Firefox (87+)
- **Behavior**: Video continues playing in floating window
- **Controls**: Play/pause, return to page
- **Use Case**: Multi-tasking while watching lectures

#### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Space` | Play/Pause |
| `→` | Forward 10 seconds |
| `←` | Backward 10 seconds |
| `↑` | Volume up |
| `↓` | Volume down |
| `M` | Mute/Unmute |
| `F` | Fullscreen toggle |
| `P` | Picture-in-picture |
| `C` | Toggle captions |
| `<` | Decrease speed |
| `>` | Increase speed |
| `0-9` | Jump to 0%-90% of video |

#### Quality Selector
- **Options**: Auto (adaptive), 360p, 720p, 1080p
- **Auto Mode**: Default setting, adjusts based on bandwidth
- **Manual Override**: User can lock to specific quality
- **Indicator**: Show current quality badge (e.g., "720p HD")
- **Tier Restriction**: 
  - Basic: Auto, 360p, 720p (stream only)
  - Intermediate: Auto, 360p, 720p (stream + download)
  - Advanced: Auto, 360p, 720p, 1080p (stream + download)

#### Download Button (Tier-Gated)
- **Basic Tier**: Button disabled with lock icon 🔒
- **Intermediate Tier**: Download 720p enabled
- **Advanced Tier**: Download 720p and 1080p enabled
- **Watermarking**: Downloaded videos include user email watermark
- **DRM Protection**: Downloaded files encrypted with user-specific key
- **File Size Indicators**:
  - 720p: ~200 MB per hour
  - 1080p: ~500 MB per hour

---

## Video Delivery Architecture

### CDN Provider Options

#### Option 1: Cloudflare Stream
**Pros**:
- Integrated CDN and video hosting
- Built-in adaptive streaming
- Analytics dashboard
- DRM support
- Global edge network

**Pricing**: 
- $1 per 1,000 minutes stored
- $1 per 1,000 minutes delivered

**Example Usage**:
```python
# Upload video to Cloudflare Stream
import requests

def upload_video_to_cloudflare(video_file_path: str) -> str:
    """Upload video and get stream URL."""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    with open(video_file_path, "rb") as video_file:
        files = {"file": video_file}
        response = requests.post(url, headers=headers, files=files)
    
    video_id = response.json()["result"]["uid"]
    stream_url = f"https://customer-{CUSTOMER_CODE}.cloudflarestream.com/{video_id}/manifest/video.m3u8"
    return stream_url
```

#### Option 2: Bunny.net Stream
**Pros**:
- Lower cost than Cloudflare
- Good global coverage
- Easy integration
- Built-in analytics

**Pricing**:
- $0.005 per GB stored
- $0.01 per GB delivered

**Example Usage**:
```python
# Upload video to Bunny.net
def upload_video_to_bunny(video_file_path: str, library_id: str) -> str:
    """Upload video to Bunny Stream."""
    url = f"https://video.bunnycdn.com/library/{library_id}/videos"
    headers = {"AccessKey": BUNNY_API_KEY}
    
    data = {"title": "Course Video"}
    response = requests.post(url, headers=headers, json=data)
    video_id = response.json()["guid"]
    
    # Upload file
    upload_url = f"https://video.bunnycdn.com/library/{library_id}/videos/{video_id}"
    with open(video_file_path, "rb") as video_file:
        requests.put(upload_url, headers=headers, data=video_file)
    
    stream_url = f"https://iframe.mediadelivery.net/embed/{library_id}/{video_id}"
    return stream_url
```

### Video Encoding Pipeline

```yaml
encoding_workflow:
  input:
    format: MP4, MOV, AVI
    max_size: 10 GB
    
  processing:
    - step: validate
      checks:
        - valid_codec
        - acceptable_duration
        - no_corruption
    
    - step: transcode
      outputs:
        - resolution: 360p
          bitrate: 500 Kbps
          codec: H.264
          audio: AAC 128 Kbps
        
        - resolution: 720p
          bitrate: 2 Mbps
          codec: H.264
          audio: AAC 128 Kbps
        
        - resolution: 1080p
          bitrate: 5 Mbps
          codec: H.264
          audio: AAC 192 Kbps
    
    - step: generate_hls
      segment_duration: 6s
      playlist: master.m3u8
    
    - step: generate_thumbnails
      count: 10
      format: JPEG
      width: 320px
    
    - step: extract_audio
      format: MP3
      bitrate: 128 Kbps
      use_case: podcast_version
    
  output:
    hls_manifest: https://cdn.example.com/{video_id}/master.m3u8
    thumbnails: https://cdn.example.com/{video_id}/thumbnails/
    metadata: duration, resolution, chapters
```

### DRM Strategy (Tier-Based)

#### Basic Tier - Watermarking Only
```python
def apply_basic_watermark(video_id: str, user_email: str):
    """
    Apply visible watermark with user email to discourage sharing.
    Watermark appears in bottom-right corner.
    """
    watermark_config = {
        "text": user_email,
        "position": "bottom-right",
        "opacity": 0.3,
        "font_size": 16,
        "color": "white"
    }
    # Apply via CDN encoding API
    return watermark_config
```

#### Intermediate Tier - Basic DRM
```python
def enable_basic_drm(video_id: str):
    """
    Enable AES-128 encryption for HLS streams.
    Prevents casual downloading via browser tools.
    """
    drm_config = {
        "encryption": "AES-128",
        "key_rotation": "per_segment",
        "key_server": "https://gai-observe.online/api/drm/keys"
    }
    return drm_config
```

#### Advanced Tier - Full DRM + Forensic Watermarking
```python
def enable_advanced_drm(video_id: str, user_id: str):
    """
    Enable Widevine/FairPlay DRM with forensic watermarking.
    Forensic watermarking embeds invisible user ID in video stream.
    """
    drm_config = {
        "widevine": True,
        "fairplay": True,
        "playready": True,
        "forensic_watermark": {
            "user_id": user_id,
            "session_id": generate_session_id(),
            "embed_frequency": "every_10_seconds"
        }
    }
    return drm_config
```

---

## Progress Tracking

### Watch Time Tracking

```python
# courseplayerapp/video/progress_tracker.py

from datetime import datetime
from typing import Optional

class VideoProgressTracker:
    """Track video watch progress for resume and completion."""
    
    def __init__(self, user_id: str, video_id: str):
        self.user_id = user_id
        self.video_id = video_id
    
    def update_progress(
        self, 
        current_position: int,  # seconds
        total_duration: int,    # seconds
        watch_event: str = "progress"
    ):
        """
        Update user's progress in video.
        
        Args:
            current_position: Current playback position in seconds
            total_duration: Total video duration in seconds
            watch_event: Type of event (progress, complete, pause, etc.)
        """
        completion_percent = int((current_position / total_duration) * 100)
        
        # Mark as completed if watched >= 90%
        is_completed = completion_percent >= 90
        
        # Save to database
        db.execute(
            """
            INSERT INTO user_progress (
                user_id, video_id, current_position, 
                completion_percent, is_completed, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id, video_id) 
            DO UPDATE SET 
                current_position = %s,
                completion_percent = %s,
                is_completed = %s,
                updated_at = %s
            """,
            (
                self.user_id, self.video_id, current_position,
                completion_percent, is_completed, datetime.now(),
                current_position, completion_percent, is_completed, datetime.now()
            )
        )
        
        # Track watch event
        self._log_watch_event(watch_event, current_position)
    
    def get_resume_position(self) -> Optional[int]:
        """Get last watched position for resume functionality."""
        result = db.query(
            """
            SELECT current_position, is_completed 
            FROM user_progress 
            WHERE user_id = %s AND video_id = %s
            """,
            (self.user_id, self.video_id)
        )
        
        if not result or result["is_completed"]:
            return None  # Start from beginning
        
        return result["current_position"]
    
    def _log_watch_event(self, event_type: str, position: int):
        """Log analytics event for watch behavior."""
        analytics.track(
            user_id=self.user_id,
            event="video_watch_event",
            properties={
                "video_id": self.video_id,
                "event_type": event_type,  # play, pause, complete, seek
                "position": position,
                "timestamp": datetime.now().isoformat()
            }
        )
```

### Frontend Integration

```javascript
// Video player progress tracking (JavaScript)
const videoPlayer = document.getElementById('video-player');
const progressInterval = 10000; // Update every 10 seconds

let progressTimer;

videoPlayer.addEventListener('play', () => {
    // Start progress tracking
    progressTimer = setInterval(() => {
        const currentPosition = Math.floor(videoPlayer.currentTime);
        const totalDuration = Math.floor(videoPlayer.duration);
        
        // Send to backend
        fetch('/api/video/progress', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                video_id: videoPlayer.dataset.videoId,
                current_position: currentPosition,
                total_duration: totalDuration,
                watch_event: 'progress'
            })
        });
    }, progressInterval);
});

videoPlayer.addEventListener('pause', () => {
    clearInterval(progressTimer);
    // Log pause event
    logWatchEvent('pause');
});

videoPlayer.addEventListener('ended', () => {
    clearInterval(progressTimer);
    // Mark video as complete
    logWatchEvent('complete');
});

videoPlayer.addEventListener('seeking', () => {
    // User is seeking (scrubbing through video)
    logWatchEvent('seek');
});

function logWatchEvent(eventType) {
    fetch('/api/video/progress', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            video_id: videoPlayer.dataset.videoId,
            current_position: Math.floor(videoPlayer.currentTime),
            total_duration: Math.floor(videoPlayer.duration),
            watch_event: eventType
        })
    });
}
```

---

## Video Player UI Components

### Streamlit Implementation

```python
# courseplayerapp/ui/components/video_player_component.py

import streamlit as st
import streamlit.components.v1 as components

def render_video_player(
    video_id: str,
    user_tier: str,
    video_title: str,
    video_description: str,
    chapters: list = None
):
    """
    Render complete video player with tier-based features.
    
    Args:
        video_id: Unique video identifier
        user_tier: User's subscription tier
        video_title: Display title
        video_description: Video description
        chapters: List of chapter markers
    """
    # Get video URLs
    stream_url = get_video_stream_url(video_id)
    
    # Header
    st.header(video_title)
    st.caption(video_description)
    
    # Video player (using custom HTML component)
    player_html = f"""
    <video 
        id="video-player"
        data-video-id="{video_id}"
        controls
        width="100%"
        style="border-radius: 8px;"
    >
        <source src="{stream_url}" type="application/x-mpegURL">
        Your browser does not support HLS video.
    </video>
    
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        var video = document.getElementById('video-player');
        var videoSrc = '{stream_url}';
        
        if (Hls.isSupported()) {{
            var hls = new Hls();
            hls.loadSource(videoSrc);
            hls.attachMedia(video);
        }}
        else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
            video.src = videoSrc;
        }}
        
        // Resume from last position
        fetch('/api/video/{video_id}/resume-position')
            .then(res => res.json())
            .then(data => {{
                if (data.position) {{
                    video.currentTime = data.position;
                }
            }});
    </script>
    """
    
    components.html(player_html, height=500)
    
    # Tier-based download buttons
    st.subheader("Download Options")
    
    if user_tier == "basic":
        st.info("🔒 Video downloads are available for Intermediate and Advanced tiers")
        st.button("💎 Upgrade to Intermediate - $247", on_click=redirect_to_upgrade)
    
    elif user_tier == "intermediate":
        col1, col2 = st.columns(2)
        with col1:
            if st.download_button(
                "⬇️ Download 720p",
                data=get_video_download(video_id, "720p"),
                file_name=f"{video_id}_720p.mp4",
                mime="video/mp4"
            ):
                st.success("Download started!")
        
        with col2:
            st.button("🔒 Download 1080p (Advanced Only)", disabled=True)
            st.caption("Upgrade to Advanced for 1080p downloads")
    
    elif user_tier == "advanced":
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download 720p",
                data=get_video_download(video_id, "720p"),
                file_name=f"{video_id}_720p.mp4",
                mime="video/mp4"
            )
        with col2:
            st.download_button(
                "⬇️ Download 1080p",
                data=get_video_download(video_id, "1080p"),
                file_name=f"{video_id}_1080p.mp4",
                mime="video/mp4"
            )
    
    # Chapters sidebar
    if chapters:
        with st.sidebar:
            st.subheader("Chapters")
            for chapter in chapters:
                if st.button(f"{chapter['time']//60}:{chapter['time']%60:02d} - {chapter['title']}"):
                    # JavaScript to seek to chapter
                    st.components.v1.html(
                        f"<script>document.getElementById('video-player').currentTime = {chapter['time']};</script>"
                    )
    
    # Progress indicator
    progress = get_video_progress(st.session_state.user_id, video_id)
    if progress:
        st.progress(progress["completion_percent"] / 100)
        st.caption(f"Progress: {progress['completion_percent']}% complete")
```

### React Implementation (Future)

```typescript
// Video player component in React (for v2)
import React, { useEffect, useRef, useState } from 'react';
import Hls from 'hls.js';

interface VideoPlayerProps {
    videoId: string;
    streamUrl: string;
    userTier: 'basic' | 'intermediate' | 'advanced';
    onProgressUpdate: (position: number, duration: number) => void;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({
    videoId,
    streamUrl,
    userTier,
    onProgressUpdate
}) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentSpeed, setCurrentSpeed] = useState(1.0);
    
    useEffect(() => {
        const video = videoRef.current;
        if (!video) return;
        
        // Initialize HLS
        if (Hls.isSupported()) {
            const hls = new Hls();
            hls.loadSource(streamUrl);
            hls.attachMedia(video);
        } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = streamUrl;
        }
        
        // Load resume position
        fetch(`/api/video/${videoId}/resume-position`)
            .then(res => res.json())
            .then(data => {
                if (data.position && video) {
                    video.currentTime = data.position;
                }
            });
        
        // Progress tracking
        const progressInterval = setInterval(() => {
            if (video && !video.paused) {
                onProgressUpdate(video.currentTime, video.duration);
            }
        }, 10000);
        
        return () => clearInterval(progressInterval);
    }, [videoId, streamUrl, onProgressUpdate]);
    
    const handlePlaybackSpeedChange = (speed: number) => {
        if (videoRef.current) {
            videoRef.current.playbackRate = speed;
            setCurrentSpeed(speed);
        }
    };
    
    return (
        <div className="video-player-container">
            <video
                ref={videoRef}
                controls
                className="video-player"
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
            />
            
            <div className="player-controls">
                <button onClick={() => handlePlaybackSpeedChange(0.5)}>0.5x</button>
                <button onClick={() => handlePlaybackSpeedChange(1.0)}>1x</button>
                <button onClick={() => handlePlaybackSpeedChange(1.5)}>1.5x</button>
                <button onClick={() => handlePlaybackSpeedChange(2.0)}>2x</button>
                <span>Current: {currentSpeed}x</span>
            </div>
        </div>
    );
};
```

---

## Analytics & Engagement Metrics

### Key Metrics to Track

1. **Watch Time**: Total minutes watched per user/video
2. **Completion Rate**: % of users who finish videos
3. **Drop-off Points**: Where users stop watching
4. **Engagement Score**: Rewatch rate, pause/resume patterns
5. **Quality Distribution**: Which qualities users watch most
6. **Download Stats**: Number of downloads per tier

### Analytics Dashboard (Advanced Tier Only)

```python
def generate_video_analytics(video_id: str) -> dict:
    """Generate analytics for a specific video (instructor view)."""
    return {
        "total_views": 1234,
        "unique_viewers": 567,
        "avg_watch_time": "23:45",
        "completion_rate": 0.73,  # 73%
        "drop_off_points": [
            {"timestamp": 300, "percent_dropped": 0.12},
            {"timestamp": 1200, "percent_dropped": 0.08}
        ],
        "quality_distribution": {
            "360p": 0.20,
            "720p": 0.60,
            "1080p": 0.20
        },
        "downloads": {
            "720p": 45,
            "1080p": 12
        }
    }
```

---

## Performance Optimization

### Video Preloading
- Preload first 10 seconds of next video in playlist
- Reduce startup time for continuous watching

### Thumbnail Sprites
- Generate sprite sheet of video thumbnails
- Show preview on timeline hover
- Improves scrubbing UX

### Lazy Loading
- Load video player component only when in viewport
- Reduces initial page load time

### CDN Edge Caching
- Cache popular videos at edge locations
- Reduce latency for global users

---

## Accessibility

### Video Accessibility Features
- **Captions**: All videos have English captions (auto-generated + human-verified)
- **Transcripts**: Full text transcripts downloadable
- **Audio Description**: Optional audio description track (planned)
- **Keyboard Navigation**: Full keyboard control without mouse
- **Screen Reader Support**: ARIA labels on all controls

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: EdGuide Video Team  
**Platform**: EdGuide (gai-observe.online)
