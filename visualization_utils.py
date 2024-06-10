import pandas as pd
import streamlit as st


def display_data_table(data_dict, selected_fields):
    filtered_data = {key: value for key, value in data_dict.items() if key in selected_fields}
    df = pd.DataFrame(list(filtered_data.items()), columns=['Key', 'Value'])
    st.table(df)
