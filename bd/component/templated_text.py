from bd.component import BDComponent
from util.data_src.data_src import DataSrc


class TemplatedText(BDComponent):
    def get_content(self, **kwargs) -> str:
        if hasattr(self, "template"):
            template = self.template
        else:
            template = self.arg0

        if isinstance(template, DataSrc):
            content = template.get_str()
        else:
            content = template

        return content.format(**kwargs)


class Subject(TemplatedText):
    def get_str(self, **kwargs) -> str:
        return self.get_content(**kwargs)
