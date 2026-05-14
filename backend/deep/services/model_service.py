import os
import joblib
import pandas as pd
import numpy as np

# Paths for model loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model.pkl")

class ModelService:
    # Service for loading and using the deep analysis ML model
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.label_map = {
            0: "Below Average",
            1: "Average",
            2: "Above Average",
        }

        self.raw_feature_names = [
            "Offer Price",
            "Issue_Size(crores)",
            "QIB",
            "HNI",
            "RII",
        ]

        self.transformed_feature_names = [
            "Issue_Size(crores)_log_transformed",
            "Offer Price_log_transformed",
            "QIB_log_transformed",
            "HNI_log_transformed",
            "RII_log_transformed",
        ]

    def get_features(self):
        return self.raw_feature_names

    def predict(self, input_dict: dict):
        # Apply log transformation to features
        transformed = {
            f"{k}_log_transformed": np.log1p(v)
            for k, v in input_dict.items()
        }

        df = pd.DataFrame([transformed])[self.transformed_feature_names]

        prediction = self.model.predict(df)[0]
        probabilities = self.model.predict_proba(df)[0]

        return {
            "prediction": int(prediction),
            "label": self.label_map[int(prediction)],
            "probabilities": {
                "Below Average": round(float(probabilities[0]), 4),
                "Average": round(float(probabilities[1]), 4),
                "Above Average": round(float(probabilities[2]), 4),
            },
        }