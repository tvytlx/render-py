from render import render, Model

# you can export the *.obj format model data from blender
render(
    Model("res/jinx.obj", texture_filename="res/jinx.tga"),
    height=4000,
    width=4000,
    filename="jinx.png",
)
