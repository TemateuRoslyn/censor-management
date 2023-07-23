import dash_mantine_components as dmc
from dash import dcc, Input, callback, Output
from dash_iconify import DashIconify
import dash_daq as daq
import math as m
from services.request import get_request


def run_capteur_callback(capteur_id: str, capteur_interval: str, capteur_mul: str):
    @callback(
        Output(capteur_id, "value"),
        Input(capteur_interval, "n_intervals"),
        Input(capteur_mul, "value"),
        prevent_initial_call=True,
    )
    def update_capteur(n, mul: int):
        datas = get_request("/acc2/next")
        value: int = datas["time "]
        return int(float(mul) * value)


def run_interval_callback(output: str, input: str):
    @callback(
        Output(output, "interval"),
        Input(input, "value"),
    )
    def update_interval(value: float):
        return m.floor(float(value)) * 1000


def create_capteur(id: str, value=0, label="Label"):
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
                daq.Gauge(
                    color="#006699",
                    id=id,
                    label=label,
                    value=10,
                    showCurrentValue=True,
                    units="C/d",
                    min=0,
                    max=200,
                ),
                style={"background-color": "#212529"},
                pt=10,
                pb=0,
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": "100%"},
    )


run_capteur_callback(
    capteur_id="capteur_1",
    capteur_interval="capteur_1_interval",
    capteur_mul="capteur_1_modal_mul",
)

run_capteur_callback(
    capteur_id="capteur_gps",
    capteur_interval="capteur_gps_interval",
    capteur_mul="capteur_gps_modal_mul",
)


run_interval_callback(output="capteur_1_interval", input="capteur_1_modal_freq")
run_interval_callback(output="capteur_gps_interval", input="capteur_gps_modal_freq")
