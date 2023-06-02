from dash import Output, Input, State, dash, ctx

from layouts.app_layout import AppLayout


class LoginCallback:
    def __init__(self, app) -> None:
        self.app = app
        self.app_layout = AppLayout()

    def register(self):
        @self.app.callback(
            Output("main-wrapper", "children", allow_duplicate=True),
            Input("login", "n_clicks"),
            Input("email", "value"),
            Input("password", "value"),
            # [State("login", "prevent_default")],
        )
        def login_callback(n_clicks, email, password):
            return
            # if n_clicks is not None:
            #     button_id = ctx.triggered_id if not None else "No clicks"
            #     if button_id == "login":
            #         print("k, ", email, " ", password)
            #         if email == "takamrushclin@gmail.com" and password == "toutoupere":
            #             return self.app_layout.render()
            #         return self.app_layout.render()
