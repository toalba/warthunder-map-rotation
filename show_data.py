import plotly.express as px
import pandas as pd
import json


def graph_lastten(data):
    fig = px.bar(data, x=0, y=1, title="Map Distribution last 10min", text_auto=True,template="plotly_dark")  
    return fig

def graph_lastone(data):
    fig = px.bar(data, x=0, y=1, title="Map Distribution last Minute", text_auto=True,template="plotly_dark")  
    return fig

def like_graph(data):
    chart=[[k,data[k]['count']-data[k]['likes']-data[k]['dislikes'],data[k]['likes'],data[k]['dislikes']] for k,v in data.items()]
    dataframe = pd.DataFrame(chart,columns=["Map","Neutral","Likes","Dislikes"])
    fig = px.bar(dataframe,x="Map",y=["Neutral","Dislikes","Likes"], title="Map Distribution", text_auto=True)
    return fig
