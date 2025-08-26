from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sunnybright-secret-key"

# --- Dummy Data ---
admin_user = {"username": "admin", "password": "1234"}
students = {"student": "1234"}  # username: password
courses = [
    {"id": 1, "name": "Web Development Basics"},
    {"id": 2, "name": "Python Programming"},
    {"id": 3, "name": "Graphic Design"}
]
student_courses = {}  # username: [course_ids]


# --- Routes ---
@app.route("/")
def home():
    return """
    <h1>📚 Sunny Bright Institute Portal</h1>
    <p>1. <a href='/login'>Student Login</a></p>
    <p>2. <a href='/admin'>Admin Login</a></p>
    <p>3. <a href='/register'>New Student? Register</a></p>
    """


# --- Student Registration ---
@app.route("/register", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in students:
            return "❌ Username already exists! <a href='/register'>Try again</a>"

        students[username] = password
        student_courses[username] = []
        return "✅ Registration successful! <a href='/login'>Login here</a>"

    return """
    <h2>Student Registration</h2>
    <form method='post'>
        Username: <input type='text' name='username' required><br>
        Password: <input type='password' name='password' required><br>
        <input type='submit' value='Register'>
    </form>
    """


# --- Student Login ---
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in students and students[username] == password:
            session["user"] = username
            return redirect(url_for("student_dashboard"))
        else:
            return "❌ Invalid login! <a href='/login'>Try again</a>"

    return """
    <h2>Student Login</h2>
    <form method='post'>
        Username: <input type='text' name='username'><br>
        Password: <input type='password' name='password'><br>
        <input type='submit' value='Login'>
    </form>
    """


# --- Student Dashboard ---
@app.route("/dashboard")
def student_dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"""
    <h2>Welcome, {session['user']}!</h2>
    <p><a href='/courses'>📚 View Available Courses</a></p>
    <p><a href='/mycourses'>🎓 My Courses</a></p>
    <p><a href='/logout'>🚪 Logout</a></p>
    """


# --- View Available Courses ---
@app.route("/courses")
def view_courses():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    registered = student_courses.get(user, [])
    available = [c for c in courses if c["id"] not in registered]

    if not available:
        return """
        <h2>No more new courses available!</h2>
        <a href='/dashboard'>⬅ Back</a>
        """

    course_list = "".join(
        [f"<li>{c['name']} <a href='/register/{c['id']}'>[Register]</a></li>" for c in available]
    )
    return f"""
    <h2>Available Courses</h2>
    <ul>{course_list}</ul>
    <a href='/dashboard'>⬅ Back</a>
    """


# --- Register for Course ---
@app.route("/register/<int:course_id>")
def register_course(course_id):
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]

    if user not in student_courses:
        student_courses[user] = []

    if course_id not in student_courses[user]:
        student_courses[user].append(course_id)

    return f"✅ Successfully registered for course ID {course_id}! <a href='/dashboard'>Back</a>"


# --- My Courses ---
@app.route("/mycourses")
def my_courses():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    registered = student_courses.get(user, [])
    course_names = [c["name"] for c in courses if c["id"] in registered]

    if not course_names:
        return """
        <h2>You have not registered for any courses yet.</h2>
        <a href='/courses'>📚 Register Now</a><br>
        <a href='/dashboard'>⬅ Back</a>
        """

    course_list = "".join([f"<li>{name}</li>" for name in course_names])
    return f"""
    <h2>My Courses</h2>
    <ul>{course_list}</ul>
    <a href='/dashboard'>⬅ Back</a>
    """


# --- Logout ---
@app.route("/logout")
def logout():
    session.pop("user", None)
    return "✅ You have been logged out. <a href='/'>Home</a>"


# --- Admin Login (basic) ---
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == admin_user["username"] and password == admin_user["password"]:
            return "<h2>Welcome Admin!</h2><p>Here you can manage students and courses later.</p>"

        return "❌ Invalid admin login! <a href='/admin'>Try again</a>"

    return """
    <h2>Admin Login</h2>
    <form method='post'>
        Username: <input type='text' name='username'><br>
        Password: <input type='password' name='password'><br>
        <input type='submit' value='Login'>
    </form>
    """


# --- Run app ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
