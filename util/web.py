CSS_FULL_WIDTH = {"width": "100%"}

HTML_NEW_LINE = "<br>"


def dict_to_css(**kwargs) -> str:
    return ";".join(map(lambda p: f"{p[0]}:{p[1]}", kwargs.items()))
