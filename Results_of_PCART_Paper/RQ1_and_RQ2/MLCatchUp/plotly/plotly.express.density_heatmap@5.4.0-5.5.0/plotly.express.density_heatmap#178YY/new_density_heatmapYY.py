import plotly.express as px
df = px.data.tips()
fig = px.density_heatmap(df, 'total_bill', 'tip', None, None, None, 0, None, None, None, hover_data=None, animation_frame=None, animation_group=None, category_orders=None, labels=None, orientation=None, color_continuous_scale=None, range_color=None, text_auto=False)