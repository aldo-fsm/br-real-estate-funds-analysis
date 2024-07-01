import json
import pandas as pd
from typing import Callable
from datetime import date, datetime
from src.storage import StorageServiceInterface
from src.status_invest.status_invest_api import StatusInvestApi
from src.status_invest.dto.advanced_search_response_dto import AdvancedSearchResponseDto


class StatusInvestExtractionService:
    def __init__(self, storage_service: StorageServiceInterface, status_invest_api: StatusInvestApi):
        self.storage_service = storage_service
        self.status_invest_api = status_invest_api

    def extract(self, callback: Callable):
        today = date.today()
        base_path = f'raw/status-invest/{today.isoformat().replace("-", "/")}'
        funds = self.get_funds(f'{base_path}/advanced-search.json')
        total = len(funds.list)
        for index, fund in enumerate(funds.list):
            ticker = fund.ticker
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/prices.json',
                self.status_invest_api.get_ticker_prices,
                [ticker],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/provents.json',
                self.status_invest_api.get_ticker_provents,
                [ticker],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/net-worth.json',
                self.status_invest_api.get_ticker_net_worth,
                [ticker],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/results.json',
                self.status_invest_api.get_results,
                [ticker],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/quarterly-statements-accounting.json',
                self.status_invest_api.get_quarterly_statements,
                [ticker, True],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/quarterly-statements-financial.json',
                self.status_invest_api.get_quarterly_statements,
                [ticker, False],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/revenues.json',
                self.status_invest_api.get_revenues,
                [ticker],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/expenses.json',
                self.status_invest_api.get_expenses,
                [ticker],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/cash.json',
                self.status_invest_api.get_cash,
                [ticker],
            )
            self.extract_data_and_save(
                f'{base_path}/tickers/{ticker}/details-page.html',
                self.status_invest_api.get_details_page,
                [ticker],
            )
            if callback:
                callback(dict(progress=(index + 1)/total,
                         ticker=ticker, index=index, total=total))
        self.register_extraction(today.isoformat())

    def get_funds(self, path: str):
        if self.storage_service.exists(path):
            content = self.storage_service.read(path)
            data = json.loads(content.decode())
            return AdvancedSearchResponseDto(data)
        funds_dict = self.status_invest_api.advanced_search()
        self.save(path, funds_dict)
        return AdvancedSearchResponseDto(funds_dict)

    def extract_data_and_save(self, path: str, extraction_function: Callable, function_args):
        if self.storage_service.exists(path):
            return
        data = extraction_function(*function_args)
        self.save(path, data)

    def save(self, path: str, data: any):
        self.storage_service.write(
            path,
            self.to_bytes(data)
        )

    def to_bytes(self, data: any):
        if type(data) in (dict, list):
            return json.dumps(data, ensure_ascii=False).encode()
        return str(data).encode()

    def load_extractions(self):
        path = 'metadata/status-invest/extractions.csv'
        if self.storage_service.exists(path):
            return self.storage_service.read_from_function(
                path,
                pd.read_csv,
            )
        return pd.DataFrame(
            [],
            columns=['reference_date', 'executed_at'],
        ).astype(
            dtype={
                'reference_date': 'str',
                'executed_at': '<M8[ns]',
            }
        )

    def register_extraction(self, reference_date: str):
        extractions = self.load_extractions()
        extractions = pd.concat(
            [
                extractions,
                pd.DataFrame([{
                    'reference_date': reference_date,
                    'executed_at': datetime.now(),
                }]),
            ],
            ignore_index=True,
        )
        self.storage_service.write_from_function(
            'metadata/status-invest/extractions.csv',
            lambda full_path: extractions.to_csv(full_path, index=False)
        )
