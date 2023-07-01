from dash import html, dcc


class InputGroup:
    def __init__(self) -> object:
        pass

    def render(
        self,
        id: str,
        value: None,
        type="text",
        placeholder=None,
        min=None,
        max=None,
        pattern=None,
        label=None,
        onchange=None,
    ):
        return html.Div(
            id="",
            className="input-group mb-3",
            children=[
                html.Span(id="", className="input-group-text", children=label),
                dcc.Input(
                    id=id,
                    value=value,
                    type=type,
                    debounce=onchange,
                    placeholder=placeholder,
                    min=min,
                    max=max,
                    className="form-control",
                    pattern=pattern,
                ),
            ],
        )
