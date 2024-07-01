import os
import tempfile
import zipfile

class ZipFileService:
    def unzip(self, zip_file_content: bytes, target_path: str):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file_path = os.path.join(temp_dir, 'file.zip')
            with open(zip_file_path, 'wb') as f:
                f.write(zip_file_content)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(target_path)
