#!/usr/bin/env python3
"""
OLLAMA Lecture Generator
Automatically generate lecture slides from topics using AI
"""

import argparse
import requests
import json
from pathlib import Path


def call_ollama(prompt, model="llama3"):
    """Call OLLAMA API to generate content"""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Error calling OLLAMA: {e}")
        return None


def generate_slides(topic, level="intermediate", format="marp"):
    """Generate lecture slides for a given topic"""
    
    prompt = f"""Create a comprehensive lecture on '{topic}' for {level} level students.

Format the output as a Marp markdown presentation with the following structure:

---
marp: true
theme: default
paginate: true
---

# {topic}

Include:
1. Learning objectives (3-5 bullet points)
2. Introduction and motivation
3. Key concepts with clear explanations
4. Code examples where applicable
5. Diagrams (describe them in text)
6. Practical applications
7. Summary and key takeaways
8. Additional resources
9. Discussion questions

Make it educational, clear, and engaging. Use appropriate emojis.
Aim for 20-30 slides.
"""
    
    print(f"Generating slides for: {topic}")
    print(f"Level: {level}, Format: {format}")
    print("This may take a minute...\n")
    
    content = call_ollama(prompt)
    
    if content:
        # Save to file
        filename = f"{topic.lower().replace(' ', '_')}_lecture.md"
        output_path = Path("generated_lectures") / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Slides generated successfully!")
        print(f"📄 Saved to: {output_path}")
        print(f"\nTo view: Open with Marp VS Code extension or use:")
        print(f"  marp {output_path} --pdf")
    else:
        print("❌ Failed to generate slides")


def generate_quiz(topic, num_questions=5):
    """Generate quiz questions for a topic"""
    
    prompt = f"""Create {num_questions} multiple choice questions about {topic}.

For each question:
- Make it challenging but fair
- Provide 4 options (A, B, C, D)
- Include the correct answer
- Provide a brief explanation

Format:
Q1: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [correct letter]
Explanation: [why this is correct]

Make questions test understanding, not just memorization.
"""
    
    print(f"Generating {num_questions} quiz questions for: {topic}\n")
    
    content = call_ollama(prompt)
    
    if content:
        filename = f"{topic.lower().replace(' ', '_')}_quiz.md"
        output_path = Path("generated_quizzes") / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(f"# Quiz: {topic}\n\n")
            f.write(content)
        
        print(f"✅ Quiz generated successfully!")
        print(f"📄 Saved to: {output_path}")
    else:
        print("❌ Failed to generate quiz")


def main():
    parser = argparse.ArgumentParser(
        description="Generate lecture slides or quizzes using OLLAMA"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Slides command
    slides_parser = subparsers.add_parser('slides', help='Generate lecture slides')
    slides_parser.add_argument('topic', help='Topic for the lecture')
    slides_parser.add_argument(
        '--level',
        choices=['beginner', 'intermediate', 'advanced'],
        default='intermediate',
        help='Difficulty level'
    )
    slides_parser.add_argument(
        '--format',
        choices=['marp', 'markdown'],
        default='marp',
        help='Output format'
    )
    
    # Quiz command
    quiz_parser = subparsers.add_parser('quiz', help='Generate quiz questions')
    quiz_parser.add_argument('topic', help='Topic for the quiz')
    quiz_parser.add_argument(
        '--num',
        type=int,
        default=5,
        help='Number of questions'
    )
    
    args = parser.parse_args()
    
    if args.command == 'slides':
        generate_slides(args.topic, args.level, args.format)
    elif args.command == 'quiz':
        generate_quiz(args.topic, args.num)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
