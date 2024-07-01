import os
import shutil
from typing import Callable, List
from src.storage import StorageServiceInterface


class LocalStorageService (StorageServiceInterface):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def write(self, path: str, content: bytes):
        full_path = self.__get_full_path(path)
        self.__make_directory(full_path)
        with open(full_path, 'wb') as f:
            f.write(content)

    def write_from_path(self, path: str, source_path: str):
        full_path = self.__get_full_path(path)
        self.__make_directory(full_path)
        shutil.copy(source_path, full_path)

    def write_from_function(self, path: str, write_function: Callable):
        full_path = self.__get_full_path(path)
        self.__make_directory(full_path)
        write_function(full_path)

    def read(self, path: str) -> bytes:
        full_path = self.__get_full_path(path)
        with open(full_path, 'rb') as f:
            return f.read()

    def read_from_function(self, path: str, read_function: Callable) -> any:
        full_path = self.__get_full_path(path)
        return read_function(full_path)

    def exists(self, path: str) -> bool:
        full_path = self.__get_full_path(path)
        return os.path.exists(full_path)

    def list(self, path: str) -> List[str]:
        full_path = self.__get_full_path(path)
        return os.listdir(full_path)

    def __get_full_path(self, path: str) -> str:
        return os.path.join(self.base_path, path)

    def __make_directory(self, full_path: str):
        directory = '/'.join(full_path.split('/')[:-1])
        os.makedirs(directory, exist_ok=True)
