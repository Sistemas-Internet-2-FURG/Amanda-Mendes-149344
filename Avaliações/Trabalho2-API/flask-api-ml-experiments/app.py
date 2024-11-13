from flask import Flask, jsonify, request
from flask_cors import CORS
from mapper import map_experiments, map_datasets, map_experiment, map_dataset, percentage_to_float
from database_functions import *
import jwt
import datetime

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'  # Keep this secret in production
CORS(app)

# Function to generate a token
def generate_token(user_id, name, email):
    token = jwt.encode({
        'user_id': user_id,
        'name': name,
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }, app.secret_key, algorithm='HS256')
    return token.decode('utf-8')  # Decode bytes to string

# Function to decode a token
def decode_token(token):
    try:
        return jwt.decode(token.replace('"', ''), app.secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the API. Go to /dashboard for data."})

@app.route("/dashboard", methods=["GET"])
def dashboard():
    token = request.headers.get('Authorization')
    if token:
        user_data = decode_token(token.split(" ")[1])  # Assuming "Bearer <token>"
        if user_data:
            experiments = map_experiments(get_experiments())
            return jsonify({
                "name": user_data['name'],
                "email": user_data['email'],
                "data": experiments
            })
    return jsonify({"data": map_experiments(get_experiments())})

@app.route("/dataset/<experiment_id>", methods=["GET"])
def dataset(experiment_id):
    token = request.headers.get('Authorization')
    print("experiment: ", experiment_id)
    if token:
        user_data = decode_token(token.split(" ")[1])
        if user_data:
            print(get_experiment(experiment_id))
            experiment = map_experiment(get_experiment(experiment_id))
            dataset = map_dataset(get_dataset(experiment["dataset_id"]))
            return jsonify({
                "name": user_data['name'],
                "email": user_data['email'],
                "experiment_id": experiment_id,
                "data": dataset
            })
    experiment = map_experiment(get_experiment(experiment_id))
    dataset = map_dataset(get_dataset(experiment["dataset_id"]))
    return jsonify({"experiment_id": experiment_id, "data": dataset})

@app.route("/datasets", methods=["GET"])
def list_datasets():
    datasets = map_datasets(get_datasets())
    return jsonify({"data": datasets})

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    name = request.json.get("name")
    user_id = get_user_by_email(email)
    print(user_id)
    if user_id is None:
        add_user(name, email)
        user_id = get_user_by_email(email)
    else:
        user_data = get_user(user_id)
        print(user_data)
        if user_data[1] != name:
            return jsonify({"error": "Name does not match the one in the database"}), 401
    token = generate_token(user_id, name, email)
    user = {"id": user_id, "name": name, "email": email}
    return jsonify({"message": "Login successful", "token": token, "user": user})

@app.route("/filter_experiments", methods=["POST"])
def filter_experiments():
    token = request.headers.get('Authorization')
    if token:
        user_data = decode_token(token.split(" ")[1])
        if user_data:
            filter_value = request.json.get('filter')
            filter_type = request.json.get('filter_type')
            experiments = map_experiments(get_experiments(filter_value, filter_type))
            return jsonify({
                "name": user_data['name'],
                "email": user_data['email'],
                "data": experiments,
                "filter": filter_value,
                "filter_type": filter_type
            })
    return jsonify({"error": "Unauthorized"}), 403

@app.route("/add_experiment", methods=["POST"])
def add_experiment():
    token = request.headers.get('Authorization')
    if not token or not decode_token(token.split(" ")[1]):
        return jsonify({"error": "Unauthorized"}), 403

    user_data = decode_token(token.split(" ")[1])
    print(request.json, user_data)
    add_experiment_fn(
        request.json.get('name'),
        request.json.get('train_accuracy'),
        request.json.get('validation_accuracy'),
        request.json.get('test_accuracy'),
        request.json.get('optimizer'),
        request.json.get('epochs'),
        request.json.get('learning_rate'),
        request.json.get('patience'),
        request.json.get('dataset_id'),
        user_data['user_id'],  # Using user_id from decoded token
    )

    return jsonify({"message": "Experiment added successfully"})

@app.route("/put_experiment", methods=["POST"])
def put_experiment():
    token = request.headers.get('Authorization')
    if not token or not decode_token(token.split(" ")[1]):
        return jsonify({"error": "Unauthorized"}), 403

    user_data = decode_token(token.split(" ")[1])
    print(request.json)
    experiment_id = request.json.get("experiment_id")
    experiment = map_experiment(get_experiment(experiment_id))

    put_experiment_fn(
        experiment_id,
        request.json.get('name') or experiment.get("name"),
        request.json.get('train_accuracy') or percentage_to_float(experiment.get('train_accuracy')),
        request.json.get('validation_accuracy') or percentage_to_float(experiment.get('validation_accuracy')),
        request.json.get('test_accuracy') or percentage_to_float(experiment.get('test_accuracy')),
        request.json.get('optimizer') or experiment.get('optimizer'),
        request.json.get('epochs') or experiment.get('epochs'),
        request.json.get('learning_rate') or experiment.get('learning_rate'),
        request.json.get('patience') or experiment.get('patience'),
        request.json.get('dataset_id') or experiment.get('dataset_id'),
        user_data['user_id'],  # Using user_id from decoded token
    )

    return jsonify({"message": "Experiment updated successfully"})

@app.route("/delete_experiment", methods=["POST"])
def delete_experiment():
    token = request.headers.get('Authorization')
    if not token or not decode_token(token.split(" ")[1]):
        return jsonify({"error": "Unauthorized"}), 403

    user_data = decode_token(token.split(" ")[1])
    print(request.json)

    delete_experiment_fn(request.json.get("experiment_id"))
    return jsonify({"message": "Experiment deleted successfully"})

@app.route('/logout', methods=["POST"])
def logout():
    return jsonify({"message": "Logout successful"})

@app.route("/experiment/<experiment_id>", methods=["GET"])
def experiment(experiment_id):
    token = request.headers.get('Authorization')
    if token:
        user_data = decode_token(token.split(" ")[1])
        if user_data:
            experiment = map_experiment(get_experiment(experiment_id))
            return jsonify({
                "name": user_data['name'],
                "email": user_data['email'],
                "experiment_id": experiment_id,
                "data": experiment
            })
    return jsonify({"experiment_id": experiment_id, "data": map_experiment(get_experiment(experiment_id))})

if __name__ == "__main__":
    app.run(port=8080, debug=True)
