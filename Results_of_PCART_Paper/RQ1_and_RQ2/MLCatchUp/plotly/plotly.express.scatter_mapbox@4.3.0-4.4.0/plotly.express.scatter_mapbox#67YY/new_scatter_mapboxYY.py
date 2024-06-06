import plotly.express as px
df = px.data.carshare()
fig = px.scatter_mapbox(df, 'centroid_lat', 'centroid_lon', 'peak_hour', None, hover_name=None, hover_data=None, custom_data=None, size=None, animation_frame=None, animation_group=None, center=None, mapbox_style=None)