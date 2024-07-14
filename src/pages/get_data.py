import streamlit as st
from datetime import date
from src.status_invest import status_invest_factory
from src.cvm import cvm_factory
from src.reporting import reporting_factory

status_invest_extraction_service = status_invest_factory.build_status_invest_extraction_service()
status_invest_parsing_service = status_invest_factory.build_status_invest_parsing_service()

cvm_extraction_service = cvm_factory.build_cvm_extraction_service()
cvm_parsing_service = cvm_factory.build_cvm_parsing_service()

reporting_service = reporting_factory.build_reporting_service()

status_invest_extraction_dates = status_invest_extraction_service\
    .load_extractions()\
    .reference_date\
    .tolist()

cvm_extraction_dates = cvm_extraction_service\
    .load_extractions()\
    .reference_date\
    .tolist()

extraction_dates = sorted(
    list(set(status_invest_extraction_dates + cvm_extraction_dates)))[::-1]

st.markdown('# Geração de Conjunto de Dados')

today = date.today().isoformat()
reference_date = st.selectbox('Data da Extração', options=extraction_dates)

new_extraction = st.button('Nova Extração')

st.markdown('## Status Invest')
status_invest_extraction_bar = st.progress(
    0.0, text='Extração de dados - Status Invest')
if new_extraction or reference_date not in status_invest_extraction_dates:
    status_invest_extraction_service.extract(
        lambda data: status_invest_extraction_bar.progress(
            data['progress'],
            text='Extração de dados - Status Invest'
        )
    )
else:
    status_invest_extraction_bar.progress(
        1.0, text='Extração de dados - Status Invest')

status_invest_parsing_bar = st.progress(
    0.0, text='Parse dos dados - Status Invest')
status_invest_parsing_service.parse(
    reference_date,
    lambda data: status_invest_parsing_bar.progress(
        data['progress'],
        text='Parse dos dados - Status Invest'
    ),
)

st.markdown('## CVM')
cvm_extraction_bar = st.progress(0.0, text='Extração de dados - CVM')
if new_extraction or reference_date not in cvm_extraction_dates:
    cvm_extraction_service.extract()
else:
    cvm_extraction_bar.progress(1.0, text='Extração de dados - CVM')

cvm_extraction_bar.progress(1.0, text='Extração de dados - CVM')

cvm_parsing_bar = st.progress(0.0, text='Parse dos dados - CVM')
cvm_parsing_service.parse(reference_date)
cvm_parsing_bar.progress(1.0, text='Parse dos dados - CVM')

st.markdown('## Geração de Relatórios')
reporting_bar = st.progress(0.0)
reporting_service.generate_reports(reference_date)
reporting_bar.progress(1.0)
