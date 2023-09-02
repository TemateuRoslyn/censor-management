from dash import callback, Input, Output, dcc
import dash_mantine_components as dmc
import dash_daq as daq
from dash_iconify import DashIconify

from services.request import post_request

from ressources.configuration import (
    api_ni_read_all,
    buffer_size,
    channels,
    device,
    host,
    period,
    rate,
    sample_size,
)


def run_analogic_callback(
    output_etat: str,
    output_valeur: str,
    output_actif: str,
    output_color: str,
    position: int,
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
        data_ai = {
            "host": host,
            "period": period,
            "rate": rate,
            "buffer_size": buffer_size,
            "sample_size": sample_size,
            "device": device,
            "channels": channels,
        }

        values = post_request(api_ni_read_all, data=data_ai)

        if values is not None:
            valeur = values["values"]["values"][position]
            channel = values["values"]["channels"][position]

            if valeur is not None:
                return [
                    False if valeur == None else True,
                    "NaN" if valeur == None else format(valeur[0], ".3f"),
                    "Inactif" if valeur == None else "Actif",
                    "red" if valeur == None else "green",
                ]

                # Dans le cas contraire
            else:
                return [
                    False,
                    "NaN",
                    "Inactif",
                    "red",
                ]
        else:
            return [
                False,
                "NaN",
                "Inactif",
                "red",
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
                        interval=10 * 1000,
                        n_intervals=1,
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
    position=0,
)
run_analogic_callback(
    output_actif="ai_1_etat",
    output_color="ai_1_etat",
    output_etat="ai_1",
    output_valeur="ai_1_valeur",
    position=1,
)
run_analogic_callback(
    output_actif="ai_2_etat",
    output_color="ai_2_etat",
    output_etat="ai_2",
    output_valeur="ai_2_valeur",
    position=2,
)
run_analogic_callback(
    output_actif="ai_3_etat",
    output_color="ai_3_etat",
    output_etat="ai_3",
    output_valeur="ai_3_valeur",
    position=3,
)
run_analogic_callback(
    output_actif="ai_4_etat",
    output_color="ai_4_etat",
    output_etat="ai_4",
    output_valeur="ai_4_valeur",
    position=4,
)
run_analogic_callback(
    output_actif="ai_5_etat",
    output_color="ai_5_etat",
    output_etat="ai_5",
    output_valeur="ai_5_valeur",
    position=5,
)
run_analogic_callback(
    output_actif="ai_6_etat",
    output_color="ai_6_etat",
    output_etat="ai_6",
    output_valeur="ai_6_valeur",
    position=6,
)
run_analogic_callback(
    output_actif="ai_7_etat",
    output_color="ai_7_etat",
    output_etat="ai_7",
    output_valeur="ai_7_valeur",
    position=7,
)
