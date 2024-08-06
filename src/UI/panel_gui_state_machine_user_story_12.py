import autogen
import panel as pn
import openai
import os
import time
import asyncio
from typing import List, Dict
import logging
from src import globals
from src.Agents.agents import *
from src.Agents.chat_manager_fsms import FSM
from src.Agents.group_chat_manager_agent import CustomGroupChatManager, CustomGroupChat
from src.UI.avatar import avatar
from src.UI.goal_tracking import GoalTracker

# logging.basicConfig(filename='debug.log', level=logging.DEBUG, 
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

os.environ["AUTOGEN_USE_DOCKER"] = "False"

script_dir = os.path.dirname(os.path.abspath(__file__))
progress_file_path = os.path.join(script_dir, '../../progress.json')

globals.input_future = None

# Instantiate GoalTracker
goal_tracker = GoalTracker()

# Define agents
agents_dict = {
    "student": student,
    "knowledge_tracer": knowledge_tracer,
    "teacher": teacher,
    "tutor": tutor,
    "problem_generator": problem_generator,
    "solution_verifier": solution_verifier,
    "programmer": programmer,
    "code_runner": code_runner,
    "learner_model": learner_model,
    "level_adapter": level_adapter,
    "motivator": motivator
}

fsm = FSM(agents_dict)

# Create the GroupChat with agents and a manager
groupchat = CustomGroupChat(
    agents=list(agents_dict.values()), 
    messages=[],
    max_round=30,
    send_introductions=True,
    speaker_selection_method=fsm.next_speaker_selector
)

manager = CustomGroupChatManager(
    groupchat=groupchat,
    filename=progress_file_path, 
    is_termination_msg=lambda x: x.get("content", "").rstrip().find("TERMINATE") >= 0
)

# --- Panel Interface ---
def create_app():
    # --- Panel Interface ---
    pn.extension(design="material")

    async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
        if not globals.initiate_chat_task_created:
            asyncio.create_task(manager.delayed_initiate_chat(tutor, manager, contents))  
        else:
            if globals.input_future and not globals.input_future.done():
                globals.input_future.set_result(contents)
            else:
                print("No input being awaited.")

    chat_interface = pn.chat.ChatInterface(callback=callback)

    def print_messages(recipient, messages, sender, config):
        print(f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")

        content = messages[-1]['content']

        if all(key in messages[-1] for key in ['name']):
            chat_interface.send(content, user=messages[-1]['name'], avatar=avatar[messages[-1]['name']], respond=False)
        else:
            chat_interface.send(content, user=recipient.name, avatar=avatar[recipient.name], respond=False)
        
        return False, None  # required to ensure the agent communication flow continues

    # Register chat interface with ConversableAgent
    for agent in groupchat.agents:
        agent.chat_interface = chat_interface
        agent.register_reply([autogen.Agent, None], reply_func=print_messages, config={"callback": None})

    # Create the Panel app object with the chat interface
    app = pn.template.BootstrapTemplate(title=globals.APP_NAME)
    app.main.append(
        pn.Row(
            pn.Column(
                chat_interface,
                sizing_mode="stretch_both",  # Ensure chat space stretches to fill available space
                width=800
            ),
            pn.Column(
                create_collapsible_panel("Goal Tracking", create_goal_tracking_panel()),
                create_collapsible_panel("Target Setup", create_target_setup_panel()),
                sizing_mode="stretch_width",  # Ensure panels take up remaining width
                width=400
            ),
            sizing_mode="stretch_both"  # Stretch both columns
        )
    )

    # Load chat history on startup 
    chat_history_messages = manager.get_messages_from_json()
    if chat_history_messages:
        manager.resume(chat_history_messages, 'exit')
        for message in chat_history_messages:
            if 'exit' not in message:
                chat_interface.send(
                    message["content"],
                    user=message["role"], 
                    avatar=avatar.get(message["role"], None),  
                    respond=False
                )
        chat_interface.send("Time to continue your studies!", user="System", respond=False)
    else:
        chat_interface.send("Welcome to the Adaptive Math Tutor! How can I help you today?", user="System", respond=False)

    return app

def create_collapsible_panel(title: str, content: pn.Column) -> pn.Column:
    """Creates a collapsible panel for the dashboard."""
    return pn.Column(
        pn.pane.Markdown(f"## {title}"),
        content,
        margin=(0, 20),
        width=400
    )

def create_goal_tracking_panel() -> pn.Column:
    """Creates the goal tracking panel."""
    student_id = "example_student_id"  # Use a real student_id if available
    progress = goal_tracker.get_progress(student_id)
    
    # Debugging prints
    print("Type of progress:", type(progress))
    print("Contents of progress:", progress)
    
    # Ensure that `progress` is a dictionary with the expected keys
    if isinstance(progress, dict) and 'completed_tasks' in progress and 'total_tasks' in progress:
        progress_widget = pn.widgets.Progress(value=progress['completed_tasks'], max=progress['total_tasks'], sizing_mode="stretch_width")
    else:
        progress_widget = pn.pane.Markdown("**Error:** Progress data is not available.")
    
    return pn.Column(
        pn.pane.Markdown("### Goal Tracking"),
        progress_widget
    )

def create_target_setup_panel() -> pn.Column:
    """Creates the target setup panel."""
    def on_set_target(event):
        target = target_input.value
        if target:
            # Generate questions
            questions = problem_generator.generate_questions(target, num_questions=10)
            print("Generated Questions:", questions)
            # Verify questions and update progress
            for question in questions:
                # Assume student answers are collected somehow
                student_answer = get_student_answer(question)
                correct = solution_verifier.verify(question, student_answer)
                if correct:
                    goal_tracker.update_progress(student_id, 1)  # Update progress by 1 for each correct answer

            # Refresh the progress display
            app.main[1] = create_goal_tracking_panel()  # Refresh the goal tracking panel

    target_input = pn.widgets.TextInput(placeholder='Enter your target here...')
    set_target_button = pn.widgets.Button(name='Set Target', button_type='primary')
    set_target_button.on_click(on_set_target)
    
    return pn.Column(
        pn.pane.Markdown("### Target Setup"),
        target_input,
        set_target_button
    )

def get_student_answer(question):
    """Mock function to get student answer."""
    # In practice, this should be replaced with actual input collection
    return "student_answer"

if __name__ == "__main__":
    app = create_app()
    #pn.serve(app, debug=True)
    pn.serve(app)
