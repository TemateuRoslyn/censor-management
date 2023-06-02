import plotly.express as px
import pandas as pd
import requests

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
    insert = requests.get("http://127.0.0.1:8000/accelerometre/insert")
    datas = requests.get("http://127.0.0.1:8000/accelerometre/next")
    if datas.status_code == requests.codes.ok:
        json_datas = datas.json()
        return pd.DataFrame(data=json_datas)

user = {
    'email':'softmaes@gmail.com',
    'password':'softm12345',
    'name':'SOFT'
}