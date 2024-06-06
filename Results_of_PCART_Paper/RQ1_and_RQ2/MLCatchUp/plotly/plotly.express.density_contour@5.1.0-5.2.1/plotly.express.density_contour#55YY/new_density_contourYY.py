import plotly.express as px
df = px.data.tips()
fig = px.density_contour(df, 'total_bill', 'tip', None, None, None, None, 0, None, facet_col_spacing=None, trendline_options=None, trendline_scope='trace')