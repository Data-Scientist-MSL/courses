# Accessibility Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Ensure WCAG 2.1 AA compliance and inclusive design

---

## Overview

EdGuide is committed to providing an inclusive learning experience for all students, including those with disabilities. This specification outlines accessibility requirements, implementation guidelines, and testing procedures to meet WCAG 2.1 Level AA standards.

---

## WCAG 2.1 Compliance

### Level AA Requirements

**Target**: 100% WCAG 2.1 Level AA compliance

**Key Principles** (POUR):
1. **Perceivable**: Information must be presentable to users in ways they can perceive
2. **Operable**: Interface components must be operable
3. **Understandable**: Information and operation must be understandable
4. **Robust**: Content must be robust enough for assistive technologies

---

## 1. Perceivable Content

### 1.1 Text Alternatives

#### Images and Media

**Requirement**: All non-text content must have text alternatives

**Implementation**:
```html
<!-- Images -->
<img src="diagram.png" alt="Neural network architecture with input, hidden, and output layers">

<!-- Decorative images -->
<img src="decorative-line.png" alt="" role="presentation">

<!-- Complex images -->
<img src="chart.png" alt="Bar chart showing accuracy improvements" longdesc="#chart-description">
<div id="chart-description">
  <p>Detailed description: The chart shows model accuracy improving from 65% in week 1 to 95% in week 8...</p>
</div>

<!-- Icons with text -->
<button>
  <svg aria-hidden="true">...</svg>
  <span>Download Video</span>
</button>

<!-- Icons without text -->
<button aria-label="Play video">
  <svg aria-hidden="true">...</svg>
</button>
```

**Video Accessibility**:
```python
def render_accessible_video(video_id, user_id):
    """Render video player with full accessibility"""
    
    video_html = f"""
    <video 
        id="course-video"
        controls
        aria-label="Course lecture video"
    >
        <source src="{get_video_url(video_id)}" type="application/x-mpegURL">
        
        <!-- Captions (required) -->
        <track 
            label="English" 
            kind="captions" 
            srclang="en" 
            src="{get_captions_url(video_id, 'en')}" 
            default
        >
        
        <!-- Subtitles (additional languages) -->
        <track 
            label="Spanish" 
            kind="subtitles" 
            srclang="es" 
            src="{get_captions_url(video_id, 'es')}"
        >
        
        <!-- Descriptions (for blind users) -->
        <track 
            label="Audio Descriptions" 
            kind="descriptions" 
            srclang="en" 
            src="{get_descriptions_url(video_id)}"
        >
        
        <!-- Fallback -->
        <p>Your browser doesn't support HTML5 video. 
           <a href="{get_download_url(video_id)}">Download the video</a> instead.
        </p>
    </video>
    """
```

#### Captions and Transcripts

**Requirements**:
- All videos must have synchronized captions (WCAG 1.2.2)
- Pre-recorded videos should have transcripts (WCAG 1.2.8)
- Live captions for live streaming (WCAG 1.2.4)

**Caption Quality Standards**:
```yaml
captions:
  accuracy: ">99%"
  synchronization: "±250ms"
  
  format: "WebVTT"
  
  styling:
    - Speaker identification
    - Sound effects notation [applause], [music]
    - Positioning for speaker identification
    
  guidelines:
    - Max 2 lines per caption
    - Max 32 characters per line
    - Display duration: 1-7 seconds
    - Reading speed: 160-180 words/minute
```

**Transcript Implementation**:
```python
def render_video_transcript(video_id):
    """Render searchable, interactive transcript"""
    
    st.subheader("📝 Transcript")
    
    transcript = get_video_transcript(video_id)
    
    # Searchable transcript
    search_term = st.text_input("Search transcript")
    
    if search_term:
        transcript = highlight_search_terms(transcript, search_term)
    
    # Interactive transcript (click to jump to timestamp)
    for segment in transcript["segments"]:
        timestamp = format_timestamp(segment["start_time"])
        
        col1, col2 = st.columns([1, 9])
        
        with col1:
            if st.button(timestamp, key=f"ts_{segment['id']}"):
                jump_to_timestamp(video_id, segment["start_time"])
        
        with col2:
            st.markdown(segment["text"])
    
    # Download transcript
    st.download_button(
        "⬇️ Download Transcript",
        data=format_transcript_as_text(transcript),
        file_name=f"transcript_{video_id}.txt",
        mime="text/plain"
    )
```

### 1.2 Adaptable Content

#### Responsive Design

**Requirement**: Content must adapt to different viewport sizes and orientations

**Breakpoints**:
```css
/* Mobile first approach */
.container {
  width: 100%;
  padding: 1rem;
}

/* Tablet */
@media (min-width: 640px) {
  .container {
    max-width: 640px;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

/* Large desktop */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}
```

#### Text Resizing

**Requirement**: Text must be resizable up to 200% without loss of functionality (WCAG 1.4.4)

```css
/* Use relative units */
body {
  font-size: 16px; /* Base size */
}

h1 {
  font-size: 2rem; /* 32px, scales with base */
}

p {
  font-size: 1rem; /* 16px, scales with base */
  line-height: 1.5; /* Maintains readability when zoomed */
}

/* Allow user font size preferences */
@media (prefers-reduced-motion: reduce) {
  font-size: 18px; /* Larger base for users who prefer it */
}
```

### 1.3 Distinguishable Content

#### Color Contrast

**Requirement**: Minimum contrast ratios (WCAG 1.4.3)
- Normal text: 4.5:1
- Large text (18pt+ or 14pt+ bold): 3:1
- UI components: 3:1

**Color Palette (AA Compliant)**:
```yaml
accessible_colors:
  # Text on white background
  text_on_light:
    primary: "#212529"     # 16.1:1 ratio ✓
    secondary: "#495057"   # 9.8:1 ratio ✓
    link: "#0056b3"        # 6.3:1 ratio ✓
    
  # Text on dark background
  text_on_dark:
    primary: "#FFFFFF"     # 21:1 ratio ✓
    secondary: "#E9ECEF"   # 17.8:1 ratio ✓
    link: "#5DADE2"        # 5.1:1 ratio ✓
    
  # UI components
  button_primary:
    bg: "#0056b3"
    text: "#FFFFFF"        # 8.6:1 ratio ✓
    
  button_secondary:
    bg: "#FFFFFF"
    text: "#0056b3"        # 8.6:1 ratio ✓
    border: "#0056b3"      # 3:1 ratio (border) ✓
```

**Validation**:
```python
def validate_color_contrast(foreground, background, text_size="normal"):
    """Validate color contrast ratio"""
    
    ratio = calculate_contrast_ratio(foreground, background)
    
    if text_size == "large":
        required_ratio = 3.0
    else:
        required_ratio = 4.5
    
    passes = ratio >= required_ratio
    
    return {
        "ratio": ratio,
        "required": required_ratio,
        "passes": passes,
        "wcag_level": "AA" if passes else "Fail"
    }
```

#### Non-Color Indicators

**Requirement**: Don't rely on color alone to convey information (WCAG 1.4.1)

**Examples**:
```python
# Bad: Color only
st.markdown("🔴 Error") # Red color only

# Good: Color + icon + text
st.error("❌ Error: Invalid input") # Icon, color, and text

# Bad: Color-coded status
if status == "success":
    st.markdown('<span style="color: green">●</span> Complete')

# Good: Icon + color + text
if status == "success":
    st.success("✅ Complete")
```

#### Focus Indicators

**Requirement**: Keyboard focus must be clearly visible (WCAG 2.4.7)

```css
/* Clear focus indicators */
a:focus,
button:focus,
input:focus,
select:focus,
textarea:focus {
  outline: 2px solid #0056b3;
  outline-offset: 2px;
  box-shadow: 0 0 0 3px rgba(0, 86, 179, 0.2);
}

/* Don't remove focus outline */
*:focus {
  outline: revert; /* Never use outline: none without replacement */
}

/* Custom focus styles */
.button:focus-visible {
  outline: 2px solid #0056b3;
  outline-offset: 2px;
}
```

---

## 2. Operable Interface

### 2.1 Keyboard Accessible

**Requirement**: All functionality must be available via keyboard (WCAG 2.1.1)

#### Keyboard Navigation

**Tab Order**:
```html
<!-- Logical tab order -->
<nav>
  <a href="#main" class="skip-link">Skip to main content</a>
  <a href="/" tabindex="0">Home</a>
  <a href="/courses" tabindex="0">Courses</a>
  <a href="/progress" tabindex="0">Progress</a>
</nav>

<main id="main">
  <!-- Main content -->
  <button tabindex="0">Start Course</button>
  <input type="text" tabindex="0" placeholder="Search">
</main>
```

**Skip Links**:
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<a href="#navigation" class="skip-link">Skip to navigation</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>
```

#### Keyboard Shortcuts

**Global Shortcuts**:
```yaml
keyboard_shortcuts:
  navigation:
    "/": "Focus search"
    "?": "Show keyboard shortcuts help"
    "h": "Go to home"
    "c": "Go to courses"
    "p": "Go to progress"
    "Esc": "Close modal/dialog"
    
  video_player:
    "Space": "Play/Pause"
    "k": "Play/Pause"
    "←": "Rewind 10 seconds"
    "→": "Forward 10 seconds"
    "↑": "Volume up"
    "↓": "Volume down"
    "m": "Mute/Unmute"
    "f": "Fullscreen"
    "c": "Toggle captions"
    "0-9": "Jump to 0%-90%"
```

**Shortcut Help Modal**:
```python
def render_keyboard_shortcuts():
    """Display keyboard shortcuts help"""
    
    if st.session_state.get("show_shortcuts"):
        with st.dialog("⌨️ Keyboard Shortcuts"):
            st.subheader("Navigation")
            st.markdown("""
            - `/` - Focus search
            - `?` - Show this help
            - `h` - Go to home
            - `c` - Go to courses
            """)
            
            st.subheader("Video Player")
            st.markdown("""
            - `Space` or `k` - Play/Pause
            - `←` - Rewind 10 seconds
            - `→` - Forward 10 seconds
            - `f` - Fullscreen
            - `c` - Toggle captions
            """)
            
            if st.button("Close"):
                st.session_state.show_shortcuts = False
                st.rerun()
```

### 2.2 Enough Time

**Requirement**: Users must have enough time to read and interact with content (WCAG 2.2.1)

#### Session Timeouts

```python
# Warning before session timeout
def render_session_timeout_warning():
    """Show warning 5 minutes before timeout"""
    
    time_remaining = get_session_time_remaining()
    
    if time_remaining <= 300:  # 5 minutes
        st.warning(
            f"⏰ Your session will expire in {time_remaining // 60} minutes. "
            "Click 'Continue' to extend."
        )
        
        if st.button("Continue Session"):
            extend_session()
            st.success("Session extended!")

# Auto-save progress
async def auto_save_progress(user_id, resource_id, position):
    """Auto-save every 30 seconds"""
    
    await save_progress(user_id, resource_id, position)
```

### 2.3 Seizures and Physical Reactions

**Requirement**: Don't use flashing content (WCAG 2.3.1)

**Guidelines**:
- No content flashes more than 3 times per second
- Avoid large flashing areas
- Provide warnings for unavoidable flashing content

```python
# Warning for content with flashing
if has_flashing_content(video_id):
    st.warning(
        "⚠️ Warning: This video contains flashing lights that may "
        "affect users with photosensitive epilepsy."
    )
```

### 2.4 Navigable

#### Page Titles

```python
# Descriptive page titles
st.set_page_config(
    page_title="Machine Learning Fundamentals - Module 3 - EdGuide",
    page_icon="🎓"
)
```

#### Headings and Labels

```html
<!-- Proper heading hierarchy -->
<h1>Course: Machine Learning Fundamentals</h1>
  <h2>Module 3: Neural Networks</h2>
    <h3>Lesson 2: Backpropagation</h3>
      <h4>Key Concepts</h4>
```

#### Link Purpose

```html
<!-- Bad: Ambiguous links -->
<a href="...">Click here</a>
<a href="...">Read more</a>

<!-- Good: Descriptive links -->
<a href="...">Download Machine Learning course syllabus (PDF, 2MB)</a>
<a href="...">Read the complete guide to Neural Networks</a>
```

---

## 3. Understandable Content

### 3.1 Readable

#### Language Declaration

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>EdGuide - Elite Agentic Learning Platform</title>
</head>
<body>
  <!-- Content in English -->
  
  <!-- Spanish section -->
  <section lang="es">
    <h2>Bienvenido</h2>
    <p>Contenido en español...</p>
  </section>
</body>
</html>
```

#### Reading Level

**Guideline**: Content should be written at a level understandable by users with lower secondary education (WCAG 3.1.5 - AAA)

**Tools**:
```python
def check_readability(text):
    """Check text readability score"""
    
    import textstat
    
    flesch_score = textstat.flesch_reading_ease(text)
    grade_level = textstat.flesch_kincaid_grade(text)
    
    return {
        "flesch_score": flesch_score,  # 60-70 = 8th-9th grade
        "grade_level": grade_level,    # Target: ≤ 9
        "recommendation": "Plain language preferred"
    }
```

### 3.2 Predictable

#### Consistent Navigation

```python
def render_main_navigation():
    """Consistent navigation across all pages"""
    
    # Same navigation structure on every page
    menu_items = ["Home", "My Courses", "Progress", "Achievements", "Profile"]
    
    selected = st.sidebar.radio("Navigation", menu_items)
    
    # Navigation always in same location (sidebar)
```

#### On Focus/Input

**Requirement**: Focus or input shouldn't cause unexpected context changes

```python
# Bad: Auto-submit on select
select = st.selectbox("Choose course", courses, on_change=submit_form)

# Good: Explicit submit
select = st.selectbox("Choose course", courses)
if st.button("Go to Course"):
    navigate_to_course(select)
```

### 3.3 Input Assistance

#### Error Identification

```python
def render_form_with_validation():
    """Form with clear error messages"""
    
    email = st.text_input("Email address")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        errors = []
        
        if not email:
            errors.append("❌ Email address is required")
        elif not is_valid_email(email):
            errors.append("❌ Email address is not valid. Please enter a valid email (e.g., user@example.com)")
        
        if not password:
            errors.append("❌ Password is required")
        elif len(password) < 8:
            errors.append("❌ Password must be at least 8 characters")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Process login
            login(email, password)
```

#### Labels and Instructions

```python
# Clear labels and instructions
st.subheader("Account Settings")

# Label with instruction
email = st.text_input(
    label="Email Address",
    help="We'll use this email for course notifications and certificate delivery"
)

# Required field indicator
st.text_input("Full Name *", placeholder="Enter your full name")
st.caption("* Required field")
```

---

## 4. Robust Content

### 4.1 Compatible

#### Valid HTML

```html
<!-- Valid, semantic HTML -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EdGuide - Course Player</title>
</head>
<body>
  <header role="banner">
    <nav role="navigation" aria-label="Main navigation">
      <!-- Navigation -->
    </nav>
  </header>
  
  <main role="main" id="main-content">
    <!-- Main content -->
  </main>
  
  <footer role="contentinfo">
    <!-- Footer -->
  </footer>
</body>
</html>
```

#### ARIA Attributes

```html
<!-- Proper ARIA usage -->

<!-- Landmark roles -->
<nav role="navigation" aria-label="Course curriculum">...</nav>
<main role="main">...</main>
<aside role="complementary" aria-label="AI Tutor">...</aside>

<!-- Live regions -->
<div role="status" aria-live="polite" aria-atomic="true">
  Progress saved successfully
</div>

<div role="alert" aria-live="assertive">
  Error: Failed to submit quiz
</div>

<!-- Interactive elements -->
<button 
  aria-label="Play video"
  aria-pressed="false"
  aria-controls="video-player"
>
  <svg aria-hidden="true">...</svg>
</button>

<!-- Expandable sections -->
<button 
  aria-expanded="false"
  aria-controls="module-content"
  id="module-toggle"
>
  Module 3: Neural Networks
</button>
<div 
  id="module-content"
  aria-labelledby="module-toggle"
  hidden
>
  <!-- Module content -->
</div>

<!-- Loading states -->
<div role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100">
  Loading: 60%
</div>
```

---

## Screen Reader Support

### Announcement Strategy

```python
def announce_to_screen_reader(message, priority="polite"):
    """Announce message to screen readers"""
    
    # Create live region
    aria_live = priority  # "polite" or "assertive"
    
    st.markdown(
        f'<div role="status" aria-live="{aria_live}" aria-atomic="true">{message}</div>',
        unsafe_allow_html=True
    )
```

### Screen Reader Testing

**Required Tests**:
- NVDA (Windows)
- JAWS (Windows)
- VoiceOver (macOS, iOS)
- TalkBack (Android)

**Test Scenarios**:
1. Navigate entire course page
2. Watch video with captions
3. Complete a lab exercise
4. Submit a quiz
5. View certificates

---

## Testing & Validation

### Automated Testing Tools

```yaml
automated_tools:
  - axe DevTools (browser extension)
  - WAVE (Web Accessibility Evaluation Tool)
  - Lighthouse (Chrome DevTools)
  - Pa11y (CI/CD integration)
  
lighthouse_targets:
  accessibility_score: ">= 90"
  performance_score: ">= 85"
  best_practices: ">= 90"
  seo: ">= 90"
```

### Manual Testing Checklist

```yaml
manual_testing:
  keyboard_navigation:
    - All interactive elements reachable via Tab
    - Logical tab order
    - Visible focus indicators
    - No keyboard traps
    
  screen_reader:
    - All images have alt text
    - Headings in proper hierarchy
    - Forms have labels
    - Links are descriptive
    - Status messages announced
    
  visual:
    - Sufficient color contrast
    - Text resizes to 200%
    - No horizontal scrolling at 320px width
    - Content reflows properly
    
  media:
    - All videos have captions
    - Captions are accurate and synchronized
    - Transcripts available
    - Audio descriptions (where applicable)
```

### Accessibility Statement

```markdown
# Accessibility Statement

EdGuide is committed to ensuring digital accessibility for people with disabilities. 
We are continually improving the user experience for everyone and applying the relevant 
accessibility standards.

## Conformance Status

The Web Content Accessibility Guidelines (WCAG) defines requirements for designers and 
developers to improve accessibility for people with disabilities. It defines three levels 
of conformance: Level A, Level AA, and Level AAA.

EdGuide CoursePlayerApp is **fully conformant** with WCAG 2.1 Level AA. Fully conformant 
means that the content fully conforms to the accessibility standard without any exceptions.

## Feedback

We welcome your feedback on the accessibility of EdGuide. Please let us know if you 
encounter accessibility barriers:

- Email: accessibility@gai-observe.online
- Phone: +1 (555) 123-4567

We try to respond to feedback within 2 business days.

## Compatibility

EdGuide is designed to be compatible with the following assistive technologies:
- Screen readers (NVDA, JAWS, VoiceOver, TalkBack)
- Screen magnification software
- Speech recognition software
- Keyboard-only navigation

## Technical Specifications

EdGuide relies on the following technologies to work:
- HTML5
- CSS3
- JavaScript
- ARIA attributes

## Limitations and Alternatives

Despite our best efforts, some limitations may exist:

1. **Third-party content**: Some embedded content (e.g., videos from external sources) 
   may not be fully accessible. We provide alternatives where possible.

2. **PDF documents**: Older PDF documents may not be fully accessible. Contact us for 
   an accessible alternative format.

3. **Live content**: Real-time collaborative features may have accessibility limitations. 
   We are working to improve these features.

## Assessment Approach

EdGuide assessed the accessibility of CoursePlayerApp by the following approaches:
- Self-evaluation
- External evaluation by accessibility consultants
- Automated testing tools
- Manual testing with assistive technologies
- User testing with people with disabilities

Last reviewed: January 12, 2026
```

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [UI/UX Design](./UI_UX_DESIGN.md)
- [Video Player](./VIDEO_PLAYER.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
