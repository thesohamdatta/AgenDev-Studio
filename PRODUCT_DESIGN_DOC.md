# AutoDev Studio: Technical Product Specification (v1.0)

## 1. PRODUCT OVERVIEW

**Product Name:** AutoDev Studio  
**Type:** Open-source AI-powered software development platform  

**Description:**
AutoDev Studio is a deterministic, Multi-Agent System (MAS) designed to automate the Software Development Life Cycle (SDLC). Unlike generative code assistants (e.g., Copilot) that function as autocompleters, AutoDev Studio operates as a virtual engineering organization. It employs specialized AI agents (Business Analysts, Architects, Engineers, QA) acting under rigid Standardized Operating Procedures (SOPs) to enforce enterprise-grade quality, auditability, and validation.

**Target Users:**
- **Engineering Teams:** For rapid prototyping and boilerplate generation compliant with internal standards.
- **Startups:** To bootstrap production-ready architectures with minimal human resource.
- **Indie Hackers:** To convert business constraints into deployable software without context switching.

**Key Differentials:**
- **SOP-Driven Execution:** Agents follow state-machine logic (`workflow.json`), preventing hallucinated workflows.
- **Traceability:** Every artifact (code, test, design) is linked via a persistence layer (`TraceabilityMatrix`).
- **Self-Healing:** Built-in execution feedback loops allow the system to fix its own runtime errors.

---

## 2. SYSTEM ARCHITECTURE

The system adheres to a **Micro-Kernel Architecture** utilizing a central Message Bus for decoupled agent communication.

### High-Level Architecture
```ascii
[ User Interface (Streamlit) ]
       | (HTTP/WebSocket)
       v
[ Orchestration Controller (Main Entry) ]
       |
       +---> [ SOP Engine (State Machine) ] <---> [ Workflow definitions (JSON) ]
       |
       +---> [ Message Bus (Pub/Sub) ] <----> [ Persistent Memory (JSON) ]
       |
       +---> [ Agent Runtime ]
       |       |
       |       +-- [ BA / PM / Architect / Engineer / QA / Governance ](Roles)
       |
       +---> [ Execution Sandbox (Docker/Subprocess) ]
       |
       v
[ File System / Workspace (Artifacts) ]
```

### Service Boundaries
- **Core Engine (`src/core`):** Orchestrator, Event Bus, State Management.
- **Agent Layer (`src/agents`):** Role profiles, Prompt templates, Reasoning logic.
- **Infrastructure (`src/infrastructure`):** Application containerization, logging, tracing.
- **UI Layer (`src/ui`):** User interaction and real-time observability.

### Data Flow
1.  **User Intent** -> UI -> Message Bus.
2.  **SOP Engine** reads Intent -> Activates 'Business Analyst' Role.
3.  **Agent** reads Intent -> Generates Artifact -> Validates Schema -> Publishes to Bus.
4.  **SOP Engine** detects Success -> Activates 'Product Manager' Role.
5.  **(Loop continues)** until 'Delivery Agent' finalizes artifacts.

---

## 3. CORE MODULES

### 3.1 Orchestration Engine (`src/core/engine`)
- **Purpose:** Manages the sequential and conditional execution of agents.
- **Responsibility:** Load `workflow.json`, enforce dependencies, manage retries.
- **Input:** User Prompt, Workflow Config.
- **Output:** Execution Status, Error Logs.

### 3.2 Message Pool (`src/core/message_pool.py`)
- **Purpose:** Centralized, time-ordered, role-filtered event store.
- **Responsibility:** Publish/Subscribe logic, context window management.
- **Input:** `Message` objects (Role, Content, Timestamp).
- **Output:** Filtered lists of messages for Agent context.

### 3.3 SOP Validator (`src/core/sop/validators.py`)
- **Purpose:** Deterministic quality gate.
- **Responsibility:** Inspect agent output for required structure (JSON keys, Markdown headers).
- **Input:** Raw Text/JSON from Agent.
- **Output:** Boolean (Pass/Fail).

### 3.4 Traceability System (`src/core/traceability.py`)
- **Purpose:** Enterprise audit trail.
- **Responsibility:** Link downstream artifacts to upstream requirements.
- **Input:** Source ID, Target ID, Relationship Type.
- **Output:** JSON Graph of project lineage.

---

## 4. AGENT DESIGN

Agents are implemented as classes inheriting from `Role` (`src/agents/base.py`).

### 4.1 Business Analyst
- **Role:** Clarify Intent.
- **Responsibility:** Identify business goals, constraints, and risks.
- **Input:** Natural language user prompt.
- **Output:** structured Markdown (Goals, Risks, Success Metrics).

### 4.2 Product Manager
- **Role:** Scoping.
- **Responsibility:** Translate analysis into strict requirements (PRD).
- **Output:** Markdown PRD (Features, Non-functional requirements, Priorities).

### 4.3 Solution Architect
- **Role:** Technical Design.
- **Responsibility:** Define modules, file structure, API interfaces.
- **Output:** JSON System Design Schema.

### 4.4 Software Engineer
- **Role:** Implementation.
- **Responsibility:** Generate code strictly matching the Design JSON.
- **Output:** Source code files written to `/workspace`.

### 4.5 QA Engineer
- **Role:** Verification.
- **Responsibility:** Generate valid Pytest cases covering the Implementation.
- **Output:** `test_*.py` files.

### 4.6 Governance Agent
- **Role:** Compliance.
- **Responsibility:** Review all artifacts for security and standards.
- **Output:** Approval Status (APPROVED/REJECTED).

---

## 5. USER WORKFLOW

1.  **Onboarding:** User pulls Docker image, runs `docker-compose up`. Accesses `localhost:8501`.
2.  **Project Creation:** User inputs "Project Name" and "Objective Statement" in Streamlit sidebar.
3.  **Execution:**
    - User clicks "Start Pipeline".
    - Progress bars show Agent activity in real-time.
    - User views intermediate artifacts (PRD, Design) as they are generated.
4.  **Review:**
    - User can inspect generated code in the UI file explorer.
    - User sees "Governance Status: Approved".
5.  **Export:** User clicks "Download Release" to get a Zip of `/workspace`.

---

## 6. EXECUTION PIPELINE

### Flow Control
The `SOPExecutor` iterates through the list defined in `workflow.json`:
1.  **Dependency Check:** Are inputs (e.g., PRD) available in Message Pool?
2.  **Execution:** Call `Agent.act()`.
3.  **Validation:** Call `get_validator(step)`.
    - **Pass:** Advance index.
    - **Fail:** Increment Retry Counter -> Trigger Agent Self-Correction -> Retry.
    - **Fatal:** Halt pipeline if Max Retries exceeded.

---

## 7. ENTERPRISE QUALITY CONTROLS

### 7.1 Validation Rules
- **Schema Validation:** Design artifacts must be valid JSON with `modules` and `files` keys.
- **Syntax Validation:** Generated Python code must parse via `ast` (simulated check).

### 7.2 Security Boundaries
- **Sandboxing:** Agents operate within Docker containers.
- **File Access:** Restricted to `/workspace` volume. No access to host OS.
- **Network:** Outbound restricted to package repositories (PyPI).

### 7.3 Traceability
- Every `link()` call in `TraceabilityMatrix` creates an immutable record linking a Requirement ID to a File Path.

---

## 8. DEPLOYMENT STRATEGY

### 8.1 Local Setup (Development)
- **Tooling:** Python 3.11, Streamlit.
- **Command:** `pip install . && python src/main.py`
- **Use Case:** Extending the framework core.

### 8.2 Docker Deployment (Production)
- **Tooling:** Docker Engine, Docker Compose.
- **Config:** `docker-compose.yml` orchestrates the App and Volumes.
- **Command:** `docker-compose up -d`.
- **Isolation:** Each project runs in an isolated context.

### 8.3 CI/CD Flow (Future)
- **GitHub Actions:** Trigger AutoDev pipeline on Pull Request.
- **Artifact Upload:** Push generated code to a new branch/repo automatically.

---

## 9. OPEN SOURCE STRATEGY

### 9.1 Repository Structure
```
autodev/
├── src/
│   ├── core/      # Orchestrator & Logic
│   ├── agents/    # Role Definitions
│   ├── ui/        # Streamlit App
│   └── infrastructure/ # Docker configs
├── tests/         # Pytest Suites
├── docs/          # Architecture Decision Records
├── pyproject.toml # Project Metadata
└── PRODUCT_DESIGN_DOC.md
```

### 9.2 Contribution Rules
- **Core Stability:** Changes to `src/core` require 2 senior approvals.
- **Agent Extensions:** Community can submit new `Role` classes via Plugins (future).
- **License:** MIT License (Permissive).

---

## 10. FUTURE EXTENSIONS

1.  **Plugin Architecture:** Implement `AutoDevPlugin` interface to allow 3rd party tools (Jira, Slack, GitHub).
2.  **Multi-Modal Agents:** Support for reading/generating images (UI Mockups).
3.  **Human-in-the-Loop (HITL):** Pause pipeline at "Governance" step for manual human approval button in UI.
4.  **SaaS Multi-Tenancy:** PostgreSQL backend for `MemoryManager` to support multiple concurrent users.
