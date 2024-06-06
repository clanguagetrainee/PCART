import plotly.express as px
df = px.data.tips()
fig = px.density_heatmap(df, 'total_bill', y='tip', z=None, facet_row=None, facet_col=None, hover_name=None, hover_data=None, animation_frame=None, facet_col_wrap=0)