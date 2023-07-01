from dash import html, Input, Output, State, dcc


class SauvegardesCallback:
    def __init__(self, app) -> None:
        self.app = app

    def register(self):
        @self.app.callback(
            Output("download_data", "data"),
            Input("svg_download", "n_clicks"),
            [
                State("svg_capteur", "value"),
                State("svg_format", "value"),
                State("svg_date_begin", "value"),
                State("svg_date_end", "value"),
                State("svg_size", "value"),
            ],
            prevent_initial_call=True,
        )
        def register_callback(
            svg_capteur,
            svg_format,
            svg_date_begin,
            svg_date_end,
            svg_size,
            svg_download,
        ):
            print(
                svg_capteur,
                svg_format,
                svg_date_begin,
                svg_date_end,
                svg_size,
                svg_download,
            )
            return dcc.send_file("https://cm.linkedin.com/in/rushclin-takam-1601a6213")
