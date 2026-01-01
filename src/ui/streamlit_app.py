import streamlit as st
import sys
import os
import json
import re

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.core.engine.sop_executor import SOPExecutor, Environment
from src.core.engine.executor import Executor
from src.core.engine.memory_manager import MemoryManager
from src.agents.implementations import (
    GuideAgent, PlannerAgent, ArchitectAgent, StructureAgent,
    BuilderAgent, TesterAgent, ShipperAgent
)

st.set_page_config(page_title="AutoDev Studio", page_icon=None, layout="wide")

# Minimalist Professional CSS
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
        color: #1a1a1a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .phase-card {
        background: #f8f9fa;
        padding: 24px;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        margin-bottom: 24px;
        border-left: 4px solid #2da44e;
    }
    .phase-title {
        font-weight: 600;
        color: #24292e;
        font-size: 16px;
        margin-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .phase-purpose {
        font-size: 14px;
        color: #586069;
        margin-bottom: 16px;
    }
    .phase-content {
        font-size: 14px;
        color: #24292e;
        line-height: 1.5;
    }
    .stButton>button {
        background-color: #2da44e;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 6px 16px;
        border: none;
        box-shadow: none;
    }
    .stButton>button:hover {
        background-color: #2c974b;
    }
    div[data-testid="stDecoration"] {
        display: none;
    }
    header {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

def parse_clean_output(text):
    data = {}
    try:
        data["title"] = re.search(r"TITLE:\s*(.*)", text).group(1).strip()
        data["purpose"] = re.search(r"PURPOSE:\s*(.*)", text).group(1).strip()
        data["output"] = re.search(r"OUTPUT:\s*(.*?)(?=NEXT STEP:)", text, re.DOTALL).group(1).strip()
    except:
        data = {"title": "PROCESSING", "purpose": "System is generating content...", "output": text}
    return data

def render_phase(msg):
    data = parse_clean_output(msg.content)
    
    st.markdown(f"""
    <div class="phase-card">
        <div class="phase-title">{data['title']}</div>
        <div class="phase-purpose">{data['purpose']}</div>
        <div class="phase-content">
    """, unsafe_allow_html=True)
    
    st.markdown(data['output'])
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

def run_project(idea):
    env = Environment()
    executor = Executor()
    memory = MemoryManager()
    
    # 7-Step Roles
    env.add_role(GuideAgent(memory))
    env.add_role(PlannerAgent(memory))
    env.add_role(ArchitectAgent(memory))
    env.add_role(StructureAgent(memory))
    env.add_role(BuilderAgent(memory))
    env.add_role(TesterAgent(memory))
    env.add_role(ShipperAgent(memory))
    
    workflow_path = os.path.join(os.getcwd(), "src/core/sop/workflow.json")
    sop = SOPExecutor(env, executor, memory, workflow_path=workflow_path)
    
    success = sop.run(idea)
    return env.message_pool.messages if success else []

# SIDEBAR
with st.sidebar:
    st.markdown("### AutoDev Studio")
    st.caption("Production Build v1.0")
    st.divider()
    st.markdown("**Instructions:**")
    st.markdown("1. Define your goal.")
    st.markdown("2. Wait for the plan.")
    st.markdown("3. Receive the code.")

# MAIN
st.markdown("# Start a Project")

if "artifacts" not in st.session_state:
    st.session_state.artifacts = []

user_input = st.chat_input("What do you want to build?")

if user_input:
    st.session_state.artifacts = [] # clear previous
    with st.status("Initializing Engineering Pipeline...", expanded=True):
        st.session_state.artifacts = run_project(user_input)

# RENDER PIPELINE
if st.session_state.artifacts:
    for msg in st.session_state.artifacts:
        if msg.role != "User":
            render_phase(msg)
    
    st.markdown("### Project Complete")
    st.markdown("Ready for deployment.")
