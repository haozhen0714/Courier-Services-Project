from os import name
import plotly
from plotly.offline import iplot
import plotly.graph_objs as go
import pandas as pd
from plotly import express

#plot graph for negative count of each company
company = ['City-link Express', 'Pos Laju', 'GDEX', 'J&T', 'DHL']
n_count = [313,182,1150,585,716]
#df = pd.read_csv("C:/Users/Hp/Documents/Visual Studio 2019/new/test.csv",error_bad_lines=False)
data = [go.Bar(
    x = company,
    y = n_count
   
)]
fig = go.Figure(data=data)
iplot(fig)
