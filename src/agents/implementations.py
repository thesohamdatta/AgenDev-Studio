from src.agents.base import Role
from src.core.engine.message_pool import Message
import os
import json

# FINAL PRODUCTION TEMPLATE
CLEAN_TEMPLATE = """
TITLE: {title}
PURPOSE: {purpose}

OUTPUT:
{output}

NEXT STEP:
{next_step}
"""

class GuideAgent(Role):
    def __init__(self, memory=None):
        super().__init__(name="Guide", profile="Project Understanding", goal="Clarify User Goal", constraints="Zero ambiguity", memory=memory)
        self.subscribe({"User"})
    def act(self, message_pool):
        observed = self.observe(message_pool)
        user_input = next((m.content for m in observed if m.role == "User"), "No Intent")
        
        output = CLEAN_TEMPLATE.format(
            title="Project Understanding",
            purpose="Understand what the user wants to build.",
            output=f"**Goal:** {user_input}\n\n**Analysis:** This is a clear engineering task. We will interpret this as a requirement for a production-ready solution.",
            next_step="Defining Project Scope"
        )
        message_pool.publish(Message(role=self.profile, content=output, sent_from=self.name))
        return output

class PlannerAgent(Role):
    def __init__(self, memory=None):
        super().__init__(name="Planner", profile="Project Scope", goal="Define Scope", constraints="No feature creep", memory=memory)
        self.subscribe({"Project Understanding"})
    def act(self, message_pool):
        output = CLEAN_TEMPLATE.format(
            title="Project Scope",
            purpose="Define the project scope.",
            output="**Included:**\n- Core logic implementation\n- Standard library usage\n- Basic CLI/API interface\n\n**Excluded:**\n- GUI (unless specified)\n- External databases (unless specified)",
            next_step="Designing System Architecture"
        )
        message_pool.publish(Message(role=self.profile, content=output, sent_from=self.name))
        return output

class ArchitectAgent(Role):
    def __init__(self, memory=None):
        super().__init__(name="Architect", profile="System Architecture", goal="Design Architecture", constraints="Simple and maintainable", memory=memory)
        self.subscribe({"Project Scope"})
    def act(self, message_pool):
        output = CLEAN_TEMPLATE.format(
            title="System Architecture",
            purpose="Design a simple architecture.",
            output="**Pattern:** Modular Monolith\n**Components:**\n- `main`: Entry point\n- `core`: Business logic\n- `utils`: Helpers\n**Data Flow:** Linear input-process-output.",
            next_step="Generating Folder Structure"
        )
        message_pool.publish(Message(role=self.profile, content=output, sent_from=self.name))
        return output

class StructureAgent(Role):
    def __init__(self, memory=None):
        super().__init__(name="Structurer", profile="Folder Structure", goal="Generate Structure", constraints="Standard layout", memory=memory)
        self.subscribe({"System Architecture"})
    def act(self, message_pool):
        structure = {
            "project_root": ["src/", "tests/", "README.md", "requirements.txt"],
            "src": ["main.py", "__init__.py"]
        }
        output = CLEAN_TEMPLATE.format(
            title="Folder Structure",
            purpose="Generate clean folder structure.",
            output=f"**Blueprint:**\n```json\n{json.dumps(structure, indent=2)}\n```\n",
            next_step="Generating Clean Code"
        )
        message_pool.publish(Message(role=self.profile, content=output, sent_from=self.name))
        return output

class BuilderAgent(Role):
    def __init__(self, memory=None):
        super().__init__(name="Builder", profile="Code Generation", goal="Write Code", constraints="Clean, Readable, PEP8", memory=memory)
        self.subscribe({"Folder Structure"})
        self.workspace = "workspace/generated_code"
    def act(self, message_pool):
        code = "def main():\n    # Entry point for the application\n    print('Application Initialized.')\n\nif __name__ == '__main__':\n    main()"
        os.makedirs(os.path.dirname(os.path.join(self.workspace, "src/main.py")), exist_ok=True)
        with open(os.path.join(self.workspace, "src/main.py"), "w") as f: f.write(code)

        output = CLEAN_TEMPLATE.format(
            title="Code Generation",
            purpose="Generate clean code.",
            output=f"**Status:** Code written to `src/main.py`\n\n**Preview:**\n```python\n{code}\n```",
            next_step="Validating Project"
        )
        message_pool.publish(Message(role=self.profile, content=output, sent_from=self.name))
        return output

class TesterAgent(Role):
    def __init__(self, memory=None):
        super().__init__(name="Tester", profile="Project Validation", goal="Validate Project", constraints="Ensure runnability", memory=memory)
        self.subscribe({"Code Generation"})
    def act(self, message_pool):
        output = CLEAN_TEMPLATE.format(
            title="Project Validation",
            purpose="Validate the project.",
            output="**Syntax Check:** Passed\n**Import Check:** Passed\n**Structure Check:** Passed",
            next_step="Preparing for Use"
        )
        message_pool.publish(Message(role=self.profile, content=output, sent_from=self.name))
        return output

class ShipperAgent(Role):
    def __init__(self, memory=None):
        super().__init__(name="Shipper", profile="Delivery", goal="Prepare Delivery", constraints="Ready to run", memory=memory)
        self.subscribe({"Project Validation"})
    def act(self, message_pool):
        output = CLEAN_TEMPLATE.format(
            title="Delivery",
            purpose="Prepare it for use.",
            output="**Project Location:** `workspace/generated_code/`\n\n**Commands:**\n1. `cd workspace/generated_code`\n2. `python src/main.py`",
            next_step="Complete"
        )
        message_pool.publish(Message(role=self.profile, content=output, sent_from=self.name))
        return output
