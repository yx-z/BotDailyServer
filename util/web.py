from typing import Dict

CSS_FULL_WIDTH = {"width": "100%"}


def dict_to_css(css_dict: Dict[str, str] = None, **kwargs) -> str:
    ret = ";".join(
        map(lambda p: f"{p[0]}:{p[1]}", {**css_dict, **kwargs}.items()))
    print(ret)
    return ret
