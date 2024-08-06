import panel as pn
from src.UI.target_management import load_targets, save_targets
from UI.problem_generator import ExtendedProblemGeneratorAgent

def create_target_setting_panel(chat_interface):
    target_input = pn.widgets.TextInput(name='Set Your Target', placeholder='Enter your target...')
    set_target_button = pn.widgets.Button(name='Set Target', button_type='primary')
    feedback = pn.pane.Markdown()

    def set_target(event):
        target = target_input.value
        if target:
            agent = ExtendedProblemGeneratorAgent()
            problems = agent.get_problems_for_target(target)
            
            targets_data = load_targets()
            targets_data["targets"].append({
                "target": target,
                "status": "not_started",
                "questions": problems
            })
            save_targets(targets_data)
            
            feedback.object = f"Target set: {target}. Problems generated: {problems}"
            chat_interface.send(f"Target set: {target}. Problems generated: {problems}", user="System", respond=False)
    
    set_target_button.on_click(set_target)

    return pn.Column(target_input, set_target_button, feedback)
