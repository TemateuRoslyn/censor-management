from dash import html, dcc


class ButtonComponent:
    def __init__(self) -> None:
        pass

    def render(self, title: str, type: None, id: str):
        if type is not None:
            return html.Button(
                title,
                className="main-btn " + type,
                id=id,
            )
        return html.Button(
            title,
            className="main-btn primary-btn",
            id=id,
        )
