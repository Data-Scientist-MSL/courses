# CoursePlayerApp Accessibility Specification

## Overview

EdGuide is committed to providing an inclusive learning experience that is accessible to all users, including those with disabilities. This specification ensures WCAG 2.1 Level AA compliance across the CoursePlayerApp platform.

---

## WCAG 2.1 AA Compliance Requirements

### Four Principles (POUR)

1. **Perceivable**: Information must be presentable in ways users can perceive
2. **Operable**: Interface components must be operable by all users
3. **Understandable**: Information and operation must be understandable
4. **Robust**: Content must be robust enough for assistive technologies

---

## Accessibility Features by Component

### 1. Video Player Accessibility

#### Closed Captions
- **Requirement**: All videos must have accurate closed captions
- **Format**: WebVTT
- **Languages**: English (primary), Spanish, French, Mandarin (auto-generated, human-verified)
- **Quality**: 99%+ accuracy
- **Controls**: Toggle captions on/off with `C` key

**Implementation**:
```html
<video controls>
    <source src="lecture.mp4" type="video/mp4">
    <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default>
    <track kind="captions" src="captions-es.vtt" srclang="es" label="Español">
    <track kind="captions" src="captions-fr.vtt" srclang="fr" label="Français">
</video>
```

#### Audio Descriptions
- **Requirement**: Videos with visual-only content must have audio descriptions
- **Implementation**: Separate audio description track
- **Toggle**: User can enable via player settings

#### Transcript
- **Requirement**: Full text transcript available for all videos
- **Format**: Downloadable TXT, PDF, HTML
- **Features**: Searchable, timestamps linked to video

**UI Implementation**:
```python
# courseplayerapp/ui/components/video_player_component.py

def render_video_accessibility_features(video_id: str):
    """Render accessibility features for video."""
    
    # Caption toggle
    st.checkbox(
        "Show Captions (C)",
        value=True,
        key=f"captions_{video_id}",
        help="Toggle closed captions on/off"
    )
    
    # Transcript download
    with st.expander("📄 View Transcript"):
        transcript = get_video_transcript(video_id)
        st.text_area(
            "Transcript",
            value=transcript,
            height=300,
            label_visibility="collapsed"
        )
        
        st.download_button(
            "Download Transcript (TXT)",
            data=transcript,
            file_name=f"transcript_{video_id}.txt",
            mime="text/plain"
        )
    
    # Audio description toggle (if available)
    if has_audio_description(video_id):
        st.checkbox(
            "Enable Audio Description",
            key=f"audio_desc_{video_id}",
            help="Provides narration of visual elements"
        )
```

---

### 2. Keyboard Navigation

#### Global Keyboard Shortcuts

| Key | Action | Context |
|-----|--------|---------|
| `Tab` | Navigate to next focusable element | All pages |
| `Shift+Tab` | Navigate to previous element | All pages |
| `Enter` / `Space` | Activate button or link | All pages |
| `Escape` | Close modal or cancel action | Modals, dropdowns |
| `/` | Focus search bar | Dashboard, course pages |
| `?` | Show keyboard shortcuts help | All pages |

#### Video Player Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play/Pause |
| `→` | Forward 10 seconds |
| `←` | Backward 10 seconds |
| `↑` | Volume up |
| `↓` | Volume down |
| `M` | Mute/Unmute |
| `F` | Fullscreen toggle |
| `C` | Toggle captions |
| `<` | Decrease speed |
| `>` | Increase speed |
| `0-9` | Jump to 0%-90% of video |

#### Navigation Shortcuts

| Key | Action |
|-----|--------|
| `H` | Go to Home/Dashboard |
| `C` | View Certificates |
| `P` | View Profile |
| `A` | Open AI Tutor (if accessible) |
| `N` | Next lesson |
| `B` | Previous lesson |

**Implementation**:
```python
# courseplayerapp/ui/components/keyboard_shortcuts.py

def register_keyboard_shortcuts():
    """Register global keyboard shortcuts."""
    
    shortcuts_js = """
    <script>
    document.addEventListener('keydown', function(e) {
        // Skip if user is typing in input field
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            return;
        }
        
        switch(e.key) {
            case '/':
                e.preventDefault();
                document.getElementById('search-input').focus();
                break;
            case '?':
                e.preventDefault();
                showKeyboardShortcutsHelp();
                break;
            case 'h':
                window.location.href = '/dashboard';
                break;
            case 'c':
                window.location.href = '/certificates';
                break;
            case 'n':
                navigateToNextLesson();
                break;
            case 'b':
                navigateToPreviousLesson();
                break;
        }
    });
    </script>
    """
    
    st.components.v1.html(shortcuts_js, height=0)

def render_keyboard_shortcuts_help():
    """Display keyboard shortcuts help modal."""
    
    st.markdown("""
    ## Keyboard Shortcuts
    
    ### Navigation
    - `H` - Home/Dashboard
    - `C` - Certificates
    - `P` - Profile
    - `N` - Next Lesson
    - `B` - Previous Lesson
    - `/` - Search
    
    ### Video Player
    - `Space` - Play/Pause
    - `→/←` - Skip forward/backward
    - `↑/↓` - Volume
    - `F` - Fullscreen
    - `C` - Toggle captions
    
    ### General
    - `Tab` - Navigate elements
    - `Escape` - Close modal
    - `?` - Show this help
    """)
```

---

### 3. Screen Reader Support

#### ARIA Labels

**Buttons**:
```html
<button aria-label="Play video">▶</button>
<button aria-label="Download certificate as PDF">📄</button>
<button aria-label="Share certificate on LinkedIn">🔗</button>
```

**Navigation**:
```html
<nav aria-label="Main navigation">
    <ul>
        <li><a href="/dashboard" aria-current="page">Dashboard</a></li>
        <li><a href="/courses">Courses</a></li>
        <li><a href="/certificates">Certificates</a></li>
    </ul>
</nav>
```

**Forms**:
```html
<label for="email">Email Address</label>
<input 
    type="email" 
    id="email" 
    name="email" 
    aria-required="true"
    aria-describedby="email-help"
>
<small id="email-help">We'll never share your email.</small>
```

**Progress Indicators**:
```html
<div 
    role="progressbar" 
    aria-valuenow="73" 
    aria-valuemin="0" 
    aria-valuemax="100"
    aria-label="Course completion progress"
>
    73% Complete
</div>
```

**Live Regions** (for dynamic updates):
```html
<!-- AI Tutor response -->
<div 
    role="status" 
    aria-live="polite" 
    aria-atomic="true"
>
    AI Tutor is thinking...
</div>

<!-- Error messages -->
<div 
    role="alert" 
    aria-live="assertive"
>
    Error: Failed to submit lab. Please try again.
</div>
```

#### Semantic HTML

```html
<!-- Use semantic elements -->
<header>...</header>
<nav>...</nav>
<main>
    <article>
        <h1>Course Title</h1>
        <section>
            <h2>Module 1</h2>
            ...
        </section>
    </article>
</main>
<aside>
    <!-- AI Tutor sidebar -->
</aside>
<footer>...</footer>
```

---

### 4. Focus Management

#### Visible Focus Indicators

```css
/* Clear focus styles for all interactive elements */
button:focus,
a:focus,
input:focus,
textarea:focus,
select:focus {
    outline: 2px solid #4a90e2;
    outline-offset: 2px;
    box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}

/* Don't remove focus styles! */
*:focus {
    outline: revert; /* Never use outline: none without replacement */
}
```

#### Focus Trap in Modals

```javascript
// Trap focus within modal when open
function trapFocus(modal) {
    const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    modal.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                }
            } else {
                if (document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        }
        
        if (e.key === 'Escape') {
            closeModal();
        }
    });
}
```

#### Skip Links

```html
<!-- Allow keyboard users to skip to main content -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #4a90e2;
    color: white;
    padding: 8px;
    text-decoration: none;
    z-index: 100;
}

.skip-link:focus {
    top: 0;
}
</style>
```

---

### 5. Color and Contrast

#### Contrast Ratios (WCAG AA)

- **Normal text** (< 24px): Minimum 4.5:1 contrast ratio
- **Large text** (≥ 24px): Minimum 3:1 contrast ratio
- **UI components**: Minimum 3:1 contrast ratio

**Color Palette with Contrast Ratios**:
```css
/* All pass WCAG AA standards */

/* Dark text on light background */
--text-on-light: #1a1a1a;    /* 14.4:1 on white */
--subtext-on-light: #4a4a4a; /* 7.9:1 on white */

/* Light text on dark background */
--text-on-dark: #ffffff;     /* 21:1 on #1a1a1a */
--subtext-on-dark: #b0b0b0;  /* 8.2:1 on #1a1a1a */

/* Interactive elements */
--link-blue: #2c5aa0;        /* 7.0:1 on white */
--button-primary: #4a90e2;   /* 3.4:1 on white - borders added for contrast */
```

#### Never Use Color Alone

```html
<!-- ❌ Bad: Color only -->
<span style="color: red;">Failed</span>
<span style="color: green;">Passed</span>

<!-- ✅ Good: Icon + Color + Text -->
<span style="color: red;">❌ Failed</span>
<span style="color: green;">✅ Passed</span>
```

#### High Contrast Mode

```python
# courseplayerapp/ui/components/contrast_mode.py

def enable_high_contrast_mode():
    """Apply high contrast color scheme."""
    
    st.markdown("""
        <style>
        :root {
            --text-primary: #000000;
            --background: #ffffff;
            --link-color: #0000ee;
            --button-bg: #000000;
            --button-text: #ffffff;
            --border: #000000;
        }
        
        /* Increase all borders */
        button, input, select, textarea {
            border: 2px solid var(--border);
        }
        
        /* Remove box shadows */
        * {
            box-shadow: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
```

---

### 6. Text Readability

#### Font Size Adjustment

```python
def render_font_size_controls():
    """Allow users to adjust font size."""
    
    font_size = st.sidebar.radio(
        "Text Size",
        options=["Small", "Medium", "Large", "Extra Large"],
        index=1,  # Default to Medium
        help="Adjust text size for better readability"
    )
    
    size_map = {
        "Small": "14px",
        "Medium": "16px",
        "Large": "18px",
        "Extra Large": "20px"
    }
    
    st.markdown(f"""
        <style>
        body, .stMarkdown, .stText {{
            font-size: {size_map[font_size]};
        }}
        </style>
    """, unsafe_allow_html=True)
```

#### Line Height and Spacing

```css
/* Readable line heights */
body {
    line-height: 1.5;
}

h1, h2, h3 {
    line-height: 1.25;
}

/* Adequate spacing */
p {
    margin-bottom: 1rem;
}

/* Max width for readability */
.content {
    max-width: 65ch; /* ~65 characters per line */
}
```

---

### 7. Form Accessibility

#### Error Handling

```html
<!-- Accessible error messages -->
<label for="email">Email Address</label>
<input 
    type="email" 
    id="email"
    aria-invalid="true"
    aria-describedby="email-error"
>
<span id="email-error" role="alert" class="error">
    Please enter a valid email address
</span>
```

**Streamlit Implementation**:
```python
def render_accessible_form():
    """Render form with proper error handling and labels."""
    
    with st.form("quiz_form"):
        st.subheader("Quiz Question 1")
        
        # Clear label associated with input
        answer = st.text_input(
            "What is the capital of France?",
            help="Enter your answer below",
            key="q1"
        )
        
        submitted = st.form_submit_button("Submit Answer")
        
        if submitted:
            if not answer:
                st.error("❌ Error: Please provide an answer", icon="🚨")
            elif answer.lower() != "paris":
                st.error("❌ Incorrect. Please try again.", icon="🚨")
            else:
                st.success("✅ Correct! Well done.", icon="✅")
```

#### Required Fields

```html
<label for="name">
    Full Name <span aria-label="required">*</span>
</label>
<input 
    type="text" 
    id="name"
    required
    aria-required="true"
>
```

---

### 8. Alternative Text for Images

#### Decorative Images

```html
<!-- Decorative images: empty alt -->
<img src="decoration.png" alt="" role="presentation">
```

#### Informative Images

```html
<!-- Informative images: descriptive alt -->
<img 
    src="course-thumbnail.png" 
    alt="Machine Learning Fundamentals course - Learn neural networks, deep learning, and AI"
>
```

#### Complex Images (Charts, Diagrams)

```html
<!-- Provide detailed description -->
<figure>
    <img 
        src="neural-network-diagram.png" 
        alt="Neural network architecture diagram"
        aria-describedby="diagram-desc"
    >
    <figcaption id="diagram-desc">
        A three-layer neural network with an input layer of 4 nodes,
        a hidden layer of 6 nodes, and an output layer of 3 nodes.
        Connections show fully connected layers between each layer.
    </figcaption>
</figure>
```

---

### 9. Mobile Accessibility

#### Touch Target Size

```css
/* Minimum 44x44px touch targets (WCAG 2.1 Level AAA, but best practice) */
button, a, input[type="checkbox"], input[type="radio"] {
    min-width: 44px;
    min-height: 44px;
    padding: 12px;
}

/* Adequate spacing between touch targets */
.button-group button {
    margin: 8px;
}
```

#### Orientation Support

```css
/* Support both portrait and landscape */
@media (orientation: landscape) {
    /* Adjust layout for landscape */
}

@media (orientation: portrait) {
    /* Adjust layout for portrait */
}

/* Don't lock orientation */
/* Allow users to rotate device freely */
```

---

### 10. Testing & Validation

#### Automated Testing Tools

**Lighthouse Accessibility Audit**:
```bash
# Run Lighthouse accessibility audit
lighthouse https://gai-observe.online --only-categories=accessibility --output=html --output-path=./accessibility-report.html
```

**Target**: Lighthouse Accessibility Score ≥ 90

**axe DevTools**:
```javascript
// Run axe accessibility checker
axe.run(document, function (err, results) {
    if (err) throw err;
    console.log(results.violations);
});
```

#### Manual Testing Checklist

- [ ] Navigate entire site using keyboard only (no mouse)
- [ ] Test with screen reader (NVDA, JAWS, or VoiceOver)
- [ ] Verify all images have appropriate alt text
- [ ] Check color contrast ratios (use WebAIM Contrast Checker)
- [ ] Test with 200% browser zoom (text remains readable)
- [ ] Verify captions work on all videos
- [ ] Test form error messages are announced to screen readers
- [ ] Confirm focus indicators are visible
- [ ] Test on mobile devices (iOS VoiceOver, Android TalkBack)
- [ ] Verify keyboard shortcuts don't conflict with screen readers

#### Screen Reader Testing

**NVDA (Windows - Free)**:
```
1. Download NVDA from https://www.nvaccess.org/
2. Navigate site using:
   - Tab: Next element
   - Shift+Tab: Previous element
   - Insert+Down Arrow: Read next line
   - Insert+Up Arrow: Read previous line
   - H: Next heading
   - Shift+H: Previous heading
```

**JAWS (Windows - Paid)**:
```
1. Professional screen reader for thorough testing
2. Similar shortcuts to NVDA
```

**VoiceOver (Mac - Built-in)**:
```
1. Enable: System Preferences > Accessibility > VoiceOver
2. Navigate:
   - Cmd+F5: Toggle VoiceOver
   - Ctrl+Option+Right Arrow: Next item
   - Ctrl+Option+Left Arrow: Previous item
```

---

### 11. Accessibility Statement

**Location**: https://gai-observe.online/accessibility

```markdown
# Accessibility Statement for EdGuide

EdGuide is committed to ensuring digital accessibility for people with disabilities. We are continually improving the user experience for everyone and applying the relevant accessibility standards.

## Conformance Status

The Web Content Accessibility Guidelines (WCAG) defines requirements for designers and developers to improve accessibility for people with disabilities. It defines three levels of conformance: Level A, Level AA, and Level AAA.

**EdGuide CoursePlayerApp is partially conformant with WCAG 2.1 Level AA.** "Partially conformant" means that some parts of the content do not fully conform to the accessibility standard.

## Measures to Support Accessibility

EdGuide takes the following measures to ensure accessibility:
- Accessibility is part of our mission statement
- Include accessibility throughout our internal policies
- Integrate accessibility into our procurement practices
- Provide continual accessibility training for our staff
- Assign clear accessibility goals and responsibilities

## Feedback

We welcome your feedback on the accessibility of EdGuide. Please let us know if you encounter accessibility barriers:

- **Email**: accessibility@gai-observe.online
- **Phone**: +1-555-EDGUIDE
- **Response Time**: We aim to respond within 2 business days

## Technical Specifications

EdGuide relies on the following technologies to work with the particular combination of web browser and any assistive technologies or plugins installed on your computer:
- HTML5
- CSS3
- JavaScript
- ARIA (Accessible Rich Internet Applications)

## Limitations and Alternatives

Despite our best efforts to ensure accessibility, there may be some limitations. Below is a description of known limitations and potential solutions:

1. **AI Tutor Chat**: Currently optimized for visual interaction. We are working on improving screen reader support.
   - **Workaround**: Contact support for email-based AI assistance

2. **Interactive Simulations**: Some simulations may not be fully keyboard accessible.
   - **Workaround**: Alternative text-based exercises available upon request

## Assessment Approach

EdGuide assessed the accessibility of CoursePlayerApp by the following approaches:
- Self-evaluation
- External evaluation by accessibility consultants
- Automated testing using Lighthouse and axe
- Manual testing with screen readers

## Formal Approval

This accessibility statement is approved by:

**EdGuide Accessibility Team**  
**Last Reviewed**: January 14, 2026
```

---

## Accessibility Compliance Checklist

### Level A (Must Have)

- [x] All images have alt text
- [x] All form inputs have labels
- [x] Keyboard navigation works throughout
- [x] No content flashes more than 3 times per second
- [x] Page titles are descriptive
- [x] Focus order is logical
- [x] Link purpose is clear
- [x] Multiple ways to navigate (menu, search, breadcrumbs)

### Level AA (Target)

- [x] Color contrast ratio ≥ 4.5:1 for normal text
- [x] Color contrast ratio ≥ 3:1 for large text
- [x] Captions for all videos
- [x] Visible focus indicators
- [x] Consistent navigation
- [x] Error identification and suggestions
- [x] Labels and instructions for forms
- [x] Resize text to 200% without loss of functionality

### Level AAA (Nice to Have)

- [ ] Sign language interpretation for videos
- [ ] Extended audio descriptions
- [ ] Color contrast ratio ≥ 7:1
- [ ] No time limits on content
- [ ] Context-sensitive help available

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: EdGuide Accessibility Team  
**Platform**: EdGuide (gai-observe.online)  
**WCAG Compliance**: Level AA
