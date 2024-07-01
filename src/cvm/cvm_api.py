import requests
from src.cvm.constants import BASE_URL

class CvmApi:
    def download_quarterly_reports(self, year: str | int) -> bytes:
        response = requests.get(
            f'{BASE_URL}/dados/FII/DOC/INF_TRIMESTRAL/DADOS/inf_trimestral_fii_{year}.zip',
        )
        response.raise_for_status()
        return response.content
