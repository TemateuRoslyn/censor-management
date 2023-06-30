from dash import html
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
from views.notifications.components.notifications_components import (
    NotificationsComponent,
)


class NotificationsView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.notification = NotificationsComponent()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                self.title_page.render("Notifications"),
                                html.Div(
                                    [
                                        self.notification.render(
                                            titre="Ajout d'un capteur",
                                            content="Le capteur numero 21 a été monté",
                                        ),
                                        self.notification.render(
                                            titre="Suppression des capteurs 12",
                                            content="Le capteur numero 21 a été monté",
                                        ),
                                        self.notification.render(
                                            titre="Suppression des capteurs 12",
                                            content="Le capteur numero 21 a été monté",
                                        ),
                                        self.notification.render(
                                            titre="Suppression des capteurs 12",
                                            content="Le capteur numero 21 a été monté",
                                        ),
                                        self.notification.render(
                                            titre="Suppression des capteurs 12",
                                            content="Le capteur numero 21 a été monté",
                                        ),
                                        self.notification.render(
                                            titre="Suppression des capteurs 12",
                                            content="Le capteur numero 21 a été monté",
                                        ),
                                    ],
                                    className="card-style mt-3",
                                ),
                            ],
                            className="container-fluid",
                        )
                    ],
                    className="section",
                ),
            ]
        )
