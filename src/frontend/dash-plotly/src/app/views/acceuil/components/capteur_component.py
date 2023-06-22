from dash import html
import dash_daq as daq
from components.button.button_component import ButtonComponent


class CapteurComponent:
    def __init__(self):
        self.button = ButtonComponent()

    def render(self, id: str, value=0, label="Label"):
        return html.Div(
            [
                daq.Gauge(
                    color="#006699",
                    id=id,
                    label=label,
                    value=value,
                    showCurrentValue=True,
                    units="m.s",
                    min=0,
                    max=200,
                ),
                self.button.render(title="Parametrer", id="modal-btn", type="primary"),
            ],
            className="card rounded-corner pt-2 pb-0",
        )
