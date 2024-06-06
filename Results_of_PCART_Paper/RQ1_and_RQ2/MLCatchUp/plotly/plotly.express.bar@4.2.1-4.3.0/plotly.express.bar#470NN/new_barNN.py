import plotly.express as px
data_canada = px.data.gapminder().query("country == 'Canada'")
fig = px.bar(data_canada, 'year', 'pop', None, None, None, None, None, None, None, None, None, None, None, None, None, {}, {}, None, {}, None, None, None, None, 'v', 'relative', log_x=False, log_y=False, range_x=None, range_y=None, facet_col_wrap=0)