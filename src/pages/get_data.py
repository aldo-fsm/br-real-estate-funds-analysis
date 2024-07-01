import streamlit as st
from datetime import date
from src.status_invest import status_invest_factory
from src.cvm import cvm_factory

status_invest_extraction_service = status_invest_factory.build_status_invest_extraction_service()
status_invest_parsing_service = status_invest_factory.build_status_invest_parsing_service()

cvm_extraction_service = cvm_factory.build_cvm_extraction_service()
cvm_parsing_service = cvm_factory.build_cvm_parsing_service()

st.markdown('# Geração de Conjunto de Dados')

reference_date = date.today().isoformat()

st.markdown('## Status Invest')
status_invest_extraction_bar = st.progress(0.0, text='Extraindo dados - Status Invest')
status_invest_extraction_service.extract(
    lambda data: status_invest_extraction_bar.progress(
        data['progress'],
        text='Extraindo dados - Status Invest'
    )
)

status_invest_parsing_bar = st.progress(0.0, text='Parse dos dados - Status Invest')
status_invest_parsing_service.parse(
    reference_date,
    lambda data: status_invest_parsing_bar.progress(
        data['progress'],
        text='Parse dos dados - Status Invest'
    ),
)

st.markdown('## CVM')
cvm_extraction_bar = st.progress(0.0, text='Extraindo dados - CVM')
cvm_extraction_service.extract()
cvm_extraction_bar.progress(1.0, text='Extraindo dados - CVM')

cvm_parsing_bar = st.progress(0.0, text='Parse dos dados - CVM')
cvm_parsing_service.parse(reference_date)
cvm_parsing_bar.progress(1.0, text='Parse dos dados - CVM')
