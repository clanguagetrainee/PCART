import plotly.express as px
df = px.data.tips()
fig = px.density_contour(df, 'total_bill', 'tip', z=None, color=None, facet_col_wrap=0)