import streamlit as st

st.set_page_config(layout='wide')
pg = st.navigation([
    st.Page("src/pages/home.py"),
    st.Page("src/pages/get_data.py"),
    st.Page("src/pages/funds.py"),
])
pg.run()
