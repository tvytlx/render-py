def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross_product(v1, v2):
    """numpy's cross product is too slow
    """
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    )


def generate_faces_with_z_buffer(triangles):
    """ draw the triangle faces with z buffer

    Args:
        triangles: groups of vertices

    https://github.com/ssloy/tinyrenderer/wiki/Lesson-3:-Hidden-faces-removal-(z-buffer)
    """
    faces = []
    zbuffer = {}
    for a, b, c in triangles:
        pixels = []
        res = sorted([a[0], b[0], c[0]])
        minx, maxx = res[0], res[-1] + 2
        res = sorted([a[1], b[1], c[1]])
        miny, maxy = res[0] - 1, res[-1] + 2
        for x in range(int(minx), int(maxx)):
            for y in range(int(miny), int(maxy)):
                sx = (c[0] - a[0], b[0] - a[0], a[0] - x)
                sy = (c[1] - a[1], b[1] - a[1], a[1] - y)
                u = cross_product(sx, sy)
                bc = None
                if abs(u[2]) > 0:
                    bcy, bcz = u[1] / u[2], u[0] / u[2]
                    bc = (1 - bcy - bcz, bcy, bcz)
                # here, -0.00001 because of the precision lose
                if not bc or any(d < -0.00001 for d in bc):
                    continue
                z = a[2] * bc[0] + b[2] * bc[1] + c[2] * bc[2]
                # https://en.wikipedia.org/wiki/Pairing_function
                idx = ((x + y) * (x + y + 1) + y) / 2
                if zbuffer.get(idx) is None or zbuffer[idx] < z:
                    zbuffer[idx] = z
                    pixels.append((x, y))
        faces.append(pixels)
    return faces
