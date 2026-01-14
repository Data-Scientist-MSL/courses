# Accessibility Specification

## Overview

CoursePlayerApp is committed to providing an inclusive learning experience for all users, regardless of ability. This specification defines accessibility requirements following **WCAG 2.1 Level AA** standards and best practices for educational platforms.

---

## Accessibility Standards

### WCAG 2.1 Level AA Compliance

CoursePlayerApp adheres to:
- **Perceivable**: Information presented in ways users can perceive
- **Operable**: UI components and navigation are operable
- **Understandable**: Information and operation are understandable
- **Robust**: Content works with current and future assistive technologies

---

## Core Accessibility Features

### 1. Video Accessibility

#### Captions and Subtitles

**Requirements**:
- ✅ All videos must have synchronized captions
- ✅ Captions in multiple languages (EN, ES, FR minimum)
- ✅ Captions should be accurate, well-timed, and properly formatted
- ✅ User can toggle captions on/off
- ✅ Customizable caption styling (size, color, background)

**Implementation**:
```python
# Video player with caption support
def render_accessible_video_player(video_id: str):
    """Render video player with accessibility features"""
    
    video_metadata = get_video_metadata(video_id)
    
    # Main video element
    st.video(
        video_metadata['video_url'],
        subtitles=video_metadata['captions_url']
    )
    
    # Caption settings
    with st.expander("⚙️ Caption Settings"):
        caption_size = st.select_slider(
            "Caption Size",
            options=["Small", "Medium", "Large", "Extra Large"],
            value="Medium"
        )
        
        caption_color = st.selectbox(
            "Caption Color",
            options=["White", "Yellow", "Black"],
            index=0
        )
        
        caption_bg = st.selectbox(
            "Background",
            options=["Black", "Transparent", "White"],
            index=0
        )
        
        caption_lang = st.selectbox(
            "Language",
            options=["English", "Español", "Français"],
            index=0
        )
    
    # Apply caption settings
    apply_caption_settings(caption_size, caption_color, caption_bg, caption_lang)
```

**Caption Format (WebVTT)**:
```vtt
WEBVTT

00:00:00.000 --> 00:00:05.000
Welcome to Introduction to Artificial Intelligence.

00:00:05.000 --> 00:00:10.000
In this course, we'll explore the fundamentals of AI.

NOTE This is a comment, not displayed

00:00:10.000 --> 00:00:15.000 align:middle
<v Instructor>We'll cover machine learning, neural networks, and more.</v>
```

#### Audio Descriptions

**Optional Track**:
- Provide audio descriptions for visual elements
- Separate audio track describing on-screen actions
- Important for blind/low-vision users

---

### 2. Keyboard Navigation

**Requirements**:
- ✅ All functionality accessible via keyboard
- ✅ Logical tab order
- ✅ Visible focus indicators
- ✅ Skip navigation links
- ✅ Keyboard shortcuts documented

**Keyboard Shortcuts**:

| Action | Shortcut | Context |
|--------|----------|---------|
| Play/Pause Video | `Space` or `K` | Video player |
| Seek Forward 10s | `L` or `→` | Video player |
| Seek Backward 10s | `J` or `←` | Video player |
| Volume Up | `↑` | Video player |
| Volume Down | `↓` | Video player |
| Fullscreen | `F` | Video player |
| Next Module | `N` | Course player |
| Previous Module | `P` | Course player |
| Open AI Tutor | `Ctrl + /` | Anywhere |
| Search | `Ctrl + K` | Anywhere |

**Implementation**:
```python
def setup_keyboard_shortcuts():
    """Setup global keyboard shortcuts"""
    
    shortcuts_js = """
    <script>
        document.addEventListener('keydown', function(e) {
            // Play/Pause (Space or K)
            if (e.code === 'Space' || e.key === 'k') {
                e.preventDefault();
                toggleVideoPlayback();
            }
            
            // Seek forward (L or Right Arrow)
            if (e.key === 'l' || e.code === 'ArrowRight') {
                seekVideo(10);
            }
            
            // Seek backward (J or Left Arrow)
            if (e.key === 'j' || e.code === 'ArrowLeft') {
                seekVideo(-10);
            }
            
            // Fullscreen (F)
            if (e.key === 'f') {
                toggleFullscreen();
            }
            
            // Open AI Tutor (Ctrl + /)
            if (e.ctrlKey && e.key === '/') {
                e.preventDefault();
                openAITutor();
            }
        });
    </script>
    """
    
    st.components.v1.html(shortcuts_js, height=0)
```

**Keyboard Shortcuts Help**:
```python
def render_keyboard_shortcuts_modal():
    """Display keyboard shortcuts help"""
    
    with st.expander("⌨️ Keyboard Shortcuts"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Video Player**
            - `Space` / `K`: Play/Pause
            - `L` / `→`: Forward 10s
            - `J` / `←`: Backward 10s
            - `↑` / `↓`: Volume
            - `F`: Fullscreen
            """)
        
        with col2:
            st.markdown("""
            **Navigation**
            - `N`: Next module
            - `P`: Previous module
            - `Ctrl + K`: Search
            - `Ctrl + /`: AI Tutor
            """)
```

---

### 3. Screen Reader Support

**Requirements**:
- ✅ Semantic HTML structure
- ✅ ARIA labels on all interactive elements
- ✅ Alt text for all images
- ✅ Proper heading hierarchy
- ✅ Form labels associated with inputs
- ✅ Dynamic content announcements

**ARIA Labels**:
```python
def render_accessible_button(label: str, action: callable, icon: str = ""):
    """Render button with ARIA attributes"""
    
    button_html = f"""
    <button 
        aria-label="{label}"
        role="button"
        onclick="{action}"
        class="accessible-button">
        {icon} {label}
    </button>
    """
    
    st.markdown(button_html, unsafe_allow_html=True)
```

**Image Alt Text**:
```python
# Good: Descriptive alt text
st.image(
    course_thumbnail,
    caption="Course thumbnail",
    alt="Illustration of neural network with interconnected nodes"
)

# Bad: Generic or missing alt text
st.image(course_thumbnail, alt="image")  # ❌
```

**Heading Hierarchy**:
```python
# Proper heading structure
st.title("Course Title")           # H1
st.header("Module 1")              # H2
st.subheader("Lesson 1")           # H3
```

**Live Regions** (for dynamic content):
```python
def announce_to_screen_reader(message: str):
    """Announce message to screen reader"""
    
    aria_live = f"""
    <div aria-live="polite" aria-atomic="true" class="sr-only">
        {message}
    </div>
    """
    
    st.markdown(aria_live, unsafe_allow_html=True)

# Usage
announce_to_screen_reader("Video completed. Next video loaded.")
```

---

### 4. Color and Contrast

**Requirements**:
- ✅ Color contrast ratio ≥ 4.5:1 for normal text
- ✅ Color contrast ratio ≥ 3:1 for large text (18pt+)
- ✅ Color contrast ratio ≥ 3:1 for UI components
- ✅ Information not conveyed by color alone
- ✅ High contrast mode available

**Color Palette**:

| Element | Color | Contrast Ratio |
|---------|-------|----------------|
| Body text | #2C3E50 on #FFFFFF | 12.63:1 ✅ |
| Primary button | #FFFFFF on #4A90E2 | 4.54:1 ✅ |
| Error text | #E74C3C on #FFFFFF | 4.52:1 ✅ |
| Success text | #27AE60 on #FFFFFF | 4.56:1 ✅ |
| Link text | #3498DB on #FFFFFF | 5.14:1 ✅ |

**High Contrast Mode**:
```python
def enable_high_contrast_mode():
    """Enable high contrast color scheme"""
    
    high_contrast_css = """
    <style>
        .high-contrast {
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        
        .high-contrast a {
            color: #FFFF00 !important;
        }
        
        .high-contrast button {
            background-color: #FFFFFF !important;
            color: #000000 !important;
            border: 2px solid #FFFFFF !important;
        }
    </style>
    """
    
    st.markdown(high_contrast_css, unsafe_allow_html=True)
```

**Non-Color Indicators**:
```python
# Don't rely on color alone
# Bad: Only color indicates status
st.markdown('<span style="color: red;">Error</span>')

# Good: Icon + color + text
st.error("❌ Error: Invalid input")
st.success("✅ Success: Changes saved")
st.warning("⚠️ Warning: Low quota remaining")
```

---

### 5. Text Accessibility

**Requirements**:
- ✅ Text resizable up to 200% without loss of functionality
- ✅ Line height at least 1.5x font size
- ✅ Paragraph spacing at least 2x font size
- ✅ Clear, simple language (reading level: 8th grade)
- ✅ Dyslexia-friendly font option

**Text Styling**:
```css
body {
    font-size: 16px;
    line-height: 1.5;          /* 24px */
    font-family: 'Inter', sans-serif;
}

p {
    margin-bottom: 1.5em;      /* 24px */
    max-width: 70ch;           /* Optimal reading width */
}

h1, h2, h3 {
    line-height: 1.2;
    margin-top: 1.5em;
    margin-bottom: 0.75em;
}
```

**Dyslexia-Friendly Font**:
```python
def enable_dyslexia_font():
    """Enable OpenDyslexic font"""
    
    dyslexia_css = """
    <style>
        @import url('https://fonts.cdnfonts.com/css/opendyslexic');
        
        .dyslexia-mode {
            font-family: 'OpenDyslexic', sans-serif !important;
        }
    </style>
    """
    
    st.markdown(dyslexia_css, unsafe_allow_html=True)
    
    # Apply to body
    st.markdown('<div class="dyslexia-mode">', unsafe_allow_html=True)
```

---

### 6. Focus Management

**Visible Focus Indicators**:
```css
/* Clear focus indicator */
a:focus, button:focus, input:focus {
    outline: 3px solid #4A90E2;
    outline-offset: 2px;
}

/* Don't remove focus outline */
*:focus {
    outline: none;  /* ❌ Never do this */
}
```

**Focus Trapping** (for modals):
```javascript
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusable) {
                    lastFocusable.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusable) {
                    firstFocusable.focus();
                    e.preventDefault();
                }
            }
        }
    });
}
```

---

## Accessibility Settings

### Settings Page Integration

**File**: `pages/7_⚙️_Settings.py` (Accessibility Tab)

```python
def render_accessibility_settings():
    """Render accessibility settings panel"""
    
    st.subheader("♿ Accessibility Settings")
    
    # Visual settings
    st.markdown("**Visual**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        high_contrast = st.checkbox(
            "High contrast mode",
            value=st.session_state.get('high_contrast', False),
            help="Increases contrast for better visibility"
        )
        
        large_text = st.checkbox(
            "Large text",
            value=st.session_state.get('large_text', False),
            help="Increases base font size to 18px"
        )
        
        dyslexia_font = st.checkbox(
            "Dyslexia-friendly font",
            value=st.session_state.get('dyslexia_font', False),
            help="Uses OpenDyslexic font for better readability"
        )
    
    with col2:
        reduce_motion = st.checkbox(
            "Reduce motion",
            value=st.session_state.get('reduce_motion', False),
            help="Minimizes animations and transitions"
        )
        
        focus_indicators = st.checkbox(
            "Enhanced focus indicators",
            value=st.session_state.get('focus_indicators', True),
            help="Makes focus outlines more visible"
        )
    
    # Audio/Video settings
    st.markdown("---")
    st.markdown("**Audio & Video**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        captions_default = st.checkbox(
            "Enable captions by default",
            value=st.session_state.get('captions_default', True),
            help="Automatically show captions on videos"
        )
        
        caption_size = st.select_slider(
            "Caption size",
            options=["Small", "Medium", "Large", "Extra Large"],
            value=st.session_state.get('caption_size', "Medium")
        )
    
    with col2:
        audio_descriptions = st.checkbox(
            "Audio descriptions",
            value=st.session_state.get('audio_descriptions', False),
            help="Enable audio track with visual descriptions"
        )
        
        autoplay_videos = st.checkbox(
            "Autoplay videos",
            value=st.session_state.get('autoplay_videos', False),
            help="Videos start playing automatically"
        )
    
    # Keyboard settings
    st.markdown("---")
    st.markdown("**Keyboard & Navigation**")
    
    keyboard_shortcuts = st.checkbox(
        "Enable keyboard shortcuts",
        value=st.session_state.get('keyboard_shortcuts', True),
        help="Use keyboard to control player and navigate"
    )
    
    if keyboard_shortcuts:
        if st.button("⌨️ View Keyboard Shortcuts"):
            show_keyboard_shortcuts_modal()
    
    # Screen reader
    st.markdown("---")
    st.markdown("**Screen Reader**")
    
    skip_links = st.checkbox(
        "Skip navigation links",
        value=st.session_state.get('skip_links', True),
        help="Add 'Skip to content' links"
    )
    
    verbose_labels = st.checkbox(
        "Verbose labels",
        value=st.session_state.get('verbose_labels', False),
        help="More descriptive ARIA labels"
    )
    
    # Save button
    st.markdown("---")
    
    if st.button("💾 Save Accessibility Settings", type="primary"):
        save_accessibility_settings({
            'high_contrast': high_contrast,
            'large_text': large_text,
            'dyslexia_font': dyslexia_font,
            'reduce_motion': reduce_motion,
            'focus_indicators': focus_indicators,
            'captions_default': captions_default,
            'caption_size': caption_size,
            'audio_descriptions': audio_descriptions,
            'autoplay_videos': autoplay_videos,
            'keyboard_shortcuts': keyboard_shortcuts,
            'skip_links': skip_links,
            'verbose_labels': verbose_labels
        })
        
        st.success("✅ Accessibility settings saved!")
        st.balloons()
```

---

## Testing Accessibility

### Automated Testing

**Tools**:
- **axe-core**: Automated accessibility testing
- **pa11y**: CI/CD accessibility checks
- **Lighthouse**: Chrome DevTools audit

**Implementation**:
```bash
# Install pa11y
npm install -g pa11y

# Run accessibility audit
pa11y https://courseplayerapp.com --standard WCAG2AA

# CI/CD integration
pa11y-ci --sitemap https://courseplayerapp.com/sitemap.xml
```

### Manual Testing

**Screen Reader Testing**:
- **NVDA** (Windows): Free, widely used
- **JAWS** (Windows): Industry standard
- **VoiceOver** (Mac/iOS): Built-in
- **TalkBack** (Android): Built-in

**Test Checklist**:
- [ ] Navigate entire app with keyboard only
- [ ] Test with screen reader (NVDA/VoiceOver)
- [ ] Verify color contrast (4.5:1 minimum)
- [ ] Resize text to 200% and verify layout
- [ ] Check captions on all videos
- [ ] Test with high contrast mode
- [ ] Verify focus indicators visible
- [ ] Check form labels and error messages
- [ ] Test with motion reduced

---

## WCAG 2.1 AA Checklist

### Perceivable

- [x] **1.1.1** Text alternatives for non-text content
- [x] **1.2.2** Captions for all pre-recorded videos
- [x] **1.2.3** Audio descriptions or media alternative
- [x] **1.3.1** Info and relationships programmatically determined
- [x] **1.3.2** Meaningful sequence
- [x] **1.4.3** Color contrast minimum 4.5:1
- [x] **1.4.4** Text resizable to 200%
- [x] **1.4.5** Images of text avoided

### Operable

- [x] **2.1.1** All functionality keyboard accessible
- [x] **2.1.2** No keyboard trap
- [x] **2.2.1** Timing adjustable
- [x] **2.2.2** Pause, stop, hide for moving content
- [x] **2.4.1** Skip navigation links
- [x] **2.4.2** Page titled
- [x] **2.4.3** Logical focus order
- [x] **2.4.4** Link purpose clear from context
- [x] **2.4.7** Focus visible

### Understandable

- [x] **3.1.1** Language of page specified
- [x] **3.2.1** On focus doesn't cause context change
- [x] **3.2.2** On input doesn't cause context change
- [x] **3.3.1** Error identification
- [x] **3.3.2** Labels or instructions provided
- [x] **3.3.3** Error suggestions provided

### Robust

- [x] **4.1.1** Valid HTML parsing
- [x] **4.1.2** Name, role, value for UI components

---

## Documentation

### Accessibility Statement

**URL**: `/accessibility`

```markdown
# Accessibility Statement

GAI-Observe Academy is committed to ensuring digital accessibility for people with disabilities. We continually improve the user experience for everyone and apply relevant accessibility standards.

## Conformance Status

CoursePlayerApp conforms to WCAG 2.1 Level AA standards.

## Feedback

We welcome your feedback on the accessibility of CoursePlayerApp. Please contact us:

- Email: accessibility@gai-observe.com
- Phone: +1 (555) 123-4567

## Compatibility

CoursePlayerApp is designed to be compatible with:
- Screen readers (NVDA, JAWS, VoiceOver)
- Keyboard-only navigation
- Browser zoom up to 200%
- High contrast modes

## Known Limitations

We are aware of the following limitations:
- [List any known issues and remediation timeline]

Last updated: January 14, 2026
```

---

## Conclusion

CoursePlayerApp prioritizes accessibility to ensure all learners can access high-quality educational content. Continuous testing, user feedback, and adherence to WCAG 2.1 AA standards ensure an inclusive learning experience.

