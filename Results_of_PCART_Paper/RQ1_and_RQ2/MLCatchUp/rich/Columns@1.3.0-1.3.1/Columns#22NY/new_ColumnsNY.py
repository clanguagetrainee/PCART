from rich.columns import Columns
renderables = [f'Column {i}' for i in range(1, 4)]
columns = Columns(renderables, (0, 1), False, False, False, right_to_left=False, width=None)