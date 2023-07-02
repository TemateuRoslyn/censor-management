from dash import html, dcc
import dash_bootstrap_components as dbc

class ModalBackdrop:
    def __init__(self) -> object:
        pass

    def render(self, modalheadermsg, modalbody, isopen):
        return dbc.Modal(
            [dbc.ModalHeader(dbc.ModalTitle(modalheadermsg), close_button=True),
            dbc.ModalBody(
                modalbody
            ),
            dbc.ModalFooter(
                dbc.Button(
                    "close",
                    id="close-backdrop",
                    className="ms-auto btn-secondary",
                    n_clicks=0
                )
            )],
            id="modal-backdrop",
            is_open=isopen
        )