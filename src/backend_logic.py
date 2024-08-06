# backend_logic.py

import json
import os
from src.Agents.agents import problem_generator, solution_verifier

TARGETS_FILE = 'targets.json'
PROGRESS_FILE = 'progress.json'

def setup_target(student_id: str, target: str):
    """Set up a new educational target for the student."""
    targets = load_json(TARGETS_FILE)
    progress = load_json(PROGRESS_FILE)

    if student_id not in targets:
        targets[student_id] = {}
    targets[student_id][target] = {'questions': [], 'completed_tasks': 0, 'total_tasks': 10}

    save_json(TARGETS_FILE, targets)
    questions = generate_questions(target)
    targets[student_id][target]['questions'] = questions
    save_json(TARGETS_FILE, targets)
    return questions

def generate_questions(target: str) -> list:
    """Generate a list of random questions related to the target."""
    return [f"Question {i+1} for {target}" for i in range(10)]

def verify_answer(student_id: str, target: str, question: str, answer: str) -> bool:
    """Verify the student's answer for a specific question."""
    correct_answer = get_correct_answer(question)
    result = solution_verifier.verify(question, answer)

    if result:
        update_progress(student_id, target)
    return result

def get_correct_answer(question: str) -> str:
    """Retrieve the correct answer for the question."""
    return "correct_answer"

def update_progress(student_id: str, target: str):
    """Update progress based on completed tasks."""
    targets = load_json(TARGETS_FILE)
    progress = load_json(PROGRESS_FILE)

    if student_id in targets and target in targets[student_id]:
        targets[student_id][target]['completed_tasks'] += 1
        progress[student_id] = targets[student_id]
        
        save_json(TARGETS_FILE, targets)
        save_json(PROGRESS_FILE, progress)

def load_json(file_path: str) -> dict:
    """Load JSON data from a file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_json(file_path: str, data: dict):
    """Save JSON data to a file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
