# src/UI/panel_gui_state_machine_user_story_10.py

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

os.environ["AUTOGEN_USE_DOCKER"] = "False"

script_dir = os.path.dirname(os.path.abspath(__file__))
progress_file_path = os.path.join(script_dir, '../../progress.json')

globals.input_future = None

fsm = FSM(agents_dict)

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

def create_app():
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
        
        return False, None

    for agent in groupchat.agents:
        agent.chat_interface = chat_interface
        agent.register_reply([autogen.Agent, None], reply_func=print_messages, config={"callback": None})

    # Create the Panel app object with the chat interface
    app = pn.template.BootstrapTemplate(title=globals.APP_NAME)

    # Add the collapsible target setting and goal tracking panels
    target_setting_panel = create_collapsible_panel("Target Setting", create_target_setting_panel(chat_interface))
    goal_tracking_panel = create_collapsible_panel("Goal Tracking", create_goal_tracking_panel())

    app.main.append(
        pn.Column(
            chat_interface,
            pn.Row(
                target_setting_panel,
                goal_tracking_panel
            )
        )
    )

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

def create_target_setting_panel(chat_interface):
    target_input = pn.widgets.TextInput(name='Set Your Target', placeholder='Enter your target...')
    set_target_button = pn.widgets.Button(name='Set Target', button_type='primary')

    def set_target(event):
        target = target_input.value
        if target:
            questions = generate_questions(target)
            question_list = '\n'.join([f"{i+1}. {q}" for i, q in enumerate(questions)])
            chat_interface.send(f"Target set: {target}. Here are some questions to start with:\n{question_list}", user="System", respond=False)
            globals.questions = questions
            globals.completed_questions = 0
            globals.update_progress()

    set_target_button.on_click(set_target)

    return pn.Column(target_input, set_target_button)

def generate_questions(target):
    # Simulate generating diverse questions based on the target
    # Replace with actual API call to the LLM
    # For example purposes, we are generating static questions here.
    questions = [f"What are the multiples of {target}?" for _ in range(10)]
    return questions

def create_goal_tracking_panel():
    progress_bar = pn.indicators.Progress(name='Progress', value=0)

    def update_progress():
        if hasattr(globals, 'questions') and hasattr(globals, 'completed_questions'):
            progress = (globals.completed_questions / len(globals.questions)) * 100
            progress_bar.value = progress
        else:
            progress_bar.value = 0

    globals.update_progress = update_progress

    return pn.Column(progress_bar)

def create_collapsible_panel(title, panel):
    return pn.Accordion((title, panel), toggle=True)

if __name__ == "__main__":
    app = create_app()
    pn.serve(app)
