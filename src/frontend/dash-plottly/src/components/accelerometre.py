from dash import dcc, Output, Input, callback
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta
import math as m

from services.request import get_request

UPDATE_INTERVAL = 1

np.random.seed(1)
N = 1000
random_x = np.linspace(0, 10, N)
random_y = np.random.randn(N)
Y = []


def create_figure(x, y, name=None):
    return go.Figure(
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
    )


def create_accelerometre(id: str, label="Graph", x=random_x, y=random_y):
    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Group(
                    children=[
                        dmc.Text(label, weight=500),
                        dmc.ActionIcon(
                            DashIconify(icon="clarity:settings-line", width=15),
                            size="md",
                            variant="outline",
                            id=id + "_modal_btn",
                            n_clicks=0,
                            mb=1,
                        ),
                    ],
                    position="apart",
                ),
                withBorder=True,
                inheritPadding=True,
                py="xs",
            ),
            dcc.Interval(
                id=id + "_interval",
                n_intervals=0,
                interval=1 * 1000,
            ),
            dmc.CardSection(
                dcc.Graph(
                    config={
                        "staticPlot": False,
                        "editable": False,
                        "displayModeBar": False,
                    },
                    figure=create_figure(x=x, name=label, y=y),
                    id=id,
                ),
                style={"background-color": "#212529"},
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": "100%"},
    )


def run_callback_accelerometre(acc_id: str, interval: str, mul: str):
    @callback(
        Output(acc_id, "figure"), Input(interval, "n_intervals"), Input(mul, "value")
    )
    def update_catpteur(n, mul):
        datas = get_request("/acc2/next")
        x = [
            datetime.now() + timedelta(seconds=i * UPDATE_INTERVAL)
            for i in range(n + 1)
        ]
        if datas is not None:
            value = datas["time "]
            Y.append(int(float(mul) * value))

            return create_figure(y=Y[-100:], x=x, name="Accélérometre")
        return


def run_interval_callback(output: str, input: str):
    @callback(
        Output(output, "interval"),
        Input(input, "value"),
    )
    def update_interval(value: float):
        return m.floor(float(value)) * 1000


# run_interval_callback(output="acc_1_interval", input="acc_1_modal_freq")
# run_interval_callback(output="acc_2_interval", input="acc_2_modal_freq")

# run_callback_accelerometre(
#     acc_id="acc_1", interval="acc_1_interval", mul="acc_1_modal_mul"
# )
# run_callback_accelerometre(
#     acc_id="acc_2", interval="acc_2_interval", mul="acc_2_modal_mul"
# )
