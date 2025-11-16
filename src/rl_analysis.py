import pandas as pd


def analyze_rl_logs(rl_df: pd.DataFrame):
    print("\n=== RL Logs: Overall Stats ===")
    print(rl_df.describe(include="all"))

    # Average reward by action
    print("\nAverage reward by action:")
    print(rl_df.groupby("action_taken")["reward"].mean())

    # Collision rate
    collision_rate = rl_df["collision"].mean()
    print(f"\nCollision rate: {collision_rate:.3f}")

    # Goal reached rate
    goal_rate = rl_df["goal_reached"].mean()
    print(f"Goal reached rate: {goal_rate:.3f}")

    # Reward per episode
    reward_per_episode = rl_df.groupby("episode")["reward"].mean()
    print("\nAverage reward per episode (first 10 episodes):")
    print(reward_per_episode.head(10))
    return reward_per_episode