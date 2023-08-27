import dash_mantine_components as dmc
from dash import html
from datetime import datetime, date, timedelta
from dash_iconify import DashIconify
import pandas as pd

from components.analogic_input import create_analogic_input_card
from components.camemberg import create_camemberg
from components.capteur import create_capteur
from components.accelerometre import create_accelerometre
from components.modal import create_modal, create_modal_ai
from components.sauvegarde_form import create_sauvegarde_form

"""Je crée ici un petit DataFrame que je vais afficher dans le tableau"""
datas = {
    "ID": [0, 1, 2, 3, 4],
    "Capteur": ["Capteur 0", "Capteur 1", "Capteur 2", "Capteur 3", "Capteur 4"],
    "Unité": ["C/M", "KG", "M", "C", "M"],
    "Valeur": [10, 2, 0.5, 4, 6],
}

data_frame = pd.DataFrame(datas)


"""Ici les donnees pour les entrees analogique concernant la page de sauvegarde"""
list_entree_analogiques = [
    "Entrée analogique 01",
    "Entrée analogique 02",
    "Entrée analogique 03",
    "Entrée analogique 04",
    "Entrée analogique 05",
    "Entrée analogique 06",
    "Entrée analogique 07",
]
type_capteurs = [
    "Accéléromètre",
    "Microphone",
]

list_unite = [
    "G",
    "Metre carré / seconde",
    "Inches / seconde carré",
]


def title(title):
    return dmc.Text(title, align="center", style={"fontSize": 30})


"""Le header du tableau de previsualisation."""


def create_preview_header(df):
    columns = df.columns.tolist()
    return html.Thead(html.Tr([html.Th(col) for col in columns]))


def create_preview_body(df):
    values = df.values
    return html.Tbody([html.Tr([html.Td(cell) for cell in row]) for row in values])


def create_table(df):
    header = create_preview_header(df)
    body = create_preview_body(df)
    return dmc.Table(
        striped=True,
        highlightOnHover=True,
        withBorder=True,
        withColumnBorders=True,
        children=[header, body],
    )


def render_analogic_inputs():
    return dmc.SimpleGrid(
        cols=4,
        spacing="lg",
        breakpoints=[
            {"maxWidth": 980, "cols": 3, "spacing": "md"},
            {"maxWidth": 755, "cols": 2, "spacing": "sm"},
            {"maxWidth": 600, "cols": 1, "spacing": "sm"},
        ],
        children=[
            html.Div(create_analogic_input_card(id="ai_0", titre="Analogic input 0")),
            html.Div(create_analogic_input_card(id="ai_1", titre="Analogic input 1")),
            html.Div(create_analogic_input_card(id="ai_2", titre="Analogic input 2")),
            html.Div(create_analogic_input_card(id="ai_3", titre="Analogic input 3")),
            html.Div(create_analogic_input_card(id="ai_4", titre="Analogic input 4")),
            html.Div(create_analogic_input_card(id="ai_5", titre="Analogic input 5")),
            html.Div(create_analogic_input_card(id="ai_6", titre="Analogic input 6")),
            html.Div(create_analogic_input_card(id="ai_7", titre="Analogic input 7")),
            create_modal_ai(title="Paramétrer l'entrée analogique", id="ai_0_modal"),
        ],
    )


def render_camemberg_graph():
    return dmc.SimpleGrid(
        cols=2,
        spacing="lg",
        mt=10,
        breakpoints=[
            {"maxWidth": 980, "cols": 2, "spacing": "md"},
            {"maxWidth": 755, "cols": 1, "spacing": "sm"},
            {"maxWidth": 600, "cols": 1, "spacing": "sm"},
        ],
        children=[
            html.Div(create_camemberg()),
            html.Div(create_camemberg()),
        ],
    )


def render_capteurs_graph():
    return dmc.SimpleGrid(
        cols=2,
        spacing="lg",
        mt=10,
        breakpoints=[
            {"maxWidth": 980, "cols": 2, "spacing": "md"},
            {"maxWidth": 755, "cols": 1, "spacing": "sm"},
            {"maxWidth": 600, "cols": 1, "spacing": "sm"},
        ],
        children=[
            html.Div(create_capteur(id="capteur_1", label="Capteur 1", value=0)),
            html.Div(create_capteur(id="capteur_gps", label="Capteur GPS", value=0)),
            create_modal(title="Parametrer le capteur 1", id="capteur_1_modal"),
            create_modal(title="Parametrer le capteur GPS", id="capteur_gps_modal"),
        ],
    )


def render_accelerometre_graph():
    return dmc.SimpleGrid(
        cols=1,
        spacing="lg",
        mt=10,
        breakpoints=[
            {"maxWidth": 980, "cols": 1, "spacing": "md"},
            {"maxWidth": 755, "cols": 1, "spacing": "sm"},
            {"maxWidth": 600, "cols": 1, "spacing": "sm"},
        ],
        children=[
            html.Div(create_accelerometre(id="acc_1", label="Accéléromètre 1")),
            html.Div(create_accelerometre(id="acc_2", label="Accéléromètre 2")),
            create_modal(title="Parametrer l'accélérometre 1", id="acc_1_modal"),
            create_modal(title="Parametrer l'accélérometre 2", id="acc_2_modal"),
        ],
    )


def render_sauvegarde_form():
    return dmc.Container(
        children=[
            create_sauvegarde_form(),
            dmc.Text("Prévisualisation des données.", weight=500, my=20),
            create_table(df=data_frame),
        ]
    )


def render_sensor_settings_form():
    return dmc.Container(
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
                    dmc.Select(
                        data=list_entree_analogiques,
                        searchable=False,
                        style={"width": "100%"},
                        id="",
                        label="Selectionnez l'entrée analigique :",
                        value=list_entree_analogiques[0],
                    ),
                    dmc.TextInput(
                        label="Entrez la sensitivité :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                        type="number",
                    ),
                ],
            ),
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
                    dmc.Select(
                        data=list_unite,
                        searchable=False,
                        style={"width": "100%"},
                        id="",
                        label="Selectionnez l'unité de la sensitivité :",
                        value=list_unite[0],
                    ),
                    dmc.Select(
                        data=type_capteurs,
                        searchable=False,
                        style={"width": "100%"},
                        id="",
                        label="Type du capteur :",
                        value=type_capteurs[0],
                    ),
                ],
            ),
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
                    dmc.TextInput(
                        label="Entrez le nom du capteur :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                        type="text",
                    ),
                    dmc.Select(
                        data=list_unite,
                        searchable=False,
                        style={"width": "100%"},
                        id="",
                        label="Unité :",
                        value=list_unite[0],
                    ),
                ],
            ),
            dmc.SimpleGrid(
                cols=4,
                spacing="lg",
                mt=20,
                breakpoints=[
                    {"maxWidth": 980, "cols": 1, "spacing": "md"},
                    {"maxWidth": 755, "cols": 1, "spacing": "sm"},
                    {"maxWidth": 600, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    dmc.Button(
                        "Valider",
                        variant="outline",
                        leftIcon=DashIconify(icon="fluent:settings-32-regular"),
                    ),
                ],
            ),
        ]
    )


def render_ai_settings_form():
    return dmc.Container(
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
                    dmc.Select(
                        data=list_entree_analogiques,
                        searchable=False,
                        style={"width": "100%"},
                        id="",
                        label="Selectionnez l'entrée analigique :",
                        value=list_entree_analogiques[0],
                    ),
                    dmc.TextInput(
                        label="Nouveau nom de la voie :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                        type="text",
                    ),
                ],
            ),
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
                    dmc.NumberInput(
                        label="Frequence d'échantillonage :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                        min=0,
                        precision=2,
                    ),
                    dmc.Select(
                        data=list_unite,
                        searchable=False,
                        style={"width": "100%"},
                        id="",
                        label="Selectionnez une unité :",
                        value=list_unite[0],
                    ),
                ],
            ),
            dmc.SimpleGrid(
                cols=3,
                spacing="lg",
                mt=20,
                breakpoints=[
                    {"maxWidth": 980, "cols": 2, "spacing": "md"},
                    {"maxWidth": 755, "cols": 1, "spacing": "sm"},
                    {"maxWidth": 600, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    dmc.NumberInput(
                        label="Offset :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                        min=0,
                        precision=2,
                    ),
                    dmc.TextInput(
                        style={"width": "100%"},
                        id="",
                        label="Gain :",
                    ),
                    dmc.TextInput(
                        label="Numéro de série :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                    ),
                ],
            ),
            dmc.SimpleGrid(
                cols=4,
                spacing="lg",
                mt=20,
                breakpoints=[
                    {"maxWidth": 980, "cols": 1, "spacing": "md"},
                    {"maxWidth": 755, "cols": 1, "spacing": "sm"},
                    {"maxWidth": 600, "cols": 1, "spacing": "sm"},
                ],
                children=[
                    dmc.Button(
                        "Valider",
                        variant="outline",
                        leftIcon=DashIconify(icon="fluent:settings-32-regular"),
                    ),
                ],
            ),
        ]
    )
