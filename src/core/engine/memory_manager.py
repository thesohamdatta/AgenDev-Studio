import json
import os

class MemoryManager:
    def __init__(self, memory_dir="memory"):
        self.memory_dir = memory_dir
        self.files = {
            "feedback": "agent_feedback.json",
            "failures": "past_failures.json",
            "patterns": "architecture_patterns.json"
        }
        os.makedirs(memory_dir, exist_ok=True)

    def _load(self, key):
        path = os.path.join(self.memory_dir, self.files[key])
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return []

    def _save(self, key, data):
        path = os.path.join(self.memory_dir, self.files[key])
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def add_failure(self, failure):
        failures = self._load("failures")
        failures.append(failure)
        self._save("failures", failures)

    def add_pattern(self, pattern):
        patterns = self._load("patterns")
        patterns.append(pattern)
        self._save("patterns", patterns)

    def add_feedback(self, feedback):
        feedbacks = self._load("feedback")
        feedbacks.append(feedback)
        self._save("feedback", feedbacks)

    def get_all_memory(self):
        return {
            "failures": self._load("failures"),
            "patterns": self._load("patterns"),
            "feedback": self._load("feedback")
        }
