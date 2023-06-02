from dash import dcc, html

from components.sidebar import SidebarComponent
from components.navbar import NavbarComponent


class AppLayout:
    def __init__(self) -> None:
        self.sidebar = SidebarComponent()
        self.navbar = NavbarComponent()

    def render(self):
        return html.Div(
            [
                self.sidebar.render(),
                html.Main(
                    id="main-wrapper",
                    className="main-wrapper",
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=1 * 1000,
                    n_intervals=0,
                ),
                dcc.Location(
                    id="url",
                    refresh=False,
                ),
            ],
            id="app-layout",
        )
