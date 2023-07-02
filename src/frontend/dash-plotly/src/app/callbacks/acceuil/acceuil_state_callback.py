from dash import Output, Input
import numpy as np


class AcceuilStateCallback:
    def __init__(self, app) -> None:
        self.app = app

    def register(self):
        @self.app.callback(
            [
                [
                    Output("id_capt1_health_valeur", "children"),
                    Output("id_capt1_health_etat", "children"),
                ],
                [
                    Output("id_acc1_health_valeur", "children"),
                    Output("id_acc1_health_etat", "children"),
                ],
                [
                    Output("id_acc2_health_valeur", "children"),
                    Output("id_acc2_health_etat", "children"),
                ],
                [
                    Output("id_capt_gps_health_valeur", "children"),
                    Output("id_capt_gps_health_etat", "children"),
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
                    (str(valeur_cap_health) + "%"),
                    etat_cap_health,
                ],
                [
                    (str(valeur_cap_health) + "%"),
                    etat_cap_health,
                ],
                [
                    (str(valeur_cap_health) + "%"),
                    etat_cap_health,
                ],
                [
                    (str(valeur_cap_health) + "%"),
                    etat_cap_health,
                ],
            ]
