from flask import Flask, request, redirect, url_for, render_template_string, session

app = Flask(__name__)
app.secret_key = "secret123"

# Dummy users
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "student": {"password": "student123", "role": "student"},
}

# Courses (sample data)
courses = [
    {"id": 1, "name": "Web Development Basics"},
    {"id": 2, "name": "Python Programming"},
    {"id": 3, "name": "Graphic Design"},
]

# Store student course registrations
student_courses = {}

# Home
@app.route("/")
def home():
    return """
    <h1>📚 Sunny Bright Institute Portal</h1>
    <a href='/login'>Login</a>
    """

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        return "❌ Invalid login"
    return """
    <h2>Login</h2>
    <form method='post'>
        Username: <input name='username'><br>
        Password: <input name='password' type='password'><br>
        <button type='submit'>Login</button>
    </form>
    """

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    role = users[user]["role"]

    if role == "student":
        return f"""
        <h2>Welcome {user}!</h2>
        <p>You are logged in as: student</p>
        <a href='/courses'>📚 View Courses</a><br>
        <a href='/mycourses'>✅ My Courses</a><br>
        <a href='/logout'>Logout</a>
        """
    else:
        return f"""
        <h2>Welcome {user}!</h2>
        <p>You are logged in as: admin</p>
        <a href='/logout'>Logout</a>
        """

# View Courses
@app.route("/courses")
def view_courses():
    if "user" not in session:
        return redirect(url_for("login"))
    course_list = "".join(
        [f"<li>{c['name']} <a href='/register/{c['id']}'>[Register]</a></li>" for c in courses]
    )
    return f"""
    <h2>Available Courses</h2>
    <ul>{course_list}</ul>
    <a href='/dashboard'>⬅ Back</a>
    """

# Register for a course
@app.route("/register/<int:course_id>")
def register_course(course_id):
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    student_courses.setdefault(user, [])
    if course_id not in student_courses[user]:
        student_courses[user].append(course_id)
    return redirect(url_for("my_courses"))

# My Courses
@app.route("/mycourses")
def my_courses():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    registered = student_courses.get(user, [])
    course_names = [c["name"] for c in courses if c["id"] in registered]
    course_list = "".join([f"<li>{name}</li>" for name in course_names]) or "No courses yet."
    return f"""
    <h2>My Courses</h2>
    <ul>{course_list}</ul>
    <a href='/dashboard'>⬅ Back</a>
    """

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
