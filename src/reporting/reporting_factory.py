from src.storage.local_storage_service import LocalStorageService
from src.constants.storage_constants import BASE_PATH
from src.reporting.reporting_service import ReportingService


def build_reporting_service():
    storage_service = LocalStorageService(BASE_PATH)
    reporting_service = ReportingService(
        storage_service=storage_service,
    )
    return reporting_service
