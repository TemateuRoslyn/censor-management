from dash import Output, Input, State,html, dcc

class RegisterControlCallback:
    def __init__(self, app) -> object:
        self.app = app
        self.form_state = 0

    def control_name(self):
        @self.app.callback(
            Output(component_id="nom-feedback", component_property="children"),
            [Input(component_id="register", component_property="n_clicks"),
            Input(component_id="nom", component_property="value")]
        )
        def check_value(n_clicks, value):
            if n_clicks is not None :
                if value is None:
                    return html.Div(className='alert alert-danger', role='alert', children=[
                        "Le champ nom est obligatoire !"
                    ])
                elif len(value) < 3:
                    return html.Div(className='alert alert-warning', role='alert', children=[
                        "Le champ nom doit contenir au moins 3 caracteres !"
                    ])
                else:
                    self.form_state +=1
                    return html.Div(className='alert alert-success', role='alert', children=[
                        "Le champ nom semble correct !"
                    ])
    def control_surname(self):
        @self.app.callback(
            Output(component_id="prenom-feedback", component_property="children"),
            [Input(component_id="register", component_property="n_clicks"),
            Input(component_id="prenom", component_property="value")]
        )
        def check_surname(n_clicks, value):
            if n_clicks is not None :
                if value is None:
                    return html.Div(className='alert alert-danger', role='alert', children=[
                        "Le champ prenom est obligatoire !"
                    ])
                elif len(value) < 3:
                    return html.Div(className='alert alert-warning', role='alert', children=[
                        "Le champ prenom doit contenir au moins 3 caracteres !"
                    ])
                else:
                    self.form_state +=1
                    return html.Div(className='alert alert-success', role='alert', children=[
                        "Le champ prenom semble correct !"
                    ])
                
    def control_email(self):
        @self.app.callback(
            Output(component_id="email-feedback", component_property="children"),
            [Input(component_id="register", component_property="n_clicks"),
            Input(component_id="email", component_property="value")]
        )
        def check_email(n_clicks, value):
            if n_clicks is not None :
                if value is None:
                    return html.Div(className='alert alert-danger', role='alert', children=[
                        "Le champ email est obligatoire !"
                    ])
                elif '@gmail.com' in value or '@yahoo.' in value:
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
            Output(component_id="password-feedback", component_property="children"),
            [Input(component_id="register", component_property="n_clicks"),
            Input(component_id="password", component_property="value")]
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
                
    def control_confirm_pass(self):
        @self.app.callback(
            Output(component_id="password-confirm-feedback", component_property="children"),
            [Input(component_id="register", component_property="n_clicks"),
            Input(component_id="password-confirm", component_property="value")]
        )
        def check_confirm_pass(n_clicks, value):
            if n_clicks is not None :
                if value is None:
                    return html.Div(className='alert alert-danger', role='alert', children=[
                        "La confirmation du mot de passe est obligatoire !"
                    ])
                elif len(value) < 8:
                    return html.Div(className='alert alert-warning', role='alert', children=[
                        "La confirmation du mot de passe doit contenir au moins 8 caracteres !"
                    ])
                else:
                    self.form_state +=1
                    return html.Div(className='alert alert-success', role='alert', children=[
                        "La confirmation du mot de passe semble correct !"
                    ])
         
    def control_matching_pass(self):
        @self.app.callback(
            Output(component_id="password-confirm-matching-feedback", component_property="children"),
            [Input(component_id="register", component_property="n_clicks"),
            Input(component_id="password", component_property="value"),
            Input(component_id="password-confirm", component_property="value"),
            ]
        )       
        def check_matching_pass(nclicks,value1:str, value2:str):
            if nclicks is not None:
                if value1 is not None and value2 is not None:
                    if value2.__eq__(value1):
                        print(self.form_state)
                        return html.Div(className='alert alert-success', role='alert', children=[
                            "Les mots de passe correspondent !"
                        ])
                    else:
                        return html.Div(className='alert alert-danger', role='alert', children=[
                            "Les mots de passe ne correspondent pas !"
                        ])
                    
    def render_callbacks(self):
        self.control_name()
        self.control_surname()
        self.control_confirm_pass()
        self.control_email()
        self.control_password()
        self.control_matching_pass()