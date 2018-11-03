# render-py

A software rasterizer written in Python.

<img alt="zbuffer corrected" src="./res/monkey_zbuffer.png" alt="monkey" width="440"> <img alt="wireframe" src="./res/monkey_wireframe.png" alt="monkey" width="440">

### Features:

- [x] basic rendering pipeline
- [x] wireframe rendering
- [x] z-buffer rendering
- [ ] textures

### Example:

```python
from render import render, Model

# the .obj file is exported from Blender.
render(Model("res/monkey.obj"), height=4000, width=4000, filename="monkey.png")
```

✨🍰✨
