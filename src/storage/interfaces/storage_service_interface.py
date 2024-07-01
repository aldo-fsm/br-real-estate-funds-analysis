from typing import Callable, List


class StorageServiceInterface:
    def write(self, path: str, content: bytes):
        raise NotImplementedError()

    def write_from_path(self, path: str, source_path: str):
        raise NotImplementedError()

    def write_from_function(self, path: str, write_function: Callable):
        raise NotImplementedError()

    def read(self, path) -> bytes:
        raise NotImplementedError()

    def read_from_function(self, path: str, read_function: Callable) -> any:
        raise NotImplementedError()

    def exists(self, path: str) -> bool:
        raise NotImplementedError()

    def list(self, path: str) -> List[str]:
        raise NotImplementedError()
