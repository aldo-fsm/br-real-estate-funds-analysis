from src.storage.local_storage_service import LocalStorageService
from src.constants.storage_constants import BASE_PATH
from src.status_invest.status_invest_api import StatusInvestApi
from src.status_invest.status_invest_extraction_service import StatusInvestExtractionService
from src.status_invest.status_invest_parsing_service import StatusInvestParsingService


def build_status_invest_extraction_service():
    storage_service = LocalStorageService(BASE_PATH)
    status_invest_api = StatusInvestApi()
    status_invest_extraction_service = StatusInvestExtractionService(
        storage_service=storage_service,
        status_invest_api=status_invest_api,
    )
    return status_invest_extraction_service


def build_status_invest_parsing_service():
    storage_service = LocalStorageService(BASE_PATH)
    status_invest_parsing_service = StatusInvestParsingService(
        storage_service=storage_service,
    )
    return status_invest_parsing_service
