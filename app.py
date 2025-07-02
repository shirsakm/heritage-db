from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)
CSV_FILE = "final.csv"


def load_data():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def get_branches(data):
    return sorted(set(row["Branch"] for row in data if row.get("Branch")))


@app.route("/", methods=["GET"])
def index():
    data = load_data()
    # Filtering by branch
    selected_branches = request.args.getlist("branch")
    if selected_branches:
        data = [row for row in data if row["Branch"] in selected_branches]
    # Filtering by name (search)
    search_query = request.args.get("search", "").strip().lower()
    if search_query:
        data = [row for row in data if search_query in row.get("Name", "").lower()]
    # Sorting
    sort_by = request.args.get("sort_by", "yGPA 1")
    reverse = request.args.get("order", "desc") == "desc"
    if sort_by in ["GPA Sem 1", "GPA Sem 2", "yGPA 1"]:

        def safe_float(val):
            try:
                return float(val)
            except:
                return float("-inf") if reverse else float("inf")

        data.sort(key=lambda x: safe_float(x.get(sort_by, "N/A")), reverse=reverse)
    # Add rank (index)
    for i, row in enumerate(data, 1):
        row["Rank"] = i
    # Hide Autonomy Roll
    for row in data:
        if "Autonomy Roll" in row:
            del row["Autonomy Roll"]
    branches = get_branches(load_data())
    return render_template(
        "table.html",
        data=data,
        branches=branches,
        selected_branches=selected_branches,
        sort_by=sort_by,
        order="desc" if reverse else "asc",
        search_query=search_query,
    )


@app.route("/ping")
def ping():
    return "pong", 200


if __name__ == "__main__":
    app.run(debug=True)
