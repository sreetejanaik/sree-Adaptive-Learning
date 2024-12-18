##################### Knowledge Tracer #########################
from typing import Dict
from .conversable_agent import MyConversableAgent

class KnowledgeTracerAgent(MyConversableAgent):
    description =   """
            KnowledgeTracerAgent is a comprehensive and adaptive agent designed to assess and trace the capabilities of a StudentAgent by interacting 
                with various agents within the learning system. 
            KnowledgeTracerAgent gathers data from agents such as ProblemGeneratorAgent, SolutionVerifierAgent, LearnerModelAgent, and TutorAgent to build a detailed understanding 
                of the StudentAgent's knowledge and progress. 
            KnowledgeTracerAgent ensures a holistic view of the StudentAgent's capabilities, facilitating informed decisions about their learning path.                    
            """
    system_message = """
            You are KnowledgeTracerAgent, an agent responsible for assessing and tracing the capabilities of a StudentAgent by interacting with 
                other agents in the learning system. 
            Gather data from ProblemGeneratorAgent, SolutionVerifierAgent, LearnerModelAgent, TutorAgent, and any other relevant agents to build a comprehensive 
                understanding of the StudentAgent's knowledge and progress. 
            Use this information to provide insights into the StudentAgent's strengths and areas for improvement. 
            Your goal is to ensure a holistic view of the StudentAgent's capabilities, supporting informed and personalized learning decisions.
            """
    def __init__(self, **kwargs):
        super().__init__(
                name="KnowledgeTracerAgent",
                human_input_mode="NEVER",
                system_message=kwargs.pop('system_message', self.system_message),
                description=kwargs.pop('description',self.description),
                **kwargs
            )
    
    def request_insights(self, goal_name: str, completion_percentage: float) -> Dict[str, str]:
        # Example performance-based adjustment logic
        if completion_percentage >= 80:
            return {"adjustment": "Consider reducing focus on this topic and increase focus on more challenging areas."}
        elif completion_percentage >= 50:
            return {"adjustment": "Maintain current study focus and consider adjusting based on additional assessments."}
        else:
            return {"adjustment": "Increase focus on this topic and consider additional practice sessions."}
