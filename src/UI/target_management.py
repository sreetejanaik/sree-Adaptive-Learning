# src/UI/target_management.py

import json
import os

class TargetManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_targets()

    def load_targets(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.targets = json.load(file)
        else:
            self.targets = {}

    def save_targets(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.targets, file, indent=4)

    def set_target(self, target):
        student_id = "default_student_id"  # Replace with actual student ID handling
        self.targets[student_id] = {'target': target, 'progress': 0}
        self.save_targets()

    def get_target(self):
        student_id = "default_student_id"
        return self.targets.get(student_id, {}).get('target', None)
