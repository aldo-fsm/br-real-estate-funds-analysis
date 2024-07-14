import streamlit as st
import pandas as pd
import numpy as np
from typing import List
from src.reporting import reporting_factory
from src.reporting.constants.filters import FUNDS_FILTERS


def render_filter(config: dict, data: pd.DataFrame):
    label = config['label']
    column = config['column']
    filter_type = config['type']
    tooltip = config.get('help')
    if filter_type == 'multiselect':
        return {
            'column': column,
            'type': filter_type,
            'value': st.sidebar.multiselect(
                label,
                data[column].unique(),
                help=tooltip,
            ),
        }
    if filter_type == 'numeric-range':
        min_value = data[column].min()
        max_value = data[column].max()
        grid_column1, grid_column2 = st.sidebar.columns(2)
        return {
            'column': column,
            'type': filter_type,
            'value': [
                grid_column1.number_input(
                    f'{label} (mínimo)',
                    min_value=min_value,
                    max_value=max_value,
                    value=None,
                    help=tooltip,
                ),
                grid_column2.number_input(
                    f'{label} (máximo)',
                    min_value=min_value,
                    max_value=max_value,
                    value=None,
                    help=tooltip,
                ),
            ],
        }
    raise NotImplementedError()


def apply_filters(
    field_filters: List[dict],
    data: pd.DataFrame
):
    filtered = data
    for field_filter in field_filters:
        column = field_filter['column']
        filter_type = field_filter['type']
        value = field_filter.get('value')
        if filter_type == 'multiselect' and value:
            filtered = filtered[np.isin(filtered[column], value)]
        if filter_type == 'numeric-range' and value:
            min_value, max_value = value
            if min_value is not None:
                filtered = filtered[filtered[column] >= min_value]
            if max_value is not None:
                filtered = filtered[filtered[column] <= max_value]
    return filtered


reporting_service = reporting_factory.build_reporting_service()

reporting_reference_dates = reporting_service\
    .load_executions()\
    .reference_date\
    .tolist()

reference_dates = sorted(list(set(reporting_reference_dates)))[::-1]

reference_date = st.selectbox('Data de Referência', options=reference_dates)

funds = reporting_service.load_funds_report(reference_date)
st.header(f'Fundos Imobiliários ({len(funds)})')
st.dataframe(funds)

filters = [
    render_filter(config, funds) for config in FUNDS_FILTERS
]

funds_filtered = apply_filters(filters, funds)
st.header(f'Fundos Imobiliários Filtrados ({len(funds_filtered)})')
st.dataframe(funds_filtered)
