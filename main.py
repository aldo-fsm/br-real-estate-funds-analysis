import streamlit as st

pg = st.navigation([
    st.Page("src/pages/home.py"),
    st.Page("src/pages/get_data.py"),
])
pg.run()
