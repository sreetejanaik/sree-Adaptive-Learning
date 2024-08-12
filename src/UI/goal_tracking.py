from .backend_logic import get_progress, update_progress

class GoalTracker:
    def __init__(self):
        pass

    def get_progress(self, student_id):
        return get_progress(student_id)

    def update_progress(self, student_id, increment):
        update_progress(student_id, increment)
