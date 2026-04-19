from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        logs = request.form["logs"].lower().split("\n")

        error_count = 0
        warning_count = 0
        errors = []

        for line in logs:
            if "error" in line:
                error_count += 1
                errors.append(line.strip())
            elif "warning" in line:
                warning_count += 1

        top_issue = Counter(errors).most_common(1)
        top_issue = top_issue[0][0] if top_issue else "None"

        if error_count >= 3:
            status = "CRITICAL 🔴"
        elif error_count > 0:
            status = "WARNING 🟠"
        else:
            status = "HEALTHY 🟢"

        result = {
            "errors": error_count,
            "warnings": warning_count,
            "status": status,
            "top_issue": top_issue
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)