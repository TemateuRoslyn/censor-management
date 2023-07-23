from dash import (
    html,
    callback,
    Input,
    Output,
    callback_context as ctx,
    clientside_callback,
    dcc,
)
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from datetime import datetime, timedelta, date
from time import sleep

from libs.datas import data_frame


def create_sauvegarde_form():
    return html.Div(
        children=[
            dmc.SimpleGrid(
                cols=2,
                spacing="lg",
                mt=20,
                breakpoints=[
                    {"maxWidth": 980, "cols": 2, "spacing": "md"},
                    {"maxWidth": 755, "cols": 1, "spacing": "sm"},
                    {"maxWidth": 600, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    dmc.MultiSelect(
                        label="Choisir les capteurs",
                        placeholder="Selectionnez un capteur",
                        id="save_capteurs",
                        value=["Capteur 0", "Capteur 1"],
                        data=[
                            {"value": "c0", "label": "Capteur 0"},
                            {"value": "c1", "label": "Capteur 1"},
                            {"value": "c2", "label": "Capteur 2"},
                        ],
                        style={"width": "100%", "marginBottom": 10},
                    ),
                    dmc.NumberInput(
                        label="La taille des données à téléchager ",
                        style={"width": "100%"},
                        id="save_size",
                        type="number",
                        step=1,
                        min=1,
                    ),
                ],
            ),
            dmc.SimpleGrid(
                cols=1,
                spacing="lg",
                mt=10,
                breakpoints=[
                    {"maxWidth": 980, "cols": 1, "spacing": "md"},
                    {"maxWidth": 755, "cols": 1, "spacing": "sm"},
                    {"maxWidth": 600, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    dmc.DateRangePicker(
                        id="save_period",
                        label="Sélectionnez une plage de date",
                        minDate=date(2020, 8, 5),
                        style={"width": "100%"},
                        value=[
                            datetime.now().date(),
                            datetime.now().date() + timedelta(days=1),
                        ],
                    ),
                ],
            ),
            dcc.Download(id="download"),
            dmc.SimpleGrid(
                cols=3,
                spacing="lg",
                mt=20,
                breakpoints=[
                    {"maxWidth": 980, "cols": 3, "spacing": "md"},
                    {"maxWidth": 755, "cols": 3, "spacing": "sm"},
                    {"maxWidth": 600, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    dmc.Button(
                        "Télécharger en CSV",
                        leftIcon=DashIconify(
                            icon="ph:file-csv-thin",
                        ),
                        id="save_download_csv",
                        variant="outline",
                    ),
                    dmc.Button(
                        "Télécharger en TXT",
                        leftIcon=DashIconify(
                            icon="bxs:file-txt",
                        ),
                        id="save_download_txt",
                        variant="outline",
                    ),
                    dmc.Button(
                        "Télécharger en JSON",
                        leftIcon=DashIconify(
                            icon="bxs:file-json",
                        ),
                        id="save_download_json",
                        variant="outline",
                    ),
                ],
            ),
        ]
    )


def run_clientsite_callback(input: str):
    clientside_callback(
        """
        function updateLoadingState(n_clicks) {
            return true
        }
        """,
        Output(input, "loading", allow_duplicate=True),
        Input(input, "n_clicks"),
        prevent_initial_call=True,
    )


run_clientsite_callback(input="save_download_csv")
run_clientsite_callback(input="save_download_txt")
run_clientsite_callback(input="save_download_json")


def run_download_callback(input: str, type: str):
    @callback(
        Output("download", "data", allow_duplicate=True),
        Output(input, "loading"),
        Input(input, "n_clicks"),
        prevent_initial_call=True,
    )
    def download(n):
        sleep(5)
        if type == "CSV":
            return (
                dcc.send_data_frame(
                    data_frame.to_csv, filename=str(datetime.now()) + "data_save.csv"
                ),
                False,
            )
        elif type == "JSON":
            return (
                dcc.send_data_frame(
                    data_frame.to_json, filename=str(datetime.now()) + "data_save.json"
                ),
                False,
            )
        elif type == "TXT":
            return (
                dcc.send_string(
                    data_frame.to_string, filename=str(datetime.now()) + "data_save.txt"
                ),
                False,
            )


run_download_callback(input="save_download_csv", type="CSV")
run_download_callback(input="save_download_json", type="JSON")
run_download_callback(input="save_download_txt", type="TXT")
