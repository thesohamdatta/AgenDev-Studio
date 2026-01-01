from src.core.engine.message_pool import Message, MessagePool
from src.core.engine.executor import Executor
from src.core.engine.memory_manager import MemoryManager
from src.core.sop.validators import get_validator
import json
import os

class Environment:
    def __init__(self):
        self.roles = set()
        self.message_pool = MessagePool()

    def add_role(self, role):
        self.roles.add(role)

    def publish_message(self, message: Message):
        self.message_pool.publish(message)

    def get_roles(self):
        return self.roles

class SOPExecutor:
    def __init__(self, env: Environment, executor: Executor, memory: MemoryManager, workflow_path="src/core/sop/workflow.json"):
        self.env = env
        self.executor = executor
        self.memory = memory
        self.workflow_path = workflow_path
        with open(workflow_path, "r") as f:
            self.workflow = json.load(f)

    def run(self, user_idea):
        print(f"[*] ENV START: {user_idea}")
        
        self.env.publish_message(Message(role="User", content=user_idea))

        for step in self.workflow:
            step_name = step["step"]
            agent_name = step["agent"]
            validator_name = step["validator"]
            max_retries = step.get("max_retries", 1)

            # Find agent by Name (Alice, Bob) OR Profile (Product Manager)
            agent = next((r for r in self.env.get_roles() if r.name == agent_name), None)
            
            if not agent:
                print(f"[!] Critical Error: Agent '{agent_name}' not found for step '{step_name}'")
                return False

            success = False
            for attempt in range(max_retries + 1):
                print(f"[*] Step: {step_name} ({agent.name}) | Attempt: {attempt + 1}")
                output = agent.act(self.env.message_pool)
                
                validator = get_validator(validator_name)
                if validator(output):
                    print(f"[+] validated.")
                    success = True
                    break
                else:
                    print(f"[-] validation failed.")

            if not success:
                print(f"[!!] Step {step_name} failed critical validation path.")
                return False

        return True
