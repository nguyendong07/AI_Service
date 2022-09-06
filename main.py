# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
from streamlit_option_menu import option_menu
from compare_face import compare
import time
import json
import pandas as pd
import numpy as np

with st.sidebar:
    selected = option_menu(menu_title="Main menu",
                           options=["Home", "Project", "Document", "Contact"],
                           icons=["house", "bag-check", "book", "envelope"],
                           menu_icon="cast",
                           default_index=0,
                           )
    # if selected == "Home":
    #     st.title(f"You have select {selected}")
    # if selected == "Project":
    #     st.title(f"You have select {selected}")
    # if selected == "Contact":
    #     st.title(f"You have select {selected}")

disable = False;

if selected == "Project":
    rs = {}
    st.header("Match face between ID card and selfie")
    col1, col2 = st.columns(2)
    with col1:
        id_card = st.file_uploader("Please choose a ID Card Image", key=1)
        if id_card is not None:
            st.image(id_card, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB",
                     output_format="auto")

    with col2:
        selfie = st.file_uploader("Please choose a Selfie Image", key=2)
        if selfie is not None:
            st.image(selfie, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB",
                     output_format="auto")
    # st.button("Match")
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    with col5:
        if st.button("Match") is True:
            if id_card is None or selfie is None:
                st.warning('Need at least 2 images', icon="⚠️")
            else:
                with st.spinner('Process is running...'):
                    distance = compare(id_card, selfie)
                    time.sleep(2)
                st.success('Done!')
                if distance < 0.45:
                    rs = {
                        "code": "200",
                        "data": {
                            "isMatch": "true",
                            "similarity": 1 - distance,
                            "isBothImgIDCard": "true"
                        },
                        "message": "request successful.",
                    }
                elif distance > 0.45:
                    rs = {
                        "code": "200",
                        "data": {
                            "isMatch": "false",
                            "similarity": 1 - distance,
                            "isBothImgIDCard": "false"
                        },
                        "message": "request successful.",
                    }
                else:
                    rs = {
                        "code": "400",
                        "data": {
                            "error": "Something went wrong, make sure both images contain face"
                        },
                        "message": "request error.",
                    }
    st.subheader("Result")

    if rs != {}:
        st.json(rs)
if selected == "Home":
    st.title('Request API in AI Service')

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data


    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache)")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.subheader('Number of request by days')
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
    st.bar_chart(hist_values)

    # Some number in the range 0-23
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    st.map(filtered_data)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
