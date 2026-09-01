import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# load dataset
data = pd.read_csv("datasets/sleep.csv")

# convert target to binary
data["SleepRisk"] = data["Sleep Disorder"].apply(
    lambda x: 0 if x == "None" else 1
)

# select features
X = data[[
    "Age",
    "Sleep Duration",
    "Stress Level",
    "Physical Activity Level",
    "Heart Rate",
    "Daily Steps"
]]

# target
y = data["SleepRisk"]

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
os.makedirs("models", exist_ok=True)

# save model
joblib.dump(model, "models/sleep_model.pkl")

print("Sleep disorder model saved successfully")