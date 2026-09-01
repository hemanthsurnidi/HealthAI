import json, urllib.request

url = "http://127.0.0.1:5000/predict"
payload = {
    "age": 45,
    "height": 1.7,
    "weight": 85,
    "bmi": 29.4,
    "glucose": 160,
    "blood_pressure": 140,
    "cholesterol": 220,
    "heart_rate": 85,
    "sleep_hours": 5,
    "stress_level": 3,
    "physical_activity": 3,
    "daily_steps": 4000,
    "smoking": 0,
}
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)
res = urllib.request.urlopen(req, timeout=10)
print(res.read().decode())
