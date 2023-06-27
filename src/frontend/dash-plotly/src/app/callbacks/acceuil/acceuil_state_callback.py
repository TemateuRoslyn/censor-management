from dash import Output, Input, State
import numpy as np


class AcceuilStateCallback:
    def __init__(self, app) -> None:
        self.app = app

    def register(self):
        @self.app.callback(
            [
                [
                    Output("id_capt_health_title", "children"),
                    Output("id_capt_health_valeur", "children"),
                    Output("id_capt_health_etat", "children"),
                ],
                [
                    Output("id_acc_health_title", "children"),
                    Output("id_acc_health_valeur", "children"),
                    Output("id_acc_health_etat", "children"),
                ],
                [
                    Output("id_ther_health_title", "children"),
                    Output("id_ther_health_valeur", "children"),
                    Output("id_ther_health_etat", "children"),
                ],
                [
                    Output("id_pres_health_title", "children"),
                    Output("id_pres_health_valeur", "children"),
                    Output("id_pres_health_etat", "children"),
                ],
            ],
            Input("interval-component", "n_intervals"),
        )
        def render(n_intervals):
            valeur_cap_health = np.random.randint(0, 101)
            etat_cap_health = ""
            if valeur_cap_health < 50:
                etat_cap_health = "Critique"
            elif valeur_cap_health == 50:
                etat_cap_health = "Stable"
            else:
                etat_cap_health = "Bon état"
            return [
                [
                    "Santé des Capteurs",
                    (str(valeur_cap_health) + "%"),
                    etat_cap_health,
                ],
                [
                    "Accélerometres",
                    (str(valeur_cap_health) + "%"),
                    etat_cap_health,
                ],
                [
                    "Capteurs Thermiques",
                    (str(valeur_cap_health) + "%"),
                    etat_cap_health,
                ],
                [
                    "Capteurs de Pression",
                    (str(valeur_cap_health) + "%"),
                    etat_cap_health,
                ],
            ]
