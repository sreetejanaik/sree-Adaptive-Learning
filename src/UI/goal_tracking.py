# src/UI/goal_tracking.py

class GoalTracker:
    def __init__(self):
        # Initialize with example data or load from a file
        self.goals = {
            "example_student_id": {
                "targets": {
                    "Math": {"target_score": 90, "current_score": 85},
                    "Science": {"target_score": 80, "current_score": 75}
                }
            }
        }

    def get_progress(self, student_id: str) -> str:
        if student_id not in self.goals:
            raise ValueError(f"No progress data found for student_id: {student_id}")
        
        progress = self.goals[student_id]["targets"]
        progress_summary = []
        for subject, data in progress.items():
            summary = (f"{subject}: {data['current_score']} / {data['target_score']}")
            progress_summary.append(summary)
        return "\n".join(progress_summary)

    def set_target(self, student_id: str, subject: str, target_score: int):
        if student_id not in self.goals:
            self.goals[student_id] = {"targets": {}}
        if subject not in self.goals[student_id]["targets"]:
            self.goals[student_id]["targets"][subject] = {}
        self.goals[student_id]["targets"][subject]["target_score"] = target_score

    def update_progress(self, student_id: str, subject: str, current_score: int):
        if student_id not in self.goals:
            raise ValueError(f"No progress data found for student_id: {student_id}")
        if subject not in self.goals[student_id]["targets"]:
            raise ValueError(f"No target data found for subject: {subject}")
        self.goals[student_id]["targets"][subject]["current_score"] = current_score

    # You can add more methods as needed
