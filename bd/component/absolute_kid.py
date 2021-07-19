import logging

from html_dsl.elements import IMG

from bd.component import BDComponent, title
from util.img import upload_img
from util.system import get_days
from util.web import dict_to_css, CSS_FULL_WIDTH


@title("绝对小孩")
class AbsoluteKid(BDComponent):
    def get_content(self, **kwargs) -> str:
        days = get_days(self.start_date) + 1
        indices = [days * 2 - 1, days * 2]
        logging.info(f"Querying indices {indices}")
        urls = list(
            map(lambda i: upload_img("absolute_kid", f"00{i}"[-3:] + ".jpg"),
                indices)
        )
        style = dict_to_css(**CSS_FULL_WIDTH)
        return str(IMG(src=urls[0], style=style)) + str(
            IMG(src=urls[1], style=style))
