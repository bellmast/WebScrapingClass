# to install Plot.ly, run `pip install plotly` in your python shell/command line
# To update, run `pip install plotly --upgrade`

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
import numpy as np
import pandas as pd

# Basic Plot
# The code below creates an html file containing your plot. Plot.ly automatically creates the underlying html, css, javascript code.

plot({
    "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
    "layout": Layout(title="Basic Plot")
})

# Plotting two series

trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])

plotly.offline.plot({
    "data": data,
    "layout": Layout(title="Plotting Two Series")
})

# Real Data - Titanic Passengers
df=pd.read_csv('https://raw.githubusercontent.com/pcsanwald/kaggle-titanic/master/train.csv')

# Exploring our data - Distribution of age
df.info()
df.head()

data = [
    Box(
        y=df.age,
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8
    )
]
plot(data)

data = [
    Box(
        y=df.age[df.sex=='female'],
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8
    )
]
plot(data)
# It looks like a ship!!!

# Age by gender
data = [
    Box(
        y=df.age,
        x=df.sex,
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8
    )
]
plot(data)

# Now let's see survival by age and gender
Survived = Box(
        y=df.age[df.survived==1],
        x=df.sex,
        name='Survived',
    )

NoSurvived = Box(
        y=df.age[df.survived==0],
        x=df.sex,
        name='NoSurvived'
    )

data = [Survived, NoSurvived]
layout = Layout(
    yaxis=dict(
        title='Survival by Age and Gender',
        zeroline=False
    ),
    boxmode='group'
)
fig = Figure(data=data, layout=layout)
plot(fig)

# Substituting gender with Class of Travel
Survived = Box(
        y=df.age[df.survived==1],
        x=df.pclass,
        name='Survived',
    )

NoSurvived = Box(
        y=df.age[df.survived==0],
        x=df.pclass,
        name='NoSurvived'
    )

data = [Survived, NoSurvived]
layout = Layout(
    yaxis=dict(
        title='Survival by Age and Gender',
        zeroline=False
    ),
    boxmode='group'
)
fig = Figure(data=data, layout=layout)
plot(fig)
