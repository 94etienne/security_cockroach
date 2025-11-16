import os
import joblib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier


def train_navigation_model(df, output_dir="outputs"):

    os.makedirs(output_dir, exist_ok=True)

    feature_cols = [
        "accel_x","accel_y","accel_z",
        "gyro_x","gyro_y","gyro_z",
        "obstacle_distance_cm","speed_cm_per_s"
    ]

    X = df[feature_cols]
    y = df["direction_label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    clf = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(n_estimators=200, random_state=42))
    ])

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print("\n=== Navigation Model Report ===")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d",
                xticklabels=clf.classes_,
                yticklabels=clf.classes_,
                cmap="Blues")
    plt.title("Navigation Confusion Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "navigation_confusion_matrix.png"))
    plt.close()

    return clf
