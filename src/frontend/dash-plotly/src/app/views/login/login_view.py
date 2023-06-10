from dash import html, dcc
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
                                # html.Div(
                                #     html.H1(id="login-error"),
                                #     className="alert alert-danger",
                                # ),
                                html.Div(
                                    html.H3("CONNEXION", className="text-center"),
                                    className="card-header",
                                ),
                                html.Div(
                                    html.Form(
                                        [
                                            self.input.render(
                                                "Adreese Email",
                                                type="email",
                                                id="email",
                                            ),
                                            self.input.render(
                                                "Mot de passe",
                                                type="password",
                                                id="password",
                                            ),
                                            html.Div(
                                                self.login_button.render(
                                                    "Se connecter",
                                                    type="primary-btn w-100",
                                                    id="login",
                                                ),
                                                # html.Button(
                                                #     "Se connecter",
                                                #     className="main-btn primary-btn",
                                                #     id="login-main-btn",
                                                # ),
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
