from dash import html, dcc
import dash_daq as daq


class AnalogicInput:
    def __init__(self) -> None:
        pass

    def render(self, title: str, etat: str, id: str):
        return html.Div(
            [
                html.Div(
                    daq.PowerButton(
                        id=id,
                        on=True,
                        color="#108DE4",
                        disabled=True,
                    ),
                    className="px-2",
                ),
                html.Div(
                    [
                        html.H6(title, className="mb-1 ", id=id + "_title"),
                        html.H3("NaN", className="text-bold", id=id + "_valeur"),
                        html.Small(
                            etat,
                            id=id + "_etat",
                            className="text-success text-small",
                        ),
                        dcc.Interval(
                            id="ai_interval",
                            interval=9 * 1000,
                            n_intervals=0,
                        ),
                    ],
                    className="content mx-2",
                ),
            ],
            className="icon-card md-4 mb-2",
        )
