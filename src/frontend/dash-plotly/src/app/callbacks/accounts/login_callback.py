from dash import Output, Input, State,html, dcc
from components.toasts.simple_toast import SimpleToast
from config import user

class LoginCallback:
    def __init__(self, app) -> None:
        self.app = app
        self.form_state = 0
        self.toast = SimpleToast()
     
    def control_email(self):
        @self.app.callback(
            Output(component_id="login-email-feedback", component_property="children"),
            [Input(component_id="login", component_property="n_clicks"),
            Input(component_id="login-email", component_property="value")]
        )
        def check_email(n_clicks, value):
            if n_clicks is not None :
                if value is None:
                    return html.Div(className='alert alert-danger', role='alert', children=[
                        "Le champ email est obligatoire !"
                    ])
                elif '@gmail.com' not in value and '@yahoo.' not in value:
                    return html.Div(className='alert alert-warning', role='alert', children=[
                        "Le champ email semble incomplet !"
                    ])
                else:
                    self.form_state +=1
                    return html.Div(className='alert alert-success', role='alert', children=[
                        "Le champ email semble correct !"
                    ])
                
    def control_password(self):
        @self.app.callback(
            Output(component_id="login-password-feedback", component_property="children"),
            [Input(component_id="login", component_property="n_clicks"),
            Input(component_id="login-password", component_property="value")]
        )
        def check_password(n_clicks, value):
            if n_clicks is not None :
                if value is None:
                    return html.Div(className='alert alert-danger', role='alert', children=[
                        "Le mot de passe est obligatoire !"
                    ])
                elif len(value) < 8:
                    return html.Div(className='alert alert-warning', role='alert', children=[
                        "Le mot de passe doit contenir au moins 8 caracteres !"
                    ])
                else:
                    self.form_state +=1
                    return html.Div(className='alert alert-success', role='alert', children=[
                        "Le mot de passe semble correct !"
                    ])
                
    def redirection(self):
        @self.app.callback(
            Output(component_id="correct-login", component_property="children"),
            [
                Input(component_id="login", component_property="n_clicks"),
                Input(component_id="login-email", component_property="value"),
                Input(component_id="login-password", component_property="value")
            ]
        )
        def redirection(n_clicks,email:str,password:str):
            if email is not None and password is not None:
                if email.__eq__(user.get('email')):
                    if password.__eq__(user.get('password')):
                        return dcc.Location(
                            id="connected",
                            pathname="/accueil",
                            refresh=True
                        )
                    else:
                        return self.toast.render(
                            msg="Le mot de passe est incorrect !",
                            title="ERREUR", ico='danger', cstyle="text-bg-danger text-dark")
                else:
                    return self.toast.render(
                        msg="L'email est incorrecte !",
                        title="ERREUR", ico='danger', cstyle="text-bg-danger text-dark")

    def render_callbacks(self):
        self.control_email()
        self.control_password()
        self.redirection()