import streamlit as st

USERS = {
    "admin": "admin123",
    "manager": "food123"
}


def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in USERS and USERS[username] == password:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid credentials")

    return False


def logout():

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()
