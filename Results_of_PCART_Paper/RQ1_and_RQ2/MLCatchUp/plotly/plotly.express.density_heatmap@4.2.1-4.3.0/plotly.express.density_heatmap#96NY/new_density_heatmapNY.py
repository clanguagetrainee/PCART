import plotly.express as px
df = px.data.tips()
fig = px.density_heatmap(df, 'total_bill', 'tip', None, None, None, None, None, None, animation_group=None, category_orders={}, labels={}, color_continuous_scale=None, facet_col_wrap=0)