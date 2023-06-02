from dash import html


class ButtonComponent:
    def __init__(self) -> None:
        pass

    def render(self, title: str, type: str):
        if type is not None:
            return html.Button(title, className="main-btn " + type)
        return html.Button(title, className="main-btn primary-btn")
