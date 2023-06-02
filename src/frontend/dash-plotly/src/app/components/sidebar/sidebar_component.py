from dash import html
class SidebarComponent:
    def __init__(self) -> None:
        pass


    def render(self):
        return html.Div(
            [
                html.H1("Le Sidebar")
            ]
        )