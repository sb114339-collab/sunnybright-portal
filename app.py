from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = []  # store student records here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']

        # generate matric no (simple example)
        matric_no = "SBIC" + str(len(students) + 1).zfill(4)

        # save student record
        students.append({
            "fullname": fullname,
            "email": email,
            "phone": phone,
            "course": course,
            "matric_no": matric_no
        })

        return render_template('success.html', fullname=fullname, matric_no=matric_no)

    return render_template('admission.html')

@app.route('/students')
def student_list():
    return render_template('students.html', students=students)

if __name__ == "__main__":
    app.run(debug=True)
