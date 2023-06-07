from dash import html
from components.button.button_component import ButtonComponent
from components.input.input_component import InputComponent


class LoginView:
    def __init__(self) -> None:
        self.login_button = ButtonComponent()
        self.input = InputComponent()

    def render(self):
        return html.Div(
            html.Div(
                html.Div(
                    html.Div(
                        html.Div(
                            [
                                html.Div(
                                    html.H3("CONNEXION", className="text-center"),
                                    className="card-header",
                                ),
                                html.Div(
                                    html.Form(
                                        [
                                            self.input.render(
                                                "Adreese Email", "email", "email"
                                            ),
                                            self.input.render(
                                                "Mot de passe", "password", "password"
                                            ),
                                            html.Div(
                                                self.login_button.render(
                                                    title="Se connecter",
                                                    type="primary-btn w-100",
                                                    id="login-btn",
                                                ),
                                                className="col-12",
                                            ),
                                        ]
                                    ),
                                    className="card-body py-5 px-md-5",
                                ),
                            ],
                            className="col-lg-12",
                        ),
                        className="card mb-3 ",
                    ),
                    className="col-md-6",
                ),
                className="row h-100 justify-content-center align-items-center",
            ),
            className="container",
        )
