"""StayWise - customer churn predictor for subscription businesses.

Trains a Random Forest classifier (same model used in this repo's
Machine_Learning_A-Z course) on a business's customer table and ranks
customers by churn risk so the business can target retention offers at
exactly the accounts about to leave.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder


def load_and_prepare(csv_path: str):
    df = pd.read_csv(csv_path)
    df = df.copy()
    encoders = {}
    for col in df.select_dtypes(include="object").columns:
        if col == "customer_id":
            continue
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
    return df, encoders


def train(csv_path: str):
    df, _ = load_and_prepare(csv_path)
    feature_cols = [c for c in df.columns if c not in ("customer_id", "churned")]
    X = df[feature_cols]
    y = df["churned"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

    df["churn_risk"] = model.predict_proba(X)[:, 1]
    at_risk = df.sort_values("churn_risk", ascending=False)[
        ["customer_id", "churn_risk", "tenure_months", "monthly_spend", "support_tickets"]
    ]
    return model, auc, at_risk, feature_cols


if __name__ == "__main__":
    model, auc, at_risk, feature_cols = train("sample_customers.csv")
    print(f"Model AUC on held-out customers: {auc:.3f}")
    print("\nTop 10 customers most likely to churn this month:")
    print(at_risk.head(10).to_string(index=False))

    importances = sorted(
        zip(feature_cols, model.feature_importances_),
        key=lambda x: -x[1],
    )
    print("\nTop churn drivers:")
    for name, imp in importances:
        print(f"  {name}: {imp:.2f}")
