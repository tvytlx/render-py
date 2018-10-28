import typing as t

import numpy as np
from copy import deepcopy
from .canvas import Canvas


class Vec2d:
    def __init__(self, x, y):
        if isinstance(x, float):
            x = int(x + 0.5)
        if isinstance(y, float):
            y = int(y + 0.5)
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vec2d({self.x}, {self.y})"

    def __truediv__(self, other):
        return (self.y - other.y) / (self.x - other.x)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def draw_line(
    v1: Vec2d, v2: Vec2d, canvas: Canvas, color: t.Union[tuple, str] = "white"
):
    """
    画一条指定颜色的直线

    https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    """
    v1, v2 = deepcopy(v1), deepcopy(v2)
    if v1 == v2:
        canvas.draw((v1.x, v1.y), color=color)
        return

    steep = abs(v1.y - v2.y) > abs(v1.x - v2.x)
    if steep:
        v1.x, v1.y = v1.y, v1.x
        v2.x, v2.y = v2.y, v2.x
    v1, v2 = (v1, v2) if v1.x < v2.x else (v2, v1)
    slope = abs((v1.y - v2.y) / (v1.x - v2.x))
    y = v1.y
    error: float = 0
    incr = 1 if v1.y < v2.y else -1
    dots = []
    for x in range(v1.x, v2.x):
        dots.append((y, x) if steep else (x, y))
        error += slope
        if abs(error) >= 0.5:
            y += incr
            error -= 1

    canvas.draw(dots, color=color)


class Rect:
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right


def line_clipping_2d(v1, v2, rect):  # noqa: C901
    """
        example:
        rect = Rect(200, 400, 200, 400)

        https://blog.csdn.net/cppyin/article/details/6172457
        https://en.wikipedia.org/wiki/Line_clipping
    """

    C = 0
    W, E, S, N = [1 << i for i in range(4)]
    NW = N | W
    NE = N | E
    SW = S | W
    SE = S | E

    def vcode(v: Vec2d) -> int:
        code = 0
        if v.y < rect.top:
            code |= N
        elif v.y > rect.bottom:
            code |= S
        if v.x < rect.left:
            code |= W
        elif v.x > rect.right:
            code |= E
        return code

    code1 = vcode(v1)
    code2 = vcode(v2)

    # 完全被删除
    if bool(code1 & code2):
        return

    # 完全被保留
    if (code1 + code2) == 0:
        return v1, v2

    # 部分被删除
    # 求 v1 与矩形的交点
    def intersection_point(code, v1, v2):
        if code == C:
            return v1

        if code in (N, NW, NE):
            y = rect.top
            x = (
                int(v1.x + (rect.top - v1.y) * (v2.x - v1.x) / (v2.y - v1.y) + 0.5)
                if v2.x != v1.x
                else v2.x
            )
            if x < rect.left:
                return intersection_point(W, v1, v2)
            if x > rect.right:
                return intersection_point(E, v1, v2)
        elif code in (S, SW, SE):
            y = rect.bottom
            x = (
                int(v1.x - (v1.y - rect.bottom) * (v2.x - v1.x) / (v2.y - v1.y) + 0.5)
                if v2.x != v1.x
                else v2.x
            )
            if x < rect.left:
                return intersection_point(W, v1, v2)
            if x > rect.right:
                return intersection_point(E, v1, v2)
        elif code == W:
            if v1.x == v2.x:
                return
            x = rect.left
            y = (
                int(v1.y + (rect.left - v1.x) * (v1 / v2) + 0.5)
                if v1.y != v2.y
                else v1.y
            )
        elif code == E:
            if v1.x == v2.x:
                return
            y = rect.right
            x = (
                int(v1.y - (v1.x - rect.right) * (v1 / v2) + 0.5)
                if v1.y != v2.y
                else v1.y
            )

        # 交点在矩形边框的直线延长线上的情况
        if x < rect.left or x > rect.right or y < rect.top or y > rect.bottom:
            return

        return Vec2d(x, y)

    nv1 = intersection_point(code1, v1, v2)
    nv2 = intersection_point(code2, v2, v1)
    if nv1 and nv2:
        return nv1, nv2


def draw_triangle(v1, v2, v3, canvas, wireframe=False):
    """
    Draw a triangle with 3 ordered vertices

    http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html
    """

    if wireframe:
        draw_line(v1, v2)
        draw_line(v2, v3)
        draw_line(v1, v3)
        return

    def sort_vertices_asc_by_y(vertices):
        return sorted(vertices, key=lambda v: v.y)

    def fill_bottom_flat_triangle(v1, v2, v3):
        invslope1 = (v2.x - v1.x) / (v2.y - v1.y)
        invslope2 = (v3.x - v1.x) / (v3.y - v1.y)

        x1 = x2 = v1.x
        y = v1.y

        while y <= v2.y:
            draw_line(Vec2d(int(x1 + 0.5), y), Vec2d(int(x2 + 0.5), y))
            x1 += invslope1
            x2 += invslope2
            y += 1

    def fill_top_flat_triangle(v1, v2, v3):
        invslope1 = (v3.x - v1.x) / (v3.y - v1.y)
        invslope2 = (v3.x - v2.x) / (v3.y - v2.y)

        x1 = x2 = v3.x
        y = v3.y

        while y > v2.y:
            draw_line(Vec2d(int(x1 + 0.5), y), Vec2d(int(x2 + 0.5), y))
            x1 -= invslope1
            x2 -= invslope2
            y -= 1

    v1, v2, v3 = sort_vertices_asc_by_y((v1, v2, v3))

    # 填充
    if v2.y == v3.y:
        fill_bottom_flat_triangle(v1, v2, v3)
    elif v1.y == v2.y:
        fill_top_flat_triangle(v1, v2, v3)
    else:
        v4 = Vec2d(int(v1.x + (v2.y - v1.y) / (v3.y - v1.y) * (v3.x - v1.x)), v2.y)
        fill_bottom_flat_triangle(v1, v2, v4)
        fill_top_flat_triangle(v2, v4, v3)


def draw_polygon(*vertices):
    """
    似乎没用到，不实现了

    http://www.sunshine2k.de/coding/java/Polygon/Kong/Kong.html
    https://en.wikipedia.org/wiki/Polygon_triangulation#Subtracting_ears_method
    http://www.cs.uu.nl/docs/vakken/ga/slides9alt.pdf
    """
    pass


# 3D part


class Vec3d:
    def __init__(self, *args, value=None):
        if value is not None:
            self.value = value
        else:
            assert len(args) == 3
            self.value = np.matrix(args)

        self.x, self.y, self.z = self.value[0, 0], self.value[0, 1], self.value[0, 2]

    def __repr__(self):
        return repr(self.value)


class Mat4d:
    def __init__(self, narr=None, value=None):
        self.value = np.matrix(narr) if value is None else value

    def __repr__(self):
        return repr(self.value)

    def __mul__(self, other):
        return self.__class__(value=self.value * other.value)


class Vec4d(Mat4d):
    def __init__(self, *args, value=None):
        if value is not None:
            self.value = value
        else:
            assert len(args) == 4
            self.value = np.matrix([[d] for d in args])

        self.x, self.y, self.z, self.w = (
            self.value[0, 0],
            self.value[1, 0],
            self.value[2, 0],
            self.value[3, 0],
        )


class MatrixUtil:
    """
    后续可以把一些Python的算术运算都换成矩阵运算，因为numpy的矩阵运算比纯Python更快。
    """

    @classmethod
    def translate(self, x, y, z) -> Mat4d:
        m = [[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]
        return Mat4d(m)

    @classmethod
    def scale(self, x, y, z) -> Mat4d:
        m = [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]
        return Mat4d(m)

    @classmethod
    def rotate(self, angle_in_degrees, Vec3d: Vec3d) -> Mat4d:
        pass


def look_at(eye: Vec3d, target: Vec3d, up: Vec3d = Vec3d(0, -1, 0)) -> Mat4d:
    """
    http://www.songho.ca/opengl/gl_camera.html#lookat

    Args:
        eye: 摄像机的世界坐标位置
        target: 观察点的位置
        up: 就是你想让摄像机立在哪个方向
            https://stackoverflow.com/questions/10635947/what-exactly-is-the-up-vector-in-opengls-lookat-function
            这里默认使用了 0, -1, 0， 因为 blender 导出来的模型数据似乎有问题，导致y轴总是反的，于是把摄像机的up也翻一下得了。
    """

    def normalize(v):
        import math

        unit = math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
        return Vec3d(v.x / unit, v.y / unit, v.z / unit)

    def dot_product(x: Vec3d, y: Vec3d):
        return x.x * y.x + x.y * y.y + x.z * y.z

    f = normalize(Vec3d(value=eye.value - target.value))
    l = normalize(Vec3d(*np.cross(up.value, f.value)[0]))  # noqa: E741
    u = Vec3d(*np.cross(f.value, l.value)[0])

    rotate_matrix = Mat4d(
        [[l.x, l.y, l.z, 0], [u.x, u.y, u.z, 0], [f.x, f.y, f.z, 0], [0, 0, 0, 1.0]]
    )
    translate_matrix = Mat4d(
        [[1, 0, 0, -eye.x], [0, 1, 0, -eye.y], [0, 0, 1, -eye.z], [0, 0, 0, 1.0]]
    )

    return Mat4d(value=(rotate_matrix * translate_matrix).value)


def perspective_project(r, t, n, f, b=None, l=None):  # noqa: E741
    """
    目的：
        把相机坐标转换成投影在视网膜的范围在(-1, 1)的笛卡尔坐标

    原理：
        对于x，y坐标，相似三角形可以算出投影点的x，y
        对于z坐标，是假设了near是-1，far是1，然后带进去算的
        http://www.songho.ca/opengl/gl_projectionmatrix.html
        https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/opengl-perspective-projection-matrix

    推导出来的矩阵：
        [
            2n/(r-l) 0        (r+l/r-l)   0
            0        2n/(t-b) (t+b)/(t-b) 0
            0        0        -(f+n)/f-n  (-2*f*n)/(f-n)
            0        0        -1          0
        ]

    实际上由于我们用的视网膜(near pane)是个关于远点对称的矩形，所以矩阵简化为：
        [
            n/r      0        0           0
            0        n/t      0           0
            0        0        -(f+n)/f-n  (-2*f*n)/(f-n)
            0        0        -1          0
        ]

    Args:
        r: right, t: top, n: near, f: far, b: bottom, l: left
    """
    return Mat4d(
        [
            [n / r, 0, 0, 0],
            [0, n / t, 0, 0],
            [0, 0, -(f + n) / (f - n), (-2 * f * n) / (f - n)],
            [0, 0, -1, 0],
        ]
    )


def render(model, height, width, filename):
    """
    Args:
        model: the Model object
        height: cavas height
        width: cavas width
        picname: picture file name
    """
    model_matrix = Mat4d([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    view_matrix = look_at(Vec3d(0, 0, 10), Vec3d(0, 0, 0))
    projection_matrix = perspective_project(0.5, 0.5, 2, 1000)
    mvp_matrix = projection_matrix * view_matrix * model_matrix

    vecs, indices = model.vecs, model.indices

    def mvp(v):
        return mvp_matrix * v

    def ndc(v):
        """
        各个坐标同时除以 w，得到 NDC 坐标
        """
        v = v.value
        w = v[3, 0]
        x, y, z = v[0, 0] / w, v[1, 0] / w, v[2, 0] / w
        return Mat4d([[x], [y], [z], [1 / w]])

    def viewport(v):
        v = Vec4d(value=v.value)
        x = y = 0
        w, h = width, height
        n = 0.3
        f = 1000
        return Vec3d(
            w * 0.5 * v.x + x + w * 0.5,
            h * 0.5 * v.y + y + h * 0.5,
            0.5 * (f - n) * v.z + 0.5 * (f + n),
        )

    # this is the render pipeline
    vecs = [viewport(ndc(mvp(v))) for v in vecs]

    canvas = Canvas(height, width)

    for index in indices:
        v1, v2, v3 = [vecs[i - 1] for i in index]
        draw_line(Vec2d(v1.x, v1.y), Vec2d(v2.x, v2.y), canvas=canvas)
        draw_line(Vec2d(v2.x, v2.y), Vec2d(v3.x, v3.y), canvas=canvas)
        draw_line(Vec2d(v3.x, v3.y), Vec2d(v1.x, v1.y), canvas=canvas)

    canvas.save(filename)
