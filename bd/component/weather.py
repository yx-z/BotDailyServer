import logging

import requests
from html_dsl.elements import EM

from bd.component import BDComponent, title


@title("天气")
class Weather(BDComponent):
    URL = (
        "https://api.darksky.net/forecast/{key}/{latitude},{longitude}?lang=zh&units=si"
    )

    def get_content(self, **kwargs) -> str:
        super().get_content()
        url = Weather.URL.format(
            key=self.DARKSKY_KEY, latitude=self.latitude, longitude=self.longitude
        )
        logging.info(f"Quering {url}")
        data = requests.get(url).json()
        weather = data["daily"]["data"][0]

        summary = weather["summary"]
        if any(w in summary for w in ["雨", "雪"]):
            summary = EM[summary]

        temperature_low = int(weather["temperatureLow"])
        temperature_low_text = f"最低 {temperature_low}°C"
        if (
            hasattr(self, "warn_temperature_low")
            and temperature_low <= self.warn_temperature_low
        ):
            temperature_low_text = EM[temperature_low_text]

        temperature_high = int(weather["temperatureHigh"])
        temperature_high_text = f"最高 {temperature_high}°C"
        if (
            hasattr(self, "warn_temperature_high")
            and temperature_high >= self.warn_temperature_high
        ):
            temperature_high_text = EM[temperature_low_text]

        return f"{self.location} - {summary} {temperature_high_text}, {temperature_low_text}。"
