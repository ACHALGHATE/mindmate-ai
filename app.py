from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


progress_data = {"streak": 0}



def get_response(user_input):
    user_input = user_input.lower()

    if "study" in user_input:
        return "Make a study plan: 2 hrs focus + 30 min revision 📚"
    elif "stress" in user_input:
        return "Take a deep breath, short break lo, sab theek hoga 💪"
    elif "career" in user_input:
        return "Apne interest aur skills identify karo, fir uske according plan banao 🚀"
    else:
        return "Main tumhari help ke liye hoon 😊"



def generate_study_plan(hours):
    try:
        hours = int(hours)
    except:
        return "Please enter valid number of hours."

    subjects = ["Math", "Physics", "English", "Revision"]
    plan = ""
    sub_index = 0

    for i in range(1, hours + 1):
        subject = subjects[sub_index % len(subjects)]
        plan += f"Hour {i}: {subject} 📚\n"

        if i % 2 == 0:
            plan += "Take 10 min break ☕\n"

        sub_index += 1

    return plan



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/chat", methods=["POST"])
def chat_route():
    user_message = request.json["message"]
    bot_response = get_response(user_message)
    return jsonify({"response": bot_response})



@app.route("/study-plan", methods=["POST"])
def study_plan_route():
    hours = request.json["hours"]
    plan = generate_study_plan(hours)
    return jsonify({"plan": plan})



@app.route("/mark-done", methods=["POST"])
def mark_done_route():
    progress_data["streak"] += 1

    msg = ""
    if progress_data["streak"] == 1:
        msg = "Great start 🔥"
    elif progress_data["streak"] == 3:
        msg = "Consistency building 💪"
    elif progress_data["streak"] == 5:
        msg = "You're unstoppable 🚀"

    return jsonify({
        "streak": progress_data["streak"],
        "message": msg
    })
users = {}

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username in users:
        return jsonify({"message": "User already exists"})
    
    users[username] = {
        "password": password,
        "streak": 0
    }

    return jsonify({"message": "Signup successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    if username in users and users[username]["password"] == password:
        return jsonify({"message": "Login successful"})
    
    return jsonify({"message": "Invalid credentials"})


  
if __name__ == "__main__":
    app.run(debug=True)
