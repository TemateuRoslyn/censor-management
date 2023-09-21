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
from components.disque import create_disque
from services.request import get_request, post_request
from ressources.configuration import api_url_usb_find_all, api_url_usb_usage


"""Je crée ici un petit DataFrame que je vais afficher dans le tableau, juste pour le test."""
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
    """Composant qui doit afficher un titre de niveau avec une taille de 30px"""
    
    return dmc.Text(title, align="center", style={"fontSize": 30})


def subTitle(subtile):
    """Composant qui doit afficher un titre de niveau 2, avec une taille de 20px"""
    
    return dmc.Text(subtile, style={"fontSize": 20}, my=10)

def create_preview_header(df):
    """Le header du tableau de previsualisation."""
    
    columns = df.columns.tolist()
    return html.Thead(html.Tr([html.Th(col) for col in columns]))


def create_preview_body(df):
    """Le body pour le preview des données lors du téléchargement"""

    values = df.values
    return html.Tbody([html.Tr([html.Td(cell) for cell in row]) for row in values])


def create_table(df=None):
    """Le composant qui doit afficher la table avec des stripe """

    return dmc.Table(
        striped=True,
        highlightOnHover=True,
        withBorder=True,
        withColumnBorders=True,
        id="preview_save_data",
    )


def render_analogic_inputs():
    """ Le composant qui doit nous rendre les entrées analogique sur la page d'acceuil"""

    return dmc.SimpleGrid(
        cols=4,
        spacing="lg",
        breakpoints=[
            {"maxWidth": 980, "cols": 3, "spacing": "md"},
            {"maxWidth": 755, "cols": 2, "spacing": "sm"},
            {"maxWidth": 600, "cols": 1, "spacing": "sm"},
        ],
        id="analogique_input_frame",
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
    """Le composant qui doit afficher les Camembergs (2)"""

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
    """Le composant qui doit afficher les different capteurs (GPS et autres)"""

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
    """Le composant qui doit afficher les deux accéléromètres, (Accéléromètre 1, Accéléromètre 2)"""

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
            create_modal(title="Paramétrer l'accéléromètre 1", id="acc_1_modal"),
            create_modal(title="Paramétrer l'accéléromètre 2", id="acc_2_modal"),
        ],
    )


def render_sauvegarde_form():
    """Le composant qui doit rendre le formulaire de sauvegarde, avec l'option de sauvegarde"""

    return dmc.Container(
        children=[
            create_sauvegarde_form(),
            dmc.Text("Prévisualisation des données.", weight=500, my=20),
            create_table(df=data_frame),
        ]
    )


def render_sensor_settings_form():
    """Le composant qui doit rendre le paramétrage des Sensors """

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
    """ Analogic Input settings form"""

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


"""Les elements de la vue systemes"""


""" Je vais un peu compliquer le code ici"""


def render_disk():
    create_disque_graph = []

    api_url_usb_find_all_ = get_request(api_url_usb_find_all)

    if api_url_usb_find_all_ is not None:
        usb_present = api_url_usb_find_all_["usb_present"]

        usb_mount_paths = api_url_usb_find_all_["usb_mount_paths"]
        message = api_url_usb_find_all_["message"]

        """Je recupère à present l'espace sur les differents disque"""
        if usb_present:
            for mount_path in usb_mount_paths:
                response = post_request(
                    api_url_usb_usage,
                    data={"mount_dir": mount_path},
                )
                values = response["values"]
                espace_libre = float(values["total"][:-3]) - float(values["used"][:-3])
                espace_occupe = values["used"][:-3]
                espace_total = values["total"]

                create_disque_graph.append(
                    html.Div(
                        create_disque(
                            id=mount_path,
                            labels=[
                                "Espace libre " + format(espace_libre, ".2f") + " GB",
                                "Espace occupé "
                                + format(float(espace_occupe), ".2f")
                                + " GB",
                            ],
                            title=mount_path + " - " + espace_total,
                            values=[espace_libre, espace_occupe],
                        )
                    )
                )

    if len(create_disque_graph) != 0:
        return dmc.SimpleGrid(
            cols=2,
            spacing="lg",
            mt=10,
            breakpoints=[
                {"maxWidth": 980, "cols": 2, "spacing": "md"},
                {"maxWidth": 755, "cols": 1, "spacing": "sm"},
                {"maxWidth": 600, "cols": 1, "spacing": "sm"},
            ],
            id="liste_disque",
            children=create_disque_graph,
        )
    else:
        return dmc.Card(
            children=[
                html.Div(
                    dmc.Text("Aucun disque n'a été détécté"),
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"width": "100%"},
        )
