from dash import dcc, html


class InputComponent:
    def __init__(self) -> None:
        pass

    def render(self, label: str, type: str, id: str):
        return html.Div(
            [
                html.Label(
                    label,
                    className="form-label",
                ),
                dcc.Input(type=type, className="form-control", id=id),
            ],
            className="input-style-1",
        )
