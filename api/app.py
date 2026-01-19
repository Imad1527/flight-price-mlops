from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load trained pipeline
model = joblib.load("/app/models/flight_price_model.pkl")

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

        # Safety guard (tree shouldn't go negative, but production hygiene)
        prediction = max(0, round(float(prediction), 2))

        return jsonify({"predicted_price": prediction}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
