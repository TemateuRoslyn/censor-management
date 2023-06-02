from dash import dcc, html

from components.navbar import NavbarComponent
from components.sidebar import SidebarComponent

class AppLayout:
    def __init__(self) -> None:
        self.navbar = NavbarComponent()
        self.sidebar = SidebarComponent()

    def render(self):
        return html.Div(
            children=[
                self.navbar.render(),
                self.sidebar.render(),
                dcc.Interval(
                    id='interval-component',
                    interval=1*1000,
                    n_intervals=0
                )
            ],
            id='app-layout',
        )