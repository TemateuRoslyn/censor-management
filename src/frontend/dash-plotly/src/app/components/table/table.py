from dash import html, dcc
import dash_bootstrap_components as dbc


class Table:
    def __init__(self) -> None:
        pass

    def renderline(self, classname,children):
        return html.Li(id='', className=classname, children=children)
    
    def renderRow(self, classname, child):
        return html.Div(id='', className=classname, children=child)

    def renderGps(self, datas):
        return html.Div(id='', className='container-tab', children=[
            html.Ul(id='', className='responsive-table', children=[
                self.renderline(
                    classname="table-header",
                    children=[
                        self.renderRow(classname="col col-1",child="ville"),
                        self.renderRow(classname="col col-2",child="region"),
                        self.renderRow(classname="col col-3",child="Habitants"),
                    ]
                ),
                self.renderline(
                    classname="table-row",
                    children=[
                        self.renderRow(classname="col col-1",child=datas['City'][0]),
                        self.renderRow(classname="col col-2",child=datas['State'][0]),
                        self.renderRow(classname="col col-3",child=datas['Population'][0]),
                    ]
                ),
                self.renderline(
                    classname="table-row",
                    children=[
                        self.renderRow(classname="col col-1",child=datas['City'][1]),
                        self.renderRow(classname="col col-2",child=datas['State'][1]),
                        self.renderRow(classname="col col-3",child=datas['Population'][1]),
                    ]
                ),
            ])
        ])