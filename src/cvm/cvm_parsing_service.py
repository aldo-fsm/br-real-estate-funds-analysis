import os
import pandas as pd
from src.storage import StorageServiceInterface


class CvmParsingService:
    def __init__(
        self,
        storage_service: StorageServiceInterface,
    ):
        self.storage_service = storage_service

    def parse(self, reference_date: str):
        year = reference_date.split('-')[0]
        source_base_path = f'raw/cvm/{reference_date.replace("-", "/")}'
        target_base_path = f'parsed/cvm/{reference_date.replace("-", "/")}'
        self.parse_and_save_real_estate(year, source_base_path, target_base_path)
        self.parse_and_save_tenants(year, source_base_path, target_base_path)

    def parse_and_save_real_estate(self, year: str, source_base_path: str, target_base_path: str):
        source_path = os.path.join(source_base_path, 'quarterly-reports', f'inf_trimestral_fii_imovel_{year}.csv')
        real_estate = self.storage_service.read_from_function(
            source_path,
            lambda full_path: pd.read_csv(full_path, sep=';', encoding='iso-8859-1'),
        )
        real_estate = real_estate.rename(columns={
            column: column.lower()
            for column in real_estate.columns
        })
        path = os.path.join(target_base_path, 'quarterly-reports', 'real-estate.parquet')
        self.save_parquet(real_estate, path)

    def parse_and_save_tenants(self, year: str, source_base_path: str, target_base_path: str):
        source_path = os.path.join(source_base_path, 'quarterly-reports', f'inf_trimestral_fii_imovel_renda_acabado_inquilino_{year}.csv')
        real_estate = self.storage_service.read_from_function(
            source_path,
            lambda full_path: pd.read_csv(full_path, sep=';', encoding='iso-8859-1'),
        )
        real_estate = real_estate.rename(columns={
            column: column.lower()
            for column in real_estate.columns
        })
        path = os.path.join(target_base_path, 'quarterly-reports', 'tenants.parquet')
        self.save_parquet(real_estate, path)

    def save_parquet(self, dataframe: pd.DataFrame, path: str):
        self.storage_service.write_from_function(
            path,
            lambda full_path: dataframe.to_parquet(full_path, index=False)
        )
