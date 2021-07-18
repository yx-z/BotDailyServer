import gkeepapi
from gkeepapi.node import TopLevelNode

from util.data_src.data_src import DataSrc


class GoogleKeepDataSrc(DataSrc):
    def __init__(self, account: str, password: str, title: str):
        self._keep = gkeepapi.Keep()
        self.account = account
        self.title = title
        self._keep.login(self.account, password)

    def get_str(self) -> str:
        return str(self._get_note().text)

    def set_str(self, text: str = ""):
        self._get_note().text = text
        self._keep.sync()

    def get_images(self):
        return list(map(self._keep.getMediaLink, self._get_note().images))

    def create_note(self, title: str, text: str):
        self._keep.createNote(title, text)

    def _get_note(self) -> TopLevelNode:
        candidates = list(
            self._keep.find(func=lambda x: x.title.startswith(self.title))
        )
        if len(candidates) == 0:
            raise Exception(f"Note {self.title} ({self.account}) doesn't exist")
        return candidates[0]
