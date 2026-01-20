import pandas as pd
import numpy as np
import joblib
import mlflow
import mlflow.sklearn

from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "users.csv"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

ARTIFACTS_DIR.mkdir(exist_ok=True)

# -----------------------------
# MLflow setup
# -----------------------------
mlflow.set_experiment("Gender Classification")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_PATH)

# Keep only valid classes
df = df[df["gender"].isin(["male", "female"])]

# Encode target
label_encoder = LabelEncoder()
df["gender_encoded"] = label_encoder.fit_transform(df["gender"])

# -----------------------------
# Text embeddings
# -----------------------------
text_model = SentenceTransformer("flax-sentence-embeddings/all_datasets_v4_MiniLM-L6")
name_embeddings = df["name"].apply(lambda x: text_model.encode(x)).tolist()

# -----------------------------
# PCA on embeddings
# -----------------------------
pca = PCA(n_components=23)
name_pca = pca.fit_transform(name_embeddings)

# -----------------------------
# Encode categorical feature
# -----------------------------
company_encoder = LabelEncoder()
df["company_encoded"] = company_encoder.fit_transform(df["company"])

# -----------------------------
# Feature matrix
# -----------------------------
X_numeric = df[["code", "company_encoded", "age"]].values
X = np.hstack((name_pca, X_numeric))
y = df["gender_encoded"].values

# -----------------------------
# Scaling
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# Train / Test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# Model
# -----------------------------
model = LogisticRegression(max_iter=1000)

with mlflow.start_run():
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # -----------------------------
    # Logging
    # -----------------------------
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "gender_classifier")

    # -----------------------------
    # Save artifacts
    # -----------------------------
    joblib.dump(model, ARTIFACTS_DIR / "gender_model.pkl")
    joblib.dump(pca, ARTIFACTS_DIR / "pca.pkl")
    joblib.dump(scaler, ARTIFACTS_DIR / "scaler.pkl")
    joblib.dump(label_encoder, ARTIFACTS_DIR / "label_encoder.pkl")
    joblib.dump(company_encoder, ARTIFACTS_DIR / "company_encoder.pkl")

    print("Training complete")
    print(f"Accuracy: {acc:.4f}")
