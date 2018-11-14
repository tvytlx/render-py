# render-py

A software rasterizer written in Python.

<img alt="zbuffer corrected monkey" src="./res/monkey_zbuffer.png" alt="monkey" width="420"> <img src="./res/monkey_wireframe.png" alt="wireframe monkey" width="420">
<img src="./res/jinx.png" alt="jinx" width="420"> <img src="./res/axe.png" alt="axe" width="420">

### Features:

- [x] basic rendering pipeline
- [x] wireframe rendering
- [x] z-buffer rendering
- [x] textures

### Example:

```python
from render import render, Model

# the .obj file is exported from Blender.
render(
    Model("res/jinx.obj", texture_filename="res/jinx.tga"),
    height=4000,
    width=4000,
    filename="jinx.png"
)
```

✨🍰✨
