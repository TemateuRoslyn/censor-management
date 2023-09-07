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
    api_url_mongo_find_session, 
    session_name
)


def create_preview_header(df):
    columns = df.columns.tolist()
    return html.Thead(html.Tr([html.Th(col) for col in columns]))


def create_preview_body(df):
    values = df.values
    return html.Tbody([html.Tr([html.Td(cell) for cell in row]) for row in values])


def create_sauvegarde_form():
    # Je dois recuperer la liste des sessions ici
    sessions_list = []
    tableau_json = []

    params = {
        "url": mongo_url,
        "db": mongo_db,
        "username": mongo_username,
        "password": mongo_password,
        "collection_name": session_name,
        "query": "nan",
    }

    sessions = post_request(api_url_mongo_find_session, data=params)

    if(sessions is not None): 
        results = sessions['results']

        for el in results:
            objet_json = json.loads(el)
            tableau_json.append(objet_json)

        for table in tableau_json: 
            start= datetime.fromisoformat(table["start_session"])
            end= datetime.fromisoformat(table["end_session"])
            new_val = {
                "value": table["start_session"] + "," + table["end_session"] , 
                "label": table["description"] + " du " + start.strftime("%d/%m/%Y %H:%M:%S") + " au " + end.strftime("%d/%m/%Y %H:%M:%S")
            }
            sessions_list.append(new_val)

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
                cols=2,
                spacing="lg",
                mt=10,
                breakpoints=[
                    {"maxWidth": 980, "cols": 2, "spacing": "md"},
                    {"maxWidth": 755, "cols": 1, "spacing": "sm"},
                    {"maxWidth": 600, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    dmc.DateRangePicker(
                        id="save_period",
                        label="Sélectionnez une plage de date",
                        minDate=date(2023, 8, 5),
                        style={"width": "100%"},
                        value=[
                            datetime.now().date(),
                            datetime.now().date() + timedelta(days=1),
                        ],
                    ),
                    dmc.Select(
                        label="Sélectionnez la session",
                        placeholder="Selectionnez une session",
                        id="session",
                        data=sessions_list,
                        value=sessions_list[0],
                        style={"width": "100%", "marginBottom": 10},
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
        Input("session", 'value'),
        prevent_initial_call=True,
    )
    def download(n, session_date_interval):
        
        date_parts = session_date_interval.split(',')
        
        start_session = date_parts[0]
        end_session = date_parts[1]

        liste_json = {}
        params = {
            "url": mongo_url,
            "db": mongo_db,
            "username": mongo_username,
            "password": mongo_password,
            "collection_name": mongo_collection_name,
            "query": "nan",
            "projection": {
                "_id": 0, 
                "time_start":0, 
                "time_stop":0, 
                "rate":1, 
                "values":1
            }
        }

        if start_session is not None:
            params["start_session"] = start_session

        if end_session is not None:
            params["end_session"] = end_session
        
        result = post_request(route=api_url_mongo_find_all, data=params)

        if result is not None:
            values = result["values"]
            for value in values:
                json_values = json.loads(value)
                liste_json.update(json_values["values"])

            df = pd.DataFrame(liste_json)

            if type == "CSV":
                return (
                    dcc.send_data_frame(
                        df.to_csv,
                        filename=str(datetime.now()) + "data_save.csv",
                    ),
                    False,
                    (create_preview_header(df.head(10)), create_preview_body(df.head(10))),
                )
            elif type == "JSON":
                return (
                    dcc.send_data_frame(
                        df.to_json,
                        filename=str(datetime.now()) + "data_save.json",
                    ),
                    False,
                    (create_preview_header(df.head(10)), create_preview_body(df.head(10))),
                )
            elif type == "TXT":
                return (
                    dcc.send_string(
                        df.to_string,
                        filename=str(datetime.now()) + "data_save.txt",
                    ),
                    False,
                    (create_preview_header(df.head(10)), create_preview_body(df.head(10))),
                )
        else:
            return


run_download_callback(input="save_download_csv", type="CSV")
run_download_callback(input="save_download_json", type="JSON")
run_download_callback(input="save_download_txt", type="TXT")
