from bd.data_src.base_data_source import DataSource


class FileBasedDataSource(DataSource):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_str(self) -> str:
        with open(self.file_path) as f:
            return f.read()

    def set_str(self, text: str = ""):
        with open(self.file_path, "w") as f:
            f.write(text)
