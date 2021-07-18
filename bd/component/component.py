import os
from abc import abstractmethod

from html_dsl.elements import DIV, IMG

from util.image import (
    draw_text,
    upload_image,
    open_image,
    save_image,
    Color,
    Coordinate,
)
from util.system import resource_exists
from util.web import CSS_FULL_WIDTH, dict_to_css


class BDComponent:
    @abstractmethod
    def get_content(self, **kwargs) -> str:
        pass

    def get_div_str(self, **kwargs) -> str:
        return str(DIV[self.get_content(**kwargs)])

    def on_email_sent(self):
        pass

    def get_name(self) -> str:
        return type(self).__name__


def div_style(**style_args):
    def wrapper(cls):
        def get_str(self, **kwargs):
            return str(
                DIV(style=dict_to_css(**style_args))[cls.get_content(self, **kwargs)]
            )

        cls.get_div_str = get_str
        return cls

    return wrapper


def title(
    title_name: str,
    *,
    position: Coordinate = (120, 25),
    text_size: int = 30,
    text_color: Color = (0, 0, 0),
    shadow_color: Color = (255, 255, 255),
    header_background_name: str = os.path.join("header", "background.png"),
    font_name: str = "Hiragino Sans GB.ttc",
):
    def get_title_image(self) -> str:
        header_file = os.path.join("header", f"{self.get_name()}.png")
        if not resource_exists(header_file):
            background = open_image(header_background_name)
            title_image = draw_text(
                background,
                title_name,
                position=position,
                text_size=text_size,
                text_color=text_color,
                shadow_color=shadow_color,
                font_name=font_name,
            )
            save_image(title_image, header_file)

        img_src = upload_image(header_file)
        return str(
            IMG(src=img_src, alt=header_file, style=dict_to_css(**CSS_FULL_WIDTH))
        )

    def wrapper(cls):
        pre_get_str = cls.get_div_str

        def get_str(self, **kwargs):
            return get_title_image(self) + pre_get_str(self, **kwargs)

        cls.get_div_str = get_str
        return cls

    return wrapper
