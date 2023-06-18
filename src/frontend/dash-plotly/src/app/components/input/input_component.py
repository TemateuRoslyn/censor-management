from dash import dcc, html


class InputComponent:
    def __init__(self) -> None:
        pass

    def render(self, label: str, type: str, id: str, name=None,value=None, placeholder=None, feedback_text=None, feedback_class=None):
        return html.Div([
            html.Div(
                [
                    html.Label(
                        label,
                        className="form-label",
                    ),
                    dcc.Input(type=type, id=id, className="form-control", value=value, name=name, placeholder=placeholder),
                ],
                className="input-style-1",
            ),
            html.Div(id=id+"-feedback",children=feedback_text),
            html.Div(id=id+"-matching-feedback",children=feedback_text)
        ])
