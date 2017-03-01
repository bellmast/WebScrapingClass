from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
import pandas as pd

df = pd.read_csv('https://plot.ly/~etpinard/191.csv')

plot({
   'data': [
       Scatter(x=df[continent+', x'],
               y=df[continent+', y'],
               text=df[continent+', text'],
               marker=Marker(size=df[continent+', size'], sizemode='area', sizeref=131868,),
               mode='markers',
               name=continent) for continent in ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
   ],
   'layout': Layout(xaxis=XAxis(title='Life Expectancy'), yaxis=YAxis(title='GDP per Capita', type='log'))
}, show_link=False)
