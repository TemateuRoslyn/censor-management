from dash import html, dcc
import dash_daq as daq
import dash_mantine_components as dmc
from dash_iconify import DashIconify


class CapteurComponent:
    def __init__(self):
        pass

    def render(self, id: str, value=0, label="Label"):
        return html.Div(
            [
                html.Div(
                    [
                        html.H6(label),
                        dmc.ActionIcon(
                            DashIconify(icon="clarity:settings-line", width=15),
                            size="md",
                            variant="outline",
                            id=id + "_modal_btn",
                            n_clicks=0,
                            mb=1,
                        ),
                    ],
                    className="mb-3 d-flex justify-content-between",
                ),
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
                        ),
                    ],
                    className="rounded pt-2 pb-0 bg-dark",
                ),
                dcc.Interval(
                    id=id + "_interval",
                    n_intervals=0,
                    interval=1 * 1000,
                ),
            ],
            className="card-style",
        )
