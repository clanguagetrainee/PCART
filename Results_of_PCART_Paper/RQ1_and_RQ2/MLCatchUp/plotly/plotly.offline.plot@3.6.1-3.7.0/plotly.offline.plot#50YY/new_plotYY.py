import plotly.graph_objs as go
import plotly.offline as pyo
trace = go.Scatter(x=[1, 2, 3], y=[4, 5, 6], auto_play=True)
data = [trace]
pyo.plot(data, False, 'Export to plot.ly', True, output_type='file', include_plotlyjs=True, filename='temp-plot.html', auto_open=True, image=None, auto_play=True)