from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for user data and food items
users = {}
food_items = []  # List to store added food items

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
        return render_template('signup.html')

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
        # Expecting these keys from the front-end:
        food_name = data.get('food_name')
        quantity = data.get('quantity')
        condition = data.get('condition')
        location = data.get('location')
        
        # Check that all required fields are provided
        if not food_name or not quantity or not condition or not location:
            return jsonify({"message": "Food name, quantity, condition, and location are required"}), 400
        
        # Store the new food item with all properties
        food_items.append({
            "food_name": food_name,
            "quantity": quantity,
            "condition": condition,
            "location": location
        })
        return jsonify({"message": "Food added successfully", "data": data}), 201
    else:
        return render_template('addFood.html')

@app.route('/get_matches', methods=['GET'])
def get_matches():
    # For demonstration, return all food items.
    # You can update this logic to implement your matching algorithm.
    return jsonify({"matches": food_items}), 200

if __name__ == '__main__':
    app.run(debug=True)
