# CoursePlayerApp - Video Player Specification

## Overview

The video player is a core component of CoursePlayerApp that delivers adaptive video experiences based on user tier. It supports streaming and downloading with tier-appropriate quality levels, playback controls, and progress tracking.

---

## Video Storage Architecture

### Storage Provider
**Primary**: Cloudflare R2 (S3-compatible object storage)
**Fallback**: AWS S3

**Advantages of R2**:
- No egress fees (cost-effective for streaming)
- Global CDN distribution
- S3-compatible API
- Built-in DDoS protection

### Video Organization

```
r2://courseplayerapp-videos/
├── courses/
│   ├── ai-01/
│   │   ├── module-01/
│   │   │   ├── video-01-intro/
│   │   │   │   ├── 480p.mp4
│   │   │   │   ├── 720p.mp4
│   │   │   │   ├── 1080p.mp4
│   │   │   │   ├── master.m3u8 (HLS manifest)
│   │   │   │   ├── subtitles-en.vtt
│   │   │   │   └── thumbnail.jpg
│   │   │   └── video-02-concepts/
│   │   │       └── ...
│   │   └── module-02/
│   │       └── ...
│   └── ai-02/
│       └── ...
└── thumbnails/
    └── ai-01-module-01-video-01.jpg
```

### Video Encoding Specifications

| Quality | Resolution | Bitrate | Codec | Audio |
|---------|-----------|---------|-------|-------|
| **480p** | 854x480 | 1.5 Mbps | H.264 (High profile) | AAC 128kbps |
| **720p** | 1280x720 | 3.0 Mbps | H.264 (High profile) | AAC 192kbps |
| **1080p** | 1920x1080 | 6.0 Mbps | H.264 (High profile) | AAC 256kbps |

**Container Format**: MP4 (for progressive download), HLS (for adaptive streaming)

**Frame Rate**: 30fps (60fps for high-motion content like coding demos)

---

## Streaming vs Download

### Streaming (All Tiers)

**Technology**: HLS (HTTP Live Streaming)

**Benefits**:
- Adaptive bitrate (automatically adjusts to network conditions)
- Fast startup (begins playback before entire video downloads)
- Bandwidth efficient (only streams what's watched)
- No local storage required

**Implementation**:
```python
# video_streaming.py
def get_hls_url(video_id: str, tier: str) -> str:
    """Generate HLS streaming URL based on tier"""
    flags = FeatureFlags.get_flags(tier)
    quality = flags["video_quality"]
    
    # Map quality to HLS variant
    quality_map = {
        "480p": "480p.m3u8",
        "720p": "720p.m3u8",
        "1080p": "1080p.m3u8"
    }
    
    variant = quality_map.get(quality, "480p.m3u8")
    
    # Generate signed URL (expires in 3 hours)
    base_url = f"https://videos.courseplayerapp.com/{video_id}/{variant}"
    signed_url = generate_signed_url(base_url, expiry=10800)
    
    return signed_url
```

### Download (Intermediate & Advanced)

**Technology**: Progressive download (MP4)

**Tier-Specific Behavior**:

| Tier | Download Allowed | Quality Options | File Size (60 min video) |
|------|-----------------|-----------------|-------------------------|
| **Basic** | ❌ No | N/A | N/A |
| **Intermediate** | ✅ Yes | 720p only | ~1.5 GB |
| **Advanced** | ✅ Yes | 1080p, 720p, 480p | 480p: ~700 MB<br>720p: ~1.5 GB<br>1080p: ~3.0 GB |

**Implementation**:
```python
# video_download.py
import streamlit as st
from utils.feature_flags import FeatureFlags

def render_download_button(video_id: str, tier: str):
    """Render download button based on tier permissions"""
    flags = FeatureFlags.get_flags(tier)
    
    if not flags["video_download"]:
        # Basic tier - show locked download
        st.button("⬇️ Download Video", disabled=True, 
                 help="🔒 Download available in Intermediate tier ($247)")
        st.caption("💡 Upgrade to download videos for offline viewing")
        return
    
    # Get available quality options
    quality_options = flags["video_quality_options"]
    
    if len(quality_options) == 1:
        # Intermediate tier - single quality
        quality = quality_options[0]
        if st.button(f"⬇️ Download Video ({quality})"):
            download_url = generate_download_url(video_id, quality)
            st.download_button(
                label=f"Click to download ({quality})",
                data=get_video_file(download_url),
                file_name=f"video_{video_id}_{quality}.mp4",
                mime="video/mp4"
            )
    else:
        # Advanced tier - quality selection
        selected_quality = st.selectbox("Download Quality", quality_options)
        if st.button(f"⬇️ Download Video"):
            download_url = generate_download_url(video_id, selected_quality)
            st.download_button(
                label=f"Click to download ({selected_quality})",
                data=get_video_file(download_url),
                file_name=f"video_{video_id}_{selected_quality}.mp4",
                mime="video/mp4"
            )


def generate_download_url(video_id: str, quality: str) -> str:
    """Generate signed download URL (expires in 1 hour)"""
    base_url = f"https://videos.courseplayerapp.com/{video_id}/{quality}.mp4"
    signed_url = generate_signed_url(base_url, expiry=3600)
    return signed_url
```

---

## Player Features

### Core Controls

**Play/Pause**
- Spacebar keyboard shortcut
- Click on video to toggle
- Large play button overlay (on pause)

**Seek / Timeline Scrubbing**
- Click on timeline to jump to position
- Drag timeline scrubber
- Arrow keys: ←→ (5 seconds), ⇧←→ (10 seconds)
- Display current time / total duration (e.g., "12:34 / 45:00")

**Volume Control**
- Volume slider (0-100%)
- Mute/unmute button
- Keyboard shortcuts: ↑↓ (volume), M (mute)
- Remember volume preference (localStorage)

**Fullscreen**
- Fullscreen button (top-right of player)
- Keyboard shortcut: F
- Exit fullscreen: ESC

### Advanced Features

**Playback Speed Control**

Available speeds: 0.5x, 0.75x, 1x (normal), 1.25x, 1.5x, 1.75x, 2x

```python
def render_speed_control():
    """Render playback speed selector"""
    speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
    speed_labels = {
        0.5: "0.5x (Slow)",
        0.75: "0.75x",
        1.0: "1x (Normal)",
        1.25: "1.25x",
        1.5: "1.5x",
        1.75: "1.75x",
        2.0: "2x (Fast)"
    }
    
    current_speed = st.session_state.get("playback_speed", 1.0)
    selected_speed = st.selectbox(
        "Speed",
        speeds,
        index=speeds.index(current_speed),
        format_func=lambda x: speed_labels[x]
    )
    
    if selected_speed != current_speed:
        st.session_state["playback_speed"] = selected_speed
        # JavaScript to update video playback rate
        st.markdown(f"""
        <script>
            document.querySelector('video').playbackRate = {selected_speed};
        </script>
        """, unsafe_allow_html=True)
```

**Captions/Subtitles**

- Support for WebVTT format (`.vtt`)
- Multiple languages (tier-dependent)
- Toggleable on/off
- Customizable styling (size, color, background)

**Tier-Specific Caption Languages**:

| Tier | Languages |
|------|-----------|
| **Basic** | English only |
| **Intermediate** | English |
| **Advanced** | English, Spanish, French, German, Chinese |

**Picture-in-Picture (PiP)**

- Browser-dependent feature (Chrome, Edge, Safari)
- Allows video to float in small window while browsing other tabs
- Enabled for all tiers
- Button appears on hover (if supported)

**Resume from Last Position**

- Automatically save playback position every 10 seconds
- On video load, offer to resume: "Resume from 12:34?"
- Store in progress database (per user, per video)

```python
# video_progress.py
import streamlit as st
from utils.progress_tracker import save_video_progress, get_video_progress

def render_video_with_resume(video_id: str, video_url: str):
    """Render video player with resume functionality"""
    user_id = st.session_state.get("user_id")
    
    # Get last watched position
    last_position = get_video_progress(user_id, video_id)
    
    if last_position > 10:  # Only offer resume if >10 seconds watched
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"⏱️ Resume from {format_time(last_position)}?")
        with col2:
            if st.button("Resume"):
                st.session_state[f"start_time_{video_id}"] = last_position
            if st.button("Start Over"):
                st.session_state[f"start_time_{video_id}"] = 0
    
    # Render video player
    start_time = st.session_state.get(f"start_time_{video_id}", 0)
    st.video(video_url, start_time=int(start_time))
    
    # Save progress on interval (via JavaScript callback)
    st.markdown("""
    <script>
        const video = document.querySelector('video');
        setInterval(() => {
            if (!video.paused) {
                // Send current time to backend
                fetch('/api/progress/video', {
                    method: 'POST',
                    body: JSON.stringify({
                        video_id: '%s',
                        position: video.currentTime
                    })
                });
            }
        }, 10000);  // Every 10 seconds
    </script>
    """ % video_id, unsafe_allow_html=True)


def format_time(seconds: int) -> str:
    """Format seconds to MM:SS or HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"
```

---

## Video Player UI Implementation

### Streamlit Native Video Player

```python
# components/video_player.py
import streamlit as st
from utils.feature_flags import FeatureFlags

def render_video_player(
    video_id: str,
    course_id: str,
    module_id: str,
    tier: str,
    title: str = "Lecture Video"
):
    """
    Render complete video player component
    
    Args:
        video_id: Unique video identifier
        course_id: Course ID (for storage path)
        module_id: Module ID (for storage path)
        tier: User's subscription tier
        title: Video title to display
    """
    st.subheader(f"🎥 {title}")
    
    # Get feature flags
    flags = FeatureFlags.get_flags(tier)
    
    # Generate streaming URL
    video_url = get_hls_url(video_id, tier)
    
    # Resume from last position
    render_video_with_resume(video_id, video_url)
    
    # Video controls row
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Playback speed
        render_speed_control()
    
    with col2:
        # Subtitles
        caption_langs = flags["video_captions"]
        if len(caption_langs) > 0:
            selected_lang = st.selectbox("Captions", ["Off"] + caption_langs)
            if selected_lang != "Off":
                load_subtitles(video_id, selected_lang)
    
    with col3:
        # Quality info
        quality = flags["video_quality"]
        st.metric("Quality", quality)
    
    # Download section (gated)
    st.divider()
    st.subheader("💾 Download")
    render_download_button(video_id, tier)
    
    # Transcript (if available)
    render_transcript(video_id)


def render_transcript(video_id: str):
    """Render video transcript (text version)"""
    with st.expander("📝 View Transcript"):
        transcript = get_video_transcript(video_id)
        if transcript:
            st.text_area("Transcript", transcript, height=300)
        else:
            st.info("Transcript not available for this video")
```

### Custom Video Player (Advanced)

For more control, use a custom HTML5 video player with JavaScript:

```python
# components/custom_video_player.py
import streamlit.components.v1 as components

def render_custom_player(video_url: str, subtitle_url: str = None):
    """Render custom HTML5 video player with advanced controls"""
    
    subtitle_track = ""
    if subtitle_url:
        subtitle_track = f'<track src="{subtitle_url}" kind="subtitles" srclang="en" label="English" default>'
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            video {{
                width: 100%;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .controls {{
                display: flex;
                align-items: center;
                gap: 10px;
                margin-top: 10px;
                padding: 10px;
                background: #f0f0f0;
                border-radius: 5px;
            }}
            .btn {{
                padding: 8px 16px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            .btn:hover {{ background: #45a049; }}
        </style>
    </head>
    <body>
        <video id="videoPlayer" controls>
            <source src="{video_url}" type="video/mp4">
            {subtitle_track}
            Your browser does not support the video tag.
        </video>
        
        <div class="controls">
            <button class="btn" onclick="setSpeed(0.5)">0.5x</button>
            <button class="btn" onclick="setSpeed(1)">1x</button>
            <button class="btn" onclick="setSpeed(1.5)">1.5x</button>
            <button class="btn" onclick="setSpeed(2)">2x</button>
            <button class="btn" onclick="togglePiP()">PiP</button>
        </div>
        
        <script>
            const video = document.getElementById('videoPlayer');
            
            function setSpeed(speed) {{
                video.playbackRate = speed;
            }}
            
            function togglePiP() {{
                if (document.pictureInPictureElement) {{
                    document.exitPictureInPicture();
                }} else {{
                    video.requestPictureInPicture();
                }}
            }}
            
            // Save progress every 10 seconds
            setInterval(() => {{
                if (!video.paused) {{
                    const progress = {{
                        position: video.currentTime,
                        duration: video.duration
                    }};
                    // Send to parent Streamlit app
                    window.parent.postMessage(progress, '*');
                }}
            }}, 10000);
        </script>
    </body>
    </html>
    """
    
    components.html(html_code, height=600)
```

---

## Video Quality Adaptation

### Automatic Quality Selection

For HLS streaming, the player automatically selects quality based on:
- Available bandwidth
- Device screen resolution
- Network stability

**Algorithm**:
1. Start with lowest quality (480p) for fast startup
2. Monitor buffer fill rate
3. If buffer is consistently full, upgrade to next quality
4. If buffer depletes, downgrade quality
5. Never exceed tier's maximum quality

### Manual Quality Override (Advanced Tier)

Advanced tier users can manually select quality:

```python
def render_quality_selector(tier: str):
    """Render quality selector for Advanced tier"""
    if tier != "advanced":
        return
    
    qualities = ["Auto", "1080p", "720p", "480p"]
    selected = st.radio("Video Quality", qualities, horizontal=True)
    
    if selected == "Auto":
        st.caption("Quality adapts to your internet speed")
    else:
        st.caption(f"Quality locked to {selected}")
        # Update HLS variant selection
```

---

## Accessibility Features

### Keyboard Navigation

| Key | Action |
|-----|--------|
| **Space** | Play/Pause |
| **←** | Rewind 5 seconds |
| **→** | Forward 5 seconds |
| **↑** | Increase volume |
| **↓** | Decrease volume |
| **M** | Mute/Unmute |
| **F** | Toggle fullscreen |
| **C** | Toggle captions |
| **0-9** | Jump to 0%-90% of video |

### Screen Reader Support

- ARIA labels for all controls
- Announce playback state changes
- Describe video content in `<video>` tag `aria-label`

```html
<video aria-label="Lecture video: Introduction to Machine Learning. Duration: 45 minutes.">
```

### Caption Customization

Advanced tier users can customize caption appearance:

```python
def render_caption_settings(tier: str):
    """Render caption customization (Advanced tier only)"""
    if tier != "advanced":
        return
    
    with st.expander("⚙️ Caption Settings"):
        font_size = st.slider("Font Size", 12, 24, 16)
        font_color = st.color_picker("Text Color", "#FFFFFF")
        bg_color = st.color_picker("Background Color", "#000000")
        bg_opacity = st.slider("Background Opacity", 0.0, 1.0, 0.7)
        
        # Apply settings via CSS
        st.markdown(f"""
        <style>
            video::cue {{
                font-size: {font_size}px;
                color: {font_color};
                background-color: {bg_color};
                opacity: {bg_opacity};
            }}
        </style>
        """, unsafe_allow_html=True)
```

---

## Performance Optimization

### Video Preloading

```html
<video preload="metadata">
```

- `metadata`: Load only metadata (duration, dimensions) - default
- `auto`: Preload entire video (only for short videos <5 min)
- `none`: Don't preload (save bandwidth)

### Thumbnail Generation

Generate thumbnail at 10% mark of video:

```bash
ffmpeg -i input.mp4 -ss 00:01:30 -vframes 1 -vf scale=320:180 thumbnail.jpg
```

Display thumbnail while video loads:

```python
st.image(f"https://videos.courseplayerapp.com/{video_id}/thumbnail.jpg", 
         caption="Video thumbnail")
```

### CDN Caching

- Videos cached at edge (Cloudflare CDN)
- Cache-Control header: `public, max-age=31536000` (1 year)
- Invalidate cache on video update (rare)

---

## Analytics & Tracking

### Video Engagement Metrics

Track:
- **Watch time**: Total seconds watched
- **Completion rate**: % of video watched (e.g., 87%)
- **Drop-off points**: Timestamps where users stop watching
- **Rewatch segments**: Sections watched multiple times
- **Average watch duration**: Across all users

**Implementation**:

```python
# utils/video_analytics.py
def track_video_event(event_type: str, video_id: str, position: float, user_id: str):
    """Track video playback events"""
    event_data = {
        "event_type": event_type,  # play, pause, seek, complete
        "video_id": video_id,
        "position_seconds": position,
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "tier": get_user_tier(user_id)
    }
    
    # Send to analytics backend
    send_to_analytics(event_data)
```

### Heatmap Visualization (Advanced Tier)

Show engagement heatmap:
- Green: High rewatch rate (important sections)
- Yellow: Normal playback
- Red: High drop-off rate (improve content)

---

## Error Handling

### Common Video Errors

**Error 1: Video Not Found (404)**
```python
if response.status_code == 404:
    st.error("🚫 Video not found. Please contact support.")
    st.info("Error Code: VID_404")
```

**Error 2: Insufficient Tier**
```python
if not has_access:
    st.warning("🔒 This video requires Intermediate tier or higher.")
    st.button("Upgrade Now")
```

**Error 3: Network Error**
```python
try:
    video_url = get_hls_url(video_id, tier)
except NetworkError:
    st.error("🌐 Network error. Please check your internet connection.")
    if st.button("Retry"):
        st.rerun()
```

**Error 4: Playback Error**
```python
st.markdown("""
<script>
    const video = document.querySelector('video');
    video.addEventListener('error', (e) => {
        console.error('Video error:', e);
        alert('Video playback error. Try refreshing the page.');
    });
</script>
""", unsafe_allow_html=True)
```

---

## Testing Checklist

### Functional Tests
- [ ] Video plays correctly for all tiers
- [ ] Quality matches tier (480p/720p/1080p)
- [ ] Download button enabled/disabled per tier
- [ ] Resume from last position works
- [ ] Playback speed control works (0.5x - 2x)
- [ ] Captions load and display correctly
- [ ] Fullscreen mode works
- [ ] Picture-in-Picture works (if supported)

### Performance Tests
- [ ] Video loads within 2 seconds (on 10 Mbps connection)
- [ ] Buffering is minimal (<5% of playback time)
- [ ] Seeking is responsive (<500ms to jump)
- [ ] No memory leaks on long playback sessions

### Accessibility Tests
- [ ] All keyboard shortcuts work
- [ ] Screen reader announces controls
- [ ] Captions are readable (contrast ≥4.5:1)
- [ ] Focus indicators visible

### Cross-Browser Tests
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (macOS/iOS)
- [ ] Mobile browsers (responsive design)

---

## Future Enhancements

### Phase 2
- **Interactive transcripts**: Click on text to jump to that point in video
- **Bookmarks**: Save favorite moments
- **Notes**: Take timestamped notes while watching
- **Variable speed per user preference**: Remember last used speed

### Phase 3
- **AI-generated summaries**: Key points from each video
- **Video chapters**: Jump to specific sections (intro, demo, summary)
- **Watch parties**: Synchronized viewing with other students
- **Offline download**: Progressive Web App (PWA) for offline viewing

---

## Conclusion

The adaptive video player provides:
- **Tier-appropriate experiences**: Clear differentiation between Basic, Intermediate, Advanced
- **Robust playback**: HLS streaming with fallback
- **Rich features**: Speed control, captions, resume, PiP
- **Accessibility**: Keyboard navigation, screen reader support
- **Performance**: CDN-delivered, optimized encoding
- **Analytics**: Comprehensive engagement tracking

This design balances user experience with business requirements, encouraging upgrades while delivering value at every tier.
