# render-py

Software rasterizer written in Python.

```python
from render import render, Model

# you can export the *.obj format model data from Blender
render(Model("res/monkey.obj"), height=4000, width=4000, filename="monkey.png")
```

Then open `monkey.png`!


<img src="./res/monkey_wireframe.png" alt="monkey" width="320" height="320">

<img src="./res/monkey_standard.png" alt="monkey" width="320" height="320">

<img src="./res/monkey_zbuffer.png" alt="monkey" width="320" height="320">

 ✨🍰✨
