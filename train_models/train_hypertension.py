import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import LabelEncoder

# load dataset
data = pd.read_csv("datasets/hypertension.csv")

# select features
X = data[[
    "Age",
    "BMI",
    "Smoking_Status",
    "Alcohol_Intake",
    "Physical_Activity_Level",
    "Salt_Intake",
    "Stress_Level"
]]

# encode categorical features
categorical_cols = ["Smoking_Status", "Physical_Activity_Level"]
le = LabelEncoder()
for col in categorical_cols:
    X[col] = le.fit_transform(X[col])

# target variable
y = data["Hypertension"]
y = le.fit_transform(y)  # encode target

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
joblib.dump(model, "models/hypertension_model.pkl")

print("Hypertension model saved successfully")