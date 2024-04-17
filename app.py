from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2

app = Flask(__name__)

# Database connection configuration
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "msithyd1"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_to_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_messages_table():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            author VARCHAR(100) NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_threads():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")
    threads = cur.fetchall()
    conn.close()
    return threads

@app.route('/discussion')
def index():
    threads = get_threads()
    return render_template('course_discussion.html', threads=threads)

@app.route('/create_thread', methods=['POST'])
def create_thread():
    title = request.form['title']
    content = request.form['content']
    user = request.form['user']
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (title, content, author) VALUES (%s, %s, %s)", (title, content, user))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

def create_replies_table():
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS replies (
                reply_text TEXT NOT NULL,
                author VARCHAR(100) NOT NULL
            );
        """)
        conn.commit()
        print("Replies table created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating replies table: {e}")
    finally:
        conn.close()

# Function to insert a reply into the replies table
def insert_reply(thread_id, reply_text, author):
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO replies (reply_text, author) VALUES (%s, %s)", (reply_text, author))
        conn.commit()
        print("Reply inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting reply: {e}")
    finally:
        conn.close()

# Call the function to create the replies table if it doesn't exist
create_replies_table()


if __name__ == '__main__':
    create_messages_table()  # Create messages table if not exists
    app.run(debug=True)
