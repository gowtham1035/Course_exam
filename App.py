import psycopg2
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Database connection configuration
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "msithyd1"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_table():
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
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
