def map_experiments(experiments):
    return list(map(map_experiment, experiments))

def map_experiment(experiment):
    return {
        "id": experiment[0],
        "name": experiment[1],
        "train_accuracy": __format_percentage(experiment[2]),
        "validation_accuracy": __format_percentage(experiment[3]),
        "test_accuracy": __format_percentage(experiment[4]),
        "optimizer": experiment[5],
        "epochs": experiment[6],
        "learning_rate": experiment[7],
        "patience": experiment[8],
        "dataset_id": experiment[9],
        "dataset_name": experiment[10],
        "user_id": experiment[11],
        "user_name": experiment[12],
    }

def map_datasets(datasets):
    return list(map(map_dataset, datasets))

def map_dataset(dataset):
    return {
        "id": dataset[0],
        "name": dataset[1],
        "size": dataset[2],
        "n_classes": dataset[3],
        "train_split": __format_percentage(dataset[4]),
        "val_split": __format_percentage(dataset[5]),
        "test_split": __format_percentage(dataset[6]),
        "imbalance_ratio": dataset[7]
    }

def __format_percentage(value):
    return f"{value:.2%}"  # Format as percentage with two decimal places

def percentage_to_float(percentage_str):
    float_value = float(percentage_str.strip('%'))
    return float_value / 100