from src.core.engine.sop_executor import SOPExecutor, Environment
from src.core.engine.executor import Executor
from src.core.engine.memory_manager import MemoryManager
from src.agents.implementations import (
    GuideAgent, PlannerAgent, ArchitectAgent, 
    BuilderAgent, TesterAgent, ShipperAgent
)
import sys
import os

def main():
    # 1. Setup Environment
    env = Environment()
    executor = Executor()
    memory = MemoryManager()
    
    # 2. Initialize User-Centric Roles
    env.add_role(GuideAgent(memory))
    env.add_role(PlannerAgent(memory))
    env.add_role(ArchitectAgent(memory))
    env.add_role(BuilderAgent(memory))
    env.add_role(TesterAgent(memory))
    env.add_role(ShipperAgent(memory))
    
    # 3. Initialize SOP Engine
    workflow_path = os.path.join(os.path.dirname(__file__), "core/sop/workflow.json")
    sop_engine = SOPExecutor(env, executor, memory, workflow_path=workflow_path)
    
    # 4. User Request
    user_idea = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "A simple tool to organize files"
    
    print("\n" + "="*80)
    print("                      AUTODEV STUDIO (User-Centric Mode)")
    print("="*80)
    
    success = sop_engine.run(user_idea)
    
    if success:
        print("\n" + "="*80)
        print("                        PROJECT COMPLETED")
        print("="*80)
        for msg in env.message_pool.messages:
            if msg.role != "User":
                print(f"\n### [{msg.role}] from {msg.sent_from}:")
                print("-" * 30)
                # Simple parser for CLI display
                import re
                try:
                    content = re.search(r"OUTPUT:\s*(.*?)(?=NEXT STEP:)", msg.content, re.DOTALL).group(1).strip()
                    print(content)
                except:
                    print(msg.content)
            
        print("\n[*] Project Ready in /workspace.")
    else:
        print("[!] Project Failed.")

if __name__ == "__main__":
    main()
