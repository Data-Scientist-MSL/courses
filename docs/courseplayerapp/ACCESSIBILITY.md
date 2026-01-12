# Accessibility Documentation

## Overview

CoursePlayerApp is designed to be fully accessible to all users, regardless of their abilities or disabilities. This document outlines our commitment to WCAG 2.1 AA compliance and specifies accessibility requirements for all components.

---

## WCAG 2.1 AA Compliance

### Four Principles (POUR)

#### 1. Perceivable
Information and user interface components must be presentable to users in ways they can perceive.

#### 2. Operable
User interface components and navigation must be operable.

#### 3. Understandable
Information and the operation of user interface must be understandable.

#### 4. Robust
Content must be robust enough to be interpreted by a wide variety of user agents, including assistive technologies.

---

## Visual Accessibility

### Color Contrast

**Requirements**:
- Normal text (< 18pt): Minimum 4.5:1 contrast ratio
- Large text (≥ 18pt or 14pt bold): Minimum 3:1 contrast ratio
- UI components and graphics: Minimum 3:1 contrast ratio

**Color Palette**:
```css
/* Primary colors with sufficient contrast */
--primary-bg: #FFFFFF;        /* White background */
--primary-text: #1A1A1A;      /* Near-black text (16:1 ratio) */
--secondary-text: #4A4A4A;    /* Dark gray (9:1 ratio) */

/* Interactive elements */
--link-color: #0066CC;         /* Blue (7:1 ratio on white) */
--link-hover: #0052A3;         /* Darker blue (9:1 ratio) */
--link-visited: #551A8B;       /* Purple (7:1 ratio) */

/* Buttons */
--btn-primary-bg: #0066CC;     
--btn-primary-text: #FFFFFF;   /* 7:1 ratio */
--btn-secondary-bg: #6C757D;   
--btn-secondary-text: #FFFFFF; /* 5:1 ratio */

/* Status colors */
--success: #198754;            /* Green (4.5:1 ratio) */
--warning: #FFC107;            /* Yellow (requires dark text) */
--error: #DC3545;              /* Red (4.5:1 ratio) */
--info: #0DCAF0;               /* Cyan (requires dark text) */

/* High contrast mode overrides */
@media (prefers-contrast: high) {
  --primary-text: #000000;
  --link-color: #0000EE;
  --link-visited: #551A8B;
}
```

**Testing**:
```javascript
// Use axe-core for automated testing
import { axe, toHaveNoViolations } from 'jest-axe';

test('color contrast meets WCAG AA', async () => {
  const { container } = render(<App />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### No Color-Only Information

**Requirements**:
- Never use color as the only means of conveying information
- Always pair color with text, icons, or patterns

**Examples**:
```html
<!-- ❌ Bad: Color only -->
<div style="color: red;">Error</div>

<!-- ✅ Good: Color + icon + text -->
<div class="error-message">
  <span class="icon" aria-label="Error">❌</span>
  <span>Error: Please enter a valid email</span>
</div>

<!-- ✅ Good: Progress with text + visual -->
<div class="progress-bar" role="progressbar" 
     aria-valuenow="45" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-fill" style="width: 45%"></div>
  <span class="progress-text">45% Complete</span>
</div>
```

### Text Resizing

**Requirements**:
- Text must be resizable up to 200% without loss of content or functionality
- Use relative units (rem, em, %) instead of fixed pixels

**Implementation**:
```css
/* Base font size */
html {
  font-size: 16px; /* Default */
}

/* Use rem for all text */
body {
  font-size: 1rem;      /* 16px */
}

h1 {
  font-size: 2.5rem;    /* 40px */
}

h2 {
  font-size: 2rem;      /* 32px */
}

p {
  font-size: 1rem;      /* 16px */
  line-height: 1.5;
}

.small-text {
  font-size: 0.875rem;  /* 14px */
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  html {
    font-size: 14px;    /* Smaller on mobile */
  }
}
```

### Focus Indicators

**Requirements**:
- All interactive elements must have visible focus indicators
- Focus indicators must have 3:1 contrast ratio with background
- Minimum 2px outline thickness

**Implementation**:
```css
/* Global focus styles */
*:focus {
  outline: 3px solid #0066CC;
  outline-offset: 2px;
}

/* High contrast mode */
@media (prefers-contrast: high) {
  *:focus {
    outline: 4px solid #000000;
    outline-offset: 3px;
  }
}

/* Custom focus for specific elements */
button:focus,
a:focus {
  outline: 3px solid #0066CC;
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.25);
}

/* Don't remove focus for mouse users */
button:focus:not(:focus-visible) {
  outline: none;
  box-shadow: none;
}
```

---

## Keyboard Navigation

### Requirements

**All functionality must be keyboard accessible**:
- Tab: Move forward through interactive elements
- Shift + Tab: Move backward
- Enter/Space: Activate buttons and links
- Arrow keys: Navigate within components (sliders, tabs, etc.)
- Escape: Close modals, cancel operations

### Tab Order

**Requirements**:
- Logical tab order (left-to-right, top-to-bottom)
- No keyboard traps (can always escape)
- Skip to main content link

**Implementation**:
```html
<!-- Skip to main content (first focusable element) -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<nav aria-label="Main navigation">
  <a href="/">Home</a>
  <a href="/courses">Courses</a>
  <a href="/progress">My Progress</a>
</nav>

<main id="main-content" tabindex="-1">
  <!-- Main content here -->
</main>
```

```css
/* Skip link (visible on focus) */
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
```

### Keyboard Shortcuts

**Video Player Shortcuts**:
```
Space / K     - Play/Pause
←/→           - Seek backward/forward 5s
J/L           - Seek backward/forward 10s
↑/↓           - Volume up/down
M             - Mute toggle
F             - Fullscreen toggle
C             - Captions toggle
< / >         - Decrease/increase playback speed
0-9           - Jump to 0%, 10%, ..., 90%
```

**Implementation**:
```javascript
// Global keyboard shortcuts
useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    // Don't trigger if typing in input
    if (e.target instanceof HTMLInputElement || 
        e.target instanceof HTMLTextAreaElement) {
      return;
    }
    
    switch(e.key.toLowerCase()) {
      case ' ':
      case 'k':
        e.preventDefault();
        togglePlayPause();
        break;
      
      case 'arrowleft':
        e.preventDefault();
        seek(-5);
        break;
      
      case 'arrowright':
        e.preventDefault();
        seek(5);
        break;
      
      case 'f':
        e.preventDefault();
        toggleFullscreen();
        break;
      
      // ... other shortcuts
    }
  };
  
  document.addEventListener('keydown', handleKeyPress);
  return () => document.removeEventListener('keydown', handleKeyPress);
}, []);

// Announce shortcut usage to screen readers
<div role="region" aria-label="Keyboard shortcuts">
  <h2>Keyboard Shortcuts</h2>
  <dl>
    <dt>Space or K</dt>
    <dd>Play or pause video</dd>
    
    <dt>Left/Right Arrow</dt>
    <dd>Seek backward/forward 5 seconds</dd>
    
    {/* ... */}
  </dl>
</div>
```

---

## Screen Reader Support

### ARIA Labels and Roles

**Requirements**:
- All interactive elements must have accessible names
- Use semantic HTML where possible
- Supplement with ARIA when needed

**Implementation**:
```html
<!-- Semantic HTML (preferred) -->
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/courses">Courses</a></li>
    <li><a href="/progress">My Progress</a></li>
  </ul>
</nav>

<!-- ARIA landmarks -->
<header role="banner">
  <!-- Site header -->
</header>

<main role="main">
  <!-- Main content -->
</main>

<aside role="complementary" aria-label="AI Tutor">
  <!-- Sidebar content -->
</aside>

<footer role="contentinfo">
  <!-- Site footer -->
</footer>

<!-- Interactive widgets -->
<div role="tablist" aria-label="Course modules">
  <button role="tab" 
          aria-selected="true" 
          aria-controls="panel-1"
          id="tab-1">
    Module 1
  </button>
  <button role="tab" 
          aria-selected="false" 
          aria-controls="panel-2"
          id="tab-2">
    Module 2
  </button>
</div>

<div role="tabpanel" 
     id="panel-1" 
     aria-labelledby="tab-1">
  <!-- Module 1 content -->
</div>

<!-- Form labels -->
<label for="email">Email Address</label>
<input type="email" 
       id="email" 
       name="email"
       aria-required="true"
       aria-describedby="email-hint">
<span id="email-hint" class="hint">
  We'll never share your email
</span>

<!-- Error messages -->
<input type="text" 
       id="name"
       aria-invalid="true"
       aria-describedby="name-error">
<span id="name-error" role="alert" class="error">
  Name is required
</span>

<!-- Progress indicators -->
<div role="progressbar" 
     aria-valuenow="45" 
     aria-valuemin="0" 
     aria-valuemax="100"
     aria-label="Course completion">
  <div style="width: 45%"></div>
</div>

<!-- Loading states -->
<button aria-busy="true" disabled>
  <span class="spinner" aria-hidden="true"></span>
  Loading...
</button>

<!-- Icon buttons -->
<button aria-label="Close modal">
  <span aria-hidden="true">×</span>
</button>

<!-- Data tables -->
<table>
  <caption>Course Progress Summary</caption>
  <thead>
    <tr>
      <th scope="col">Course</th>
      <th scope="col">Progress</th>
      <th scope="col">Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Data Science 101</th>
      <td>65%</td>
      <td>87</td>
    </tr>
  </tbody>
</table>
```

### Live Regions

**For dynamic content updates**:
```html
<!-- Polite announcements (non-urgent) -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  {statusMessage}
</div>

<!-- Assertive announcements (urgent) -->
<div aria-live="assertive" aria-atomic="true" class="sr-only">
  {errorMessage}
</div>

<!-- Status announcements -->
<div role="status" aria-live="polite">
  Progress saved successfully
</div>

<!-- Alert announcements -->
<div role="alert" aria-live="assertive">
  Error: Failed to submit lab
</div>
```

```css
/* Screen reader only class */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## Media Accessibility

### Video Captions

**Requirements**:
- All videos must have closed captions
- Captions must be accurate (99% accuracy)
- Captions must be synchronized within 0.5 seconds

**Implementation**:
```html
<video controls>
  <source src="lesson-01.mp4" type="video/mp4">
  
  <!-- English captions (default) -->
  <track kind="captions" 
         src="lesson-01-en.vtt" 
         srclang="en" 
         label="English"
         default>
  
  <!-- Spanish captions -->
  <track kind="captions" 
         src="lesson-01-es.vtt" 
         srclang="es" 
         label="Español">
  
  <!-- Descriptive audio (for visually impaired) -->
  <track kind="descriptions"
         src="lesson-01-desc.vtt"
         srclang="en"
         label="Audio Description">
</video>
```

**VTT Caption Format**:
```
WEBVTT

00:00:00.000 --> 00:00:03.500
Welcome to Data Science 101.

00:00:03.500 --> 00:00:07.000
In this lesson, we'll cover the fundamentals.

00:00:07.000 --> 00:00:10.500
[Instructor points to whiteboard]
```

### Transcripts

**Requirements**:
- Full text transcripts available for all video content
- Transcripts must include speaker identification
- Downloadable as text file

**Implementation**:
```html
<div class="video-player">
  <video controls>
    <!-- video source -->
  </video>
  
  <div class="transcript-container">
    <button onclick="toggleTranscript()" 
            aria-expanded="false"
            aria-controls="transcript">
      Show Transcript
    </button>
    
    <div id="transcript" hidden>
      <h3>Video Transcript</h3>
      <div class="transcript-content">
        <p><strong>Instructor:</strong> Welcome to Data Science 101...</p>
        <p><strong>Instructor:</strong> Today we'll learn about...</p>
      </div>
      <a href="/transcripts/lesson-01.txt" download>
        Download Transcript
      </a>
    </div>
  </div>
</div>
```

### Alternative Text for Images

**Requirements**:
- All images must have alt text
- Decorative images use empty alt (`alt=""`)
- Complex images have detailed descriptions

**Implementation**:
```html
<!-- Informative image -->
<img src="chart.png" 
     alt="Bar chart showing 65% course completion rate">

<!-- Decorative image -->
<img src="decoration.png" 
     alt=""
     role="presentation">

<!-- Complex image with long description -->
<figure>
  <img src="complex-diagram.png" 
       alt="Data science workflow diagram"
       aria-describedby="diagram-desc">
  
  <figcaption id="diagram-desc">
    Detailed description: The diagram shows a 5-step workflow:
    1. Data Collection from multiple sources...
    2. Data Cleaning and preprocessing...
    (continue detailed description)
  </figcaption>
</figure>

<!-- Image with text -->
<img src="logo.png" alt="CoursePlayerApp">

<!-- Icon buttons -->
<button aria-label="Play video">
  <img src="play-icon.svg" alt="" aria-hidden="true">
</button>
```

---

## Form Accessibility

### Labels and Instructions

**Requirements**:
- All form inputs must have associated labels
- Required fields must be clearly marked
- Instructions must be provided before form

**Implementation**:
```html
<form>
  <!-- Required field indicator -->
  <p><span aria-hidden="true">*</span> Required fields</p>
  
  <!-- Text input with label -->
  <div class="form-group">
    <label for="username">
      Username <span aria-label="required">*</span>
    </label>
    <input type="text" 
           id="username" 
           name="username"
           aria-required="true"
           aria-describedby="username-hint">
    <span id="username-hint" class="hint">
      3-20 characters, letters and numbers only
    </span>
  </div>
  
  <!-- Email with validation -->
  <div class="form-group">
    <label for="email">
      Email <span aria-label="required">*</span>
    </label>
    <input type="email" 
           id="email" 
           name="email"
           aria-required="true"
           aria-invalid="false"
           aria-describedby="email-error">
    <span id="email-error" role="alert" class="error" hidden>
      Please enter a valid email address
    </span>
  </div>
  
  <!-- Radio buttons -->
  <fieldset>
    <legend>Select your tier <span aria-label="required">*</span></legend>
    <div>
      <input type="radio" id="tier-basic" name="tier" value="basic">
      <label for="tier-basic">Basic ($97/year)</label>
    </div>
    <div>
      <input type="radio" id="tier-int" name="tier" value="intermediate">
      <label for="tier-int">Intermediate ($247/year)</label>
    </div>
    <div>
      <input type="radio" id="tier-adv" name="tier" value="advanced">
      <label for="tier-adv">Advanced ($497/year)</label>
    </div>
  </fieldset>
  
  <!-- Checkbox -->
  <div class="form-group">
    <input type="checkbox" id="terms" name="terms" required>
    <label for="terms">
      I agree to the <a href="/terms">Terms of Service</a>
    </label>
  </div>
  
  <!-- Submit button -->
  <button type="submit">Create Account</button>
</form>
```

### Error Handling

**Requirements**:
- Errors must be clearly identified
- Error messages must be associated with fields
- Suggest corrections when possible

**Implementation**:
```javascript
// Validation with accessible errors
const handleSubmit = (e) => {
  e.preventDefault();
  const errors = [];
  
  // Validate username
  if (!username) {
    errors.push({
      field: 'username',
      message: 'Username is required'
    });
  }
  
  // Validate email
  if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
    errors.push({
      field: 'email',
      message: 'Please enter a valid email address (e.g., user@example.com)'
    });
  }
  
  if (errors.length > 0) {
    // Show errors
    errors.forEach(error => {
      const field = document.getElementById(error.field);
      const errorSpan = document.getElementById(`${error.field}-error`);
      
      field.setAttribute('aria-invalid', 'true');
      errorSpan.textContent = error.message;
      errorSpan.hidden = false;
    });
    
    // Focus first error
    document.getElementById(errors[0].field).focus();
    
    // Announce to screen readers
    announceToScreenReader(`Form has ${errors.length} errors. ${errors[0].message}`);
  }
};
```

---

## Testing

### Automated Testing Tools

**Browser Extensions**:
- axe DevTools
- WAVE
- Lighthouse Accessibility Audit

**JavaScript Libraries**:
- jest-axe
- pa11y
- cypress-axe

**Example Test Suite**:
```javascript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  test('video player has no accessibility violations', async () => {
    const { container } = render(<VideoPlayer />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  test('form has proper labels', async () => {
    const { container } = render(<LoginForm />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  test('navigation is keyboard accessible', () => {
    const { getByRole } = render(<Navigation />);
    const nav = getByRole('navigation');
    
    // Check tab order
    const links = nav.querySelectorAll('a');
    links.forEach(link => {
      expect(link).toHaveAttribute('tabindex', '0');
    });
  });
});
```

### Manual Testing

**Screen Reader Testing**:
- NVDA (Windows) - Free
- JAWS (Windows) - Commercial
- VoiceOver (Mac) - Built-in
- TalkBack (Android) - Built-in

**Test Checklist**:
```markdown
- [ ] Navigate entire site with keyboard only
- [ ] Navigate with screen reader (NVDA/VoiceOver)
- [ ] Zoom text to 200% - content still usable
- [ ] Check color contrast with axe DevTools
- [ ] Test with high contrast mode
- [ ] Test with forced colors mode
- [ ] Verify focus indicators visible
- [ ] Verify form error handling
- [ ] Verify media has captions
- [ ] Test with voice control (Dragon)
```

---

## Accessibility Statement

**To be published on website**:

```markdown
# Accessibility Statement for CoursePlayerApp

We are committed to ensuring digital accessibility for people with disabilities.
We are continually improving the user experience for everyone and applying the 
relevant accessibility standards.

## Conformance Status

CoursePlayerApp conforms to WCAG 2.1 Level AA. These guidelines explain how 
to make web content more accessible for people with disabilities.

## Measures to Support Accessibility

CoursePlayerApp takes the following measures to ensure accessibility:

- Include accessibility as part of our mission statement
- Assign clear accessibility goals and responsibilities
- Employ formal accessibility quality assurance methods
- Provide continual accessibility training for our staff

## Technical Specifications

Accessibility of CoursePlayerApp relies on the following technologies to work:

- HTML
- WAI-ARIA
- CSS
- JavaScript

These technologies are relied upon for conformance with the accessibility standards used.

## Assessment Approach

We assessed the accessibility of CoursePlayerApp by the following approaches:

- Self-evaluation
- External evaluation by accessibility consultants

## Feedback

We welcome your feedback on the accessibility of CoursePlayerApp. Please let us 
know if you encounter accessibility barriers:

- Email: accessibility@courseplayerapp.com
- Phone: 1-800-COURSES
- Visitor address: 123 Education St, Learning City, LC 12345

We try to respond to feedback within 2 business days.

## Date

This statement was created on January 1, 2024 using the W3C Accessibility Statement Generator.
```

---

## Conclusion

CoursePlayerApp's accessibility implementation ensures:

1. **WCAG 2.1 AA Compliance** - Meeting industry standards
2. **Keyboard Navigation** - Full functionality without mouse
3. **Screen Reader Support** - Proper ARIA labels and semantic HTML
4. **Visual Accessibility** - High contrast, resizable text, no color-only info
5. **Media Accessibility** - Captions, transcripts, audio descriptions
6. **Form Accessibility** - Clear labels, error handling, instructions
7. **Comprehensive Testing** - Automated and manual testing protocols

This commitment to accessibility ensures all users can benefit from our learning platform regardless of their abilities.
