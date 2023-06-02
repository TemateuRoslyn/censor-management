from dash import html


class DividerComponent:
    def __init__(self) -> None:
        pass

    def render(self):
        return html.Span(
            html.Hr(),
            className="divider",
        )
