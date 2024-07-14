import os
import pandas as pd
import tempfile
from datetime import date, datetime
from src.storage import StorageServiceInterface, ZipFileService
from src.cvm.cvm_api import CvmApi


class CvmExtractionService:
    def __init__(
        self,
        storage_service: StorageServiceInterface,
        cvm_api: CvmApi,
        zip_file_service: ZipFileService
    ):
        self.storage_service = storage_service
        self.cvm_api = cvm_api
        self.zip_file_service = zip_file_service

    def extract(self):
        today = date.today()
        year = today.year
        base_path = f'raw/cvm/{today.isoformat().replace("-", "/")}'
        self.extract_quarterly_reports(year, base_path)
        self.register_extraction(today.isoformat())

    def extract_quarterly_reports(self, year: str | int, target_dir: str):
        content = self.cvm_api.download_quarterly_reports(year)
        with tempfile.TemporaryDirectory() as temp_dir:
            self.zip_file_service.unzip(content, temp_dir)
            for filename in os.listdir(temp_dir):
                path = os.path.join(temp_dir, filename)
                target_path = os.path.join(
                    target_dir, 'quarterly-reports', filename)
                self.storage_service.write_from_path(target_path, path)

    def load_extractions(self) -> pd.DataFrame:
        path = 'metadata/cvm/extractions.csv'
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
            'metadata/cvm/extractions.csv',
            lambda full_path: extractions.to_csv(full_path, index=False)
        )
