import pytest
from engine.sop_executor import SOPExecutor, Environment
from engine.executor import Executor
from engine.memory_manager import MemoryManager

# Mock classes for lighter testing
class MockExecutor:
    def execute(self, cmd):
        return {"success": True, "stdout": "Test Output", "stderr": "", "code": 0}

def test_environment_initialization():
    env = Environment()
    assert env.message_pool is not None
    assert len(env.roles) == 0

def test_sop_loading():
    # Requires workflow.json to exist
    executor = MockExecutor()
    memory = MemoryManager()
    env = Environment()
    try:
        sop = SOPExecutor(env, executor, memory, workflow_path="sop/workflow.json")
        assert len(sop.workflow) > 0
    except FileNotFoundError:
        pytest.fail("Workflow JSON not found")

def test_memory_persistence():
    memory = MemoryManager()
    assert "feedback" in memory.files
    # Test valid JSON structure (if files exist/are created)
    data = memory.get_all_memory()
    assert isinstance(data, dict)
