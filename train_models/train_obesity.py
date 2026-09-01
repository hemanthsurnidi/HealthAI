import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# load dataset
data = pd.read_csv("datasets/obesity.csv")

# convert target to binary
data["Obesity"] = data["ObesityCategory"].apply(
    lambda x: 1 if x in ["Obese", "Overweight"] else 0
)

# select features
X = data[[
    "Age",
    "Height",
    "Weight",
    "PhysicalActivityLevel"
]]

# target
y = data["Obesity"]

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
joblib.dump(model, "models/obesity_model.pkl")

print("Obesity model saved successfully")