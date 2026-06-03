import pandas as pd

from sklearn.ensemble import RandomForestRegressor

from config import (
    FORECAST_DAYS,
    MODEL_RANDOM_STATE
)


def predict_sales(df):

    df.columns = df.columns.str.strip().str.lower()

    sales_by_day = (
        df.groupby("day")["sales"]
        .sum()
        .reset_index()
    )

    X = sales_by_day[["day"]]
    y = sales_by_day["sales"]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=MODEL_RANDOM_STATE
    )

    model.fit(X, y)

    max_day = int(sales_by_day["day"].max())

    future_days = pd.DataFrame({
        "day": range(
            max_day + 1,
            max_day + FORECAST_DAYS + 1
        )
    })

    future_days["predicted_sales"] = model.predict(
        future_days
    )

    future_days["predicted_sales"] = (
        future_days["predicted_sales"]
        .clip(lower=0)
    )

    return future_days
