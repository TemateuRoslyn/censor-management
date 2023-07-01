from dash import html, dcc
import dash_daq as daq


class CapteurComponent:
    def __init__(self):
        pass

    def render(self, id: str, value=0, label="Label"):
        return html.Div(
            [
                html.H6(label, className="mb-3"),
                html.Div(
                    [
                        html.Div(
                            daq.Gauge(
                                color="#006699",
                                id=id,
                                label=label,
                                value=value,
                                showCurrentValue=True,
                                units="C",
                                min=0,
                                max=200,
                            ),
                            # className="card-body",
                        ),
                        # html.Div(
                        #     html.Button("Modifier", className="btn btn-primary"),
                        #     className="card-footer",
                        # ),
                    ],
                    className="rounded pt-2 pb-0 bg-dark",
                ),
            ],
            className="card-style",
        )
