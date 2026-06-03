import streamlit as st
import pandas as pd
import plotly.express as px

from auth import login, logout

from forecasting import predict_sales

from recommendations import get_recommendations

from config import APP_NAME


st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)

if not login():
    st.stop()

logout()

st.title("🍽️ AI Food Supply Prediction")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Upload Data",
        "Predict Sales",
        "Dish Insights",
        "AI Recommendations"
    ]
)

if "data" not in st.session_state:
    st.session_state.data = None

# -----------------------------------
# Upload Page
# -----------------------------------

if menu == "Upload Data":

    st.header("Upload CSV")

    file = st.file_uploader(
        "Upload Sales Data",
        type=["csv"]
    )

    if file:

        df = pd.read_csv(file)

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
        )

        st.session_state.data = df

        st.success("Data uploaded")

        st.dataframe(df.head())

# -----------------------------------
# Prediction Page
# -----------------------------------

elif menu == "Predict Sales":

    if st.session_state.data is None:

        st.error("Upload data first")

    else:

        future = predict_sales(
            st.session_state.data
        )

        st.subheader(
            "7 Day Forecast"
        )

        st.dataframe(future)

        fig = px.line(
            future,
            x="day",
            y="predicted_sales",
            title="Future Sales"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        csv = future.to_csv(
            index=False
        )

        st.download_button(
            "Download Forecast",
            csv,
            "forecast.csv",
            "text/csv"
        )

# -----------------------------------
# Dish Insights
# -----------------------------------

elif menu == "Dish Insights":

    if st.session_state.data is None:

        st.error("Upload data first")

    else:

        df = st.session_state.data

        dish_sales = (
            df.groupby("dish")["sales"]
            .sum()
            .reset_index()
        )

        dish_sales = dish_sales.sort_values(
            by="sales",
            ascending=False
        )

        st.dataframe(dish_sales)

        fig = px.bar(
            dish_sales,
            x="dish",
            y="sales",
            title="Dish Popularity"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# -----------------------------------
# Recommendations
# -----------------------------------

elif menu == "AI Recommendations":

    if st.session_state.data is None:

        st.error("Upload data first")

    else:

        rec = get_recommendations(
            st.session_state.data
        )

        st.success(
            f"Prepare more: {rec['top_dish']}"
        )

        st.warning(
            f"Reduce production: {rec['low_dish']}"
        )

        st.info(
            "Use forecasting to reduce waste and improve inventory planning."
        )
