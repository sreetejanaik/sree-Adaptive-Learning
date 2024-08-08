import panel as pn
from crewai import Crew, Process, Agent, Task
from langchain_openai import ChatOpenAI
from src import globals
from src.UI.avatar import avatar
import os
import asyncio

pn.extension(design="material")

script_dir = os.path.dirname(os.path.abspath(__file__))
progress_file_path = os.path.join(script_dir, '../../progress.json')

globals.input_future = None

# CrewAI Setup
llm = ChatOpenAI(model="gpt-4")

tutor_agent = Agent(
    role='Math Tutor',
    backstory='You are a math tutor with knowledge of various math topics. You should be able to explain and solve problems across different areas of mathematics.',
    goal="Assist with any math-related questions or problems.",
    llm=llm
)

# Define the process for CrewAI
def process_with_crew_ai(question):
    task = Task(
        description=f"Provide an explanation or solution for the following math question: {question}",
        agent=tutor_agent,
        expected_output="A detailed explanation or solution."
    )

    crew = Crew(
        tasks=[task],
        agents=[tutor_agent],
        manager_llm=llm,
        process=Process.hierarchical
    )

    result = crew.kickoff()
    return str(result)

# Create the Panel app
def create_app():
    # Panel UI setup
    title = pn.pane.Markdown("# Adaptive Tutor", sizing_mode='stretch_width')
    text_area = pn.widgets.TextAreaInput(placeholder="Type your math question here...")
    submit_button = pn.widgets.Button(name="Submit")
    rerun_button = pn.widgets.Button(name="", icon='refresh')
    result_pane = pn.pane.Markdown("**Response will appear here...**", sizing_mode='stretch_width')
    history_pane = pn.pane.Markdown("### Conversation History", sizing_mode='stretch_width')

    last_question = None
    last_response = None

    async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
        if contents:
            response = process_with_crew_ai(contents)
            history_pane.object += f"**Student:** {contents}\n\n**Tutor:** {response}\n\n"
            result_pane.object = response
            text_area.value = ""  # Clear the text area
        else:
            result_pane.object = "Please enter a question."

    def on_submit(event):
        global last_question, last_response
        question = text_area.value
        if question:
            response = process_with_crew_ai(question)
            last_question = question
            last_response = response
            history_pane.object += f"**Student:** {question}\n\n**Tutor:** {response}\n\n"
            result_pane.object = response
            text_area.value = ""  # Clear the text area
        else:
            result_pane.object = "Please enter a question."

    def on_rerun(event):
        global last_question, last_response
        if last_question:
            response = process_with_crew_ai(last_question)
            last_response = response
            history_pane.object += f"**Student:** {last_question}\n\n**Tutor:** {response}\n\n"
            result_pane.object = response
        else:
            result_pane.object = "No previous question to rerun."

    submit_button.on_click(on_submit)
    rerun_button.on_click(on_rerun)

    buttons_row = pn.Row(submit_button, rerun_button)
    layout = pn.Column(title, history_pane, result_pane, text_area, buttons_row)

    # Initialize with a greeting
    history_pane.object = "### Conversation History\n**Tutor:** I'm a math tutor. How can I help you today?\n\n"

    return layout

if __name__ == "__main__":
    app = create_app()
    pn.serve(app)
