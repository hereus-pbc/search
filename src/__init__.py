from bevyframe import *


def get(r: Request) -> Page:
    if r.query.get('q', None) is not None:
        return redirect(f"/Search.py?q={r.query['q']}")
    return Page(
        title="HereUS Search",
        selector=f'body_{r.user.id.settings.theme_color}',
        childs=[
            Container(
                position=Position.fixed(top=Size.pixel(10), right=Size.pixel(10)),
                onclick="window.location.href='/Profile.py'",
                childs=[
                    Button('small', innertext="Login")
                    if r.email.split('@')[0] == 'Guest' else
                    Image(
                        r.user.id.profile_photo,
                        alt="Your Account",
                        height=Size.pixel(50),
                        width=Size.pixel(50),
                        border_radius=Size.percent(50)
                    )
                ]
            ),
            Container(
                width=Size.Viewport.width(90),
                max_width=Size.pixel(500),
                margin=Margin(
                    top=substract_style(Size.Viewport.height(50), Size.pixel(27)),
                    left=Size.auto,
                    right=Size.auto
                ),
                childs=[
                    Form(
                        method='GET',
                        childs=[
                            Textbox(
                                selector="the_box",
                                name='q',
                                placeholder="Search Web...",
                                border_radius=Size.pixel(50),
                                width=Size.percent(100),
                                max_width=Size.percent(100),
                                padding=Padding(top=Size.pixel(10), left=Size.pixel(30)),
                                css={"border": "1px solid #808080A0"},
                            )
                        ]
                    )
                ]
            )
        ]
    )
