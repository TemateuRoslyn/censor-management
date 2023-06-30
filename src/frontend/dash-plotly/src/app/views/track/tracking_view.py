from dash import html, dcc
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

us_cities = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv"
)

fig = px.scatter_mapbox(
    us_cities,
    lat="lat",
    lon="lon",
    hover_name="City",
    hover_data=["State", "Population"],
    color_discrete_sequence=["fuchsia"],
    zoom=3,
    height=300,
)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.update_layout(mapbox_bounds={"west": -180, "east": -50, "south": 20, "north": 90})

fig.update_layout(
    autosize=True,
    hovermode='closest'
)

class TrackingView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                            html.Div(
                        [

                            dcc.Interval(
                                id="graph-interval",
                                disabled=False,
                                n_intervals=0,
                                interval=2500,
                                max_intervals=10
                            ),
                            self.title_page.render(
                                "TRACKING",
                                description="Suivez votre evolution a la trace !",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id="maps-render",
                                        figure=fig
                                    )
                                ],
                                className="row ",
                            ),
                        ],
                        className="container-fluid",
                        )
                    ],
                    className="section m-5 shadow p-3 mb-5 bg-body rounded",
                ),
            ]
        )
