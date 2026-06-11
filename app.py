import streamlit as st
import pandas as pd
import plotly.express as px
import random

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


# -------------------------
# Different pastel per page
# -------------------------

page_colors = {

    "Upload Data": "#FFF1F5",

    "Predict Sales": "#EEF7FF",

    "Dish Insights": "#F3FFF0",

    "AI Recommendations": "#FFF8E7"

}


bg_color = page_colors[menu]


# -------------------------
# Background + doodles
# -------------------------

st.markdown(
f"""
<style>

.stApp {{

background-color:{bg_color};

background-image:

url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E

%3Cg fill='none' stroke='%23777777' stroke-width='3' opacity='0.18'%3E


%3Ccircle cx='55' cy='55' r='25'/%3E
%3Cpath d='M30 55h50 M55 30v50'/%3E


%3Crect x='170' y='40' width='55' height='35' rx='10'/%3E
%3Cpath d='M180 40v-15 M195 40v-15 M210 40v-15'/%3E


%3Ccircle cx='80' cy='190' r='30'/%3E
%3Cpath d='M55 190h50'/%3E


%3Cpath d='M180 210 Q220 160 260 210 Q220 260 180 210'/%3E


%3Cpath d='M20 260 C70 220 120 300 170 260'/%3E


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



section[data-testid="stSidebar"] {{

background-color:#E8FFF6;

}}



.stButton button {{

background:#7ED6A5;

color:white;

border-radius:25px;

border:none;

padding:10px 25px;

font-weight:bold;

}}



.stButton button:hover {{

background:#55C88A;

}}



div[data-testid="metric-container"] {{

background:white;

border-radius:20px;

padding:18px;

box-shadow:0px 5px 15px #cccccc;

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

st.write(
"✨ Predict demand • Reduce waste • Cook smarter"
)



if "data" not in st.session_state:

    st.session_state.data = None



# -------------------------
# Upload Page
# -------------------------

if menu == "Upload Data":


    st.header("📂 Upload Restaurant Sales Data")


    file = st.file_uploader(
        "Upload CSV",
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
            "🎉 Data uploaded successfully"
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
            "Upload data first"
        )

    else:

        future = predict_sales(
            st.session_state.data
        )


        c1,c2,c3 = st.columns(3)


        c1.metric(
            "Forecast Days",
            len(future)
        )


        c2.metric(
            "Average Demand",
            int(
                future["predicted_sales"].mean()
            )
        )


        c3.metric(
            "Maximum Demand",
            int(
                future["predicted_sales"].max()
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
            markers=True
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



# -------------------------
# Dish Insights
# -------------------------

elif menu == "Dish Insights":


    st.header("🥘 Dish Insights")


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
            y="sales"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



# -------------------------
# Recommendations
# -------------------------

elif menu == "AI Recommendations":


    st.header("💡 AI Recommendations")


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
            f"⚠ Reduce: {result['low_dish']}"
        )


        st.info(
            "AI tip: Use forecasts to prepare food in smaller batches."
        )
