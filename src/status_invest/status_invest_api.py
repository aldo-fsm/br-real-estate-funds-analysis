import requests
import json
from datetime import date
from src.status_invest.constants import BASE_URL, USER_AGENT, DEFAULT_FILTERS

class StatusInvestApi:
    def advanced_search(self):
        response = requests.get(
            f'{BASE_URL}/category/advancedsearchresultpaginated',
            params=dict(
                search=json.dumps(DEFAULT_FILTERS),
                orderColumn='',
                isAsc='',
                page=0,
                take=9999,
                CategoryType=2,
            ),
            headers={
                'user-agent': USER_AGENT
            }
        )
        response.raise_for_status()
        return response.json()

    def get_ticker_prices(self, ticker: str):
        response = requests.get(
            f'{BASE_URL}/fii/tickerprice',
            params={
                'ticker': ticker,
                'type': 4,
                'currences[]': 1,
            },
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_ticker_provents(self, ticker: str):
        response = requests.get(
            f'{BASE_URL}/fii/companytickerprovents',
            params={
                'ticker': ticker,
                'chartProventsType': 2,
            },
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_ticker_net_worth(self, ticker: str):
        response = requests.get(
            f'{BASE_URL}/fii/getpatrimonioliquido',
            params={
                'code': ticker,
                'type': 1,
            },
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_results(self, ticker: str):
        response = requests.get(
            f'{BASE_URL}/fii/getresultado',
            params={
                'code': ticker,
                'type': 0,
            },
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_quarterly_statements(self, ticker: str, is_accounting: bool):
        response = requests.get(
            f'{BASE_URL}/fii/demonstracoestrimestrais',
            params={
                'code': ticker,
                'contabil': is_accounting,
                'type': 1,
                'range.min': 1999,
                'range.max': date.today().year,
            },
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_revenues(self, ticker: str):
        response = requests.get(
            f'{BASE_URL}/fii/getreceitas',
            params={
                'code': ticker,
                'type': 1,
            },
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_expenses(self, ticker: str):
        response = requests.get(
            f'{BASE_URL}/fii/getdespesas',
            params={
                'code': ticker,
                'type': 1,
            },
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_cash(self, ticker: str):
        response = requests.get(
            f'{BASE_URL}/fii/getcaixa',
            params={
                'code': ticker,
                'type': 1,
            },
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.json()

    def get_details_page(self, ticker: str) -> str:
        response = requests.get(
            f'{BASE_URL}/fundos-imobiliarios/{ticker}',
            headers={
                'user-agent': USER_AGENT,
            },
        )
        response.raise_for_status()
        return response.text
