###################### Student ########################
from .conversable_agent import MyConversableAgent
from src.Models.llm_config import gpt3_config

class StudentAgent(MyConversableAgent):  
    description = """ 
                Help me learn algebra
                Tutor me in calculus
                Explain polynomial factorization"""
    def __init__(self):
        super().__init__(
            name="Student",
            human_input_mode="ALWAYS",
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("exit"),
            llm_config=gpt3_config,
            system_message=self.description,
            description=self.description
        )
            