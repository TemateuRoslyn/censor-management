from dash import html
import dash_daq as daq


class CapteurComponent:
    def __init__(self):
        pass

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
            ],
            className="card rounded-corner pt-2 pb-0",
        )
