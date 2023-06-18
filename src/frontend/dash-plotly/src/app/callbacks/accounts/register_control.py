from dash import Output, Input, State,html, dcc

class RegisterControlCallback:
    def __init__(self, app) -> None:
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
                    return html.Div(className='alert alert-danger', role='alert', children=[
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
                    return html.Div(className='alert alert-danger', role='alert', children=[
                        "Le champ prenom doit contenir au moins 3 caracteres !"
                    ])
                else:
                    self.form_state +=1
                    return html.Div(className='alert alert-success', role='alert', children=[
                        "Le champ prenom semble correct !"
                    ])
                
    def render_callbacks(self):
        self.control_name()
        self.control_surname()