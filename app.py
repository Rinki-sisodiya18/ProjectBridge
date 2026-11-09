from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Database Create Karna
def create_database():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Projects Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    """)

    # Tasks Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            task_name TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            owner TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]

    if "owner" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN owner TEXT")
    
    # Blockers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blockers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Open',
            next_step TEXT
        )
    """)
    cursor.execute("PRAGMA table_info(blockers)")
    columns = [column[1] for column in cursor.fetchall()]

    if "next_step" not in columns:
        cursor.execute("ALTER TABLE blockers ADD COLUMN next_step TEXT")


    # Activity Updates Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            update_text TEXT NOT NULL,
            date TEXT
        )
    """)
    # Decisions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            title TEXT NOT NULL,
            reason TEXT
        )
    """) 

    # Documents Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            title TEXT NOT NULL,
            link TEXT,
            description TEXT
        )
    """) 

    conn.commit()
    conn.close()


create_database()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Dashboard Page
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Total Projects
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    # Pending Tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Pending'")
    pending_tasks = cursor.fetchone()[0]

    # Completed Tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
    completed_tasks = cursor.fetchone()[0]

    # Open Blockers
    cursor.execute("SELECT COUNT(*) FROM blockers WHERE status = 'Open'")
    open_blockers = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_projects=total_projects,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        open_blockers=open_blockers
    )


# Projects Page
@app.route("/projects", methods=["GET", "POST"])
def projects():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]

        cursor.execute(
            "INSERT INTO projects (name, description) VALUES (?, ?)",
            (name, description)
        )

        conn.commit()
        conn.close()

        return redirect("/projects")

    cursor.execute("SELECT * FROM projects")
    project_list = cursor.fetchall()

    conn.close()

    return render_template("projects.html", projects=project_list)


# Tasks Page
@app.route("/tasks", methods=["GET", "POST"])
def tasks():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        task_name = request.form["task_name"]
        project_id = request.form["project_id"]
        owner = request.form["owner"]

        cursor.execute(
            "INSERT INTO tasks (project_id, task_name, owner) VALUES (?, ?, ?)",
            (project_id, task_name, owner)
        )

        conn.commit()
        conn.close()

        return redirect("/tasks")

    cursor.execute("SELECT * FROM tasks")
    task_list = cursor.fetchall()

    cursor.execute("SELECT * FROM projects")
    project_list = cursor.fetchall()

    conn.close()

    return render_template(
        "tasks.html",
        tasks=task_list,
        projects=project_list
    )
@app.route("/complete_task/<int:task_id>")
def complete_task(task_id):

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/tasks")

@app.route("/blockers", methods=["GET", "POST"])
def blockers():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        project_id = request.form["project_id"]
        next_step = request.form["next_step"]

        cursor.execute(
            """INSERT INTO blockers
            (project_id, title, description, next_step)
            VALUES (?, ?, ?, ?)""",
            (project_id, title, description, next_step)
        )

        conn.commit()
        conn.close()

        return redirect("/blockers")

    cursor.execute("SELECT * FROM blockers")
    blocker_list = cursor.fetchall()

    cursor.execute("SELECT * FROM projects")
    project_list = cursor.fetchall()

    conn.close()

    return render_template(
        "blockers.html",
        blockers=blocker_list,
        projects=project_list
    )

# Update Blocker Status
@app.route("/update_blocker/<int:blocker_id>", methods=["POST"])
def update_blocker(blocker_id):

    status = request.form["status"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE blockers SET status = ? WHERE id = ?",
        (status, blocker_id)
    )

    conn.commit()
    conn.close()

    return redirect("/blockers")

@app.route("/updates", methods=["GET", "POST"])
def updates():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        update_text = request.form["update_text"]
        project_id = request.form["project_id"]

        cursor.execute(
            "INSERT INTO updates (project_id, update_text, date) VALUES (?, ?, ?)",
            (project_id, update_text, request.form["date"])
        )

        conn.commit()
        conn.close()

        return redirect("/updates")

    cursor.execute("SELECT * FROM updates")
    update_list = cursor.fetchall()

    cursor.execute("SELECT * FROM projects")
    project_list = cursor.fetchall()

    conn.close()

    return render_template(
        "updates.html",
        updates=update_list,
        projects=project_list
    )

@app.route("/decisions", methods=["GET", "POST"])
def decisions():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        reason = request.form["reason"]
        project_id = request.form["project_id"]

        cursor.execute(
            "INSERT INTO decisions (project_id, title, reason) VALUES (?, ?, ?)",
            (project_id, title, reason)
        )

        conn.commit()
        conn.close()

        return redirect("/decisions")

    cursor.execute("SELECT * FROM decisions")
    decision_list = cursor.fetchall()

    cursor.execute("SELECT * FROM projects")
    project_list = cursor.fetchall()

    conn.close()

    return render_template(
        "decisions.html",
        decisions=decision_list,
        projects=project_list
    )

@app.route("/documents", methods=["GET", "POST"])
def documents():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        link = request.form["link"]
        description = request.form["description"]
        project_id = request.form["project_id"]

        cursor.execute(
            "INSERT INTO documents (project_id, title, link, description) VALUES (?, ?, ?, ?)",
            (project_id, title, link, description)
        )

        conn.commit()
        conn.close()

        return redirect("/documents")

    cursor.execute("SELECT * FROM documents")
    document_list = cursor.fetchall()

    cursor.execute("SELECT * FROM projects")
    project_list = cursor.fetchall()

    conn.close()

    return render_template(
        "documents.html",
        documents=document_list,
        projects=project_list
    )

@app.route("/handover")
def handover():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # All Projects
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    # All Tasks
    cursor.execute("""
        SELECT tasks.*, projects.name
        FROM tasks
        LEFT JOIN projects ON tasks.project_id = projects.id
    """)
    tasks = cursor.fetchall()

    # All Blockers
    cursor.execute("""
        SELECT blockers.*, projects.name
        FROM blockers
        LEFT JOIN projects ON blockers.project_id = projects.id
    """)
    blockers = cursor.fetchall()

    # All Activity Updates
    cursor.execute("""
        SELECT updates.*, projects.name
        FROM updates
        LEFT JOIN projects ON updates.project_id = projects.id
    """)
    updates = cursor.fetchall()

    # All Decisions
    cursor.execute("""
        SELECT decisions.*, projects.name
        FROM decisions
        LEFT JOIN projects ON decisions.project_id = projects.id
    """)
    decisions = cursor.fetchall()

    # All Documents
    cursor.execute("""
        SELECT documents.*, projects.name
        FROM documents
        LEFT JOIN projects ON documents.project_id = projects.id
    """)
    documents = cursor.fetchall()

    conn.close()

    return render_template(
        "handover.html",
        projects=projects,
        tasks=tasks,
        blockers=blockers,
        updates=updates,
        decisions=decisions,
        documents=documents
    )
@app.route("/gap-check")
def gap_check():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    gaps = []

    # 1. Projects without tasks
    cursor.execute("""
        SELECT name FROM projects
        WHERE id NOT IN (
            SELECT project_id FROM tasks
        )
    """)

    for project in cursor.fetchall():
        gaps.append("No tasks added in project: " + project[0])

    # 2. Pending tasks without owners
    cursor.execute("""
        SELECT task_name FROM tasks
        WHERE (owner IS NULL OR owner = '')
        AND COALESCE(LOWER(TRIM(status)), '') != 'completed'
    """)

    for task in cursor.fetchall():
        gaps.append("Missing task owner for: " + task[0])    

    # 3. Active blockers without descriptions
    cursor.execute("""
        SELECT title FROM blockers
        WHERE (description IS NULL OR description = '')
        AND LOWER(TRIM(status)) != 'resolved'
    """)

    for blocker in cursor.fetchall():
        gaps.append("Missing description for blocker: " + blocker[0])


    # 4. Active blockers without next steps
    cursor.execute("""
        SELECT title FROM blockers
        WHERE (next_step IS NULL OR next_step = '')
        AND LOWER(TRIM(status)) != 'resolved'
    """)
    for blocker in cursor.fetchall():
        gaps.append("Missing next step for blocker: " + blocker[0])
        
    # 5. Decisions without reasons
    cursor.execute("""
        SELECT title FROM decisions
        WHERE reason IS NULL OR reason = ''
    """)

    for decision in cursor.fetchall():
        gaps.append("Missing reason for decision: " + decision[0])

    # 6. Documents without links
    cursor.execute("""
        SELECT title FROM documents
        WHERE link IS NULL OR link = ''
    """)

    for document in cursor.fetchall():
        gaps.append("Missing document link: " + document[0])

    conn.close()

    return render_template("gap_check.html", gaps=gaps)
# Run Application
if __name__ == "__main__":

    create_database()

    app.run(debug=True, port=5001)