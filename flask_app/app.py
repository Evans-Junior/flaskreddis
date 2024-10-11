from flask import Flask, request
import redis
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

# Redis setup
r = redis.Redis(host="redis", port=6379)

# PostgreSQL connection setup with error handling
def connect_db():
    try:
        conn = psycopg2.connect(
            host="postgres",  # Update this to match the container name in docker-compose
            database="app_db",
            user="app_user",
            password="app_password"
        )
        return conn
    except OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

conn = connect_db()
if conn:
    cur = conn.cursor()

    # Create users table if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100)
    )
    """)
    conn.commit()
else:
    print("PostgreSQL connection failed")

@app.route("/")
def home():
    count = r.incr("hits")
    return f"This page has been visited {count} times."

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        if name and conn:
            cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            conn.commit()
            return f"User {name} added successfully!"
    return '''
        <form method="post">
            Name: <input type="text" name="name">
            <input type="submit" value="Add User">
        </form>
    '''

@app.route("/users")
def users():
    if conn:
        cur.execute("SELECT name FROM users")
        users_list = cur.fetchall()
        return f"Users: {', '.join([user[0] for user in users_list])}"
    else:
        return "Database connection not available."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
