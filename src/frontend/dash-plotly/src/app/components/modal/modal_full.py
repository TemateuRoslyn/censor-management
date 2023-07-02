from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

class ModalFull:
    def __init__(self) -> object:
        pass

    def paginationList(self, step:int):
        us_cities = pd.read_csv("us-cities-top-1k.csv")
        # print(us_cities.columns[3])
        body = []
        for i in range(6):
            body.append(
                html.Tr(id='', className='', children=[
                    html.Td(id='', className='ps-5', children='{0}'.format(i+step)),
                    html.Td(id='', className='', children=us_cities[us_cities.columns[0]][i+step]),
                    html.Td(id='', className='', children=us_cities[us_cities.columns[1]][i+step]),
                    html.Td(id='', className='', children=us_cities[us_cities.columns[2]][i+step]),
                    html.Td(id='', className='', children=us_cities[us_cities.columns[3]][i+step]),
                    html.Td(id='', className='', children=us_cities[us_cities.columns[4]][i+step]),
                ]),
            )
        return body


    def render(self):
        us_cities = pd.read_csv("us-cities-top-1k.csv")
        # print(len(us_cities))
        return dbc.Modal(
            [
                dbc.ModalHeader(
                    [
                        dbc.ModalTitle("DONNEES GPS DES ETATS UNIS"),
                        dbc.Accordion([
                            dbc.AccordionItem([
                                html.Button(id='', className='btn btn-lg border-0', children=[
                                    html.Span(id='', className='material-symbols-outlined icon fs-1 text-warning', children="csv")
                                ]),
                                html.Button(id='', className='btn btn-lg border-0', children=[
                                    html.Span(id='', className='material-symbols-outlined icon fs-1', children="csv")
                                ]),
                                html.Button(id='', className='btn btn-lg border-0', children=[
                                    html.Span(id='', className='material-symbols-outlined icon fs-1', children="csv")
                                ]),
                            ],
                            title="Exporter",
                            className="justify-content-between")
                        ],
                        # start_collapsed=True,
                        className="ms-5 w-25")
                    ],
                    close_button=True,
                ),
                dbc.ModalBody([
                    html.Div(id='', className='card', children=[
                        dbc.Table([
                            html.Thead(id='', className='', children=
                                html.Tr(id='', className='justify-content-around text-uppercase bg-secondary', children=[
                                    html.Th(id='', className='border border-0 ps-5', children='id'),
                                    html.Th(id='', className='border border-0', children='Regions'),
                                    html.Th(id='', className='border border-0', children='Villes'),
                                    html.Th(id='', className='border border-0', children='Habitants'),
                                    html.Th(id='', className='border border-0', children='Lattitude'),
                                    html.Th(id='', className='border border-0', children='Longitude'),
                                ])
                            ),
                            html.Tbody(id='table-body', className='', children=self.paginationList(step=1))
                        ],
                        class_name="table-striped")
                    ]),
                    dbc.Pagination(
                        id="paginate-tab",
                        max_value=int(len(us_cities)/6),
                        className="text-secondary mt-1",
                        fully_expanded=False,
                        min_value=1,
                        previous_next=True,
                        active_page=1
                    )
                ]),
            ],
            id="modal-full",
            keyboard=False,
            size="xl",
            is_open=True,
            backdrop='static',
        )