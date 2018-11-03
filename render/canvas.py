import typing as t

from PIL import Image, ImageColor


class Canvas:
    def __init__(self, height=500, width=500):
        self.height, self.width = height, width
        self.img = Image.new("RGB", (self.height, self.width))

    def draw(self, dots, color: t.Union[tuple, str]):
        if isinstance(color, str):
            color = ImageColor.getrgb(color)
        if isinstance(dots, tuple):
            dots = [dots]
        for dot in dots:
            self.img.putpixel(dot, color)

    def save(self, filename="test.png"):
        self.img.save(filename)
