from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)
CSV_FILES = {
    "2024": "data/2024/final.csv",
    "2023": "data/2023/final.csv",
    "2022": "data/2022/final.csv"
}


def load_data(batch):
    file = CSV_FILES.get(batch, CSV_FILES["2024"])
    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def get_branches(data):
    key = "Branch" if "Branch" in data[0] else "Department"
    return sorted(set(row[key] for row in data if row.get(key)))


@app.route("/")
def index():
    return render_template("batch_select.html", batches=CSV_FILES.keys())


@app.route("/batch/<batch>", methods=["GET"])
def batch_table(batch):
    data = load_data(batch)
    key = "Branch" if "Branch" in data[0] else "Department"
    # Filtering by branch
    selected_branches = request.args.getlist("branch")
    if selected_branches:
        data = [row for row in data if row[key] in selected_branches]
    # Filtering by name (search)
    search_query = request.args.get("search", "").strip().lower()
    if search_query:
        data = [row for row in data if search_query in row.get("Name", "").lower()]
    # Sorting
    sort_by = request.args.get("sort_by")
    reverse = request.args.get("order", "desc") == "desc"
    if batch == "2023":
        # 2023: 4 SGPAs, 2 YGPAs, avg YGPA default
        def safe_float(val):
            try:
                return float(val)
            except:
                return float("-inf") if reverse else float("inf")

        def avg_ygpa(row):
            try:
                return (float(row.get("YGPA 1", 0)) + float(row.get("YGPA 2", 0))) / 2
            except:
                return float("-inf") if reverse else float("inf")

        if sort_by == "Rank" or not sort_by:
            data.sort(key=avg_ygpa, reverse=True)
            sort_by = "Rank"
        elif sort_by in data[0]:
            data.sort(key=lambda x: safe_float(x.get(sort_by, "N/A")), reverse=reverse)
    elif batch == "2022":
        # 2022: 6 SGPAs, 3 YGPAs, avg YGPA default
        def safe_float(val):
            try:
                return float(val)
            except:
                return float("-inf") if reverse else float("inf")

        def avg_ygpa(row):
            try:
                return (float(row.get("YGPA 1", 0)) + float(row.get("YGPA 2", 0)) + float(row.get("YGPA 3", 0))) / 3
            except:
                return float("-inf") if reverse else float("inf")

        if sort_by == "Rank" or not sort_by:
            data.sort(key=avg_ygpa, reverse=True)
            sort_by = "Rank"
        elif sort_by in data[0]:
            data.sort(key=lambda x: safe_float(x.get(sort_by, "N/A")), reverse=reverse)
    else:
        # Default for 2024 batch
        if not sort_by:
            sort_by = "yGPA 1"
        if sort_by in data[0]:
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
    branches = get_branches(data)
    return render_template(
        "table.html",
        data=data,
        branches=branches,
        selected_branches=selected_branches,
        sort_by=sort_by,
        order="desc" if reverse else "asc",
        search_query=search_query,
        batch=batch
    )


@app.route("/ping")
def ping():
    return "Pong!", 200


if __name__ == "__main__":
    app.run(debug=True)
