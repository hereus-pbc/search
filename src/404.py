from bevyframe import *
import os


def get(r: Request) -> Page:
    return Page(
        title="HereUS Search",
        selector=f'body_{r.user.id.settings.theme_color}',
        childs=[
            Title("404 Not Found"),
        ]
   )
