from plotly.dashboard_objs import Dashboard
my_dboard = Dashboard()
box_1 = {'type': 'box', 'boxType': 'plot', 'fileId': 'graph-1', 'title': 'first graph'}
my_dboard.insert(box=box_1, side='above', box_id=1, fill_percent=50)