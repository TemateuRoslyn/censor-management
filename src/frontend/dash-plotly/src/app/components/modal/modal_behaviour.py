from dash import html, dcc
import dash_bootstrap_components as dbc

class ModalBehaviour:
    def __init__(self) -> object:
        pass

    def render(self, modalheadermsg, modalbody):
        return dbc.Modal(
            [dbc.ModalHeader(dbc.ModalTitle(modalheadermsg), close_button=False),
            dbc.ModalBody(
                modalbody
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "Ajouter",
                    id="close-backdrop",
                    className="ms-auto btn-secondary",
                    n_clicks=0
                )
            )],
            id="modal-behaviour",
            keyboard=False,
            is_open=False,
            backdrop='static'
        )