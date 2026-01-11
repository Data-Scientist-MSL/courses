# Contributing to Data Science Specialization 2.0

Thank you for your interest in contributing! ��

## Ways to Contribute

### 1. 📝 Content Creation
- Write new modules or lessons
- Create practice exercises
- Develop real-world projects
- Add dataset examples

### 2. 🐛 Bug Reports
- Report issues with labs
- Document errors
- Suggest improvements

### 3. 💻 Code Contributions
- Fix bugs
- Improve performance
- Add features to Streamlit app
- Enhance OLLAMA integrations

### 4. 📚 Documentation
- Improve README files
- Add tutorials
- Translate content
- Create video guides

### 5. 🎨 Design & UX
- Streamlit UI improvements
- Diagram creation
- Visual assets
- Accessibility enhancements

## Getting Started

### Setup Development Environment

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/courses
cd courses/courses-v2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install black pylint mypy pytest
```

### Run Tests

```bash
# Code formatting
black .

# Linting
pylint **/*.py

# Type checking
mypy --strict **/*.py

# Unit tests (when available)
pytest tests/
```

## Contribution Workflow

### 1. Create an Issue
Before starting work, create an issue to discuss:
- What you want to add/change
- Why it's needed
- How you plan to implement it

### 2. Fork & Branch
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bug fix
git checkout -b fix/bug-description
```

### 3. Make Changes
- Write clean, documented code
- Follow existing code style
- Add tests if applicable
- Update documentation

### 4. Commit
```bash
# Use conventional commits
git commit -m "feat: add new NLP lab on sentiment analysis"
git commit -m "fix: resolve OLLAMA connection timeout"
git commit -m "docs: update installation guide"
```

**Conventional Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### 5. Push & Create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to related issue
- Screenshots (if UI changes)
- Checklist of completed items

## Content Guidelines

### Slides (Marp)
- Use consistent theme
- Include learning objectives
- Add code examples
- End with exercises and resources

### Jupyter Notebooks
- Clear markdown explanations
- Commented code cells
- Expected outputs shown
- Requirements at top
- Use free datasets only

### Documentation
- Clear headings
- Code examples
- Beginner-friendly language
- Links to resources

## Code Style

### Python
```python
"""Module docstring."""

def function_name(param: str) -> str:
    """
    Brief description.
    
    Args:
        param: Description
    
    Returns:
        Description
    """
    return result
```

- Use type hints
- Google-style docstrings
- Black formatting
- Pylint compliance

### File Organization
```
module_name/
├── __init__.py
├── slides/
├── labs/
├── datasets/
└── README.md
```

## Review Process

1. **Automated Checks**: CI runs Black, Pylint, tests
2. **Manual Review**: Maintainer reviews code & content
3. **Feedback**: Address any requested changes
4. **Merge**: Once approved, changes are merged

## License

By contributing, you agree that your contributions will be licensed under:
- **Content**: CC-BY-NC-SA 4.0
- **Code**: MIT License

## Questions?

- Open an issue
- Join discussions
- Email maintainers

## Recognition

Contributors will be:
- Listed in README
- Credited in commit history
- Recognized in release notes

Thank you for helping make education accessible! 🚀
