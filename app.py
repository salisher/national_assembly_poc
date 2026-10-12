from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Simulated Database
documents = [
    {
        "id": 1,
        "title": "Flood Preparedness Brief 2026.pdf",
        "raw_text": "Meeting regarding national flood preparedness and NDMA coordination responsibilities across provinces.",
        "summary": "Meeting discusses flood preparedness and assigns NDMA coordination responsibilities.",
        "category": "Disaster Management",
        "priority": "High",
        "status": "Approved",
        "language": "English"
    },
    {
        "id": 2,
        "title": "NA_Speaker_Directive_Urdu.pdf",
        "raw_text": "قومی اسمبلی کے بریفنگ سیشن کی تیاری کی ہدایت۔",
        "summary": "Directive issued for the preparation of the upcoming National Assembly briefing session.",
        "category": "Parliamentary Affairs",
        "priority": "Medium",
        "status": "Pending Review",
        "language": "Urdu"
    }
]

directions = [
    {
        "id": 1,
        "doc_id": 1,
        "direction": "Review flood preparedness arrangements and submit report.",
        "officer": "Ahmed Khan",
        "deadline": "2026-09-15",
        "status": "In Progress"
    }
]

audit_logs = [
    {"timestamp": "2026-09-09 10:00:00", "user": "System", "action": "Initialized Prototype Environment"},
    {"timestamp": "2026-09-09 10:15:00", "user": "Speaker Staff", "action": "Uploaded Flood Preparedness Brief 2026.pdf"},
    {"timestamp": "2026-09-09 10:16:00", "user": "AI Module", "action": "Generated Summary and Auto-Classified Category"},
    {"timestamp": "2026-09-09 10:20:00", "user": "Speaker Staff", "action": "Approved AI extraction for Doc #1"},
    {"timestamp": "2026-09-09 10:25:00", "user": "Speaker Office", "action": "Assigned Direction to Ahmed Khan (Due: 15 Sep 2026)"}
]

# HTML Template embedded directly in app.py
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>National Assembly - Speaker AI Workspace PoC</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; color: #333; }
        .header { background: #004018; color: #fff; padding: 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { margin: 0; font-size: 24px; }
        .header p { margin: 5px 0 0 0; font-size: 14px; opacity: 0.8; }
        .metrics { display: flex; gap: 20px; margin-bottom: 20px; }
        .card { background: #fff; padding: 20px; border-radius: 8px; flex: 1; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; border-left: 5px solid #004018; }
        .card h3 { margin: 0; font-size: 32px; color: #004018; }
        .card p { margin: 5px 0 0 0; color: #666; font-weight: bold; }
        .container { background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; }
        h2 { color: #004018; border-bottom: 2px solid #f4f6f9; padding-bottom: 10px; margin-top: 0; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; color: #333; }
        .badge { padding: 5px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; }
        .badge-high { background: #f8d7da; color: #721c24; }
        .badge-medium { background: #fff3cd; color: #856404; }
        .badge-approved { background: #d4edda; color: #155724; }
        .badge-pending { background: #e2e3e5; color: #383d41; }
        input[type="text"], textarea, select { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; margin-top: 5px; }
        button { background: #004018; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background: #002b10; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1>NATIONAL ASSEMBLY OF PAKISTAN</h1>
            <p>Speaker's Office – Digital & AI Workspace (PoC Evaluation Demo)</p>
        </div>
        <span style="background: #ffffff22; padding: 8px 15px; border-radius: 5px; font-size: 13px;">Confidentiality Level: Synthetic Demo Data</span>
    </div>

    <div class="metrics">
        <div class="card"><h3>{{ docs|length }}</h3><p>Total Documents</p></div>
        <div class="card" style="border-left-color: #d9534f;"><h3 style="color:#d9534f;">{{ pending_count }}</h3><p>Pending Review</p></div>
        <div class="card" style="border-left-color: #f0ad4e;"><h3 style="color:#f0ad4e;">{{ directions|length }}</h3><p>Active Directions</p></div>
        <div class="card" style="border-left-color: #0275d8;"><h3 style="color:#0275d8;">100%</h3><p>Audit Compliance</p></div>
    </div>

    <div class="grid-2">
        <!-- Document Upload & AI Processing -->
        <div class="container">
            <h2>1. Upload Document & Run AI Engine</h2>
            <form action="/upload" method="POST">
                <label><b>Document Title:</b></label>
                <input type="text" name="title" placeholder="e.g. NDMA Flood Response Report.pdf" required>
                
                <label style="margin-top:10px; display:block;"><b>Document Text Content:</b></label>
                <textarea name="raw_text" rows="4" placeholder="Paste document content here..." required></textarea>
                
                <button type="submit" style="margin-top:15px;">Upload & Execute AI Processing</button>
            </form>
        </div>

        <!-- Smart AI Search -->
        <div class="container">
            <h2>2. AI Natural Language Search</h2>
            <form action="/search" method="GET">
                <input type="text" name="q" value="{{ query }}" placeholder="e.g. Show decisions related to disaster management or flood">
                <button type="submit" style="margin-top:15px;">Search Repository</button>
            </form>

            {% if search_results is not none %}
                <h3 style="margin-top:20px; font-size:14px; color:#555;">Search Results:</h3>
                <ul>
                {% for r in search_results %}
                    <li><b>{{ r.title }}</b> ({{ r.category }}) — <i>"{{ r.summary }}"</i></li>
                {% else %}
                    <li>No matching documents found.</li>
                {% endfor %}
                </ul>
            {% endif %}
        </div>
    </div>

    <!-- Repository & AI Extracted Metadata -->
    <div class="container">
        <h2>3. Document Processing Pipeline (Human-in-the-Loop Gate)</h2>
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>AI Suggested Category</th>
                    <th>Priority</th>
                    <th>AI Generated Summary</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for doc in docs %}
                <tr>
                    <td><b>{{ doc.title }}</b><br><small>Lang: {{ doc.language }}</small></td>
                    <td>{{ doc.category }}</td>
                    <td><span class="badge badge-{{ doc.priority.lower() }}">{{ doc.priority }}</span></td>
                    <td><small>{{ doc.summary }}</small></td>
                    <td><span class="badge badge-{{ 'approved' if doc.status == 'Approved' else 'pending' }}">{{ doc.status }}</span></td>
                    <td>
                        {% if doc.status != 'Approved' %}
                            <a href="/approve/{{ doc.id }}"><button style="padding: 5px 10px; font-size:12px;">Approve AI Summary</button></a>
                        {% else %}
                            <span style="color:green; font-size:12px;">✓ Approved</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="grid-2">
        <!-- Assign Speaker Direction -->
        <div class="container">
            <h2>4. Issue Speaker Direction</h2>
            <form action="/assign_direction" method="POST">
                <label><b>Select Approved Document:</b></label>
                <select name="doc_id">
                    {% for doc in docs %}
                        <option value="{{ doc.id }}">{{ doc.title }}</option>
                    {% endfor %}
                </select>

                <label style="margin-top:10px; display:block;"><b>Speaker Direction / Instruction:</b></label>
                <input type="text" name="direction" placeholder="e.g. Submit compliance report" required>

                <label style="margin-top:10px; display:block;"><b>Responsible Officer:</b></label>
                <input type="text" name="officer" placeholder="e.g. Director General NDMA" required>

                <label style="margin-top:10px; display:block;"><b>Deadline:</b></label>
                <input type="date" name="deadline" required>

                <button type="submit" style="margin-top:15px;">Assign Direction</button>
            </form>
        </div>

        <!-- Active Directions Tracker -->
        <div class="container">
            <h2>5. Active Directions Tracker</h2>
            <table>
                <thead>
                    <tr>
                        <th>Instruction</th>
                        <th>Officer</th>
                        <th>Deadline</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for d in directions %}
                    <tr>
                        <td>{{ d.direction }}</td>
                        <td><b>{{ d.officer }}</b></td>
                        <td>{{ d.deadline }}</td>
                        <td><span class="badge badge-medium">{{ d.status }}</span></td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Audit Trail -->
    <div class="container">
        <h2>6. System Audit Trail (Verification Traceability)</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>User / System Actor</th>
                    <th>Action Performed</th>
                </tr>
            </thead>
            <tbody>
                {% for log in logs[::-1] %}
                <tr>
                    <td><small>{{ log.timestamp }}</small></td>
                    <td><b>{{ log.user }}</b></td>
                    <td>{{ log.action }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

</body>
</html>
"""

@app.route("/")
def dashboard():
    pending_count = sum(1 for d in documents if d["status"] != "Approved")
    query = request.args.get("q", "")
    search_results = None
    
    if query:
        search_results = [
            d for d in documents 
            if query.lower() in d["title"].lower() 
            or query.lower() in d["summary"].lower() 
            or query.lower() in d["category"].lower()
        ]

    return render_template_string(
        HTML_TEMPLATE, 
        docs=documents, 
        directions=directions, 
        logs=audit_logs, 
        pending_count=pending_count,
        search_results=search_results,
        query=query
    )

@app.route("/upload", methods=["POST"])
def upload():
    title = request.form.get("title")
    raw_text = request.form.get("raw_text")
    
    is_urdu = any("\u0600" <= char <= "\u06FF" for char in raw_text)
    doc_id = len(documents) + 1
    
    simulated_summary = (raw_text[:120] + "...") if len(raw_text) > 120 else raw_text
    category = "Disaster Management" if "flood" in raw_text.lower() or "سیلاب" in raw_text else "General Administration"
    priority = "High" if "urgent" in raw_text.lower() or "عدالت" in raw_text or "ضروری" in raw_text else "Medium"
    
    documents.append({
        "id": doc_id,
        "title": title,
        "raw_text": raw_text,
        "summary": f"[AI Extracted] {simulated_summary}",
        "category": category,
        "priority": priority,
        "status": "Pending Review",
        "language": "Urdu" if is_urdu else "English"
    })
    
    audit_logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": "Speaker Staff",
        "action": f"Uploaded document '{title}'"
    })
    audit_logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": "AI Engine Module",
        "action": f"Extracted metadata & summary for Doc #{doc_id}"
    })
    
    return redirect(url_for("dashboard"))

@app.route("/approve/<int:doc_id>")
def approve(doc_id):
    for d in documents:
        if d["id"] == doc_id:
            d["status"] = "Approved"
            audit_logs.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user": "Speaker Staff",
                "action": f"Approved AI extraction for Doc #{doc_id} ('{d['title']}')"
            })
            break
    return redirect(url_for("dashboard"))

@app.route("/assign_direction", methods=["POST"])
def assign_direction():
    doc_id = int(request.form.get("doc_id"))
    direction_text = request.form.get("direction")
    officer = request.form.get("officer")
    deadline = request.form.get("deadline")
    
    directions.append({
        "id": len(directions) + 1,
        "doc_id": doc_id,
        "direction": direction_text,
        "officer": officer,
        "deadline": deadline,
        "status": "In Progress"
    })
    
    audit_logs.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": "Speaker Office",
        "action": f"Assigned direction to {officer} (Deadline: {deadline})"
    })
    
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)