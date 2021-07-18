import logging
from typing import Optional

import requests
from html_dsl.elements import EM

from bd.component import BDComponent, title


@title("天气")
class Weather(BDComponent):
    def __init__(
        self, latitude: float, longitude: float, location: Optional[str] = None
    ):
        self.url = (
            "https://api.darksky.net/forecast/{key}/"
            + f"{latitude},{longitude}?lang=zh&units=si"
        )
        self.location = location

    def get_content(self, **kwargs) -> str:
        if "DARKSKY_KEY" not in kwargs:
            raise Exception("Require DARKSKY_KEY")
        logging.info(f"Querying {self.url}")
        data = requests.get(self.url.format(key=kwargs["DARKSKY_KEY"])).json()
        weather = data["daily"]["data"][0]

        summary = weather["summary"]
        if any(w in summary for w in ["雨", "雪"]):
            summary = EM[summary]

        min_temperature = int(weather["temperatureLow"])
        min_temperature_text = f"最低 {min_temperature}°C"
        if min_temperature <= 0:
            min_temperature_text = EM[min_temperature_text]

        max_temperature = int(weather["temperatureHigh"])
        max_temperature_text = f"最高 {max_temperature}°C"
        if max_temperature >= 35:
            max_temperature_text = EM[min_temperature_text]

        return f"{self.location} - {summary} {max_temperature_text}, {min_temperature_text}。"
