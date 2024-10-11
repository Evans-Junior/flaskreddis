from flask import Flask
import redis
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set up Redis connection
r = redis.Redis(host="redis", port=6379)

# Set up PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a simple User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route("/")
def home():
    # Increment the hit counter in Redis
    count = r.incr("hits")
    
    # Check if the User table exists, and create if not
    db.create_all()  # This ensures the database and table are created

    # Add a test user if the database is empty
    if not User.query.first():
        test_user = User(username="Evans")
        db.session.add(test_user)
        db.session.commit()

    # Retrieve all users from the database
    users = User.query.all()
    user_list = ", ".join(user.username for user in users)
    return f"This page has been visited {count} times. Users in the database: {user_list}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
