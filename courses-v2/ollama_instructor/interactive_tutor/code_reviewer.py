#!/usr/bin/env python3
"""AI code reviewer using OLLAMA."""

import requests


def review_code(code: str, language: str = "python", model: str = "llama3") -> dict:
    """Review code and provide feedback."""
    
    prompt = f"""
Review this {language} code and provide detailed feedback:

```{language}
{code}
```

Provide:
1. Code quality score (0-10)
2. Potential bugs or issues
3. Performance improvements
4. Best practices violations
5. Security concerns
6. Improved version

Review:
"""
    
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    review = response.json()["response"]
    
    return {
        "original_code": code,
        "review": review,
        "language": language
    }


if __name__ == "__main__":
    sample_code = """
def calc_avg(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)
"""
    
    result = review_code(sample_code)
    print(result["review"])
