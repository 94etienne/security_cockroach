import os
import pandas as pd


def load_navigation_data(data_dir="data"):
    path = os.path.join(data_dir, "navigation_dataset.csv")
    return pd.read_csv(path, parse_dates=["timestamp"])


def load_thermal_data(data_dir="data"):
    path = os.path.join(data_dir, "thermal_dataset.csv")
    return pd.read_csv(path, parse_dates=["timestamp"])


def load_environment_data(data_dir="data"):
    path = os.path.join(data_dir, "environment_dataset.csv")
    return pd.read_csv(path, parse_dates=["timestamp"])


def load_mapping_data(data_dir="data"):
    path = os.path.join(data_dir, "mapping_dataset.csv")
    return pd.read_csv(path, parse_dates=["timestamp"])


def load_rl_data(data_dir="data"):
    path = os.path.join(data_dir, "rl_training_dataset.csv")
    return pd.read_csv(path)
def load_all_data(data_dir="data"):
    navigation_data = load_navigation_data(data_dir)
    thermal_data = load_thermal_data(data_dir)
    environment_data = load_environment_data(data_dir)
    mapping_data = load_mapping_data(data_dir)
    rl_data = load_rl_data(data_dir)

    return {
        "navigation": navigation_data,
        "thermal": thermal_data,
        "environment": environment_data,
        "mapping": mapping_data,
        "rl": rl_data,
    }