from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

CSV_FILE = os.path.join("storage", "appointments.csv")

# Ensure storage folder exists
os.makedirs("storage", exist_ok=True)

# Create file if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "email", "mobile", "department", "message"])


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        department = request.form["department"]
        message = request.form["message"]

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([name, email, mobile, department, message])

        return """
        <h2>✅ Appointment Submitted Successfully!</h2>
        <a href="/register">Go Back</a> | <a href="/show">View All</a>
        """

    return render_template("index.html")


@app.route("/show")
def show():
    data = []

    search = request.args.get("search", "").lower()

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (
                search == ""
                or search in row["name"].lower()
                or search in row["email"].lower()
                or search in row["mobile"]
            ):
                data.append(row)

    return render_template("show.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
