from dash import html
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
from components.input.input_component import InputComponent
from components.divider.divider_component import DividerComponent
from components.button.button_component import ButtonComponent


class ParametrageView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.input = InputComponent()
        self.divider = DividerComponent()
        self.button = ButtonComponent()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                self.title_page.render(
                                    "Parametrages",
                                    description="Parametrer les composants. Capteur, Accelerometres, et autres...",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "Parametrer les capteurs",
                                                    className="text-sm my-2",
                                                ),
                                                html.Div(
                                                    self.input.render(
                                                        label="Texte",
                                                        id="input-1",
                                                        type="number",
                                                    ),
                                                    className="mb-2",
                                                ),
                                                html.Div(
                                                    self.input.render(
                                                        label="Axis",
                                                        id="input-1",
                                                        type="text",
                                                    ),
                                                    className="mb-2",
                                                ),
                                                html.Div(
                                                    self.button.render(
                                                        title="Valider",
                                                        id="button-1",
                                                        type="primary-btn w-50",
                                                    ),
                                                    className="mb-3 text-end",
                                                ),
                                            ],
                                            className="col-md-6 col-sm-12 bg-white rounded",
                                        )
                                    ],
                                    className="row",
                                ),
                            ],
                            className="container-fluid",
                        )
                    ],
                    className="section",
                ),
            ]
        )
