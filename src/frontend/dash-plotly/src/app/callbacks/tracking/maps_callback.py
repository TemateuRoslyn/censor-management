from dash import Input, Output

class MapCallback:
    def __init__(self, app) -> None:
        self.app = app
    def changeMapCallback(self):
        @self.app.callback(
            Output(component_id="maps-render", component_property="figure"),
            [
                
                Input(component_id="maps-render", component_property="figure"),
            ]
        )
        def changeMap(a,b,c,d,e,fig):
            print(a,b,c,d,e)
            return None