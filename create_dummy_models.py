import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

os.makedirs('models', exist_ok=True)

models = ['diabetes_model.pkl', 'heart_model.pkl', 'hypertension_model.pkl', 'obesity_model.pkl', 'sleep_model.pkl', 'stroke_model.pkl']

# Create dummy data
# We just need it to accept any number of features and output 2 classes (0 and 1)
# Actually, random forest needs the same number of features at prediction as training.
# Let's train a model for each based on their expected feature count.
# diabetes: 4 features
# heart: 5 features
# hypertension: 7 features
# obesity: 4 features
# sleep: 6 features
# stroke: 6 features

features = {
    'diabetes_model.pkl': 4,
    'heart_model.pkl': 5,
    'hypertension_model.pkl': 7,
    'obesity_model.pkl': 4,
    'sleep_model.pkl': 6,
    'stroke_model.pkl': 6
}

for model_name, n_features in features.items():
    X = np.random.rand(10, n_features)
    y = np.random.randint(0, 2, 10) # 0 or 1
    
    # ensure both classes are present
    y[0] = 0
    y[1] = 1
    
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)
    
    joblib.dump(model, os.path.join('models', model_name))

print("Valid dummy models created successfully.")
