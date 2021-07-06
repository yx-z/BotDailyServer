from bd.component.base_component import BaseComponent


class Subject(BaseComponent):
    def __init__(self, dated_template: str):
        self.template = dated_template

    def get_content(self, **kwargs) -> str:
        content = self.template
        for template, actual in kwargs.items():
            content = content.replace("{" + template + "}", actual)
        return content
