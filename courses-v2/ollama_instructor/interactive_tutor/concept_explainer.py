#!/usr/bin/env python3
"""Multi-level concept explainer (ELI5 to PhD)."""

import requests


def explain_concept(concept: str, level: str = "intermediate", model: str = "llama3") -> str:
    """Explain concept at specified level."""
    
    levels = {
        "eli5": "Explain to a 5-year-old",
        "beginner": "Explain to a beginner",
        "intermediate": "Explain with technical details",
        "advanced": "Explain with advanced concepts",
        "phd": "Explain at research level with math"
    }
    
    instruction = levels.get(level, levels["intermediate"])
    
    prompt = f"{instruction}: {concept}"
    
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    return response.json()["response"]


if __name__ == "__main__":
    concept = "gradient descent"
    
    for level in ["eli5", "intermediate", "phd"]:
        print(f"\n{'='*80}")
        print(f"Level: {level.upper()}")
        print('='*80)
        print(explain_concept(concept, level=level))
