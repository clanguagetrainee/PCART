import plotly.express as px
df = px.data.tips()
fig = px.histogram(df, 'total_bill', None, None, None, None, None, 0, None, facet_col_spacing=None, hover_name=None, hover_data=None, animation_frame=None, animation_group=None, text_auto=False)