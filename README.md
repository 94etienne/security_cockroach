# AI for Confined-Space Search & Rescue (Synthetic Dataset)

This project uses fully synthetic sensor datasets to simulate an AI system that assists
navigation and sensing in confined or hazardous environments (e.g., collapsed buildings,
vents, rubble). The "platform" is an abstract small mobile agent equipped with:

- IMU sensors (acceleration, gyroscope)
- Distance sensor
- Thermal sensor
- Environmental sensors (gas, humidity, sound, dust)
- Mapping/SLAM-like position estimates
- Reinforcement-learning logs for navigation actions

> ⚠️ This project is purely educational and research-oriented.
> It **does NOT** provide any instructions for real-world surveillance, weapons,
> or invasive deployment. All data are synthetic.

## Datasets

All CSV files are synthetic and located in `data/`:

- `navigation_dataset.csv`  
  IMU + obstacle distance + speed + direction labels.
- `thermal_dataset.csv`  
  Ambient/surface/infrared temperature + heat-detection flag.
- `environment_dataset.csv`  
  Gas, humidity, sound, vibration, dust density.
- `mapping_dataset.csv`  
  2D positions, zones, mapping confidence.
- `rl_training_dataset.csv`  
  State, episode, action, reward, collision, goal flags.

## Goals

1. Perform exploratory data analysis (EDA) on all sensor streams.
2. Train a classifier to predict **direction_label** from navigation sensor data.
3. Train a classifier to predict **human_heat_detected** from thermal data.
4. Analyze simple reinforcement-learning logs: average reward, collisions, goals.
5. Visualize a simple "trajectory map" from mapping data.

## How to Run

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
