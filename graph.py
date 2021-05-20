from os import name
import plotly
from plotly.offline import iplot
import plotly.graph_objs as go
import pandas as pd
from plotly import express

#plot graph for positive count of each company
company = ['City-link Express', 'Pos Laju', 'GDEX', 'J&T', 'DHL']
p_count = [197,132,824,407,505]
#df = pd.read_csv("C:/Users/Hp/Documents/Visual Studio 2019/new/test.csv",error_bad_lines=False)
data = [go.Bar(
    x = company,
    y = p_count
   
)]
fig = go.Figure(data=data)
iplot(fig)


