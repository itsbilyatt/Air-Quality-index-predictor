import streamlit as st
from datetime import datetime


def funny_welcome():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Welcome Guest,Good morning, sunshine! 🌞"
    elif 12 <= current_hour < 18:
        return "Welcome Guest,Good afternoon! Time for a snack break? 🍪"
    else:
        return "Welcome Guest,Good evening! 🌙"


st.title(
    funny_welcome()
)

st.title(
    "**Air quality Index prediction**"
)

st.markdown(
    "**About Project:** To do data analysis on India Air Quality data and predict tha value of Air Quality Index "
    "based on given features of concentration of sulphur dioxide,nitrogen dioxide, respirable suspended particualte "
    "matter, suspended particulate matter and classify the Air Quality as good, moderate, poor, unhealthy, healthy."
)

start_button = st.button(
    "Click here to predict Air quality"
)

if start_button:

    try:

        st.page_link(
            st.page_link(r'pages\main_page.py', label="Main Page", icon="🌎")
        )
    except:
        st.markdown(
            "        "
        )


# Example usage:
