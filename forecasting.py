import pandas as pd
from prophet import Prophet


def predict_sales(df):

    df = df.copy()

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )


    # Convert day-wise sales into daily totals

    daily_sales = (
        df.groupby("day")["sales"]
        .sum()
        .reset_index()
    )


    # Prophet needs:
    # ds = date
    # y = value


    start_date = pd.Timestamp("2025-01-01")


    daily_sales["ds"] = (
        start_date +
        pd.to_timedelta(
            daily_sales["day"] - 1,
            unit="D"
        )
    )


    prophet_data = daily_sales[
        ["ds","sales"]
    ]


    prophet_data.columns = [
        "ds",
        "y"
    ]


    # Create model

    model = Prophet(

        yearly_seasonality=True,

        weekly_seasonality=True,

        daily_seasonality=False,

        changepoint_prior_scale=0.15

    )


    model.fit(prophet_data)



    # Future 30 days

    future = model.make_future_dataframe(
        periods=30,
        freq="D"
    )


    forecast = model.predict(future)



    # Only future predictions

    result = forecast[
        forecast["ds"] >
        prophet_data["ds"].max()
    ][
        [
            "ds",
            "yhat"
        ]
    ]


    result.columns = [
        "date",
        "predicted_sales"
    ]


    result["predicted_sales"] = (
        result["predicted_sales"]
        .round()
        .astype(int)
    )


    return result
