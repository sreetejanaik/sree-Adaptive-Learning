###################### Student ########################
from .conversable_agent import MyConversableAgent
from src.Models.llm_config import gpt3_config

class StudentAgent(MyConversableAgent):  
    description = """ 
                Guide me through algebraic equations
Explain geometric proofs
Teach me about trigonometry
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
            