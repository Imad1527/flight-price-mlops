from flask import Flask, request, jsonify
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from pathlib import Path

# -----------------------------
# App initialization
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Paths (Docker-safe)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = BASE_DIR / "artifacts"

# -----------------------------
# Load artifacts
# -----------------------------
model = joblib.load(ARTIFACTS_DIR / "gender_model.pkl")
pca = joblib.load(ARTIFACTS_DIR / "pca.pkl")
scaler = joblib.load(ARTIFACTS_DIR / "scaler.pkl")
label_encoder = joblib.load(ARTIFACTS_DIR / "label_encoder.pkl")
company_encoder = joblib.load(ARTIFACTS_DIR / "company_encoder.pkl")

# -----------------------------
# Load sentence transformer
# -----------------------------
text_model = SentenceTransformer(
    "flax-sentence-embeddings/all_datasets_v4_MiniLM-L6"
)

# -----------------------------
# Health check endpoint
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200

# -----------------------------
# Prediction endpoint
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or empty JSON"}), 400

    # Validate inputs
    required_fields = ["name", "company", "age", "code"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        name = str(data["name"])
        company = str(data["company"])
        age = int(data["age"])
        code = int(data["code"])
    except ValueError:
        return jsonify({"error": "Invalid data type"}), 400

    # -----------------------------
    # Feature engineering
    # -----------------------------
    # Text embedding
    name_embedding = text_model.encode(name)
    name_embedding = np.array(name_embedding).reshape(1, -1)

    # PCA transformation
    name_pca = pca.transform(name_embedding)

    # Encode company
    company_encoded = company_encoder.transform([company])[0]

    # Final feature vector
    X = np.hstack(
        (
            name_pca,
            [[code, company_encoded, age]]
        )
    )

    # Scaling
    X_scaled = scaler.transform(X)

    # Prediction
    prediction = model.predict(X_scaled)[0]
    gender = label_encoder.inverse_transform([prediction])[0]

    return jsonify({"prediction": gender})

# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

    
