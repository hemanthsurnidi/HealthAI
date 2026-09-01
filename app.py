from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "*"}})

import os
import subprocess

# Generate models if they don't exist (e.g., on Render where they are gitignored)
if not os.path.exists("models") or not os.path.exists("models/diabetes_model.pkl"):
    print("Models not found. Generating dummy models for deployment...")
    subprocess.run(["python", "create_dummy_models.py"], check=True)

# load models
try:
    diabetes_model = joblib.load("models/diabetes_model.pkl")
    heart_model = joblib.load("models/heart_model.pkl")
    hypertension_model = joblib.load("models/hypertension_model.pkl")
    obesity_model = joblib.load("models/obesity_model.pkl")
    sleep_model = joblib.load("models/sleep_model.pkl")
    stroke_model = joblib.load("models/stroke_model.pkl")
except Exception as e:
    raise RuntimeError("Failed to load model files. Make sure models/*.pkl exist.") from e


def risk_level(score):

    if score < 30:
        return "Low"
    elif score < 60:
        return "Medium"
    else:
        return "High"


def get_reasons(age,bmi,glucose,blood_pressure,cholesterol,smoking,stress_level,sleep_hours):

    reasons = {}

    reasons["Diabetes"] = []
    if bmi > 25:
        reasons["Diabetes"].append("High BMI")
    if glucose > 140:
        reasons["Diabetes"].append("High blood sugar")
    if blood_pressure > 130:
        reasons["Diabetes"].append("High blood pressure")

    reasons["Heart Disease"] = []
    if cholesterol > 200:
        reasons["Heart Disease"].append("High cholesterol")
    if smoking == 1:
        reasons["Heart Disease"].append("Smoking habit")

    reasons["Hypertension"] = []
    if blood_pressure > 130:
        reasons["Hypertension"].append("High blood pressure")
    if stress_level >= 3:
        reasons["Hypertension"].append("High stress level")

    reasons["Obesity"] = []
    if bmi > 25:
        reasons["Obesity"].append("High BMI")

    reasons["Sleep Disorder"] = []
    if sleep_hours < 6:
        reasons["Sleep Disorder"].append("Low sleep duration")
    if stress_level >= 3:
        reasons["Sleep Disorder"].append("High stress")

    reasons["Stroke"] = []
    if blood_pressure > 130:
        reasons["Stroke"].append("High blood pressure")
    if smoking == 1:
        reasons["Stroke"].append("Smoking habit")

    return reasons


def prevention_steps():

    return [
        "Exercise at least 30 minutes daily",
        "Maintain a healthy body weight",
        "Reduce sugar and junk food intake",
        "Eat more fruits and vegetables",
        "Drink enough water daily",
        "Sleep 7–8 hours every night",
        "Reduce stress through relaxation or meditation",
        "Avoid smoking and limit alcohol consumption",
        "Monitor blood pressure and glucose regularly"
    ]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json or {}

    age = float(data.get("age", 0))
    height = float(data.get("height", 1.7))
    weight = float(data.get("weight", 85))
    bmi = float(data.get("bmi", 0) or (weight / (height * height) if height > 0 else 0))
    glucose = float(data.get("glucose", 0))
    blood_pressure = float(data.get("blood_pressure", 0))
    cholesterol = float(data.get("cholesterol", 0))
    heart_rate = float(data.get("heart_rate", 0))
    sleep_hours = float(data.get("sleep_hours", 0))
    stress_level = float(data.get("stress_level", 0))
    physical_activity = float(data.get("physical_activity", 0))
    daily_steps = float(data.get("daily_steps", 0))
    smoking = int(data.get("smoking", 0))

    model_inputs = {
        "diabetes": [[age, bmi, glucose, blood_pressure]],
        "heart": [[age, 1, blood_pressure, cholesterol, heart_rate]],
        "hypertension": [[age, bmi, smoking, 0, physical_activity, 2, stress_level]],
        "obesity": [[age, height, weight, physical_activity]],
        "sleep": [[age, sleep_hours, stress_level, physical_activity, heart_rate, daily_steps]],
        "stroke": [[age, 1, 1, glucose, bmi, smoking]],
    }

    diabetes_risk = diabetes_model.predict_proba(model_inputs["diabetes"])[0][1] * 100
    heart_risk = heart_model.predict_proba(model_inputs["heart"])[0][1] * 100
    hypertension_risk = hypertension_model.predict_proba(model_inputs["hypertension"])[0][1] * 100
    obesity_risk = obesity_model.predict_proba(model_inputs["obesity"])[0][1] * 100

    sleep_prob = sleep_model.predict_proba(model_inputs["sleep"])[0]
    sleep_risk = sleep_prob[1] * 100 if len(sleep_prob) > 1 else 0

    stroke_risk = stroke_model.predict_proba(model_inputs["stroke"])[0][1] * 100

    reasons = get_reasons(
        age, bmi, glucose, blood_pressure, cholesterol, smoking, stress_level, sleep_hours
    )

    result = {"diseases": [], "prevention": prevention_steps()}

    for name, risk, why in [
        ("Diabetes", diabetes_risk, reasons["Diabetes"]),
        ("Heart Disease", heart_risk, reasons["Heart Disease"]),
        ("Hypertension", hypertension_risk, reasons["Hypertension"]),
        ("Obesity", obesity_risk, reasons["Obesity"]),
        ("Sleep Disorder", sleep_risk, reasons["Sleep Disorder"]),
        ("Stroke", stroke_risk, reasons["Stroke"]),
    ]:
        result["diseases"].append(
            {
                "name": name,
                "risk": round(risk, 2),
                "level": risk_level(risk),
                "why": why,
            }
        )

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)