from dash import html, dcc
from components.button.button_component import ButtonComponent
from components.input.input_component import InputComponent


class LoginView:
    def __init__(self) -> None:
        self.login_button = ButtonComponent()
        self.input = InputComponent()

    def render(self):
        return html.Div(
            className="left-content show-up header-text wow fadeInLeft",
            style={'visibility': 'visible',
                   '-webkit-animation-duration': '1s',
                    '-moz-animation-duration': '1s', 
                    'animation-duration': '1s',
                    "-webkit-animation-delay": '0.5s', 
                    '-moz-animation-delay': '0.5s', 
                    'animation-delay': '0.5s'
                    },
            children=html.Div(
                html.Div(
                    html.Div(
                        html.Div(
                            [
                                html.Div(
                                    id="correct-login",
                                    className="position-absolute m-auto",
                                ),
                                html.Div(
                                    html.H3("CONNEXION", className="text-center"),
                                    className="card-header",
                                ),
                                html.Div(
                                    html.Div(
                                        [
                                            self.input.render(
                                                "Email:",
                                                type="email",
                                                id="login-email",
                                                name="email",
                                                placeholder="softmaes@yahoo.fr",
                                                debounce=True,
                                            ),
                                            self.input.render(
                                                "Mot de passe:",
                                                type="password",
                                                id="login-password",
                                                name="password",
                                                debounce=True,
                                            ),
                                            html.Div(
                                                self.login_button.render(
                                                    "Se connecter",
                                                    type="primary-btn w-100",
                                                    id="login",
                                                ),
                                                className="col-12",
                                            ),
                                            dcc.Link(
                                                "S'enregistrer",
                                                href="/sign-up",
                                                className="mt-2 text-reset",
                                                refresh=True,
                                            ),
                                        ]
                                    ),
                                    id="login-form",
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
        )
