class StorageServiceInterface:
    def write(self, path: str, content: bytes):
        raise NotImplementedError()

    def read(self, path):
        raise NotImplementedError()
