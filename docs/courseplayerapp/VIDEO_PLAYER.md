# Video Player Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Define adaptive video player features and delivery architecture

---

## Overview

The video player is a core component of CoursePlayerApp, providing high-quality, adaptive streaming with tier-based download capabilities. It ensures smooth playback across devices and network conditions while enforcing feature gating.

---

## Video Player Features

### Core Playback Features

#### 1. HLS Adaptive Streaming
- **Protocol**: HTTP Live Streaming (HLS)
- **Adaptive Bitrate**: Automatically adjusts quality based on network speed
- **Resolutions**: 360p, 720p, 1080p
- **Video Codec**: H.264 (AVC)
- **Audio Codec**: AAC
- **Container**: MP4 fragments

#### 2. Playback Controls

**Speed Control**
- Range: 0.25x, 0.5x, 0.75x, 1x (normal), 1.25x, 1.5x, 1.75x, 2x
- Keyboard shortcuts: `<` (slower), `>` (faster)
- Preserves speed preference across videos

**Volume Control**
- Volume slider (0-100%)
- Mute/unmute toggle
- Keyboard shortcuts: `↑` (louder), `↓` (quieter), `M` (mute)
- Remembers last volume setting

**Playback State**
- Play/Pause: `Space` or click video
- Seek forward/backward: `←` (10s back), `→` (10s forward)
- Jump to start: `Home`
- Jump to end: `End`
- Frame-by-frame: `,` (back), `.` (forward)

#### 3. Subtitles & Captions

**Format**: WebVTT (.vtt)

**Features**:
- Multiple language support
- Adjustable font size
- Background opacity control
- Position control (top/bottom)
- Color customization (accessibility)

**Example WebVTT**:
```vtt
WEBVTT

00:00:00.000 --> 00:00:05.000
Welcome to this course on Machine Learning.

00:00:05.500 --> 00:00:10.000
Today we'll explore supervised learning algorithms.
```

#### 4. Chapter Markers

**Purpose**: Quick navigation to specific topics within video

**Implementation**:
```json
{
  "chapters": [
    {
      "time": 0,
      "title": "Introduction",
      "thumbnail": "chapter-0-thumb.jpg"
    },
    {
      "time": 120,
      "title": "Prerequisites",
      "thumbnail": "chapter-1-thumb.jpg"
    },
    {
      "time": 300,
      "title": "Core Concepts",
      "thumbnail": "chapter-2-thumb.jpg"
    }
  ]
}
```

**UI Elements**:
- Timeline markers showing chapter boundaries
- Chapter list in sidebar (collapsible)
- Thumbnail preview on hover
- Click to jump to chapter

#### 5. Bookmark & Resume Functionality

**Auto-Resume**:
- Saves playback position every 5 seconds
- Resumes from last position on return
- Shows "Resume from [timestamp]" or "Start from beginning" option

**Manual Bookmarks**:
- Add bookmark with note: `B` key
- View bookmarks in sidebar
- Jump to bookmarked position
- Export bookmarks for later review

**Storage**:
```json
{
  "user_id": "user123",
  "video_id": "ml-intro-001",
  "last_position": 450.5,
  "bookmarks": [
    {
      "timestamp": 120,
      "note": "Important concept: gradient descent"
    },
    {
      "timestamp": 300,
      "note": "Example code to review"
    }
  ],
  "updated_at": "2026-01-12T10:30:00Z"
}
```

#### 6. Picture-in-Picture Mode

**Functionality**:
- Detach video to floating window
- Continue watching while browsing other content
- Resize and reposition window
- Return to normal mode

**Keyboard**: `P` key to toggle

**Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

#### 7. Quality Selector

**Manual Quality Selection**:
- Auto (adaptive - default)
- 360p (for slow connections)
- 720p (standard quality)
- 1080p (high definition - Advanced tier streaming, all tiers if network permits)

**Visual Indicator**:
- Current quality shown in player (e.g., "720p")
- Network speed indicator (Fast/Medium/Slow)
- Buffer health indicator

#### 8. Download Button (Tier-Gated)

**Basic Tier**: 🔒 Locked
- Button disabled
- Tooltip: "Upgrade to Intermediate to download videos"

**Intermediate Tier**: ✅ Enabled (up to 720p)
- Quality options: 360p, 720p
- Download format: MP4
- Watermarked with user email
- Download quota: 100 videos/month

**Advanced Tier**: ✅ Enabled (up to 1080p)
- Quality options: 360p, 720p, 1080p
- Download format: MP4
- Forensic watermarking
- No download quota

**Download UI**:
```python
if user_tier == "basic":
    st.button("🔒 Download Video", disabled=True, 
              help="Upgrade to Intermediate to download")
elif user_tier == "intermediate":
    quality = st.selectbox("Quality", ["360p", "720p"])
    if st.button("⬇️ Download Video"):
        download_video(video_id, quality, watermark=user.email)
else:  # advanced
    quality = st.selectbox("Quality", ["360p", "720p", "1080p"])
    if st.button("⬇️ Download Video"):
        download_video(video_id, quality, watermark=user.email, drm=True)
```

#### 9. Keyboard Shortcuts Summary

| Key | Action |
|-----|--------|
| `Space` | Play/Pause |
| `K` | Play/Pause |
| `←` | Seek backward 10s |
| `→` | Seek forward 10s |
| `J` | Seek backward 10s |
| `L` | Seek forward 10s |
| `↑` | Increase volume |
| `↓` | Decrease volume |
| `M` | Mute/Unmute |
| `F` | Toggle fullscreen |
| `P` | Picture-in-picture |
| `C` | Toggle captions |
| `<` | Decrease speed |
| `>` | Increase speed |
| `0-9` | Jump to 0%-90% |
| `Home` | Jump to start |
| `End` | Jump to end |
| `B` | Add bookmark |

---

## Video Delivery Architecture

### CDN Options

#### Option 1: Cloudflare Stream (Recommended)
- **Pros**:
  - Global CDN network
  - Automatic encoding (upload once, serve multiple resolutions)
  - Built-in analytics
  - Low latency
  - DRM support
  - Thumbnail generation
  - Live streaming support (future)
  
- **Pricing**:
  - Storage: $5/1000 minutes
  - Delivery: $1/1000 minutes viewed
  - No bandwidth limits

- **API Integration**:
```python
import requests

# Upload video
response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/stream",
    headers={"Authorization": f"Bearer {api_token}"},
    files={"file": open("video.mp4", "rb")},
    data={
        "meta": {
            "name": "ML Introduction - Lecture 1",
            "requireSignedURLs": True
        }
    }
)

video_id = response.json()["result"]["uid"]

# Generate signed URL for playback
signed_url = generate_signed_url(
    video_id=video_id,
    expires_in=3600,  # 1 hour
    user_id=user.id
)

# HLS manifest URL
hls_url = f"https://videodelivery.net/{video_id}/manifest/video.m3u8?token={signed_url}"
```

#### Option 2: Bunny.net Stream
- **Pros**:
  - Cost-effective
  - Global CDN
  - MP4 fallback
  - Simple API
  - Good analytics
  
- **Pricing**:
  - Storage: $0.01/GB/month
  - Delivery: $0.01/GB (varies by region)

### Video Encoding Pipeline

```yaml
encoding_pipeline:
  input:
    format: "MP4, MOV, AVI, MKV"
    max_size: "10GB"
    
  processing:
    - analyze_source
    - extract_audio
    - generate_thumbnails (every 10s)
    - extract_chapters (if metadata present)
    - encode_multiple_resolutions
    
  outputs:
    360p:
      resolution: "640x360"
      bitrate: "800 kbps"
      fps: 30
      codec: "H.264"
      
    720p:
      resolution: "1280x720"
      bitrate: "2500 kbps"
      fps: 30
      codec: "H.264"
      
    1080p:
      resolution: "1920x1080"
      bitrate: "5000 kbps"
      fps: 30
      codec: "H.264"
      
  packaging:
    - generate_hls_manifest
    - create_dash_manifest (future)
    - generate_thumbnails_sprite
    - extract_subtitles (if present)
```

### DRM & Watermarking

#### Tier-Based Protection

**Basic Tier**:
- **Watermarking**: Visible text overlay
  - Position: Bottom right corner
  - Content: User email (faded)
  - Frequency: Every 60 seconds
  - Purpose: Discourage unauthorized sharing

```python
def add_watermark(video_path, user_email, tier):
    if tier == "basic":
        return add_visible_watermark(
            video_path,
            text=user_email,
            position="bottom_right",
            opacity=0.3,
            frequency_seconds=60
        )
```

**Intermediate Tier**:
- **Basic DRM**: AES-128 encryption for HLS
  - Encrypted video segments
  - Key rotation per user session
  - Time-limited decryption keys

```python
def generate_drm_key(user_id, video_id, expires_in=3600):
    key = generate_aes_key()
    
    # Store key in Redis with expiration
    redis.setex(
        f"drm:key:{user_id}:{video_id}",
        expires_in,
        key
    )
    
    return {
        "key_uri": f"https://api.gai-observe.online/drm/key/{user_id}/{video_id}",
        "key": key,
        "expires_at": datetime.now() + timedelta(seconds=expires_in)
    }
```

**Advanced Tier**:
- **Full DRM**: Widevine/FairPlay/PlayReady
- **Forensic Watermarking**: Invisible watermark unique to user
  - Embedded in video frames
  - Survives re-encoding
  - Traceable to specific user
  - Used for piracy detection

```python
def add_forensic_watermark(video_path, user_id, tier):
    if tier == "advanced":
        return add_invisible_watermark(
            video_path,
            payload=generate_unique_watermark(user_id),
            algorithm="spread_spectrum",
            robustness="high"
        )
```

### Download Management

#### Download Quota System

```python
# core/download_manager.py

class DownloadManager:
    def __init__(self, db, redis):
        self.db = db
        self.redis = redis
    
    async def check_download_quota(self, user_id, tier):
        """Check if user has download quota available"""
        
        if tier == "advanced":
            return True, "unlimited"
        
        if tier == "intermediate":
            # Check monthly quota
            month_key = f"downloads:{user_id}:{datetime.now().strftime('%Y-%m')}"
            downloads_this_month = int(self.redis.get(month_key) or 0)
            
            quota_limit = 100
            remaining = quota_limit - downloads_this_month
            
            if remaining <= 0:
                return False, {
                    "error": "Monthly download quota exceeded",
                    "used": downloads_this_month,
                    "limit": quota_limit,
                    "reset_date": self._get_next_month_start()
                }
            
            return True, {
                "remaining": remaining,
                "limit": quota_limit
            }
        
        # Basic tier
        return False, "Download feature not available in Basic tier"
    
    async def record_download(self, user_id, video_id, quality, tier):
        """Record a video download"""
        
        # Increment quota counter
        if tier == "intermediate":
            month_key = f"downloads:{user_id}:{datetime.now().strftime('%Y-%m')}"
            self.redis.incr(month_key)
            self.redis.expire(month_key, timedelta(days=60))
        
        # Log download event
        await self.db.execute(
            """
            INSERT INTO download_logs (user_id, video_id, quality, tier, downloaded_at)
            VALUES (:user_id, :video_id, :quality, :tier, NOW())
            """,
            {
                "user_id": user_id,
                "video_id": video_id,
                "quality": quality,
                "tier": tier
            }
        )
```

---

## Progress Tracking

### Watch Time Tracking

```python
# video/progress_tracker.py

class VideoProgressTracker:
    def __init__(self, db, redis):
        self.db = db
        self.redis = redis
        self.save_interval = 5  # Save progress every 5 seconds
    
    async def update_progress(self, user_id, video_id, current_time, duration):
        """Update video watch progress"""
        
        # Calculate completion percentage
        completion_percent = (current_time / duration * 100) if duration > 0 else 0
        
        # Determine status
        status = "in_progress"
        if completion_percent >= 90:
            status = "completed"
        elif current_time < 10:
            status = "not_started"
        
        # Update in Redis (real-time)
        redis_key = f"video_progress:{user_id}:{video_id}"
        self.redis.hset(redis_key, mapping={
            "current_time": current_time,
            "duration": duration,
            "completion_percent": completion_percent,
            "status": status,
            "last_updated": datetime.now().isoformat()
        })
        self.redis.expire(redis_key, timedelta(days=30))
        
        # Update in database (persistent)
        await self.db.execute(
            """
            INSERT INTO video_progress 
                (user_id, video_id, current_time, duration, completion_percent, status, updated_at)
            VALUES 
                (:user_id, :video_id, :current_time, :duration, :completion_percent, :status, NOW())
            ON CONFLICT (user_id, video_id) DO UPDATE SET
                current_time = :current_time,
                completion_percent = :completion_percent,
                status = :status,
                updated_at = NOW()
            """,
            {
                "user_id": user_id,
                "video_id": video_id,
                "current_time": current_time,
                "duration": duration,
                "completion_percent": completion_percent,
                "status": status
            }
        )
        
        # Award achievement if completed
        if status == "completed":
            await self._award_video_completion(user_id, video_id)
    
    async def get_resume_position(self, user_id, video_id):
        """Get position to resume playback"""
        
        # Try Redis first (faster)
        redis_key = f"video_progress:{user_id}:{video_id}"
        progress = self.redis.hgetall(redis_key)
        
        if progress:
            return float(progress.get("current_time", 0))
        
        # Fallback to database
        result = await self.db.fetch_one(
            "SELECT current_time FROM video_progress WHERE user_id = :user_id AND video_id = :video_id",
            {"user_id": user_id, "video_id": video_id}
        )
        
        return result["current_time"] if result else 0
```

### Completion Criteria

- **Started**: Video played for > 10 seconds
- **In Progress**: 10% - 89% watched
- **Completed**: ≥ 90% watched OR user manually marks as complete

**Why 90%?**: Allows skipping credits/outro while still counting as complete

---

## Analytics & Monitoring

### Video Analytics to Track

```python
video_analytics = {
    "playback_metrics": {
        "plays": "Total number of video plays",
        "unique_viewers": "Unique users who watched",
        "completion_rate": "% who watched to 90%",
        "avg_watch_time": "Average time spent watching",
        "avg_completion_percent": "Average % of video watched"
    },
    
    "engagement_metrics": {
        "replays": "Times users re-watched",
        "bookmarks_added": "Number of bookmarks created",
        "shares": "Times video was shared",
        "chapter_skips": "Most skipped chapters"
    },
    
    "quality_metrics": {
        "buffering_ratio": "% of time spent buffering",
        "startup_time": "Time to first frame",
        "quality_switches": "Adaptive bitrate changes",
        "error_rate": "Playback errors"
    },
    
    "user_behavior": {
        "playback_speed_distribution": "Speed preferences",
        "caption_usage": "% using subtitles",
        "pip_usage": "Picture-in-picture usage",
        "most_rewatched_segments": "Popular rewind points"
    }
}
```

### Player Performance Monitoring

```python
# monitoring/video_metrics.py

class VideoMetrics:
    @staticmethod
    async def track_playback_event(event_type, video_id, user_id, metadata):
        """Track video player events"""
        
        events = {
            "play": lambda: track_play(video_id, user_id),
            "pause": lambda: track_pause(video_id, user_id, metadata["timestamp"]),
            "complete": lambda: track_complete(video_id, user_id),
            "buffer": lambda: track_buffer(video_id, user_id, metadata["duration"]),
            "error": lambda: track_error(video_id, user_id, metadata["error"]),
            "quality_change": lambda: track_quality_change(video_id, user_id, metadata["quality"])
        }
        
        if event_type in events:
            await events[event_type]()
        
        # Send to analytics pipeline
        await send_to_analytics({
            "event": event_type,
            "video_id": video_id,
            "user_id": user_id,
            "timestamp": datetime.now(),
            "metadata": metadata
        })
```

---

## UI Implementation Examples

### Streamlit Video Player

```python
# ui/components/video_player_component.py

import streamlit as st
import streamlit.components.v1 as components

def render_video_player(video_id, user_tier, user_id):
    """Render video player with all features"""
    
    # Get resume position
    resume_position = get_resume_position(user_id, video_id)
    
    # Get video metadata
    video = get_video_metadata(video_id)
    
    # Header
    st.title(video["title"])
    st.caption(f"Duration: {format_duration(video['duration'])} | Instructor: {video['instructor']}")
    
    # Player container
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Video player (custom HTML component)
        video_html = f"""
        <video 
            id="course-video"
            controls
            controlsList="nodownload"
            oncontextmenu="return false;"
            width="100%"
            data-video-id="{video_id}"
            data-user-id="{user_id}"
        >
            <source src="{get_video_url(video_id, user_id)}" type="application/x-mpegURL">
            <track label="English" kind="subtitles" srclang="en" src="{get_subtitle_url(video_id, 'en')}" default>
        </video>
        
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        <script>
            const video = document.getElementById('course-video');
            const hls = new Hls();
            hls.loadSource(video.querySelector('source').src);
            hls.attachMedia(video);
            
            // Resume from last position
            video.currentTime = {resume_position};
            
            // Track progress every 5 seconds
            setInterval(() => {{
                fetch('/api/videos/{video_id}/progress', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        current_time: video.currentTime,
                        duration: video.duration
                    }})
                }});
            }}, 5000);
        </script>
        """
        
        components.html(video_html, height=500)
        
        # Resume prompt
        if resume_position > 10:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("▶️ Resume from " + format_duration(resume_position)):
                    st.rerun()
            with col_b:
                if st.button("🔄 Start from beginning"):
                    reset_progress(user_id, video_id)
                    st.rerun()
        
        # Download button (tier-gated)
        st.markdown("---")
        render_download_section(video_id, user_tier, user_id)
    
    with col2:
        # Sidebar: Chapters
        st.subheader("📑 Chapters")
        for chapter in video["chapters"]:
            if st.button(
                f"{format_duration(chapter['time'])} - {chapter['title']}",
                key=f"chapter_{chapter['time']}"
            ):
                # Jump to chapter (would need JS integration)
                st.info(f"Jumping to {chapter['title']}")
        
        st.markdown("---")
        
        # Bookmarks
        st.subheader("🔖 Bookmarks")
        bookmarks = get_user_bookmarks(user_id, video_id)
        if bookmarks:
            for bm in bookmarks:
                st.write(f"**{format_duration(bm['timestamp'])}**")
                st.caption(bm['note'])
        else:
            st.caption("No bookmarks yet. Press 'B' while watching to add.")

def render_download_section(video_id, user_tier, user_id):
    """Render tier-gated download section"""
    
    st.subheader("⬇️ Download Video")
    
    if user_tier == "basic":
        st.button(
            "🔒 Download Video",
            disabled=True,
            help="Upgrade to Intermediate to download videos",
            use_container_width=True
        )
        st.info("⬆️ Upgrade to Intermediate tier to download videos up to 720p")
    
    elif user_tier == "intermediate":
        # Check quota
        quota_info = get_download_quota(user_id, user_tier)
        st.metric("Downloads Remaining", f"{quota_info['remaining']}/100 this month")
        
        if quota_info['remaining'] > 0:
            quality = st.selectbox("Select Quality", ["360p", "720p"])
            if st.button("⬇️ Download Video", use_container_width=True):
                download_url = initiate_download(video_id, quality, user_id)
                st.success(f"[Click here to download]({download_url})")
        else:
            st.warning("Monthly quota exceeded")
            st.info("⬆️ Upgrade to Advanced for unlimited downloads")
    
    else:  # advanced
        st.metric("Downloads", "Unlimited ♾️")
        quality = st.selectbox("Select Quality", ["360p", "720p", "1080p"])
        if st.button("⬇️ Download Video (Premium)", use_container_width=True):
            download_url = initiate_download(video_id, quality, user_id, drm=True)
            st.success(f"[Click here to download]({download_url})")
```

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [Feature Gating](./FEATURE_GATING.md)
- [UI/UX Design](./UI_UX_DESIGN.md)
- [Progress Tracking](./PROGRESS_TRACKING.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
