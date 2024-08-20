import unittest
from src.Agents.student_agent import StudentAgent

class TestStudentAgentPrompt(unittest.TestCase):
    def setUp(self):
        self.agent = StudentAgent()

    def test_student_agent_prompt(self):
        prompt = "Explain how to factorize quadratic equations."
        expected_output = "To factorize a quadratic equation, find two numbers that multiply to give the constant term..."
        actual_output = self.agent.get_response(prompt)
        self.assertIn(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()
