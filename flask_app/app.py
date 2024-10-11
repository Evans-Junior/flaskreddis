from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import redis
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://myuser:mypassword@postgres:5432/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Redis configuration
r = redis.Redis(host="redis", port=6379)

# Model definition
class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'count': self.count
        }

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def home():
    # Increment visit count in Redis
    visit_count = r.incr("hits")

    # Check if a Visit record exists
    visit = Visit.query.first()
    if visit is None:
        # If no records exist, create one
        visit = Visit(count=visit_count)
        db.session.add(visit)
    else:
        # Update existing Visit record
        visit.count = visit_count

    db.session.commit()

    return f"This page has been visited {visit.count} times."

@app.route("/visits", methods=["GET"])
def get_visits():
    visits = Visit.query.all()
    return jsonify([visit.to_dict() for visit in visits])

if __name__ == "__main__":
    app.run(host="0.0.0.0")
