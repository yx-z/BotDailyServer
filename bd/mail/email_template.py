from typing import List, Tuple

from bd.component.base_component import BaseComponent
from bd.component.subject import Subject


class EmailTemplate:
    def __init__(
            self,
            subject: Subject,
            *components: List[BaseComponent],
    ):
        self.subject = subject
        self.components = components

    def instantiate(self, **kwargs) -> Tuple[str, List[str]]:
        return self.subject.get_content(**kwargs), list(
            map(lambda c: c.get_content(**kwargs), self.components)
        )
