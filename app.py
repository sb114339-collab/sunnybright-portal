from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy users
users = {
    "student": "1234",
    "admin": "admin123"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            return redirect(url_for("dashboard", user=username))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard/<user>")
def dashboard(user):
    return render_template("dashboard.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
