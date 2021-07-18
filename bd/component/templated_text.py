from typing import Union

from bd.component.component import BDComponent
from util.data_src.data_src import DataSrc


class TemplatedText(BDComponent):
    def __init__(self, template: Union[DataSrc, str]):
        self.template = template

    def get_content(self, **kwargs) -> str:
        if isinstance(self.template, DataSrc):
            content = self.template.get_str()
        else:
            content = self.template

        return content.format(**kwargs)


class Subject(TemplatedText):
    def get_div_str(self, **kwargs) -> str:
        return self.get_content(**kwargs)
