import requests
import json
from datetime import date
from src.status_invest.constants import BASE_URL, USER_AGENT, DEFAULT_FILTERS

class StatusInvestApi:
    def advancedSearch(self):
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

    def getTickerPrices(self, ticker: str):
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

    def getTickerProvents(self, ticker: str):
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

    def getTickerNetWorth(self, ticker: str):
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

    def getResults(self, ticker: str):
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

    def getQuarterlyStatements(self, ticker: str, is_accounting: bool):
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

    def getRevenues(self, ticker: str):
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

    def getExpenses(self, ticker: str):
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

    def getCash(self, ticker: str):
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
