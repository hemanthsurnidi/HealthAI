import joblib

# load models
diabetes_model = joblib.load("models/diabetes_model.pkl")
heart_model = joblib.load("models/heart_model.pkl")
hypertension_model = joblib.load("models/hypertension_model.pkl")
obesity_model = joblib.load("models/obesity_model.pkl")
sleep_model = joblib.load("models/sleep_model.pkl")
stroke_model = joblib.load("models/stroke_model.pkl")


# example user inputs
age = 45
bmi = 30
glucose = 160
blood_pressure = 140
cholesterol = 220
heart_rate = 85
sleep_hours = 5
stress_level = 3
physical_activity = 1
daily_steps = 4000
smoking = 1


# prepare inputs
diabetes_input = [[age, bmi, glucose, blood_pressure]]
heart_input = [[age, 1, blood_pressure, cholesterol, heart_rate]]
hypertension_input = [[age, bmi, smoking, 0, physical_activity, 2, stress_level]]
obesity_input = [[age, 1.70, 85, physical_activity]]
sleep_input = [[age, sleep_hours, stress_level, physical_activity, heart_rate, daily_steps]]
stroke_input = [[age, 1, 1, glucose, bmi, smoking]]


# predictions
diabetes_risk = diabetes_model.predict_proba(diabetes_input)[0][1] * 100
heart_risk = heart_model.predict_proba(heart_input)[0][1] * 100
hypertension_risk = hypertension_model.predict_proba(hypertension_input)[0][1] * 100
obesity_risk = obesity_model.predict_proba(obesity_input)[0][1] * 100

sleep_prob = sleep_model.predict_proba(sleep_input)[0]
sleep_risk = sleep_prob[1] * 100 if len(sleep_prob) > 1 else 0

stroke_risk = stroke_model.predict_proba(stroke_input)[0][1] * 100


# risk level
def risk_level(score):

    if score < 30:
        return "Low"

    elif score < 60:
        return "Medium"

    else:
        return "High"


# function to generate reasons
def get_reasons():

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
    if physical_activity == 0:
        reasons["Heart Disease"].append("Low physical activity")

    reasons["Hypertension"] = []
    if blood_pressure > 130:
        reasons["Hypertension"].append("High blood pressure")
    if stress_level >= 3:
        reasons["Hypertension"].append("High stress level")
    if bmi > 25:
        reasons["Hypertension"].append("High BMI")

    reasons["Obesity"] = []
    if bmi > 25:
        reasons["Obesity"].append("High BMI")
    if physical_activity == 0:
        reasons["Obesity"].append("Low physical activity")

    reasons["Sleep Disorder"] = []
    if sleep_hours < 6:
        reasons["Sleep Disorder"].append("Low sleep duration")
    if stress_level >= 3:
        reasons["Sleep Disorder"].append("High stress level")

    reasons["Stroke"] = []
    if blood_pressure > 130:
        reasons["Stroke"].append("High blood pressure")
    if smoking == 1:
        reasons["Stroke"].append("Smoking habit")
    if glucose > 140:
        reasons["Stroke"].append("High blood sugar")

    return reasons


reasons = get_reasons()


# print report
print("\nHEALTH RISK REPORT\n")

print("Diabetes:", round(diabetes_risk,2), "% -", risk_level(diabetes_risk))
print("Why:")
for r in reasons["Diabetes"]:
    print("•", r)

print()

print("Heart Disease:", round(heart_risk,2), "% -", risk_level(heart_risk))
print("Why:")
for r in reasons["Heart Disease"]:
    print("•", r)

print()

print("Hypertension:", round(hypertension_risk,2), "% -", risk_level(hypertension_risk))
print("Why:")
for r in reasons["Hypertension"]:
    print("•", r)

print()

print("Obesity:", round(obesity_risk,2), "% -", risk_level(obesity_risk))
print("Why:")
for r in reasons["Obesity"]:
    print("•", r)

print()

print("Sleep Disorder:", round(sleep_risk,2), "% -", risk_level(sleep_risk))
print("Why:")
for r in reasons["Sleep Disorder"]:
    print("•", r)

print()

print("Stroke Risk:", round(stroke_risk,2), "% -", risk_level(stroke_risk))
print("Why:")
for r in reasons["Stroke"]:
    print("•", r)