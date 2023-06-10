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
                dcc.Input(type=type, id=id, className="form-control", value=None),
            ],
            className="input-style-1",
        )
