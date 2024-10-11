from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use the DATABASE_URL from the .env file
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

r = redis.Redis(host="redis", port=6379)

# Ensure tables are created before the first request
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    count = r.incr("hits")
    return f"This page has been visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
