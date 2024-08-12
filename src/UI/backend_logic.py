import json
import os

# Path to the progress file
progress_file = 'path/to/your/progress.json'  # Update this path as necessary

def load_json():
    """Load JSON data from the file."""
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            data = json.load(f)
            print(f"Loaded data: {data}")  # Debug print
            if isinstance(data, dict):
                return data
            else:
                # If data is not a dictionary, reset to an empty dictionary
                print("Data is not a dictionary, resetting to empty.")  # Debug print
                return {}
    print("Progress file does not exist. Returning empty dictionary.")  # Debug print
    return {}

def save_progress(data):
    """Save JSON data to the file."""
    with open(progress_file, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Saved data: {data}")  # Debug print

def get_progress(student_id):
    """Get progress data for a specific student."""
    data = load_json()
    print(f"Retrieved data for get_progress: {data}")  # Debug print
    return data.get(student_id, {"completed_tasks": 0, "total_tasks": 10})

def update_progress(student_id, completed_tasks):
    """Update progress data for a specific student."""
    data = load_json()
    if student_id in data:
        data[student_id]["completed_tasks"] = completed_tasks
    else:
        data[student_id] = {"completed_tasks": completed_tasks, "total_tasks": 10}
    save_progress(data)
