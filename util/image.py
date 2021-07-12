import logging
from typing import Tuple

from PIL import Image
from PIL import ImageDraw, ImageFilter, ImageChops, ImageFont

from util.system import get_resource_path

Color = Tuple[int, int, int]
Coordinate = Tuple[int, int]


def draw_text(
    image: Image,
    text: str,
    *,
    position: Coordinate,
    font_name: str,
    text_color: Color,
    shadow_color: Color,
    text_size: int,
) -> Image:
    x, y = position
    font = ImageFont.truetype(get_resource_path(font_name), text_size)
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x + 1, y + 1), text, font=font, fill=shadow_color)
    blurred_shadow = shadow.filter(ImageFilter.BLUR)

    ImageDraw.Draw(blurred_shadow).text(position, text, font=font, fill=text_color)
    return Image.composite(image, blurred_shadow, ImageChops.invert(blurred_shadow))


def open_image(*path: str) -> Image:
    return Image.open(get_resource_path(*path))


def save_image(image: Image, *path: str):
    image.save(get_resource_path(*path))


def upload_image(*path: str) -> str:
    import config

    resource_path = get_resource_path(*path)
    logging.info(f"Uploading {resource_path}")
    url = config.IMGUR_API.upload_image(resource_path).link
    logging.info(f"Uploaded as {url}")
    return url
