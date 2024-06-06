import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, 'sepal_width', 'sepal_length', None, None, None, hover_name=None, hover_data=None, trendline_options=None, trendline_scope='trace')