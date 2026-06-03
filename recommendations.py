def get_recommendations(df):

    df.columns = df.columns.str.strip().str.lower()

    dish_sales = (
        df.groupby("dish")["sales"]
        .sum()
        .reset_index()
    )

    dish_sales = dish_sales.sort_values(
        by="sales",
        ascending=False
    )

    top_dish = dish_sales.iloc[0]["dish"]

    low_dish = dish_sales.iloc[-1]["dish"]

    return {
        "top_dish": top_dish,
        "low_dish": low_dish
    }
