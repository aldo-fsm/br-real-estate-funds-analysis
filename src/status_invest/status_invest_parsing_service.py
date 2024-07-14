import json
import os
import pandas as pd
from bs4 import BeautifulSoup
from typing import Callable
from src.storage import StorageServiceInterface
from src.utils.date_utils import to_iso_date


class StatusInvestParsingService:
    def __init__(self, storage_service: StorageServiceInterface):
        self.storage_service = storage_service

    def parse(self, reference_date: str, callback: Callable):
        source_base_path = f'raw/status-invest/{reference_date.replace("-", "/")}'
        target_base_path = f'parsed/status-invest/{reference_date.replace("-", "/")}'

        self.parse_and_save_advanced_search(source_base_path, target_base_path)
        callback(dict(progress=1/4))

        self.parse_and_save_detail_page(source_base_path, target_base_path)
        callback(dict(progress=2/4))

        self.parse_and_save_provents(source_base_path, target_base_path)
        callback(dict(progress=3/4))

        self.parse_and_save_prices(source_base_path, target_base_path)
        callback(dict(progress=4/4))

    def load_text(self, path):
        content = self.storage_service.read(path)
        return content.decode()

    def load_json(self, path):
        text = self.load_text(path)
        return json.loads(text)

    def parse_and_save_detail_page(self, source_base_path: str, target_base_path: str):
        target_path = os.path.join(target_base_path, 'details-page.parquet')
        if self.storage_service.exists(target_path):
            return
        data = []
        tickers_path = os.path.join(source_base_path, 'tickers')
        for ticker in self.storage_service.list(tickers_path):
            path = os.path.join(tickers_path, ticker, 'details-page.html')
            html = self.load_text(path)
            if 'Não encontramos o que você está procurando' in html:
                continue
            soup = BeautifulSoup(html)
            cnpj = self.extract_cnpj(soup)
            data.append(dict(
                ticker=ticker,
                cnpj=cnpj,
            ))
        details_page = pd.DataFrame(data)
        self.save_parquet(details_page, target_path)

    def extract_cnpj(self, soup: BeautifulSoup):
        fund_info_divs = soup \
            .find(attrs={'id': 'fund-section'}) \
            .find_all(attrs={'class': 'info'})
        for div in fund_info_divs:
            if 'CNPJ' in div.text:
                return div.find(attrs={'class': 'value'}).text

    def parse_and_save_advanced_search(self, source_base_path: str, target_base_path: str):
        target_path = os.path.join(target_base_path, 'funds.parquet')
        if self.storage_service.exists(target_path):
            return
        path = os.path.join(source_base_path, 'advanced-search.json')
        data = self.load_json(path)
        funds = pd.DataFrame(data['list'])
        funds = funds.rename(
            columns={
                'companyid': 'id',
                'companyname': 'nome',
                'ticker': 'ticker',
                'price': 'preco',
                'sectorid': 'id_setor',
                'sectorname': 'nome_setor',
                'subsectorid': 'id_subsetor',
                'subsectorname': 'nome_subsetor',
                'segment': 'segmento',
                'segmentid': 'id_segmento',
                'gestao': 'gestao',
                'gestao_f': 'tipo_gestao',
                'dy': 'dividend_yield',
                'p_vp': 'p_vp',
                'valorpatrimonialcota': 'valor_patrimonial_cota',
                'liquidezmediadiaria': 'liquidez_media_diaria',
                'percentualcaixa': 'percentual_caixa',
                'dividend_cagr': 'dividend_yield_cagr',
                'cota_cagr': 'cota_cagr',
                'numerocotistas': 'numero_cotistas',
                'numerocotas': 'numero_cotas',
                'patrimonio': 'patrimonio_liquido',
                'lastdividend': 'ultimo_dividendo',
            }
        )
        self.save_parquet(funds, target_path)

    def parse_and_save_provents(self, source_base_path: str, target_base_path: str):
        target_path = os.path.join(target_base_path, 'provents.parquet')
        if self.storage_service.exists(target_path):
            return
        data = []
        tickers_path = os.path.join(source_base_path, 'tickers')
        for ticker in self.storage_service.list(tickers_path):
            path = os.path.join(tickers_path, ticker, 'provents.json')
            provents = self.load_json(path)
            data.extend([{
                **item,
                'ticker': ticker
            }
                for item in provents['assetEarningsModels']
            ])
        provents = pd.DataFrame(data)
        provents = provents[['ticker', 'ed', 'etd', 'v']].rename(columns={
            'ed': 'data',
            'etd': 'tipo',
            'v': 'valor',
        })
        provents['data'] = provents['data'].apply(to_iso_date)
        self.save_parquet(provents, target_path)

    def parse_and_save_prices(self, source_base_path: str, target_base_path: str):
        target_path = os.path.join(target_base_path, 'prices.parquet')
        if self.storage_service.exists(target_path):
            return
        data = []
        tickers_path = os.path.join(source_base_path, 'tickers')
        for ticker in self.storage_service.list(tickers_path):
            path = os.path.join(tickers_path, ticker, 'prices.json')
            prices = self.load_json(path)
            data.extend([{**item, 'ticker': ticker}
                        for item in prices[0]['prices']])
        prices = pd.DataFrame(data)
        prices = prices[['ticker', 'date', 'price']].rename(columns={
            'date': 'data',
            'price': 'preco',
        })
        prices['data'] = prices['data'].apply(to_iso_date)
        self.save_parquet(prices, target_path)

    def save_parquet(self, dataframe: pd.DataFrame, path: str):
        self.storage_service.write_from_function(
            path,
            lambda full_path: dataframe.to_parquet(full_path, index=False)
        )
