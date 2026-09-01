import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# load dataset
data = pd.read_csv("datasets/diabetes.csv")

# select features
X = data[["Age","BMI","Glucose","BloodPressure"]]

# target variable
y = data["Outcome"]

# split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train model
model = RandomForestClassifier()

model.fit(X_train, y_train)
# predictions
y_pred = model.predict(X_test)

# accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# classification report
report = classification_report(y_test, y_pred)
print("Classification Report:")
print(report)

# save model
joblib.dump(model, "models/diabetes_model.pkl")

print("Diabetes model trained successfully")