import os
from pathlib import Path

from util.data_src.data_src import DataSrc


class FileDataSrc(DataSrc):
    def __init__(self, file_path: str):
        Path.mkdir(Path(os.path.dirname(file_path)), exist_ok=True, parents=True)
        if not os.path.exists(file_path):
            with open(file_path, "w"):
                pass
        self.file_path = file_path

    def get_str(self) -> str:
        with open(self.file_path) as f:
            return f.read()

    def set_str(self, text: str = ""):
        with open(self.file_path, "w") as f:
            f.write(text)
