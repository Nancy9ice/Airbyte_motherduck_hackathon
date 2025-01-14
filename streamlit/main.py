import streamlit as st

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

from streamlit_option_menu import option_menu
from dashboard_app import display_dashboard_app
from student_bio import display_student_bio
from student_performance import display_student_performance
from helper_functions import fetch_data
import pandas as pd


# st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header('Profile Parameters')

# Navigation menu
selected = option_menu(
    menu_title=None,
    options=["Dashboard Summary", "Student Bio", "Student Performance"],
    icons=["card-checklist", "person-lines-fill", "award"],
    default_index=0,
    orientation="horizontal"
)

df, df2 = fetch_data()

# Call the appropriate function based on the selected menu option
if selected == "Dashboard Summary":
    st.title('Dashboard Summary')
    display_dashboard_app(df2)
elif selected == "Student Bio":
    st.title('Student Profile')
    display_student_bio(df)
elif selected == "Student Performance":
    st.title('Students Performance')
    display_student_performance(df, df2)
