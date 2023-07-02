from dash import Input, Output

class ModalCallback:
    def __init__(self, app) -> None:
        self.app = app
    def closeModalCallback(self):
        @self.app.callback(
            Output(component_id="modal-backdrop", component_property="is_open"),
            [
                Input(component_id="close-backdrop", component_property="n_clicks"),
            ]
        )
        def closeModal(clicks):
            if clicks > 0:
                return False
            return True