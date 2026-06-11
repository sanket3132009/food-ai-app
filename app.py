import streamlit as st
import pandas as pd
import plotly.express as px

from auth import login, logout
from forecasting import predict_sales
from recommendations import get_recommendations
from config import APP_NAME


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🍽️",
    layout="wide"
)


# -------------------------
# Pastel Theme
# -------------------------

st.markdown(
"""
<style>

body {
    background-color: #FFF8F0;
}

.stApp {
    background-color: #FFF8F0;
}


/* Main title */

h1 {
    color: #5B5FEF;
    font-family: Arial;
    font-weight: 800;
}


/* Headers */

h2, h3 {
    color: #FF7A8A;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #E8F8F5;
}


/* Buttons */

.stButton button {

    background-color: #7ED6A5;
    color: white;

    border-radius: 20px;
    border: none;

    font-weight: bold;

    padding: 10px 25px;
}


.stButton button:hover {

    background-color: #5CC98B;

}


/* Cards */

div[data-testid="metric-container"] {

    background-color: #FFFFFF;

    border-radius: 20px;

    padding: 15px;

    box-shadow: 0px 4px 12px #dddddd;

}


</style>
""",
unsafe_allow_html=True
)


# -------------------------
# Login
# -------------------------

if not login():
    st.stop()


logout()


# -------------------------
# Title
# -------------------------

st.title("🍽️ Food AI Assistant")

st.markdown(
"""
### Smart demand prediction for restaurants
Predict sales • Reduce waste • Improve planning 🚀
"""
)


menu = st.sidebar.radio(
    "🌈 Menu",
    [
        "Upload Data",
        "Predict Sales",
        "Dish Insights",
        "AI Recommendations"
    ]
)


if "data" not in st.session_state:
    st.session_state.data = None



# -------------------------
# Upload
# -------------------------

if menu == "Upload Data":

    st.header("📂 Upload Restaurant Data")

    file = st.file_uploader(
        "Choose CSV file",
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


        st.success(
            "🎉 Data uploaded successfully!"
        )


        st.dataframe(
            df,
            use_container_width=True
        )



# -------------------------
# Prediction
# -------------------------

elif menu == "Predict Sales":


    st.header("📈 Future Demand Prediction")


    if st.session_state.data is None:

        st.warning(
            "Upload data first"
        )

    else:


        future = predict_sales(
            st.session_state.data
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Predicted Days",
                len(future)
            )


        with col2:

            st.metric(
                "Average Demand",
                int(
                    future["predicted_sales"]
                    .mean()
                )
            )



        st.dataframe(
            future,
            use_container_width=True
        )


        fig = px.line(
            future,
            x="day",
            y="predicted_sales",
            markers=True,
            title="Upcoming Sales"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



# -------------------------
# Dish Insights
# -------------------------

elif menu == "Dish Insights":


    st.header(
        "🥘 Dish Performance"
    )


    if st.session_state.data is None:

        st.warning(
            "Upload data first"
        )

    else:


        df = st.session_state.data


        dish_sales = (
            df.groupby("dish")["sales"]
            .sum()
            .reset_index()
            .sort_values(
                "sales",
                ascending=False
            )
        )


        st.dataframe(
            dish_sales,
            use_container_width=True
        )


        fig = px.bar(
            dish_sales,
            x="dish",
            y="sales",
            title="Most Loved Dishes"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



# -------------------------
# Recommendations
# -------------------------

elif menu == "AI Recommendations":


    st.header(
        "💡 Smart Suggestions"
    )


    if st.session_state.data is None:

        st.warning(
            "Upload data first"
        )


    else:


        result = get_recommendations(
            st.session_state.data
        )


        st.success(
            f"⭐ Prepare more: {result['top_dish']}"
        )


        st.warning(
            f"⚠ Reduce production: {result['low_dish']}"
        )


        st.info(
            "AI tip: Cook in smaller batches to reduce wastage."
        )
