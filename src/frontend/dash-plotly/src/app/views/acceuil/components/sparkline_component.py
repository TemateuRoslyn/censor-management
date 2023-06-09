from dash import dcc, html
import plotly.graph_objs as go
import numpy as np
import dash_mantine_components as dmc
from dash_iconify import DashIconify

np.random.seed(1)


class SparkLineComponent:
    def __init__(self) -> None:
        self.N = 1000
        self.random_x = np.linspace(0, 10, self.N)
        self.random_y = np.random.randn(self.N)

    def render(self, id: str, x=None, y=None, name="Graph"):
        if x is None:
            x = self.random_x
        if y is None:
            array = []
            array = [0 for i in range(2)]
            y = array
        fig = dcc.Graph(
            config={
                "staticPlot": False,
                "editable": False,
                "displayModeBar": False,
            },
            id=id,
            figure=go.Figure(
                {
                    "data": [
                        {
                            "x": x,
                            "y": y,
                            "mode": "lines+markers",
                            "name": name,
                            "line": {"color": "#f4d44d"},
                        }
                    ],
                    "layout": {
                        "xaxis": dict(showline=False, showgrid=False, zeroline=False),
                        "yaxis": dict(showgrid=False, showline=False, zeroline=False),
                        "autosize": True,
                        "showlegend": True,
                        "paper_bgcolor": "rgba(0,0,0,0)",
                        "plot_bgcolor": "rgba(0,0,0,0)",
                        "font": {"color": "white"},
                        "height": 300,
                        "uirevision": True,
                        "margin": dict(l=0, r=0, t=4, b=4, pad=4),
                        "uirevision": True,
                    },
                }
            ),
            className="py-2 px-4 bg-dark rounded",
        )

        return html.Div(
            [
                html.Div(
                    [
                        html.H6(name, className="mb-3"),
                        dmc.ActionIcon(
                            DashIconify(icon="clarity:settings-line", width=15),
                            size="md",
                            variant="outline",
                            id=id + "_modal_btn",
                            n_clicks=0,
                            mb=1,
                        ),
                        dcc.Interval(
                            id=id + "_interval",
                            n_intervals=0,
                            interval=1 * 1000,
                        ),
                    ],
                    className="mb-3 d-flex justify-content-between",
                ),
                fig,
            ],
            className="card-style",
        )
