import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import callback, Input, Output, State

# Définition des constantes
list_unite = [
    "G",
    "Metre carré / seconde",
    "Inches / seconde carré",
]


def create_modal(title: str, id: str):
    return dmc.Modal(
        title=title,
        id=id,
        centered=True,
        zIndex=10000,
        children=[
            dmc.NumberInput(
                label="Entrez la fréquence de récupération (en secondes)",
                id=id + "_freq",
                value=1,
                min=1,
                step=1,
            ),
            dmc.NumberInput(
                label="Multiplicateur",
                id=id + "_mul",
                value=1,
                min=1,
                step=1,
            ),
            dmc.Button(
                "Valider",
                leftIcon=DashIconify(icon="fluent:database-plug-connected-20-filled"),
                variant="outline",
                mt=5,
                id=id + "_close",
            ),
        ],
    )


# Ici, je vais ecrire le code du composant de modal qui doit permettre de parametrer les entrées analogiques
def create_modal_ai(title: str, id: str):
    return dmc.Modal(
        title=title,
        id=id,
        centered=True,
        zIndex=10000,
        size="lg",
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
                    dmc.TextInput(
                        label="Nouveau nom de la voie :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                        type="text",
                    ),
                    dmc.NumberInput(
                        label="Frequence d'échantillonage :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                        min=0,
                        precision=2,
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
                        label="Selectionnez une unité :",
                        value=list_unite[0],
                    ),
                    dmc.NumberInput(
                        label="Offset :",
                        style={"width": "100%"},
                        # error="Valeur invalide",
                        id="",
                        min=0,
                        precision=2,
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
                        leftIcon=DashIconify(
                            icon="fluent:database-plug-connected-20-filled"
                        ),
                        variant="outline",
                        mt=5,
                        id=id + "_close",
                    ),
                ],
            ),
        ],
    )


def run_callback_modal(output_modal: str, input_btn: str, input_btn_close: str):
    @callback(
        Output(output_modal, "opened"),
        [
            Input(input_btn, "n_clicks"),
            Input(input_btn_close, "n_clicks"),
        ],
        State(output_modal, "opened"),
        prevent_initial_call=True,
    )
    def toogle_modal(n_clicks, closed, opened):
        return not opened


# Le calnack pour le modal des AI
def run_calback_modal_ai(output_modal: str, input_btn: str, input_btn_close: str):
    @callback(
        Output(output_modal, "opened"),
        [
            Input(input_btn, "n_clicks"),
            Input(input_btn_close, "n_clicks"),
        ],
        State(output_modal, "opened"),
        prevent_initial_call=True,
    )
    def toggle_modal_ai(n_click, closed, opened):
        return not opened


# run_callback_modal(
#     input_btn="capteur_1_modal_btn",
#     input_btn_close="capteur_1_modal_close",
#     output_modal="capteur_1_modal",
# )

# run_callback_modal(
#     input_btn="acc_1_modal_btn",
#     input_btn_close="acc_1_modal_close",
#     output_modal="acc_1_modal",
# )

# run_callback_modal(
#     input_btn="capteur_gps_modal_btn",
#     input_btn_close="capteur_gps_modal_close",
#     output_modal="capteur_gps_modal",
# )

# run_callback_modal(
#     input_btn="acc_2_modal_btn",
#     input_btn_close="acc_2_modal_close",
#     output_modal="acc_2_modal",
# )


# # J'execute donc ces differents callbacks
run_calback_modal_ai(
    input_btn="ai_0_modal_btn",
    input_btn_close="ai_0_modal_close",
    output_modal="ai_0_modal",
)
