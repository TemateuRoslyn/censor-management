from dash import Input, Output, State
from services.APIRequest import APIRequest


class AnalogicInputCallback:
    """
    Notons que notre callback doit récupérer les données après 09 secondes
    """

    def __init__(self, app) -> None:
        self.app = app
        self.request = APIRequest()

    def register_ai_0(self):
        @self.app.callback(
            [
                Output("ai_0", "on"),
                Output("ai_0_valeur", "children"),
                Output("ai_0_etat", "children"),
            ],
            Input("ai_interval", "n_intervals"),
        )
        def update_ai_0(n):
            result = self.request.get("/analogic-input")

            etat = result["etat"]
            valeur = result["valeur"]
            return [
                etat,
                "NaN" if valeur == 0 else valeur,
                "Inactif" if etat == False else "Actif",
            ]

    def register_ai_1(self):
        @self.app.callback(
            [
                Output("ai_1", "on"),
                Output("ai_1_valeur", "children"),
                Output("ai_1_etat", "children"),
            ],
            Input("ai_interval", "n_intervals"),
        )
        def update_ai_1(n):
            result = self.request.get("/analogic-input")

            etat = result["etat"]
            valeur = result["valeur"]
            return [
                etat,
                "NaN" if valeur == 0 else valeur,
                "Inactif" if etat == False else "Actif",
            ]

    def register_ai_2(self):
        @self.app.callback(
            [
                Output("ai_2", "on"),
                Output("ai_2_valeur", "children"),
                Output("ai_2_etat", "children"),
            ],
            Input("ai_interval", "n_intervals"),
        )
        def update_ai_2(n):
            result = self.request.get("/analogic-input")

            etat = result["etat"]
            valeur = result["valeur"]
            return [
                etat,
                "NaN" if valeur == 0 else valeur,
                "Inactif" if etat == False else "Actif",
            ]

    def register_ai_3(self):
        @self.app.callback(
            [
                Output("ai_3", "on"),
                Output("ai_3_valeur", "children"),
                Output("ai_3_etat", "children"),
            ],
            Input("ai_interval", "n_intervals"),
        )
        def update_ai_3(n):
            result = self.request.get("/analogic-input")

            etat = result["etat"]
            valeur = result["valeur"]
            return [
                etat,
                "NaN" if valeur == 0 else valeur,
                "Inactif" if etat == False else "Actif",
            ]

    def register_ai_4(self):
        @self.app.callback(
            [
                Output("ai_4", "on"),
                Output("ai_4_valeur", "children"),
                Output("ai_4_etat", "children"),
            ],
            Input("ai_interval", "n_intervals"),
        )
        def update_ai_4(n):
            result = self.request.get("/analogic-input")

            etat = result["etat"]
            valeur = result["valeur"]
            return [
                etat,
                "NaN" if valeur == 0 else valeur,
                "Inactif" if etat == False else "Actif",
            ]

    def register_ai_5(self):
        @self.app.callback(
            [
                Output("ai_5", "on"),
                Output("ai_5_valeur", "children"),
                Output("ai_5_etat", "children"),
            ],
            Input("ai_interval", "n_intervals"),
        )
        def update_ai_5(n):
            result = self.request.get("/analogic-input")

            etat = result["etat"]
            valeur = result["valeur"]
            return [
                etat,
                "NaN" if valeur == 0 else valeur,
                "Inactif" if etat == False else "Actif",
            ]

    def register_ai_6(self):
        @self.app.callback(
            [
                Output("ai_6", "on"),
                Output("ai_6_valeur", "children"),
                Output("ai_6_etat", "children"),
            ],
            Input("ai_interval", "n_intervals"),
        )
        def update_ai_6(n):
            result = self.request.get("/analogic-input")

            etat = result["etat"]
            valeur = result["valeur"]
            return [
                etat,
                "NaN" if valeur == 0 else valeur,
                "Inactif" if etat == False else "Actif",
            ]

    def register_ai_7(self):
        @self.app.callback(
            [
                Output("ai_7", "on"),
                Output("ai_7_valeur", "children"),
                Output("ai_7_etat", "children"),
            ],
            Input("ai_interval", "n_intervals"),
        )
        def update_ai_7(n):
            result = self.request.get("/analogic-input")

            etat = result["etat"]
            valeur = result["valeur"]
            return [
                etat,
                "NaN" if valeur == 0 else valeur,
                "Inactif" if etat == False else "Actif",
            ]
