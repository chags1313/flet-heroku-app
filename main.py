import os

import flet
from flet import ElevatedButton, Image, Page

port = os.getenv("PORT")
if port:
    try:
        port = int(port)
    except ValueError:
        port = None  # or a default port number that your app uses when not running on Heroku

def main(page: Page):

    c = Image(src="https://picsum.photos/200/300", opacity=None, animate_opacity=300)

    def animate_opacity(e):
        c.opacity = 0 if c.opacity == 1 else 1
        c.update()

    page.add(
        c,
        ElevatedButton(
            "Animate opacity",
            on_click=animate_opacity,
        ),
    )


flet.app(target=main, port=port, view = ft.WEB_BROWSER)
