from dash import html, dcc
from components.button.button_component import ButtonComponent
from components.input.input_component import InputComponent


class SignUpView:
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
                                    html.H3("CREATION DE COMPTE", className="text-center"),
                                    className="card-header",
                                ),
                                html.Div(
                                    html.Form(
                                        [
                                            self.input.render(
                                                "Nom:",
                                                type="text",
                                                id="nom",
                                                name="nom",
                                                placeholder="Entrez votre nom",
                                            ),
                                            self.input.render(
                                                "Prenom:",
                                                type="text",
                                                id="prenom",
                                                name="prenom",
                                                placeholder="Entrez votre prenom"
                                            ),
                                            self.input.render(
                                                "Adreese email:",
                                                type="email",
                                                id="email",
                                                name="email",
                                                placeholder="softmaes@yahoo.fr"
                                            ),
                                            self.input.render(
                                                "Mot de passe:",
                                                type="password",
                                                id="password",
                                                name="password"
                                            ),
                                            self.input.render(
                                                "Confirmer le mot de passe:",
                                                type="password",
                                                id="password-confirm",
                                                name="password-confirm"
                                            ),
                                            html.Div(
                                                self.login_button.render(
                                                    "S'enregistrer",
                                                    type="primary-btn w-100",
                                                    id="register",
                                                ),
                                                className="col-12",
                                            ),
                                        ],
                                        id="register-form"
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
            className="mt-5 left-content show-up header-text wow fadeInLeft",
            style={'visibility': 'visible',
                   '-webkit-animation-duration': '1s',
                    '-moz-animation-duration': '1s', 
                    'animation-duration': '1s',
                    "-webkit-animation-delay": '0.5s', 
                    '-moz-animation-delay': '0.5s', 
                    'animation-delay': '0.5s'
                    }
        )
