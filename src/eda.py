import matplotlib.pyplot as plt
import seaborn as sns
import os


def basic_info(df, name="DataFrame"):
    print(f"\n===== {name} HEAD =====")
    print(df.head())
    print(f"\n===== {name} INFO =====")
    print(df.info())
    print(f"\n===== {name} DESCRIBE =====")
    print(df.describe(include="all"))


def plot_histograms(df, cols, title_prefix, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    for col in cols:
        if col not in df.columns:
            continue
        plt.figure()
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"{title_prefix}: {col}")
        plt.xlabel(col)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{title_prefix}_{col}.png"))
        plt.close()


def plot_trajectory(mapping_df, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure()
    plt.plot(mapping_df["x_position_m"], mapping_df["y_position_m"], marker=".", linestyle="-")
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.title("Simulated Trajectory in 2D Space")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "trajectory_2d.png"))
    plt.close()
def plot_temperature_over_time(thermal_df, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure()
    plt.plot(thermal_df["timestamp"], thermal_df["temperature_c"], marker=".", linestyle="-")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.title("Temperature Over Time")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "temperature_over_time.png"))
    plt.close()
def plot_rl_rewards(rl_df, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure()
    plt.plot(rl_df["episode"], rl_df["reward"], marker=".", linestyle="-")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Reinforcement Learning Rewards Over Episodes")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "rl_rewards_over_episodes.png"))
    plt.close()
def plot_environmental_factors(environment_df, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure()
    plt.plot(environment_df["timestamp"], environment_df["humidity_percent"], marker=".", linestyle="-", label="Humidity (%)")
    plt.plot(environment_df["timestamp"], environment_df["air_quality_index"], marker=".", linestyle="-", label="Air Quality Index")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Environmental Factors Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "environmental_factors_over_time.png"))
    plt.close()
    