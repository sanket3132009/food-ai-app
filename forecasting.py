import pandas as pd
from prophet import Prophet


def predict_sales(df):

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )


    # Combine all dishes into daily total sales

    daily_sales = (
        df.groupby("day")["sales"]
        .sum()
        .reset_index()
    )


    # Create dates

    start_date = pd.Timestamp("2025-01-01")

    daily_sales["date"] = (
        start_date +
        pd.to_timedelta(
            daily_sales["day"] - 1,
            unit="D"
        )
    )


    prophet_df = daily_sales[
        ["date", "sales"]
    ]


    prophet_df.columns = [
        "ds",
        "y"
    ]


    # Prophet model

    model = Prophet(
        weekly_seasonality=True,
        yearly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.2
    )


    model.fit(prophet_df)


    # Predict next 30 days

    future_dates = model.make_future_dataframe(
        periods=30,
        freq="D"
    )


    forecast = model.predict(
        future_dates
    )


    prediction = forecast[
        forecast["ds"] > prophet_df["ds"].max()
    ][
        ["ds", "yhat"]
    ]


    prediction.columns = [
        "date",
        "predicted_sales"
    ]


    prediction["predicted_sales"] = (
        prediction["predicted_sales"]
        .round()
        .astype(int)
    )


    # Keep compatibility with old app.py

    prediction["day"] = range(
        int(df["day"].max()) + 1,
        int(df["day"].max()) + 31
    )


    return prediction[
        [
            "day",
            "predicted_sales",
            "date"
        ]
    ]
