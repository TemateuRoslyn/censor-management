from dash import Input, Output, no_update

class FullModalCallback:
    def __init__(self, app) -> None:
        self.app = app
    def closeFullModalCallback(self):
        @self.app.callback(
            Output(component_id="modal-full", component_property="is_open"),
            [
                Input(component_id="show-full-1", component_property="n_clicks"),
            ]
        )
        def closeFullModal(n2):
            if n2:
                return True 
            return no_update