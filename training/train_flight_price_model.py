
### 📌 Paste This Code (READ CAREFULLY — THIS IS IMPORTANT)
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# 1. Load dataset
data = pd.read_csv("flights.csv")
# --- Date feature engineering ---
data["date"] = pd.to_datetime(data["date"])

data["day"] = data["date"].dt.day
data["month"] = data["date"].dt.month
data["weekday"] = data["date"].dt.weekday

# Drop raw date column
data.drop(columns=["date"], inplace=True)


# 2. Separate features and target
X = data.drop(
    columns=["price", "travelCode", "userCode"],
    axis=1
)

y = data["price"]

# 3. Identify column types
categorical_cols = X.select_dtypes(include=["object"]).columns
numerical_cols = X.select_dtypes(exclude=["object"]).columns

# 4. Preprocessing pipelines
categorical_pipeline = OneHotEncoder(handle_unknown="ignore")
numerical_pipeline = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", categorical_pipeline, categorical_cols),
        ("num", numerical_pipeline, numerical_cols)
    ]
)

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Models to evaluate
models = {
    "LinearRegression": LinearRegression(),
    "DecisionTree": DecisionTreeRegressor(max_depth=10, random_state=42)
}

results = {}

# 7. Train & evaluate
for name, model in models.items():
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)

    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))

    results[name] = {
        "model": pipeline,
        "r2": r2,
        "mae": mae,
        "rmse": rmse
    }

    print(f"{name} -> R2: {r2:.3f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}")

# 8. Select best model
best_model_name = "DecisionTree"
best_model = results[best_model_name]["model"]

# 9. Save best model
joblib.dump(best_model, "models/flight_price_model.pkl")

print(f"\nBest Model: {best_model_name}")
print("Model saved to models/flight_price_model.pkl")
