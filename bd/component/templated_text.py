from typing import Union

from bd.component.base_component import BaseComponent
from bd.data_src.base_data_source import DataSource


class TemplatedText(BaseComponent):
    def __init__(self, template: Union[DataSource, str]):
        self.template = template

    def get_content(self, **kwargs) -> str:
        if isinstance(self.template, DataSource):
            content = self.template.get_str()
        else:
            content = self.template

        for placeholder, actual in kwargs.items():
            content = content.replace("{" + placeholder + "}", str(actual))
        return content


class Subject(TemplatedText):
    def get_div_str(self, **kwargs) -> str:
        return self.get_content(**kwargs)
