import plotly.express as px
df = px.data.tips()
fig = px.density_heatmap(df, 'total_bill', 'tip', None, None, None, None, None, None, None, {}, labels={}, color_continuous_scale=None, range_color=None, color_continuous_midpoint=None, facet_col_wrap=0)