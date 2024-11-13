import psycopg2

# Connect to the database
con = psycopg2.connect(host='localhost', database='autos', user='autos-user', password='autos-pass')
cur = con.cursor()

# SQL script
sql = """
-- Drop tables if they exist
DROP TABLE IF EXISTS experiment CASCADE;
DROP TABLE IF EXISTS dataset CASCADE;
DROP TABLE IF EXISTS app_user CASCADE;

-- Create extensions and tables
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "unaccent";

CREATE TABLE app_user (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE dataset (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    size INT NOT NULL,
    num_classes INT NOT NULL,
    train_split FLOAT NOT NULL,
    val_split FLOAT NOT NULL,
    test_split FLOAT NOT NULL,
    imbalance_ratio FLOAT NOT NULL
);

CREATE TABLE experiment (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    train_accuracy FLOAT NOT NULL,
    validation_accuracy FLOAT NOT NULL,
    test_accuracy FLOAT NOT NULL,
    optimizer VARCHAR(100) NOT NULL,
    epochs INT NOT NULL,
    learning_rate FLOAT NOT NULL,
    patience INT NOT NULL,
    dataset_id UUID REFERENCES dataset(id) ON DELETE SET NULL,
    added_by_user_id UUID REFERENCES app_user(id) ON DELETE SET NULL
);

-- Insert example users
INSERT INTO app_user (id, name, email)
VALUES
  (uuid_generate_v4(), 'Amanda', 'amanda@teste.com');

-- Insert example datasets
INSERT INTO dataset (id, name, size, num_classes, train_split, val_split, test_split, imbalance_ratio)
VALUES
  (uuid_generate_v4(), 'MNIST', 70000, 10, 0.60, 0.20, 0.20, 1.0),
  (uuid_generate_v4(), 'CIFAR-10', 60000, 10, 0.50, 0.25, 0.25, 1.0),
  (uuid_generate_v4(), 'ImageNet', 14000000, 1000, 0.70, 0.15, 0.15, 0.5);

-- Insert example experiments with names
INSERT INTO experiment (id, name, train_accuracy, validation_accuracy, test_accuracy, optimizer, epochs, learning_rate, patience, dataset_id, added_by_user_id)
VALUES
  (uuid_generate_v4(), 'Experiment 1', 0.95, 0.93, 0.92, 'Adam', 30, 0.001, 5, (SELECT id FROM dataset WHERE name = 'MNIST'), (SELECT id FROM app_user WHERE name = 'Amanda')),
  (uuid_generate_v4(), 'Experiment 2', 0.85, 0.84, 0.83, 'SGD', 50, 0.01, 10, (SELECT id FROM dataset WHERE name = 'CIFAR-10'), (SELECT id FROM app_user WHERE name = 'Amanda')),
  (uuid_generate_v4(), 'Experiment 3', 0.75, 0.74, 0.73, 'RMSprop', 40, 0.001, 8, (SELECT id FROM dataset WHERE name = 'ImageNet'), (SELECT id FROM app_user WHERE name = 'Amanda'));
"""

# Execute the SQL script
cur.execute(sql)
con.commit()

# Close the connection
cur.close()
con.close()