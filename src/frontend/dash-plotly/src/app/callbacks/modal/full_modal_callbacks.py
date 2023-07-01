from dash import Input, Output, html, dcc
import pandas as pd

class PaginateCallback:
    def __init__(self, app) -> None:
        self.app = app
        self.us_cities = pd.read_csv("us-cities-top-1k.csv")
    def paginateCallback(self):
        @self.app.callback(
            Output(component_id="table-body", component_property="children"),
            [
                Input(component_id="paginate-tab", component_property="active_page"),
            ]
        )
        def paginate(step):
            # print(step)
            body = []
            for i in range(6):
                body.append(
                    html.Tr(id='', className='', children=[
                        html.Td(id='', className='ps-5', children='{0}'.format(i + 1 + (step-1)*6)),
                        html.Td(id='', className='', children=self.us_cities[self.us_cities.columns[0]][i + (step-1)*6]),
                        html.Td(id='', className='', children=self.us_cities[self.us_cities.columns[1]][i + (step-1)*6]),
                        html.Td(id='', className='', children=self.us_cities[self.us_cities.columns[2]][i + (step-1)*6]),
                        html.Td(id='', className='', children=self.us_cities[self.us_cities.columns[3]][i + (step-1)*6]),
                        html.Td(id='', className='', children=self.us_cities[self.us_cities.columns[4]][i + (step-1)*6]),
                    ]),
                )
            return body
        

    def dfToCSVCallback(self):
        @self.app.callback(
            Output(component_id="exp-csv-d", component_property="data"),
            [
                Input(component_id="exp-csv", component_property="n_clicks"),
            ],
        )
        def dfToCSV(nclicks):
            if nclicks > 0:
                return dcc.send_data_frame(self.us_cities.to_csv,"data.csv")
    
    def dfToHTMLCallback(self):
        @self.app.callback(
            Output(component_id="exp-html-d", component_property="data"),
            [
                Input(component_id="exp-html", component_property="n_clicks"),
            ],
        )
        def dfToHTML(nclicks):
            if nclicks > 0:
                return dcc.send_data_frame(self.us_cities.to_html,"data.html")
    
    def dfToJSONCallback(self):
        @self.app.callback(
            Output(component_id="exp-json-d", component_property="data"),
            [
                Input(component_id="exp-json", component_property="n_clicks"),
            ],
        )
        def dfToJSON(nclicks):
            if nclicks > 0:
                return dcc.send_data_frame(self.us_cities.to_json,"data.json")
    
    def downloadCallbacks(self):
        self.dfToCSVCallback()
        self.dfToHTMLCallback()
        self.dfToJSONCallback()