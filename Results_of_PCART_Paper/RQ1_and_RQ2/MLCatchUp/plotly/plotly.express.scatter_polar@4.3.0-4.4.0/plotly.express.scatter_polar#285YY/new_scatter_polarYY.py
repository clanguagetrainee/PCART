import plotly.express as px
df = px.data.wind()
fig = px.scatter_polar(df, 'frequency', 'direction', None, None, None, None, None, None, None, None, None, {}, {}, None, color_discrete_map={}, color_continuous_scale=None, range_color=None, color_continuous_midpoint=None, symbol_sequence=None, symbol_map={}, opacity=None, direction='clockwise', range_theta=None)