import streamlit as st
import pickle
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

# start_button = st.button(
#     "Click here to predict Air quality"
# )

# if start_button:
#
try:

    st.title(
        "AIR QUALITY INDEX Prediction"
    )
    st.markdown("[Read About AQI](https://en.wikipedia.org/wiki/Air_quality_index)")
    st.markdown(
        "**Predict Air quality on the basis of:** ")
    st.markdown(
        "[so2 (sulphur dioxide concentration)](https://en.wikipedia.org/wiki/Sulfur_dioxide)")
    st.markdown(
        "[**no2 (nitrogen dioxide concentration)**](https://en.wikipedia.org/wiki/Nitrogen_dioxide)")
    st.markdown(
        "[**rspm (respirable suspended particualte matter concentration):**](https://en.wikipedia.org/wiki/Particulates) ")
    st.markdown(
        "[**spm (suspended particulate matter** ](https://en.wikipedia.org/wiki/Particulates)")

    st.header(
        'To predict AQI Please give require input values', divider="rainbow"

    )

    # ask user for input
    # so2
    so2_input = st.number_input("**Please Enter SO2 vaule**")


    def calculate_si(so2):
        si = 0
        if (so2 <= 40):
            si = so2 * (50 / 40)
        if (so2 > 40 and so2 <= 80):
            si = 50 + (so2 - 40) * (50 / 40)
        if (so2 > 80 and so2 <= 380):
            si = 100 + (so2 - 80) * (100 / 300)
        if (so2 > 380 and so2 <= 800):
            si = 200 + (so2 - 380) * (100 / 800)
        if (so2 > 800 and so2 <= 1600):
            si = 300 + (so2 - 800) * (100 / 800)
        if (so2 > 1600):
            si = 400 + (so2 - 1600) * (100 / 800)
        return si


    soi = calculate_si(so2_input)

    no2_input = st.number_input("**Please Enter NO2 vaule**")


    def calculate_ni(no2):
        ni = 0
        if (no2 <= 40):
            ni = no2 * 50 / 40
        elif (no2 > 40 and no2 <= 80):
            ni = 50 + (no2 - 14) * (50 / 40)
        elif (no2 > 80 and no2 <= 180):
            ni = 100 + (no2 - 80) * (100 / 100)
        elif (no2 > 180 and no2 <= 280):
            ni = 200 + (no2 - 180) * (100 / 100)
        elif (no2 > 280 and no2 <= 400):
            ni = 300 + (no2 - 280) * (100 / 120)
        else:
            ni = 400 + (no2 - 400) * (100 / 120)
        return ni


    ni = calculate_ni(no2_input)

    rspm_input = st.number_input("**Please Enter rspm vaule**")


    def calculate_(rspm):
        rpi = 0
        if (rpi <= 30):
            rpi = rpi * 50 / 30
        elif (rpi > 30 and rpi <= 60):
            rpi = 50 + (rpi - 30) * 50 / 30
        elif (rpi > 60 and rpi <= 90):
            rpi = 100 + (rpi - 60) * 100 / 30
        elif (rpi > 90 and rpi <= 120):
            rpi = 200 + (rpi - 90) * 100 / 30
        elif (rpi > 120 and rpi <= 250):
            rpi = 300 + (rpi - 120) * (100 / 130)
        else:
            rpi = 400 + (rpi - 250) * (100 / 130)
        return rpi


    rpi = calculate_(rspm_input)

    spm_input = st.number_input("**Please Enter spm vaule**")


    def calculate_spi(spm):
        spi = 0
        if (spm <= 50):
            spi = spm
        if (spm < 50 and spm <= 100):
            spi = spm
        elif (spm > 100 and spm <= 250):
            spi = 100 + (spm - 100) * (100 / 150)
        elif (spm > 250 and spm <= 350):
            spi = 200 + (spm - 250)
        elif (spm > 350 and spm <= 450):
            spi = 300 + (spm - 350) * (100 / 80)
        else:
            spi = 400 + (spm - 430) * (100 / 80)
        return spi


    spi = calculate_spi(spm_input)


    def calculate_aqi(si, ni, spi, rpi):
        aqi = 0
        if (si > ni and si > spi and si > rpi):
            aqi = si
        if (spi > si and spi > ni and spi > rpi):
            aqi = spi
        if (ni > si and ni > spi and ni > rpi):
            aqi = ni
        if (rpi > si and rpi > ni and rpi > spi):
            aqi = rpi
        return aqi


    def Aqi_analysis(x):
        if x <= 50:
            return "Good"
        elif x > 50 and x <= 100:
            return "Moderate"
        elif x > 100 and x <= 200:
            return "Poor"
        elif x > 200 and x <= 300:
            return "Unhealthy"
        elif x > 400:
            return "Hazardous"


    submit = st.button(
        "SUBMIT"
    )

    if so2_input and no2_input and rspm_input and spm_input:
        if submit:
            with open(r"model.pkl", "rb") as f:
                model = pickle.load(f)

            aqi = float(model.predict([[soi, ni, rpi, spi]]))

            quality = Aqi_analysis(aqi)

            aqi_val = calculate_aqi(soi, ni, rpi, spi)

            st.title(
                f"The AQI For given input is {aqi_val}  and the quality of air is {quality}"
            )
    elif so2_input or no2_input or rspm_input or spm_input:
        if submit:
            st.title(
                "Please give all required input"
            )


except:
    st.markdown(
        " "
    )
