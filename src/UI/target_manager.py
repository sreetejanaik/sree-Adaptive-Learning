# src/UI/target_manager.py
import openai

class TargetManager:
    def __init__(self):
        self.targets = {}
        self.topics = {}
        self.progress = {}

    def set_target(self, user, target):
        self.targets[user] = target
        self.topics[user] = self.generate_topics(target)
        self.progress[user] = [0] * len(self.topics[user])
    
    def get_target(self, user):
        return self.targets.get(user, "")
    
    def get_topics(self, user):
        return self.topics.get(user, [])
    
    def update_progress(self, user, topic_index):
        if user in self.progress:
            self.progress[user][topic_index] = 100  # Mark as complete
    
    def get_progress(self, user):
        return self.progress.get(user, [])

    def generate_topics(self, target):
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=f"Generate 10 questions or topics related to {target}.",
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.5
        )
        topics = response.choices[0].text.strip().split('\n')
        return [topic for topic in topics if topic]

target_manager = TargetManager()
