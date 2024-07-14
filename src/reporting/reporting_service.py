import pandas as pd
from datetime import datetime
from src.storage import StorageServiceInterface


class ReportingService:
    def __init__(
        self,
        storage_service: StorageServiceInterface,
    ):
        self.storage_service = storage_service

    def generate_reports(self, reference_date: str):
        executions = self.load_executions()
        if reference_date in executions.reference_date.values:
            return
        status_invest_base_path = f'parsed/status-invest/{reference_date.replace("-", "/")}'
        cvm_base_path = f'parsed/cvm/{reference_date.replace("-", "/")}'
        target_base_path = f'reports/{reference_date.replace("-", "/")}'
        self.generate_funds_report(
            status_invest_base_path,
            cvm_base_path,
            target_base_path,
        )
        self.register_execution(reference_date)

    def load_funds_report(self, reference_date: str):
        base_path = f'reports/{reference_date.replace("-", "/")}'
        path = f'{base_path}/funds.parquet'
        return self.load_parquet(path)

    def generate_funds_report(
        self,
        status_invest_base_path: str,
        cvm_base_path: str,
        target_base_path: str,
    ):
        funds = self.load_parquet(f'{status_invest_base_path}/funds.parquet')
        details_page = self.load_parquet(
            f'{status_invest_base_path}/details-page.parquet')
        funds_details = funds.merge(details_page, how='left', on='ticker')
        real_estate = self.load_parquet(
            f'{cvm_base_path}/quarterly-reports/real-estate.parquet')
        tenants = self.load_parquet(
            f'{cvm_base_path}/quarterly-reports/tenants.parquet')

        real_estate_count = self.get_real_estate_count(real_estate)
        real_estate_max_revenue_percentage = self.get_real_estate_max_revenue_percentage(
            real_estate,
        )
        tenants_max_revenue_percentage = self.get_tenants_max_revenue_percentage(
            tenants)
        tenants_count = self.get_tenants_count(tenants)

        funds_report = funds_details.merge(
            pd.concat([
                real_estate_count,
                real_estate_max_revenue_percentage,
                tenants_max_revenue_percentage,
                tenants_count,
            ], axis=1),
            how='left',
            left_on='cnpj',
            right_on='cnpj_fundo',
        )
        path = f'{target_base_path}/funds.parquet'
        self.save_parquet(funds_report, path)

    def get_real_estate_count(self, real_estate: pd.DataFrame) -> pd.DataFrame:
        return real_estate\
            .groupby('cnpj_fundo')\
            .classe\
            .value_counts()\
            .reset_index()\
            .pivot_table(values='count', index='cnpj_fundo', columns='classe')\
            .fillna(0)\
            .rename(
                columns={
                    'Imóveis para renda acabados': 'qtd_imoveis_renda_acabados',
                    'Imóveis para venda acabados': 'qtd_imoveis_venda_acabados',
                    'Imóveis para venda em construção': 'qtd_imoveis_venda_construcao',
                    'Imóveis para renda em construção': 'qtd_imoveis_renda_construcao',
                },
            )

    def get_real_estate_max_revenue_percentage(self, real_estate: pd.DataFrame) -> pd.DataFrame:
        return real_estate[real_estate.classe == 'Imóveis para renda acabados']\
            .groupby('cnpj_fundo')\
            .percentual_receitas_fii\
            .max()\
            .reset_index()\
            .rename(
                columns={
                    'percentual_receitas_fii': 'max_percentual_receitas_imovel',
                },
        )\
            .set_index('cnpj_fundo')

    def get_tenants_max_revenue_percentage(self, tenants: pd.DataFrame) -> pd.DataFrame:
        return tenants\
            .groupby('cnpj_fundo')\
            .percentual_receitas_fii\
            .max()\
            .reset_index()\
            .rename(
                columns={
                    'percentual_receitas_fii': 'max_percentual_receitas_inquilino',
                },
            )\
            .set_index('cnpj_fundo')

    def get_tenants_count(self, tenants: pd.DataFrame) -> pd.DataFrame:
        return tenants\
            .groupby('cnpj_fundo')\
            .nome_imovel\
            .count()\
            .reset_index()\
            .rename(
                columns={
                    'nome_imovel': 'qtd_inquilinos',
                },
            )\
            .set_index('cnpj_fundo')

    def load_parquet(self, path: str) -> pd.DataFrame:
        return self.storage_service.read_from_function(
            path,
            pd.read_parquet
        )

    def save_parquet(self, dataframe: pd.DataFrame, path: str):
        self.storage_service.write_from_function(
            path,
            lambda full_path: dataframe.to_parquet(full_path, index=False)
        )

    def load_executions(self) -> pd.DataFrame:
        path = 'metadata/reports/executions.csv'
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

    def register_execution(self, reference_date: str):
        executions = self.load_executions()
        executions = pd.concat(
            [
                executions,
                pd.DataFrame([{
                    'reference_date': reference_date,
                    'executed_at': datetime.now(),
                }]),
            ],
            ignore_index=True,
        )
        self.storage_service.write_from_function(
            'metadata/reports/executions.csv',
            lambda full_path: executions.to_csv(full_path, index=False)
        )
