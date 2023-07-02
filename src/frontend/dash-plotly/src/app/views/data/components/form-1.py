from dash import dash, html
from components.button.button_component import ButtonComponent
from components.input.input_component import InputComponent


class Form1:
    def __init__(self) -> None:
        self.input = InputComponent()
        self.button = ButtonComponent()

    def render(self):
        return html.Div(
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
