import cython
import numpy as np
cimport numpy as np
cimport cython


cdef extern from "math.h":
    double sqrt(double x)


def normalize(double x, double y, double z):
    cdef double unit = sqrt(x * x + y * y + z * z)
    if unit == 0:
        return 0, 0, 0
    return x / unit, y / unit, z / unit


cdef (int, int) get_min_max(double a, double b, double c):
    cdef double min = a
    cdef double max = a
    if min > b:
        min = b
    if min > c:
        min = c
    if max < b:
        max = b
    if max < c:
        max = c
    return int(min), int(max)



@cython.boundscheck(False)
cpdef double dot_product(double a0, double a1, double a2, double b0, double b1, double b2):
    cdef double r = a0 * b0 + a1 * b1 + a2 * b2
    return r


@cython.boundscheck(False)
cpdef (double, double, double) cross_product(double a0, double a1, double a2, double b0, double b1, double b2):
    cdef double x = a1 * b2 - a2 * b1
    cdef double y = a2 * b0 - a0 * b2
    cdef double z = a0 * b1 - a1 * b0
    return x,y,z


@cython.boundscheck(False)
def generate_faces_with_z_buffer(double [:, :, :] triangles):
    """ draw the triangle faces with z buffer

    Args:
        triangles: groups of vertices

    https://github.com/ssloy/tinyrenderer/wiki/Lesson-3:-Hidden-faces-removal-(z-buffer)
    """
    cdef int i, j, k, length
    cdef double bcy, bcz, x, y, z
    cdef double a[3], b[3], c[3], u[3], bc[3]
    cdef int minx, maxx, miny, maxy
    length = triangles.shape[0]
    zbuffer = {}
    faces = []
    for i in range(length):
        a = triangles[i, 0, 0], triangles[i, 0, 1], triangles[i, 0, 2]
        b = triangles[i, 1, 0], triangles[i, 1, 1], triangles[i, 1, 2]
        c = triangles[i, 2, 0], triangles[i, 2, 1], triangles[i, 2, 2]
        minx, maxx = get_min_max(a[0], b[0], c[0])
        miny, maxy = get_min_max(a[1], b[1], c[1])
        pixels = []
        for j in range(minx, maxx + 2):
            for k in range(miny - 1, maxy + 2):
                # 必须转换成 double 参与底下的运算，不然算出来的结果是错的，这也太奇葩了吧
                # 关键是我还不知道隐式的 cast 到底是在哪里出了问题
                x = j
                y = k

                u[0], u[1], u[2] = cross_product(c[0] - a[0], b[0] - a[0], a[0] - x, c[1] - a[1], b[1] - a[1], a[1] - y)
                if abs(u[2]) > 0:
                    bcy = u[1] / u[2]
                    bcz = u[0] / u[2]
                    bc = (1 - bcy - bcz, bcy, bcz)
                else:
                    continue

                # here, -0.00001 because of the precision lose
                if bc[0] < -0.00001 or bc[1] < -0.00001 or bc[2] < -0.00001:
                    continue

                z = a[2] * bc[0] + b[2] * bc[1] + c[2] * bc[2]
                # https://en.wikipedia.org/wiki/Pairing_function
                idx = ((x + y) * (x + y + 1) + y) / 2
                if zbuffer.get(idx) is None or zbuffer[idx] < z:
                    zbuffer[idx] = z
                    pixels.append((j, k, i))

        faces.append(pixels)
    return faces
