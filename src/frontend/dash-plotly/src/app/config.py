import plotly.express as px
import pandas as pd

graph ={
    'icons':None,
    'label':[
        'BAR GRAPH', 'AREA GRAPH', 'HISTOGRAM GRAPH','SCATTER GRAPH' 
    ]
}

def renderGraph(option:str, x:str, y:str, color:str, df):
    if option.__eq__('AREA GRAPH'):
        return px.area(df, x, y, color)
    elif option.__eq__('HISTOGRAM GRAPH'):
        return px.histogram(df, x, y, color)
    elif option.__eq__('SCATTER GRAPH'):
        return px.scatter(df, x, y, color)
    else:
        return px.bar(df, x, y, color)
    
def renderDF():
    return pd.DataFrame({
            "Fruits": ["Pommes", "Oranges", "Bananes", "pommes", "Oranges",
                    "Bananes", "Pommes", "Oranges", "Bananes", "Pommes", 
                    "Oranges", "Bananes"],
            "prix": [400, 150, 225, 254, 444, 545, 765, 409, 692, 950, 300, 275],
            "ville": [
                "Dschang", "Bafoussam", "Bouda", "Badjoun", "Bangangte", 
                "Baham", "Douala", "Kribi", "Mbepanda", "Fomopea", "Bafia",
                "Tongolo"]
        })

user = {
    'email':'tom@gmail.com',
    'password':'tom12345'
}