#!/usr/bin/env python3
"""Generate adaptive quizzes using OLLAMA."""

import requests
import json


def generate_quiz(topic: str, num_questions: int = 5, difficulty: str = "intermediate", model: str = "llama3") -> list:
    """Generate quiz questions."""
    
    prompt = f"""
Generate {num_questions} {difficulty} level quiz questions about: {topic}

Format each question as JSON:
{{
    "question": "Question text",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "correct": "A",
    "explanation": "Why this is correct"
}}

Generate questions now:
"""
    
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    return response.json()["response"]


if __name__ == "__main__":
    quiz = generate_quiz("Machine Learning Basics", num_questions=3)
    print(quiz)
