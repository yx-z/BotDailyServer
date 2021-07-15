from typing import List, Union, Any

from flask import request, Response, redirect

CSS_FULL_WIDTH = {"width": "100%"}

HTML_NEW_LINE = "<br>"


def get_form_value(value_names: Union[str, List[str]]) -> Union[Any, List[Any]]:
    if isinstance(value_names, str):
        value_names = [value_names]
    results = list(map(request.form.get, value_names))
    if len(results) == 1:
        return results[0]
    else:
        return results


def dict_to_css(**kwargs) -> str:
    return ";".join(map(lambda p: f"{p[0]}:{p[1]}", kwargs.items()))


def home() -> Response:
    return redirect("/")
