from flask import Flask, render_template, request, redirect, session, url_for

from mapper import map_experiments, map_datasets, map_experiment, map_dataset, percentage_to_float
from database_functions import *

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("dashboard"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if session.get("email") is not None:
        return render_template("index.html", name=session.get("name"), email=session.get("email"), session_id=session.get("session_id"), data=map_experiments(get_experiments()))
    
    return render_template("index.html", data=map_experiments(get_experiments()))

@app.route("/dataset/<experiment_id>", methods=["GET", "POST"])
def dataset(experiment_id):
    experiment = map_experiment(get_experiment(experiment_id))
    if session.get("email") is not None:
        return render_template("index.html", name=session.get("name"), email=session.get("email"), session_id=session.get("session_id"),
                               data=map_experiments(get_experiments()), dataset=map_dataset(get_dataset(experiment["dataset_id"])), experiment_id=experiment_id)
    
    return render_template("index.html", data=map_experiments(get_experiments()), dataset=map_dataset(get_dataset(experiment["dataset_id"])), experiment_id=experiment_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    maybe_user = get_user_by_email(request.form.get("email"))
    # Persist user in the database if not exists
    if maybe_user is None: 
        add_user(request.form.get("name"), request.form.get("email"))
    # Update user name based on email
    else: 
        put_user(request.form.get("name"), request.form.get("email"))

    session["name"] = request.form.get("name")
    session["email"] = request.form.get("email")
    session["session_id"] = get_user_by_email(request.form.get("email"))
    return redirect(url_for("dashboard"))

@app.route("/filter_experiments", methods=["GET", "POST"])
def filter_experiments():
    # Get filters selected by user and persist on template after filter submission
    filter_value = request.form.get('filter')
    filter_type = request.form.get('filter_type')
    experiments = map_experiments(get_experiments(filter_value, filter_type))
    return render_template("index.html", name=session.get("name"), email=session.get("email"), session_id=session.get("session_id"), data=experiments, filter=filter_value, filter_type=filter_type)

@app.route("/add_experiment", methods=["GET", "POST"])
def add_experiment():
    # Only users with session can add experiments
    if session.get("email") is None:
        return redirect(url_for("login"))
    
    # Return the form template
    if request.form.get('name') is None:
        return render_template("add_experiment.html", name=session.get("name"), email=session.get("email"), datasets=map_datasets(get_datasets()))

    # Add experiment to the database, binded to current user session
    add_experiment_fn(
        request.form.get('name'),
        request.form.get('train_accuracy'),
        request.form.get('validation_accuracy'),
        request.form.get('test_accuracy'),
        request.form.get('optimizer'),
        request.form.get('epochs'),
        request.form.get('learning_rate'),
        request.form.get('patience'),
        request.form.get('dataset_id'),
        session.get("session_id")
    )

    return redirect(url_for("dashboard"))

@app.route("/put_experiment", methods=["GET", "POST"])
def put_experiment():
    # Only users with session can edit experiments
    if session.get("email") is None:
        return redirect(url_for("dashboard"))

    # Only user that registered the experiment can edit it
    if session.get("session_id") != request.form.get("added_by_user_id"):
        return redirect(url_for("dashboard"))
    
    # Return the form template
    if request.form.get('name') is None:
        experiment = map_experiment(get_experiment(request.form.get("experiment_id")))
        return render_template("put_experiment.html", name=session.get("name"), email=session.get("email"), datasets=map_datasets(get_datasets()), experiment=experiment)

    # Update experiment in the database, binded to current user session
    experiment = map_experiment(get_experiment(request.form.get("experiment_id")))
    put_experiment_fn(
        request.form.get("experiment_id"),
        request.form.get('name') or experiment.get("name"),
        request.form.get('train_accuracy') or percentage_to_float(experiment.get('train_accuracy')),
        request.form.get('validation_accuracy') or percentage_to_float(experiment.get('validation_accuracy')),
        request.form.get('test_accuracy') or percentage_to_float(experiment.get('test_accuracy')),
        request.form.get('optimizer') or experiment.get('optimizer'),
        request.form.get('epochs') or experiment.get('epochs'),
        request.form.get('learning_rate') or experiment.get('learning_rate'),
        request.form.get('patience') or experiment.get('patience'),
        request.form.get('dataset_id') or experiment.get('dataset_id'),
        session.get("session_id")
    )

    return redirect(url_for("dashboard"))

@app.route("/delete_experiment", methods=["POST"])
def delete_experiment():
    # Only users with session can delete experiments
    if session.get("email") is None:
        return redirect(url_for("dashboard"))
    # Only user that registered the experiment can delete it
    if session.get("session_id") != request.form.get('added_by_user_id'):
        return redirect(url_for("dashboard"))
    
    delete_experiment_fn(request.form.get("experiment_id"))
    return redirect(url_for("dashboard"))

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if session.get("email") is not None:
        del session["name"]
        del session["email"]
        del session["session_id"]

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(port=8080, debug=True) 