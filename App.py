from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from flask import jsonify

app = Flask(__name__)

# Database connection configuration
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "msithyd1"
DB_HOST = "localhost"
DB_PORT = "5432"


# Function to establish database connection
def connect_to_db():
    return psycopg2.connect(
def create_table():
    # Connect to the database
    conn = psycopg2.connect(

        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# Function to create the courses table if not exists
def create_courses_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS coursesExam (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            teacher VARCHAR(100) NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# Function to add a new course to the database
def add_course(name, teacher):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO coursesExam (name, teacher) VALUES (%s, %s)", (name, teacher))
    conn.commit()
    conn.close()

# Function to delete a course from the database
def drop_course(course_id):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM coursesExam WHERE id = %s", (course_id,))
    conn.commit()
    conn.close()

# Function to retrieve all courses from the database
def get_all_courses():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM coursesExam")
    courses = cur.fetchall()
    conn.close()
    return courses

# Create the courses table if not exists
create_courses_table()

def create_enrolled_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrolled (
            course_name VARCHAR(100) NOT NULL
        );
    """)
    conn.commit()
    conn.close()

# Create the enrolled table if not exists
create_enrolled_table()
@app.route('/courses')
def get_courses():
    courses = get_all_courses()
    print(courses)
    return jsonify(courses)


@app.route('/teacher/dashboard')
def teacher_dashboard():
    courses = get_all_courses()
    return render_template('teacher_dashboard.html', courses=courses)

@app.route('/student/dashboard')
def student_dashboard():
    courses = get_all_courses()
    return render_template('student_dashboard.html', courses=courses)

@app.route('/create_course', methods=['POST'])
def create_course():
    name = request.form['name']
    teacher = request.form['teacher']
    add_course(name, teacher)
    return redirect(url_for('teacher_dashboard'))

@app.route('/drop_course/<int:course_id>', methods=['POST'])
def drop_course_route(course_id):
    drop_course(course_id)
    return redirect(url_for('teacher_dashboard'))

# Route to enroll in a course
@app.route('/enroll', methods=['POST'])
def enroll():
    course_name = request.form['course']
    # Add the enrollment logic here, e.g., insert into the enrolled table
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO enrolled (course_name) VALUES (%s)", (course_name,))
    conn.commit()
    conn.close()
    response = {'status': 'success', 'message': f'Enrolled in {course_name}'}
    return jsonify(response)
    cur = conn.cursor()

    # Create the student table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS studentDB (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        );
    """)

    # Create the teacher table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teacherDB (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL
        );
    """)

    conn.commit()

# def add_user(username, password, role):
#     conn = psycopg2.connect(
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         host=DB_HOST,
#         port=DB_PORT
#     )
#     cur = conn.cursor()

#     if role == 'student':
#         cur.execute("INSERT INTO studentDB (username, password) VALUES (%s, %s)", (username, password))
#     elif role == 'teacher':
#         cur.execute("INSERT INTO teacherDB (username, password) VALUES (%s, %s)", (username, password))

#     conn.commit()
#     conn.close()

def authenticate_user(username, password):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("SELECT * FROM studentDB WHERE username = %s AND password = %s", (username, password))
    student = cur.fetchone()

    if student:
        return True, 'student'
    
    cur.execute("SELECT * FROM teacherDB WHERE username = %s AND password = %s", (username, password))
    teacher = cur.fetchone()

    if teacher:
        return True, 'teacher'

    return False, None

create_table()

# # Add mock users to the database
# add_user("student123", "password123", "student")
# add_user("teacher456", "password456", "teacher")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']
    
    authenticated, role = authenticate_user(username, password)
    
    if authenticated:
        if role == 'student':
            return redirect(url_for('student_dashboard'))
        elif role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
    else:
        error = 'Invalid username or password. Please try again.'
        return render_template('login.html', error=error)

@app.route('/student/dashboard')
def student_dashboard():
    return render_template('student.html')

@app.route('/teacher/dashboard')
def teacher_dashboard():
    return render_template('teacher.html')

if __name__ == '__main__':
    app.run(debug=True)
