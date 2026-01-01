import abc
from src.core.engine.message_pool import Message

class Role(abc.ABC):
    def __init__(self, name, profile, goal, constraints, memory=None):
        self.name = name
        self.profile = profile
        self.goal = goal
        self.constraints = constraints
        self.memory = memory
        self.subscription = set()
        self._rc = [] # Role context (messages observed)

    def subscribe(self, roles: set):
        self.subscription.update(roles)

    def observe(self, message_pool):
        """
        MetaGPT Observation Phase: Fetch messages subscribed to.
        """
        all_msgs = message_pool.fetch()
        # Filter messages based on subscription
        observed = [m for m in all_msgs if m.role in self.subscription]
        self._rc = observed
        return observed

    @abc.abstractmethod
    def act(self, message_pool):
        """
        MetaGPT Action Phase: Process context and publish new artifacts.
        """
        pass

    def get_memory_context(self):
        if self.memory:
            lessons = self.memory.get_all_memory()
            return f"\n[RECALLING MEMORY]\n- Past Failures: {len(lessons['failures'])}\n- Successful Patterns: {len(lessons['patterns'])}\n"
        return ""

    def __repr__(self):
        return f"<{self.name}({self.profile})>"
