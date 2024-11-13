import psycopg2
con = psycopg2.connect(host='localhost', database='autos', user='autos-user', password='autos-pass')
cur = con.cursor()

def get_experiments(filter_value=None, filter_type=None):
    query = """SELECT experiment.id, experiment.name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience, 
                      dataset.id as dataset_id, dataset.name as dataset_name, app_user.id as user_id, app_user.name as user_name
               FROM experiment
               JOIN dataset ON experiment.dataset_id = dataset.id
               JOIN app_user ON experiment.added_by_user_id = app_user.id"""

    # Add filtering conditions based on filter_type and filter_value
    if filter_value and filter_type:
        if filter_type in ["experiment.name", "experiment.optimizer", "dataset.name", "app_user.name", "app_user.email"]:
            query += f" WHERE unaccent({filter_type}) ILIKE unaccent('%{filter_value}%')"
        elif filter_type in ["experiment.train_accuracy", "experiment.validation_accuracy", "experiment.test_accuracy", "experiment.learning_rate",
                             "dataset.train_split_percentage", "dataset.validation_split_percentage", "dataset.test_split_percentage", "dataset.imbalance_ratio"]:
            try:
                filter_value = float(filter_value)  # Ensure the filter value is a float for accuracy fields
                query += f" WHERE {filter_type} = {filter_value}"
            except ValueError:
                query += f" WHERE {filter_type} = {1e10}"
        elif filter_type in ["experiment.epochs", "experiment.patience", "dataset.size", "dataset.num_classes"]:
            try:
                filter_value = int(filter_value)  # Ensure the filter value is an integer for count-based fields
                query += f" WHERE {filter_type} = {filter_value}"
            except ValueError:
                query += f" WHERE {filter_type} = {1e10}"
        elif filter_type == "experiment.dataset_id" or filter_type == "experiment.added_by_user_id":
            query += f" WHERE {filter_type} = '{filter_value}'"  # Assume the value is a UUID, no further checks needed

    # Execute query
    cur.execute(query)
    return cur.fetchall()


def get_experiment(id):
    query = f"""SELECT experiment.id, experiment.name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience,
                       dataset.id as dataset_id, dataset.name as dataset_name, app_user.id as user_id, app_user.name as user_name
                FROM experiment
                JOIN dataset ON experiment.dataset_id = dataset.id
                JOIN app_user ON experiment.added_by_user_id = app_user.id
                WHERE experiment.id = '{id}'"""
    cur.execute(query)
    return cur.fetchone()


def get_datasets():
    query = "SELECT id, name, size, num_classes, train_split, val_split, test_split, imbalance_ratio FROM dataset;"
    cur.execute(query)
    return cur.fetchall()

def get_dataset(id):
    query = f"""SELECT id, name, size, num_classes, train_split, val_split, test_split, imbalance_ratio
                FROM dataset
                WHERE id = '{id}'"""
    cur.execute(query)
    return cur.fetchone()

def add_experiment_fn(name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience, dataset_id, added_by_user_id):
    query = """
        INSERT INTO experiment (id, name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience, dataset_id, added_by_user_id)
        VALUES (uuid_generate_v4(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience, dataset_id, added_by_user_id))
    con.commit()
    print((name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience, dataset_id, added_by_user_id))

def put_experiment_fn(id, name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience, dataset_id, added_by_user_id):
    query = """UPDATE experiment 
               SET name = %s, train_accuracy = %s, validation_accuracy = %s, test_accuracy = %s, 
                   optimizer = %s, epochs = %s, learning_rate = %s, patience = %s, 
                   dataset_id = %s, added_by_user_id = %s 
               WHERE id = %s"""
    values = (name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience, dataset_id, added_by_user_id, id)
    cur.execute(query, values)
    con.commit()

def delete_experiment_fn(id):
    query = f"DELETE FROM experiment WHERE id='{id}'"
    cur.execute(query)
    con.commit()

def get_user_by_email(email):
    query = f"SELECT id FROM app_user WHERE email = '{email}'"
    cur.execute(query)
    result = cur.fetchone()
    return result[0] if result is not None else None

def get_user(user_id):
    query = f"SELECT id, name, email FROM app_user WHERE id = '{user_id}'"
    cur.execute(query)
    return cur.fetchone()

def add_user(name, email):
    query = f"INSERT INTO app_user (id, name, email) VALUES (uuid_generate_v4(), '{name}', '{email}')"
    cur.execute(query)
    con.commit() 

def put_user(name, email):
    query = f"UPDATE app_user SET name='{name}' WHERE email='{email}'"
    cur.execute(query)
    con.commit() 

# change names in add/put
# check result[0] in get_user_by_email
# improve try/except in filtering
# do not allow overwriting of user name
# add dataset info when clicked
# select color in edit
# a tag vs. button