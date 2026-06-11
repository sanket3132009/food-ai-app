import streamlit as st
import pandas as pd
import plotly.express as px
import random

from auth import login, logout
from forecasting import predict_sales
from recommendations import get_recommendations
from config import APP_NAME


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🍽️",
    layout="wide"
)


# -------------------------
# Random Pastel Background
# -------------------------

if "bg_color" not in st.session_state:

    st.session_state.bg_color = random.choice(
        [
            "#FFF1F2",
            "#FFF7E6",
            "#EFFFF7",
            "#EEF5FF",
            "#F8F0FF",
            "#FFFBEA",
            "#F0FFF4"
        ]
    )


bg = st.session_state.bg_color


st.markdown(
f"""
<style>

.stApp {{

background-color:{bg};

background-image:

url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E

%3Cg fill='%23888888' fill-opacity='0.13'%3E

%3Ctext x='20' y='50' font-size='45'%3E🍕%3C/text%3E

%3Ctext x='150' y='70' font-size='45'%3E🍔%3C/text%3E

%3Ctext x='60' y='170' font-size='45'%3E🍜%3C/text%3E

%3Ctext x='210' y='220' font-size='45'%3E🥗%3C/text%3E

%3Ctext x='180' y='150' font-size='45'%3E🍩%3C/text%3E

%3Ctext x='20' y='260' font-size='45'%3E🍟%3C/text%3E

%3C/g%3E

%3C/svg%3E");

background-size:300px 300px;

}}



h1 {{

color:#5B5FEF;

font-weight:900;

}}



h2 {{

color:#FF6B81;

font-weight:800;

}}



h3 {{

color:#FF9F43;

}}



section[data-testid="stSidebar"] {{

background-color:#E8FFF6;

}}



.stButton button {{

background-color:#7ED6A5;

color:white;

border-radius:25px;

border:none;

padding:10px 25px;

font-weight:bold;

}}



.stButton button:hover {{

background-color:#55C88A;

}}



div[data-testid="metric-container"] {{

background:white;

padding:20px;

border-radius:20px;

box-shadow:0px 5px 15px #cccccc;

}}



.stDataFrame {{

border-radius:20px;

}}


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
## Smart restaurant demand prediction

✨ Predict sales  
✨ Find popular dishes  
✨ Reduce food waste  
✨ Plan cooking smarter

"""
)



# -------------------------
# Navigation
# -------------------------

menu = st.sidebar.radio(
    "🌈 Navigation",
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
# Upload Data
# -------------------------

if menu == "Upload Data":

    st.header("📂 Upload Restaurant Sales Data")


    file = st.file_uploader(
        "Upload CSV file",
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

    st.header("📈 Future Sales Prediction")


    if st.session_state.data is None:

        st.warning(
            "Please upload data first"
        )


    else:

        future = predict_sales(
            st.session_state.data
        )


        col1,col2,col3 = st.columns(3)


        with col1:

            st.metric(
                "Forecast Days",
                len(future)
            )


        with col2:

            st.metric(
                "Average Demand",
                int(
                    future["predicted_sales"].mean()
                )
            )


        with col3:

            st.metric(
                "Maximum Demand",
                int(
                    future["predicted_sales"].max()
                )
            )


        st.dataframe(
            future,
            use_container_width=True
        )


        graph = px.line(
            future,
            x="day",
            y="predicted_sales",
            markers=True,
            title="Upcoming Demand"
        )


        st.plotly_chart(
            graph,
            use_container_width=True
        )


        csv = future.to_csv(
            index=False
        )


        st.download_button(
            "⬇ Download Forecast",
            csv,
            "forecast.csv",
            "text/csv"
        )



# -------------------------
# Dish Insights
# -------------------------

elif menu == "Dish Insights":

    st.header("🥘 Dish Performance")


    if st.session_state.data is None:

        st.warning(
            "Please upload data first"
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


        chart = px.bar(
            dish_sales,
            x="dish",
            y="sales",
            title="Most Popular Dishes"
        )


        st.plotly_chart(
            chart,
            use_container_width=True
        )



# -------------------------
# AI Recommendations
# -------------------------

elif menu == "AI Recommendations":

    st.header("💡 AI Waste Reduction")


    if st.session_state.data is None:

        st.warning(
            "Please upload data first"
        )


    else:

        result = get_recommendations(
            st.session_state.data
        )


        st.success(
            f"⭐ Increase preparation of: {result['top_dish']}"
        )


        st.warning(
            f"⚠ Reduce production of: {result['low_dish']}"
        )


        st.info(
            """
            AI Tip:
            
            Use predicted demand to prepare food in smaller batches
            and reduce unnecessary wastage.
            """
        )
