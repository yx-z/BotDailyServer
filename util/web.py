from typing import List

from flask import request

CSS_FULL_WIDTH = {"width": "100%"}

HTML_NEW_LINE = "<br>"


def get_form_values(value_names: List[str]) -> List:
    return list(map(request.form.get, value_names))


def dict_to_css(**kwargs) -> str:
    return ";".join(map(lambda p: f"{p[0]}:{p[1]}", kwargs.items()))
