from PIL import Image, ImageDraw
image = Image.new('RGB', (300, 300), 'white')
draw = ImageDraw.Draw(image)
draw.regular_polygon(bounding_circle=(150, 150, 100), n_sides=6, rotation=0, width=1)