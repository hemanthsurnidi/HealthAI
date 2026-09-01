import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


def train_model(dataset_path, feature_columns, target_column, model_name):

    # load dataset
    data = pd.read_csv(dataset_path)

    # select features
    X = data[feature_columns]

    # target variable
    y = data[target_column]

    # split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # predictions
    y_pred = model.predict(X_test)

    # evaluation
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # create models folder
    os.makedirs("../models", exist_ok=True)

    # save model
    joblib.dump(model, f"../models/{model_name}.pkl")

    print(model_name, "saved successfully")