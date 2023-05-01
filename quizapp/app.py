import sqlite3

# connect to the database
conn = sqlite3.connect('hw12.db')

# insert the sample data - I remarked this after the initial run of the script
#conn.execute("INSERT INTO students (id, firstname, lastname) VALUES (1, 'John', 'Smith')")

# commit the changes
#conn.commit()

# close the connection
#conn.close()



from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'password':
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login', error='Invalid username or password'))

@app.route('/dashboard')
def dashboard():
    # Fetch list of students and quizzes from the database
    students = Student.query.all()
    quizzes = Quiz.query.all()

    # Render the dashboard template with the list of students and quizzes
    return render_template('dashboard.html', students=students, quizzes=quizzes)

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, QuizResult

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw12.db'
db.init_app(app)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        student = Student(firstname=firstname, lastname=lastname)
        try:
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully.')
            return redirect(url_for('dashboard'))
        except:
            flash('Error: Student could not be added.')
            return render_template('add_student.html')
    else:
        return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from models import db, Quiz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw12.db'
db.init_app(app)

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'POST':
        subject = request.form['subject']
        num_questions = request.form['num_questions']
        quiz_date = datetime.strptime(request.form['quiz_date'], '%Y-%m-%d').date()
        quiz = Quiz(subject=subject, num_questions=num_questions, quiz_date=quiz_date)
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('add_quiz.html')


@app.route('/student/<int:id>')
def student_results(id):
    student = Student.query.get(id)
    results = QuizResult.query.filter_by(student_id=id).all()
    return render_template('student_results.html', student=student, results=results)

@app.route('/results/add', methods=['GET', 'POST'])
def add_quiz_result():
    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        grade = request.form['grade']

        try:
            result = QuizResult(student_id=student_id, quiz_id=quiz_id, grade=grade)
            db.session.add(result)
            db.session.commit()
            flash('Quiz result added successfully!')
            return redirect('/dashboard')
        except Exception as e:
            db.session.rollback()
            flash('Error adding quiz result: ' + str(e))
            return render_template('add_result.html', students=Student.query.all(), quizzes=Quiz.query.all())

    return render_template('add_result.html', students=Student.query.all(), quizzes=Quiz.query.all())


@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect('/login')

    if request.method == 'POST':
        student_id = request.form['student_id']
        quiz_id = request.form['quiz_id']
        grade = request.form['grade']

        # validate inputs
        if not student_id or not quiz_id or not grade:
            error = 'Please fill out all fields.'
            return render_template('add_result.html', students=get_students(),
                                   quizzes=get_quizzes(), error=error)

        try:
            grade = int(grade)
        except ValueError:
            error = 'Please enter a valid grade.'
            return render_template('add_result.html', students=get_students(),
                                   quizzes=get_quizzes(), error=error)

        # add result to database
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO quiz_results (student_id, quiz_id, grade) VALUES (?, ?, ?)',
                       (student_id, quiz_id, grade))
        db.commit()

        flash('Quiz result added successfully.')
        return redirect('/dashboard')

    return render_template('add_result.html', students=get_students(), quizzes=get_quizzes())
