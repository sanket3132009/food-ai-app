import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def predict_sales(df):

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )


    # Total daily sales
    daily = (
        df.groupby("day")["sales"]
        .sum()
        .reset_index()
    )


    # Add useful features

    daily["day_of_week"] = (
        daily["day"] % 7
    )


    daily["weekend"] = (
        daily["day_of_week"]
        .isin([5,6])
        .astype(int)
    )


    X = daily[
        [
            "day",
            "day_of_week",
            "weekend"
        ]
    ]

    y = daily["sales"]


    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )


    model.fit(X,y)


    last_day = int(
        daily["day"].max()
    )


    future = pd.DataFrame(
        {
            "day":range(
                last_day+1,
                last_day+8
            )
        }
    )


    future["day_of_week"] = (
        future["day"] % 7
    )


    future["weekend"] = (
        future["day_of_week"]
        .isin([5,6])
        .astype(int)
    )


    future["predicted_sales"] = (
        model.predict(
            future[
                [
                    "day",
                    "day_of_week",
                    "weekend"
                ]
            ]
        )
    )


    return future
