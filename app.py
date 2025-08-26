from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy database (we’ll replace with real DB later)
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "student": {"password": "student123", "role": "student"}
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            role = users[username]["role"]
            return redirect(url_for("dashboard", role=role, user=username))
        else:
            return "Invalid username or password. Try again."
    return render_template("login.html")

@app.route("/dashboard/<role>/<user>")
def dashboard(role, user):
    return render_template("dashboard.html", role=role, user=user)

if __name__ == "__main__":
    app.run(debug=True)
