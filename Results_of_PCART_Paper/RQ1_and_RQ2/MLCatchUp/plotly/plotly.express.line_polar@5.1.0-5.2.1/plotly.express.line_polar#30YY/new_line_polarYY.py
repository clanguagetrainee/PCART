import plotly.express as px
df = px.data.wind()
fig = px.line_polar(df, 'frequency', 'direction', 'strength', None, None, hover_data=None, symbol=None, symbol_sequence=None, symbol_map=None, markers=False)