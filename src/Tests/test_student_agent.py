import unittest
from src.Agents.student_agent import StudentAgent

class TestStudentAgent(unittest.TestCase):

    def setUp(self):
        self.agent = StudentAgent()

    def test_explain_how_to_factorize_polynomials(self):
        prompt = "Explain how to factorize polynomials"
        response = self.agent.respond_to_prompt(prompt)
        expected_keywords = ["polynomial", "factorize", "factors", "example"]
        for keyword in expected_keywords:
            self.assertIn(keyword, response.lower(), f"Response should contain the keyword '{keyword}'")
        self.assertNotIn("I don't know", response, "Response should not indicate lack of knowledge")

    def test_teach_me_about_trigonometry(self):
        prompt = "Teach me about trigonometry"
        response = self.agent.respond_to_prompt(prompt)
        expected_keywords = ["trigonometry", "sine", "cosine", "tangent", "angles"]
        for keyword in expected_keywords:
            self.assertIn(keyword, response.lower(), f"Response should contain the keyword '{keyword}'")
        self.assertNotIn("I don't know", response, "Response should not indicate lack of knowledge")

    def test_explain_the_concept_of_limits_in_calculus(self):
        prompt = "Explain the concept of limits in calculus"
        response = self.agent.respond_to_prompt(prompt)
        expected_keywords = ["limits", "calculus", "approaches", "value", "function"]
        for keyword in expected_keywords:
            self.assertIn(keyword, response.lower(), f"Response should contain the keyword '{keyword}'")
        self.assertNotIn("I don't know", response, "Response should not indicate lack of knowledge")

if __name__ == '__main__':
    unittest.main()
