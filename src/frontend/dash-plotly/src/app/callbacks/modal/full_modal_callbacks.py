from dash import Input, Output, html
import pandas as pd

class PaginateCallback:
    def __init__(self, app) -> None:
        self.app = app
    def paginateCallback(self):
        @self.app.callback(
            Output(component_id="table-body", component_property="children"),
            [
                Input(component_id="paginate-tab", component_property="active_page"),
            ]
        )
        def paginate(step):
            us_cities = pd.read_csv("us-cities-top-1k.csv")
            # print(step)
            body = []
            for i in range(6):
                body.append(
                    html.Tr(id='', className='', children=[
                        html.Td(id='', className='ps-5', children='{0}'.format(i + 1 + (step-1)*6)),
                        html.Td(id='', className='', children=us_cities[us_cities.columns[0]][i + (step-1)*6]),
                        html.Td(id='', className='', children=us_cities[us_cities.columns[1]][i + (step-1)*6]),
                        html.Td(id='', className='', children=us_cities[us_cities.columns[2]][i + (step-1)*6]),
                        html.Td(id='', className='', children=us_cities[us_cities.columns[3]][i + (step-1)*6]),
                        html.Td(id='', className='', children=us_cities[us_cities.columns[4]][i + (step-1)*6]),
                    ]),
                )
            return body