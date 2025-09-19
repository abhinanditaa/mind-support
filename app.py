from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.json_util import dumps
import datetime
# Placeholder for AI sentiment analysis
# from transformers import pipeline  

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate

# ----------------------------
# MongoDB Setup
# ----------------------------
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client.mindsupport

users_collection = db.users
moods_collection = db.moods
resources_collection = db.resources
appointments_collection = db.appointments

# ----------------------------
# AI Placeholder
# ----------------------------
def analyze_sentiment(text):
    # TODO: Replace with actual Hugging Face sentiment analysis
    # Example: return sentiment_pipeline(text)
    if "stress" in text.lower() or "anxious" in text.lower():
        return {"sentiment": "negative", "score": 0.9}
    return {"sentiment": "positive", "score": 0.8}

# ----------------------------
# Home Route
# ----------------------------
@app.route("/")
def home():
    return jsonify({"message": "Welcome to Mind Support!"})

# ----------------------------
# User Onboarding
# ----------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    data["created_at"] = datetime.datetime.utcnow()
    users_collection.insert_one(data)
    return jsonify({"message": "User registered successfully", "data": data})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = users_collection.find_one({"email": data.get("email")})
    if user:
        # TODO: Add password check & JWT auth
        return jsonify({"message": "Login successful", "data": {"email": user["email"]}})
    return jsonify({"message": "User not found"}), 404

# ----------------------------
# Mood Tracking
# ----------------------------
@app.route("/mood", methods=["POST"])
def log_mood():
    data = request.get_json()
    sentiment = analyze_sentiment(data.get("note", ""))
    mood_entry = {
        "user_email": data.get("email"),
        "mood": data.get("mood"),
        "note": data.get("note"),
        "sentiment": sentiment,
        "created_at": datetime.datetime.utcnow()
    }
    moods_collection.insert_one(mood_entry)
    return jsonify({"message": "Mood logged", "data": mood_entry})

@app.route("/mood", methods=["GET"])
def get_mood():
    email = request.args.get("email")
    mood_history = list(moods_collection.find({"user_email": email}))
    return dumps(mood_history)

# ----------------------------
# Resources
# ----------------------------
@app.route("/resources", methods=["GET"])
def get_resources():
    resources = list(resources_collection.find())
    if not resources:
        # Sample resources
        resources = [
            {"title": "Meditation Tips", "link": "#"},
            {"title": "Stress Management Article", "link": "#"}
        ]
        resources_collection.insert_many(resources)
    return dumps(resources)

# ----------------------------
# Peer Matching (Placeholder)
# ----------------------------
@app.route("/peer_matching", methods=["POST"])
def peer_matching():
    # TODO: Use AI clustering for anonymous peer groups
    return jsonify({"message": "Peers matched successfully (demo placeholder)"})

# ----------------------------
# Counselor Booking
# ----------------------------
@app.route("/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json()
    data["created_at"] = datetime.datetime.utcnow()
    appointments_collection.insert_one(data)
    return jsonify({"message": "Appointment booked successfully", "data": data})

@app.route("/appointments", methods=["GET"])
def get_appointments():
    email = request.args.get("email")
    appointments = list(appointments_collection.find({"user_email": email}))
    return dumps(appointments)

# ----------------------------
# Run the App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
