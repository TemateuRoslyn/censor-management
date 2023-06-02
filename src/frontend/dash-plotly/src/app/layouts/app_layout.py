from dash import dcc, html

from components.navbar import NavbarComponent


class AppLayout:
    def __init__(self) -> None:
        self.navbar = NavbarComponent()

    def render(self):
        return html.Div(
            [
                # self.sidebar.render(),
                html.Main(
                    id="main-wrapper",
                    className="main-wrapper p-0 bg-dark m-0",
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=1 * 1000,
                    n_intervals=0,
                ),
                dcc.Location(
                    id="url",
                    refresh=True,
                ),
            ],
            id="app-layout",
            className='bg-dark'
        )
