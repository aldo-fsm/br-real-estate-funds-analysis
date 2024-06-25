from src.storage import StorageServiceInterface

class StatusInvestExtractionService:
    def __init__(self, storage_service: StorageServiceInterface):
        self.storage_service = storage_service
