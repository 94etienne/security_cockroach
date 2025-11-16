# train_models.py

import pandas as pd
import joblib
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

os.makedirs("outputs", exist_ok=True)
os.makedirs("models", exist_ok=True)

def train_navigation_model(df):
    features = [
        "accel_x","accel_y","accel_z",
        "gyro_x","gyro_y","gyro_z",
        "obstacle_distance_cm","speed_cm_per_s"
    ]

    X = df[features]
    y = df["direction_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(n_estimators=200, random_state=42))
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("=== Navigation Model Results ===")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d",
                xticklabels=model.classes_,
                yticklabels=model.classes_,
                cmap="Blues")
    plt.tight_layout()
    plt.savefig("outputs/navigation_confusion_matrix.png")
    plt.close()

    joblib.dump(model, "models/navigation_model.joblib")
    print("Navigation model saved.")


def train_thermal_model(df):
    X = df[["ambient_temp_c","surface_temp_c","infrared_temp_c"]]
    y = df["human_heat_detected"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("logreg", LogisticRegression(max_iter=1000))
    ])

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]

    print("\n=== Thermal Model Results ===")
    print(classification_report(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))

    joblib.dump(model, "models/thermal_model.joblib")
    print("Thermal model saved.")


def run_training():
    print("Loading datasets...")
    nav_df = pd.read_csv("data/navigation_dataset.csv")
    thermal_df = pd.read_csv("data/thermal_dataset.csv")

    print("\nTraining navigation model...")
    train_navigation_model(nav_df)

    print("\nTraining thermal model...")
    train_thermal_model(thermal_df)

    print("\n✔ All models trained successfully!")


if __name__ == "__main__":
    run_training()
