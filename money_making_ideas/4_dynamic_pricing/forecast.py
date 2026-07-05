"""PricePilot - demand forecasting + price recommendation for small sellers.

Trains a regression model (Random Forest, from this repo's regression
coursework) on a seller's historical price/units-sold data, forecasts next
week's demand, and recommends a price that maximizes expected revenue
(price * predicted units) over a small candidate range.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


def load(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    return df


def train_per_product(df: pd.DataFrame, product: str):
    sub = df[df["product"] == product]
    features = ["price", "competitor_price", "is_holiday_season", "day_of_week", "month"]
    X = sub[features]
    y = sub["units_sold"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    mae = mean_absolute_error(y_test, model.predict(X_test))
    return model, mae, sub


def recommend_price(model, latest_row: pd.Series, price_range=None) -> dict:
    if price_range is None:
        base = latest_row["price"]
        price_range = np.round(np.arange(base * 0.8, base * 1.25, base * 0.05), 2)

    best_price, best_revenue, best_units = None, -1, 0
    for price in price_range:
        row = latest_row.copy()
        row["price"] = price
        features = ["price", "competitor_price", "is_holiday_season", "day_of_week", "month"]
        predicted_units = model.predict(row[features].to_frame().T)[0]
        revenue = price * predicted_units
        if revenue > best_revenue:
            best_price, best_revenue, best_units = price, revenue, predicted_units

    return {
        "recommended_price": round(float(best_price), 2),
        "predicted_units": round(float(best_units), 1),
        "predicted_revenue": round(float(best_revenue), 2),
    }


if __name__ == "__main__":
    df = load("sample_sales.csv")
    for product in df["product"].unique():
        model, mae, sub = train_per_product(df, product)
        latest_row = sub.sort_values("date").iloc[-1]
        rec = recommend_price(model, latest_row)
        print(f"\n=== {product} ===")
        print(f"Model MAE (units/day): {mae:.1f}")
        print(f"Current price: ${latest_row['price']:.2f}")
        print(f"Recommended price: ${rec['recommended_price']:.2f}  "
              f"-> predicted {rec['predicted_units']:.0f} units/day, "
              f"${rec['predicted_revenue']:.2f}/day revenue")
