# ProjectBridge

### A Project Handover and Management System

ProjectBridge is a web-based application designed to make project handovers easier when a team member leaves or becomes unavailable.

It provides one place to manage project information, tasks, activity updates, blockers, decisions and documents. It also checks for missing information before preparing a handover report.

## Live Demo

**Live Website:** https://rinkisisodiya18.pythonanywhere.com/

**GitHub Repository:** https://github.com/Rinki-sisodiya18/ProjectBridge

## Problem Statement

During a project, important information is often scattered across different platforms and messages. When a team member leaves, other members may struggle to understand pending tasks, project progress, blockers and important decisions.

ProjectBridge helps organise this information in one workspace and makes the handover process easier.

## Key Features

- **Dashboard:** Provides an overview of projects, tasks and blockers.
- **Project Management:** Allows users to add and manage projects.
- **Task Management:** Helps organise tasks and assign owners.
- **Activity Updates:** Records project progress and updates.
- **Blocker Management:** Stores project problems and their next steps.
- **Decision Management:** Maintains important project decisions.
- **Document Management:** Keeps document references organised.
- **Gap Check:** Identifies missing project information before handover.
- **Handover Report:** Generates a structured report containing project information.
- **PDF Export:** Allows users to download the handover report as a PDF.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Database |
| HTML | Page structure |
| CSS | Styling |
| Bootstrap | Responsive interface |
| Jinja2 | Dynamic HTML templates |

## How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Rinki-sisodiya18/ProjectBridge.git
```

### 2. Open the Project Folder

```bash
cd ProjectBridge
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

Open the local application in your browser at:

`http://127.0.0.1:5001`

## Project Workflow

1. Add and manage projects.
2. Create tasks and assign owners.
3. Record activity updates.
4. Add blockers and important decisions.
5. Store document references.
6. Run Gap Check to identify missing information.
7. Generate and download the Handover Report.

## Future Scope

The following improvements can be added in future versions:

- **AI-Powered Handover Summary:** Generate summaries of project activities.
- **Smart Gap Detection:** Identify missing information and suggest what needs confirmation.
- **Project Activity Timeline:** Display project activities in chronological order.
- **External Integrations:** Connect with platforms such as GitHub and task management tools.

## Conclusion

ProjectBridge aims to make project handovers more organised, clear and reliable. It brings important project information into one workspace and helps teams maintain continuity when responsibilities change.

---

**Developed by:** Rinki Sisodiya