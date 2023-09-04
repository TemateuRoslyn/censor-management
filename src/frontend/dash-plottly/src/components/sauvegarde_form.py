from dash import (
    html,
    callback,
    Input,
    Output,
    clientside_callback,
    dcc,
)
import pandas as pd
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from datetime import datetime, timedelta, date
from time import sleep
import json

from services.request import post_request
from ressources.configuration import (
    api_url_mongo_find_all,
    mongo_url,
    mongo_db,
    mongo_collection_name,
    mongo_password,
    mongo_username,
)


def create_preview_header(df):
    columns = df.columns.tolist()
    return html.Thead(html.Tr([html.Th(col) for col in columns]))


def create_preview_body(df):
    values = df.values
    return html.Tbody([html.Tr([html.Td(cell) for cell in row]) for row in values])


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
        Output("preview_save_data", "children", allow_duplicate=True),
        Input(input, "n_clicks"),
        prevent_initial_call=True,
    )
    def download(n):
        liste_json = []
        prarams = {
            "url": mongo_url,
            "db": mongo_db,
            "username": mongo_username,
            "password": mongo_password,
            "collection_name": mongo_collection_name,
            "query": {},
        }
        result = post_request(route=api_url_mongo_find_all, data=prarams)

        if result is not None:
            values = result["values"]
            for value in values:
                json_values = json.loads(value)
                liste_json.append(json_values["values"])

            df = pd.DataFrame(liste_json)

            if type == "CSV":
                return (
                    dcc.send_data_frame(
                        df.to_csv,
                        filename=str(datetime.now()) + "data_save.csv",
                    ),
                    False,
                    (create_preview_header(df.head()), create_preview_body(df.head())),
                )
            elif type == "JSON":
                return (
                    dcc.send_data_frame(
                        df.to_json,
                        filename=str(datetime.now()) + "data_save.json",
                    ),
                    False,
                    (create_preview_header(df.head()), create_preview_body(df.head())),
                )
            elif type == "TXT":
                return (
                    dcc.send_string(
                        df.to_string,
                        filename=str(datetime.now()) + "data_save.txt",
                    ),
                    False,
                    (create_preview_header(df.head()), create_preview_body(df.head())),
                )
        else:
            return


run_download_callback(input="save_download_csv", type="CSV")
run_download_callback(input="save_download_json", type="JSON")
run_download_callback(input="save_download_txt", type="TXT")
