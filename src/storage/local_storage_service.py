import os
from src.storage import StorageServiceInterface

class LocalStorageService (StorageServiceInterface):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def write(self, path: str, content: bytes):
        directory = '/'.join(path.split('/')[:-1])
        os.makedirs(directory, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(content)

    def read(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            return f.read()
