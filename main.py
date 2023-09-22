import os
import random
from math import pi

import flet
from flet import Container, ElevatedButton, Page, Stack, colors


def main(page: Page):
    page.add(flet.Text("Hello World"))

flet.app(target=main, port=os.getenv("PORT"), route_url_strategy="path")
