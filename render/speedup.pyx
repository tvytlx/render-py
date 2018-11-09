import cython
import numpy as np
cimport numpy as np
cimport cython

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
cpdef dot_product(np.ndarray[np.float_t, ndim=1] a, np.ndarray[np.float_t, ndim=1] b):
    cdef double r = a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    return r


@cython.boundscheck(False)
cpdef (double, double, double) cross_product(double v10, double v11, double v12, double v20, double v21, double v22):
    cdef double x = v11 * v22 - v12 * v21
    cdef double y = v12 * v20 - v10 * v22
    cdef double z = v10 * v21 - v11 * v20
    return x,y,z


cdef min_max(double a, double b, double c):
    cdef double t
    if a > b:
        t = b
        a = b
        b = a
    return (a,b,c)


@cython.binding(True)
@cython.boundscheck(False)
#def generate_faces_with_z_buffer(np.ndarray[np.float_t, ndim=3] triangles):
def generate_faces_with_z_buffer(double [:, :, :] triangles):
    """ draw the triangle faces with z buffer

    Args:
        triangles: groups of vertices

    https://github.com/ssloy/tinyrenderer/wiki/Lesson-3:-Hidden-faces-removal-(z-buffer)
    """
    cdef int i = 0, length, x, y
    cdef double z, bcy, bcz
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
        for x in range(minx, maxx + 2):
            for y in range(miny - 1, maxy + 2):
                u[0], u[1], u[2] = cross_product(c[0] - a[0], b[0] - a[0], a[0] - x, c[1] - a[1], b[1] - a[1], a[1] - y)
                if abs(u[2]) > 0:
                    bcy, bcz = u[1] / u[2], u[0] / u[2]
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
                    pixels.append((x, y, i))
        faces.append(pixels)
    return faces
