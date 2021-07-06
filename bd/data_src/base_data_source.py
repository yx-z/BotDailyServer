from abc import abstractmethod


class DataSource:
    @abstractmethod
    def get_str(self) -> str:
        pass

    @abstractmethod
    def set_str(self, text: str = ""):
        pass
