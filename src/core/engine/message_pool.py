class Message:
    def __init__(self, role, content, cause_by="", sent_from=""):
        self.role = role
        self.content = content
        self.cause_by = cause_by
        self.sent_from = sent_from

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."

class MessagePool:
    def __init__(self):
        self.messages = []

    def publish(self, message: Message):
        self.messages.append(message)

    def fetch(self, subscriber_role=None):
        """
        In a real publish-subscribe system, we'd filter based on subscriptions.
        For now, we return all messages or filter by role if needed.
        """
        return self.messages

    def find_latest(self, role):
        for msg in reversed(self.messages):
            if msg.role == role:
                return msg
        return None
