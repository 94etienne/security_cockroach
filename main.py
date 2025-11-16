import os
import joblib

from src.data_loading import (
    load_navigation_data,
    load_thermal_data,
    load_environment_data,
    load_mapping_data,
    load_rl_data
)
from src.eda import basic_info, plot_histograms, plot_trajectory
from src.navigation_model import train_navigation_model
from src.thermal_model import train_thermal_model
from src.rl_analysis import analyze_rl_logs


def main():
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("models", exist_ok=True)

    # Load datasets
    nav_df = load_navigation_data()
    thermal_df = load_thermal_data()
    env_df = load_environment_data()
    mapping_df = load_mapping_data()
    rl_df = load_rl_data()

    # EDA
    basic_info(nav_df, "Navigation Data")
    basic_info(thermal_df, "Thermal Data")
    basic_info(env_df, "Environment Data")
    basic_info(mapping_df, "Mapping Data")
    basic_info(rl_df, "RL Training Data")

    plot_histograms(nav_df, ["obstacle_distance_cm","speed_cm_per_s"], "nav")
    plot_histograms(thermal_df, ["ambient_temp_c","infrared_temp_c"], "thermal")
    plot_histograms(env_df, ["gas_level_ppm","humidity_percent"], "env")

    plot_trajectory(mapping_df)

    # Train navigation model
    nav_model = train_navigation_model(nav_df, output_dir="outputs")
    joblib.dump(nav_model, "models/navigation_model.joblib")

    # Train thermal model
    thermal_model = train_thermal_model(thermal_df, output_dir="outputs")
    joblib.dump(thermal_model, "models/thermal_model.joblib")

    # RL Logs
    analyze_rl_logs(rl_df)

    print("\n✔ All tasks completed!")


if __name__ == "__main__":
    main()
