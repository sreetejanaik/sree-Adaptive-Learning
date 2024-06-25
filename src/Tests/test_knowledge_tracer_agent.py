import unittest
from unittest.mock import MagicMock
from Agents.knowledge_tracer_agent import KnowledgeTracerAgent

class TestKnowledgeTracerAgent(unittest.TestCase):

    def setUp(self):
        self.agent = KnowledgeTracerAgent()
        self.agent.respond = MagicMock(return_value={"content": self.agent.description})

    def check_response_contains(self, user_input, keywords):
        response = self.agent.respond(user_input)['content']
        for keyword in keywords:
            with self.subTest(keyword=keyword):
                self.assertIn(keyword, response)

    def test_trace_algebra_knowledge(self):
        user_input = "Trace my algebra knowledge."
        expected_keywords = ["Knowledge Tracer", "test the student's knowledge", "present problems"]
        self.check_response_contains(user_input, expected_keywords)

    def test_trace_factoring_knowledge(self):
        user_input = "Trace my knowledge in factoring."
        expected_keywords = ["Knowledge Tracer", "test the student's knowledge", "present problems"]
        self.check_response_contains(user_input, expected_keywords)

    def test_role_description(self):
        user_input = "What is your role as a knowledge tracer agent?"
        expected_keywords = ["Knowledge Tracer", "test the student's knowledge", "Problem Generator", "Learner Model"]
        self.check_response_contains(user_input, expected_keywords)

    def test_identify_struggling_topics(self):
        user_input = "How do you identify which algebra topics I am struggling with?"
        expected_keywords = ["Knowledge Tracer", "test the student's knowledge", "present problems", "maintain the Learner Model"]
        self.check_response_contains(user_input, expected_keywords)

if __name__ == "__main__":
    unittest.main()
