import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import callback, Input, Output, State


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


run_callback_modal(
    input_btn="capteur_1_modal_btn",
    input_btn_close="capteur_1_modal_close",
    output_modal="capteur_1_modal",
)

run_callback_modal(
    input_btn="acc_1_modal_btn",
    input_btn_close="acc_1_modal_close",
    output_modal="acc_1_modal",
)

run_callback_modal(
    input_btn="capteur_gps_modal_btn",
    input_btn_close="capteur_gps_modal_close",
    output_modal="capteur_gps_modal",
)

run_callback_modal(
    input_btn="acc_2_modal_btn",
    input_btn_close="acc_2_modal_close",
    output_modal="acc_2_modal",
)
