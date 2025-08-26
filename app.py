from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Store student admissions
students = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']

        # Generate matric number
        matric_no = "SBIC" + str(random.randint(1000, 9999))

        # Save student details
        student = {
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "course": course,
            "matric_no": matric_no
        }
        students.append(student)

        return render_template('success.html', student=student)

    return render_template('admission.html')

@app.route('/students')
def student_list():
    return render_template('students.html', students=students)

if __name__ == "__main__":
    app.run(debug=True)
