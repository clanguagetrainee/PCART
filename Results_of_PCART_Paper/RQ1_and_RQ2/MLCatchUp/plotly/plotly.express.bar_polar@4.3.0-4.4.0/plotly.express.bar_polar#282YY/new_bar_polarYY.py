import plotly.express as px
df = px.data.wind()
fig = px.bar_polar(df, 'frequency', 'direction', 'strength', None, None, None, None, None, {}, {}, None, {}, None, 'relative', 'clockwise', 90, None, log_r=False, title=None, template=None, width=None, height=None, range_theta=None)