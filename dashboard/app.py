import json
from pathlib import Path
from flask import Flask, render_template_string

app = Flask(__name__)

REPORT_FILE = Path("compliance/reports/compliance_report.json")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CANAF Compliance Dashboard</title>
</head>
<body>
    <h1>CANAF Compliance Dashboard</h1>

    <h2>Compliance Summary</h2>
    <p>Total Rules: {{ total }}</p>
    <p>Passed: {{ passed }}</p>
    <p>Failed: {{ failed }}</p>
    <p>Compliance Score: {{ score }}%</p>

    <table border="1" cellpadding="8">
        <tr>
            <th>Rule ID</th>
            <th>Rule Name</th>
            <th>Severity</th>
            <th>Status</th>
            <th>Findings</th>
        </tr>

        {% for rule in report %}
        <tr>
            <td>{{ rule.rule_id }}</td>
            <td>{{ rule.rule_name }}</td>
            <td>{{ rule.severity }}</td>
            <td>{{ rule.status }}</td>
            <td>{{ rule.findings }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route("/")
def dashboard():
    report = json.loads(REPORT_FILE.read_text())

    total = len(report)
    passed = sum(1 for rule in report if rule["status"] == "PASS")
    failed = sum(1 for rule in report if rule["status"] == "FAIL")
    score = round((passed / total) * 100, 2)

    return render_template_string(
        HTML_TEMPLATE,
        report=report,
        total=total,
        passed=passed,
        failed=failed,
        score=score,
    )


if __name__ == "__main__":
    app.run(debug=True)