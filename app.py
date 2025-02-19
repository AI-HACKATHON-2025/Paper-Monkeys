from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)


genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction="You are helping with the distribution of food to NGOs accordng to there need from the donated food which will be provided to u as an array have to allocate the food to NGOs by checking the nutrietions of the food available to you and rationing the required amount for the number of people",
)

chat_session = model.start_chat(
  history=[
  ]
)

# In-memory storage for user data and food items
users = {}
food_items = []

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username in users:
            return jsonify({"message": "User already exists"}), 400
        
        users[username] = password
        return jsonify({"message": "Signup successful", "data": data}), 201
    else:
        return render_template('signUp.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username not in users or users[username] != password:
            return jsonify({"message": "Invalid username or password"}), 401
        
        return jsonify({"message": "Login successful", "data": data}), 200
    else:
        return render_template('login.html')

@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    if request.method == "POST":
        data = request.get_json()
        food_name = data.get('foodName')
        quantity = data.get('quantity')
        perishable = data.get('perishable')
        
        food_items.append({'foodName': food_name, 'quantity': quantity, 'perishable': perishable})
        return jsonify({"message": "Food added successfully", "data": data}), 201
    else:
        return render_template('addFood.html')

@app.route('/get_matches', methods=['GET'])
def get_matches():
    return jsonify({"matches": food_items}), 200

if __name__ == '__main__':
    app.run(debug=True)