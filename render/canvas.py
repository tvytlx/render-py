import typing as t

from PIL import Image, ImageColor


class Canvas:
    def __init__(self, filename=None, height=500, width=500):
        self.filename = filename
        self.height, self.width = height, width
        self.img = Image.new("RGBA", (self.height, self.width), (0, 0, 0, 0))

    def draw(self, dots, color: t.Union[tuple, str]):
        if isinstance(color, str):
            color = ImageColor.getrgb(color)
        if isinstance(dots, tuple):
            dots = [dots]
        for dot in dots:
            self.img.putpixel(dot, color + (255,))

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.img.save(self.filename)
