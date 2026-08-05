from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"
ADMIN_PASSWORD = "karunya123"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = load_data()

    new_user = {
        "name": request.form["name"],
        "room": request.form["room"],
        "room_type": int(request.form["room_type"]),
        "gender": request.form["gender"],
        "block": request.form["block"],
        "year": request.form["year"],
        "contact": request.form["contact"]
    }

    room_people = [p for p in data if p["room"] == new_user["room"]]

    if len(room_people) < new_user["room_type"]:
        data.append(new_user)
        save_data(data)

    return redirect(url_for("result", room=new_user["room"]))

@app.route("/result/<room>")
def result(room):
    data = load_data()
    people = [p for p in data if p["room"] == room]

    if not people:
        return "No data found"

    room_type = people[0]["room_type"]
    full = len(people) >= room_type

    return render_template("result.html", people=people, full=full)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            data = load_data()
            return render_template("admin.html", data=data)
        else:
            return "Wrong Password"
    return render_template("admin_login.html")

@app.route("/reset")
def reset():
    save_data([])
    return "All data cleared!"

if __name__ == "__main__":
    app.run(debug=True)