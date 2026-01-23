from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# -------------------------------------------------
# Model path handling (LOCAL + DOCKER SAFE)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOCAL_MODEL_PATH = os.path.join(
    BASE_DIR, "..", "models", "flight_price_model.pkl"
)

DOCKER_MODEL_PATH = "/app/models/flight_price_model.pkl"

MODEL_PATH = DOCKER_MODEL_PATH if os.path.exists(DOCKER_MODEL_PATH) else LOCAL_MODEL_PATH

model = joblib.load(MODEL_PATH)

# -------------------------------------------------
# Required features (UNCHANGED)
# -------------------------------------------------
REQUIRED_FEATURES = [
    "from", "to", "flightType",
    "time", "distance", "agency",
    "day", "month", "weekday"
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        missing = [f for f in REQUIRED_FEATURES if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        df = pd.DataFrame([data], columns=REQUIRED_FEATURES)

        prediction = model.predict(df)[0]

        prediction = max(0, round(float(prediction), 2))

        return jsonify({"predicted_price": prediction}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
