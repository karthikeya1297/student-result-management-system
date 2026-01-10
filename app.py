from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",
    database="student_results"
)

cursor = db.cursor()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            if user[0] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/student')

    return render_template('login.html')





@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        branch = request.form['branch']
        subject = request.form['subject']
        marks = int(request.form['marks'])

        cursor.execute(
            "INSERT IGNORE INTO students VALUES (%s,%s,%s)",
            (student_id, name, branch)
        )


        cursor.execute(
            "INSERT INTO marks (student_id, subject, marks) VALUES (%s,%s,%s) "
            "ON DUPLICATE KEY UPDATE marks=%s",
            (student_id, subject, marks, marks)
        )



        db.commit()

    return render_template('admin.html')


@app.route('/student', methods=['GET', 'POST'])
def student():
    result = []
    total = 0
    grade = ""

    if request.method == 'POST':
        student_id = request.form['student_id']

        cursor.execute(
            "SELECT subject, marks FROM marks WHERE student_id=%s",
            (student_id,)
        )
        result = cursor.fetchall()

        total = sum(m[1] for m in result)

        if total >= 90:
            grade = "A"
        elif total >= 75:
            grade = "B"
        elif total >= 60:
            grade = "C"
        else:
            grade = "Fail"

    return render_template('student.html', result=result, total=total, grade=grade)


if __name__ == '__main__':
    app.run(debug=True)
