import plotly.express as px
df = px.data.gapminder().query("country=='Brazil'")
fig = px.line_3d(df, 'gdpPercap', 'pop', 'year', None, None, None, None, None, None, None, None, None, None, None, None, None, None, animation_group=None, category_orders=None, labels=None, color_discrete_sequence=None, symbol=None, symbol_sequence=None, symbol_map=None, markers=False)