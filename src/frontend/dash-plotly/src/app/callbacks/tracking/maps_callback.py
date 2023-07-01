from dash import Input, Output

class MapCallback:
    def __init__(self, app) -> None:
        self.app = app
    def id1Callback(self):
        @self.app.callback(
            Output(component_id="id-1", component_property="value"),
            [
                Input(component_id="maps-render", component_property="figure"),
                Input(component_id="open-street-map", component_property="n_clicks"),
            ]
        )
        def changeMapId1(figure, n):
            if n > 0:
                figure.get('layout').get('mapbox').update({'style':'carto-positron'})
                print(figure.get('layout').get('mapbox'),"\n")
                return "open-street-map"
        
    def id2Callback(self):
        @self.app.callback(
            Output(component_id="id-2", component_property="value"),
            [
                
                Input(component_id="carto-positron", component_property="n_clicks"),
            ]
        )
        def changeMapId2(n):
            if n > 0:
                return "carto-positron"
        
    def id3Callback(self):
        @self.app.callback(
            Output(component_id="id-3", component_property="value"),
            [
                
                Input(component_id="carto-darkmatter", component_property="n_clicks"),
            ]
        )
        def changeMapId3(n):
            if n > 0:
                return 'carto-darkmatter'
        
    def id4Callback(self):
        @self.app.callback(
            Output(component_id="id-4", component_property="value"),
            [
                Input(component_id="maps-render", component_property="figure"),
                Input(component_id="stamen-terrain", component_property="n_clicks"),
            ]
        )
        def changeMapId4(n):
            if n > 0:
                return 'stamen-terrain'
        
    def id5Callback(self):
        @self.app.callback(
            Output(component_id="id-5", component_property="value"),
            [
                
                Input(component_id="stamen-toner", component_property="n_clicks"),
            ]
        )
        def changeMapId5(n):
            if n > 0:
                return "stamen-toner"
    def loadCallbacks(self):
        self.id1Callback()
        self.id2Callback()
        self.id3Callback()
        self.id4Callback()
        self.id5Callback()