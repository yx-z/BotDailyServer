import os
from abc import abstractmethod, ABC

from html_dsl.elements import DIV, IMG

from util.img import (
    draw_txt,
    upload_img,
    open_img,
    save_img,
    Color,
    Coordinate,
)
from util.res_log_cfg import res_exists
from util.web import CSS_FULL_WIDTH, to_css


class BDComponent(ABC):
    def __init__(self, *args, **kwargs):
        for i, v in enumerate(args):
            arg_name = f"arg{i}"
            setattr(self, arg_name, v)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    def get_content(self, **kwargs) -> str:
        pass

    def on_email_sent(self):
        pass

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def set_getter(cls, **kwargs):
        def getter(_, attr):
            if attr in kwargs:
                v = kwargs[attr]
                return v
            raise AttributeError(f"{cls.get_name()} requires {attr}")

        cls.__getattr__ = getter

    def get_str(self, **kwargs) -> str:
        type(self).set_getter(**kwargs)
        return str(DIV[self.get_content(**kwargs)])


def div_style(**style_args):
    def wrapper(cls):
        def get_str(self, **kwargs):
            return str(DIV(style=to_css(**style_args))[cls.get_content(self, **kwargs)])

        cls.get_str = get_str
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
        if not res_exists(header_file):
            background = open_img(header_background_name)
            title_image = draw_txt(
                background,
                title_name,
                pos=position,
                txt_size=text_size,
                txt_color=text_color,
                shadow_color=shadow_color,
                font=font_name,
            )
            save_img(title_image, header_file)

        img_src = upload_img(header_file)
        return str(IMG(src=img_src, alt=header_file, style=to_css(**CSS_FULL_WIDTH)))

    def wrapper(cls):
        pre_get_str = cls.get_str

        def get_str(self, **kwargs):
            return get_title_image(self) + pre_get_str(self, **kwargs)

        cls.get_str = get_str
        return cls

    return wrapper
