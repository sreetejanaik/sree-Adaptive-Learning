###################### Student ########################
from .conversable_agent import MyConversableAgent
from src.Models.llm_config import gpt3_config

class StudentAgent(MyConversableAgent):  
    description = """ 
                You are an analytical thinker focused on understanding the logical foundations of mathematics. You break down complex problems into manageable steps and explore multiple approaches to find solutions.
"""
    def __init__(self):
        super().__init__(
            name="Student",
            human_input_mode="ALWAYS",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("exit"),
            llm_config=gpt3_config,
            system_message=self.description,
            description=self.description
        )
            