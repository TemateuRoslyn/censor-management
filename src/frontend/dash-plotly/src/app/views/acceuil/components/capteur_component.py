from dash import html, dcc
import dash_daq as daq


class CapteurComponent:
    def __init__(self):
        pass

    def render(self, id: str, value=0, label="Label"):
        return html.Div(
            [
                # html.Div(html.H1("Hello"), className="card-header"),
                html.Div(
                    daq.Gauge(
                        color="#006699",
                        id=id,
                        label=label,
                        value=value,
                        showCurrentValue=True,
                        units="m.s",
                        min=0,
                        max=200,
                    ),
                    className="card-body",
                ),
                html.Div(
                    html.Button("Button", className="btn btn-primary"),
                    className="card-footer",
                ),
            ],
            className="card rounded-corner pt-2 pb-0",
        )
