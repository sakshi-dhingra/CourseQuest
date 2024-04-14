import string
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Simulated database
DB = {
    "users": [],
    "liked_courses": []
}

app_context = {}

# Helper function to generate user ID
def generate_user_id():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))

# Endpoint for user signup (POST)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    user_id = generate_user_id()  # Automatically generate user_id
    user_data = {
        "user_id": user_id,
        "user_name": data["user_name"],
        "user_password": data["user_password"],
        "user_email": data["user_email"]
    }
    DB["users"].append(user_data)
    return jsonify({"message": "User signed up successfully", "user_id": user_id}), 201

# Endpoint for user login (GET)
@app.route('/login', methods=['GET'])
def login():
    user_email = request.args.get('user_email')
    user_password = request.args.get('user_password')
    user = next((user for user in DB["users"] if user["user_email"] == user_email and user["user_password"] == user_password), None)
    if user:
        return jsonify({"message": "Login successful", "user_id": user["user_id"]}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Endpoint to get courses liked by a user (GET)
@app.route('/liked_courses', methods=['GET'])
def get_liked_courses():
    liked_courses = [course["course_name"] for course in DB["liked_courses"]]
    return jsonify({ "liked_courses": liked_courses}), 200

# Endpoint to like a course (POST)
@app.route('/like_course', methods=['POST'])
def like_course():
    data = request.json
    course_data = {
        "course_name": data["course_name"],
        
        
    }
    DB["liked_courses"].append(course_data)
    return jsonify({"message": "Course liked successfully"}), 201

# Endpoint to delete a user (DELETE)
@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    DB["users"] = [user for user in DB["users"] if user["user_id"] != user_id]
    DB["liked_courses"] = [course for course in DB["liked_courses"] if course["user_id"] != user_id]
    return jsonify({"message": "User deleted successfully"}), 200

# Endpoint to update user details (PUT)
@app.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    for user in DB["users"]:
        if user["user_id"] == user_id:
            user.update(data)
            return jsonify({"message": "User details updated successfully"}), 200
    return jsonify({"message": "User not found"}), 404

# Endpoint to unlike a course (DELETE)
@app.route('/unlike_course', methods=['DELETE'])
def unlike_course():
    data = request.json
    #user_id = data["user_id"]
    course_name = data["course_name"]
    DB["liked_courses"] = [course for course in DB["liked_courses"] if not (course["course_name"] == course_name)]
    return jsonify({"message": "Course unliked successfully"}), 200

# Endpoint to get recommendations
@app.route('/generate_recommendations', methods=['POST'])
def generate_recommendations():
    data = request.json
    #user_id = data["user_id"]
    keyword = ''.join(data["attributes"])
    difficulty = data["difficulty"]
    website = data["website"]
    fees = data["paid"]
    recs = app_context["recommendation_engine"].get_recommendations(keyword, difficulty, website, fees)

    return jsonify({"recommended_courses": recs.to_dict(orient='records')}), 200

# Endpoint to get courses similar to coureses liked by a user (GET)
@app.route('/similar_courses/<user_id>', methods=['GET'])
def get_similar_courses(user_id):
    liked_courses = [course["course_name"] for course in DB["liked_courses"] if course["user_id"] == user_id]
    if not liked_courses:
        return jsonify({"user_id": user_id, "similar_courses": []}), 200
    
    recs = app_context["recommendation_engine"].get_similar_courses(liked_courses)
    return jsonify({"user_id": user_id, "similar_courses": recs.to_dict(orient='records')}), 200

# Endpoint to get recommendations
@app.route('/keywords', methods=['GET'])
def get_keywords():
    return jsonify({"keywords": app_context["recommendation_engine"].cleaned_tags}), 200


# @app.route('/course_details', methods=['GET'])
# def course_details():
#     return app_context["recommendation_engine"].courses_all[courses_all['Course Name'] == liked_course]


if __name__ == '__main__':
    app.run(debug=True)
