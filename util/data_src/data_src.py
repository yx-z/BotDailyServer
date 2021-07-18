from abc import abstractmethod


class DataSrc:
    @abstractmethod
    def get_str(self) -> str:
        pass

    @abstractmethod
    def set_str(self, text: str = ""):
        pass
