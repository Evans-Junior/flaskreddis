from flask import Flask, request, render_template
import redis
import psycopg2

app = Flask(__name__)

# Redis setup
r = redis.Redis(host="redis", port=6379)

# PostgreSQL connection setup
conn = psycopg2.connect(
    host="db",
    database="app_db",
    user="app_user",
    password="app_password"
)
cur = conn.cursor()

# Create users table if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
)
""")
conn.commit()

@app.route("/")
def home():
    count = r.incr("hits")
    return f"This page has been visited {count} times."

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        if name:
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
    cur.execute("SELECT name FROM users")
    users_list = cur.fetchall()
    return f"Users: {', '.join([user[0] for user in users_list])}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
