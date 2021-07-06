from abc import abstractmethod

from html_dsl.elements import DIV, IMG

from util.const import Color, CSS_FULL_WIDTH, Coordinate
from util.image import draw_text, upload_image, open_image, save_image
from util.misc import resource_exists


class BaseComponent:
    @abstractmethod
    def get_content(self, **kwargs) -> str:
        pass

    def get_str(self, **kwargs) -> str:
        return str(DIV[self.get_content(**kwargs)])

    def on_finish(self):
        pass

    def get_name(self) -> str:
        return type(self).__name__


def set_title(
        title: str,
        *,
        position: Coordinate = (120, 25),
        text_size: int = 30,
        text_color: Color = (0, 0, 0),
        shadow_color: Color = (255, 255, 255),
        banner_background_name: str = "banner/background.png",
        font_name: str = "Hiragino Sans GB.ttc",
):
    def get_title_image(self) -> str:
        header_file = f"banner/{type(self).__name__}.png"
        if not resource_exists(header_file):
            background = open_image(banner_background_name)
            title_image = draw_text(
                background,
                title,
                position=position,
                text_size=text_size,
                text_color=text_color,
                shadow_color=shadow_color,
                font_name=font_name,
            )
            save_image(title_image, header_file)

        img_src = upload_image(header_file)
        return str(IMG(src=img_src, alt=header_file, style=CSS_FULL_WIDTH))

    def wrapper(cls):
        pre_get_as_str = cls.get_str

        def get_as_str(self, **kwargs):
            return get_title_image(self) + pre_get_as_str(self, **kwargs)

        cls.get_str = get_as_str
        return cls

    return wrapper
