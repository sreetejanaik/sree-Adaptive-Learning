import panel as pn
from src.UI.target_management import load_targets

def create_goal_tracking_panel(chat_interface):
    progress_bar = pn.indicators.Progress(name='Progress')

    def update_progress():
        targets_data = load_targets()
        total_tasks = len(targets_data["targets"])
        completed_tasks = sum(1 for t in targets_data["targets"] if t.get("status") == "completed")
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        return progress

    progress_bar.value = update_progress()

    goal_input = pn.widgets.TextInput(name='Set Your Goal', placeholder='Enter your goal...')
    set_goal_button = pn.widgets.Button(name='Set Goal', button_type='success')

    def set_goal(event):
        goal = goal_input.value
        if goal:
            chat_interface.send(f"Goal set: {goal}", user="System", respond=False)

    set_goal_button.on_click(set_goal)

    return pn.Column(goal_input, set_goal_button, progress_bar)
