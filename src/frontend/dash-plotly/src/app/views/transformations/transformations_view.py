from dash import html
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
import dash_bootstrap_components as dbc


class TransformationsView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()

    def params(self, id):
        state = "bg-success"
        val = id/3
        if id > 5:
            state = "bg-danger"
            val = "NAN"
        return html.Div([
            html.Div([
                dbc.InputGroup([
                    dbc.InputGroupText("State"),
                    dbc.Input(value=str(val), className=state),
                ],className="mb-1")
            ],className="col-lg-6"),
            html.Div([
                dbc.InputGroup([
                    dbc.InputGroupText("Sensitivite"),
                    dbc.Input(value=4,type="number"),
                    dbc.Select(options=[
                        {"label":"milliVolt/Unite", "value":1},
                        {"label":"volt/Unite", "value":2},
                    ],value=id%2 + 1),
                    dbc.InputGroupText("sensitivity_units")
                ],className="mb-1")
            ],className="col-lg-6"),
            html.Div([
                dbc.InputGroup([
                    dbc.InputGroupText("rate"),
                    dbc.Input(value=4000,type="number"),
                    dbc.InputGroupText("Hz"),
                ],className="mb-1")
            ],className="col-lg-6"),
            html.Div([
                dbc.InputGroup([
                    dbc.InputGroupText("name"),
                    dbc.Input(value="captor #" + str(id),type="text"),
                ],className="mb-1")
            ],className="col-lg-6"),
            html.Div([
                dbc.InputGroup([
                    dbc.InputGroupText("Sensor Type"),
                    dbc.Select(options=[
                        {"label":"Accelerometre", "value":1},
                        {"label":"Micro", "value":2},
                    ],value=id%2 + 1),
                ],className="mb-1")
            ],className="col-lg-6"),
            html.Div([
                dbc.InputGroup([
                    dbc.InputGroupText("Units"),
                    dbc.Select(options=[
                        {"label":"G", "value":1},
                        {"label":"m/s", "value":2},
                        {"label":"inches/s", "value":3},
                        {"label":"custom", "value":4},
                    ],value=id%4 + 1),
                ],className="mb-1")
            ],className="col-lg-6"),
        ],className="row")

    def render(self):
        accItem = []
        for i in range(7):
            accItem.append(
                dbc.AccordionItem(
                    self.params(id=i+1),
                    title="AI "+ str(i+1)
                )
            )
        return html.Div(
            [
                self.header.render(),
                html.Label(["Parametrer les donnees recus par les differents capteurs !"],className="w-100 text-center pt-3 fs-4"),
                html.Section(
                    [
                        dbc.Accordion(
                            accItem,
                            start_collapsed=True,
                        className="w-100")
                    ],
                    className="section m-5 d-flex justify-content-center w-80",
                ),
            ]
        )
