from src.storage import LocalStorageService, ZipFileService
from src.constants.storage_constants import BASE_PATH
from src.cvm.cvm_api import CvmApi
from src.cvm.cvm_extraction_service import CvmExtractionService
from src.cvm.cvm_parsing_service import CvmParsingService


def build_cvm_extraction_service():
    storage_service = LocalStorageService(BASE_PATH)
    cvm_api = CvmApi()
    zip_file_service = ZipFileService()
    cvm_extraction_service = CvmExtractionService(
        storage_service=storage_service,
        cvm_api=cvm_api,
        zip_file_service=zip_file_service,
    )
    return cvm_extraction_service

def build_cvm_parsing_service():
    storage_service = LocalStorageService(BASE_PATH)
    cvm_parsing_service = CvmParsingService(
        storage_service=storage_service,
    )
    return cvm_parsing_service
