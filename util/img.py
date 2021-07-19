import logging
from typing import Tuple

from PIL import Image
from PIL import ImageDraw, ImageFilter, ImageChops, ImageFont

from util.system import get_res

Color = Tuple[int, int, int]
Coordinate = Tuple[int, int]


def draw_txt(
    img: Image,
    txt: str,
    *,
    pos: Coordinate,
    font: str,
    txt_color: Color,
    shadow_color: Color,
    txt_size: int,
) -> Image:
    x, y = pos
    font = ImageFont.truetype(get_res(font), txt_size)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x + 1, y + 1), txt, font=font, fill=shadow_color)
    blurred_shadow = shadow.filter(ImageFilter.BLUR)

    ImageDraw.Draw(blurred_shadow).text(pos, txt, font=font, fill=txt_color)
    return Image.composite(img, blurred_shadow, ImageChops.invert(blurred_shadow))


def open_img(*path: str) -> Image:
    return Image.open(get_res(*path))


def save_img(img: Image, *path: str):
    img.save(get_res(*path))


def upload_img(*path: str) -> str:
    import config

    res = get_res(*path)
    logging.info(f"Uploading {res}")
    url = config.IMGUR_API.upload_img(res).link
    logging.info(f"Uploaded as {url}")
    return url
