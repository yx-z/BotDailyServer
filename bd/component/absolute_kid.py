import logging

from html_dsl.elements import IMG

from bd.component import BDComponent, title
from util.img import upload_img
from util.system import get_days, get_res
from util.web import dict_to_css, CSS_FULL_WIDTH


@title("绝对小孩")
class AbsoluteKid(BDComponent):
    URL = "https://raw.githubusercontent.com/yx-z/YunDaily/master/Yun/res/absolute-kids/{i}.jpg"

    def get_content(self, **kwargs) -> str:
        days = get_days(self.start_date) + 1
        urls = list(
            map(
                lambda i: upload_img(get_res(f"00{i}"[-3:])),
                [days * 2 - 1, days * 2],
            )
        )
        logging.info(f"Loading {urls}")
        style = dict_to_css(**CSS_FULL_WIDTH)
        return str(IMG(src=urls[0], style=style)) + str(IMG(src=urls[1], style=style))
