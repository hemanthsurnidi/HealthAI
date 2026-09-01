import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# load dataset
data = pd.read_csv("datasets/stroke.csv")

# handle missing BMI values
data["bmi"].fillna(data["bmi"].mean(), inplace=True)

# convert smoking status to numeric
data["smoking_status"] = data["smoking_status"].map({
    "never smoked": 0,
    "formerly smoked": 1,
    "smokes": 2,
    "Unknown": 0
})

# select features
X = data[[
    "age",
    "hypertension",
    "heart_disease",
    "avg_glucose_level",
    "bmi",
    "smoking_status"
]]

# target
y = data["stroke"]

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
joblib.dump(model, "models/stroke_model.pkl")

print("Stroke model saved successfully")