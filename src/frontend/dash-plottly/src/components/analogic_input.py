from dash import callback, Input, Output, dcc
import dash_mantine_components as dmc
import dash_daq as daq
from dash_iconify import DashIconify

from services.request import get_request


def run_analogic_callback(
    output_etat: str, output_valeur: str, output_actif: str, output_color: str
):
    """C'est juste pour les callback des entrées analogiques"""

    @callback(
        [
            Output(output_etat, "on"),
            Output(output_valeur, "children"),
            Output(output_actif, "children"),
            Output(output_color, "color"),
        ],
        Input("ai_interval", "n_intervals"),
        prevent_initial_call=True,
    )
    def update_analogique_input(n):
        result_ai_7 = get_request("/analogic-input")
        etat = result_ai_7["etat"]
        valeur = result_ai_7["valeur"]

        return [
            etat,
            "NaN" if valeur == 0 else valeur,
            "Inactif" if etat == False else "Actif",
            "red" if etat == False else "green",
        ]


def create_analogic_input_card(titre: str, id: str):
    """Le composant qui doit nous permettre de rendre les differentes entrées analogiques"""
    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Group(
                    children=[
                        dmc.Text(titre, weight=500),
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
            dmc.Group(
                [
                    daq.PowerButton(id=id, on=False, color="#108DE4", disabled=True),
                    dmc.Stack(
                        [
                            dmc.Text("", weight=500, id=id + "_valeur"),
                            dmc.Badge(
                                "", color="green", variant="light", id=id + "_etat"
                            ),
                        ],
                        align="center",
                        style={"width": "60%"},
                    ),
                    dcc.Interval(
                        id="ai_interval",
                        interval=9 * 1000,
                        n_intervals=0,
                    ),
                ],
                position="apart",
                mt="md",
                mb="xs",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": "100%"},
    )


"""Ici je dois mettre les callbacks pour les 8 entrées analogiques"""


run_analogic_callback(
    output_actif="ai_0_etat",
    output_color="ai_0_etat",
    output_etat="ai_0",
    output_valeur="ai_0_valeur",
)
run_analogic_callback(
    output_actif="ai_1_etat",
    output_color="ai_1_etat",
    output_etat="ai_1",
    output_valeur="ai_1_valeur",
)
run_analogic_callback(
    output_actif="ai_2_etat",
    output_color="ai_2_etat",
    output_etat="ai_2",
    output_valeur="ai_2_valeur",
)
run_analogic_callback(
    output_actif="ai_3_etat",
    output_color="ai_3_etat",
    output_etat="ai_3",
    output_valeur="ai_3_valeur",
)
run_analogic_callback(
    output_actif="ai_4_etat",
    output_color="ai_4_etat",
    output_etat="ai_4",
    output_valeur="ai_4_valeur",
)
run_analogic_callback(
    output_actif="ai_5_etat",
    output_color="ai_5_etat",
    output_etat="ai_5",
    output_valeur="ai_5_valeur",
)

run_analogic_callback(
    output_actif="ai_6_etat",
    output_color="ai_6_etat",
    output_etat="ai_6",
    output_valeur="ai_6_valeur",
)

run_analogic_callback(
    output_actif="ai_7_etat",
    output_color="ai_7_etat",
    output_etat="ai_7",
    output_valeur="ai_7_valeur",
)
