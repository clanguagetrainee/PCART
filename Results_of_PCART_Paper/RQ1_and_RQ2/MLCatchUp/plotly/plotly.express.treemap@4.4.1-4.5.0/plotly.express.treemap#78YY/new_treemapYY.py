import plotly.express as px
df = px.data.tips()
fig = px.treemap(data_frame=df, names=None, values='total_bill', parents=None, ids=None, color=None, color_continuous_scale=None, range_color=None, color_continuous_midpoint=None, color_discrete_sequence=None, color_discrete_map={}, path=None)