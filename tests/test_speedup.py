import json
from hashlib import md5


def test_dot_product():
    from render.speedup import dot_product

    res = dot_product([1, 2, 3], [4, 4, 5])
    assert res == 27


def test_cross_product():
    from render.speedup import cross_product

    res = cross_product([1, 2, 3], [4, 4, 5])
    assert res == (-2, 7, -4)


def test_generate_faces_with_z_buffer(read_data):
    from render.speedup import generate_faces_with_z_buffer

    data = read_data("triangles.json")
    res = generate_faces_with_z_buffer(data)
    return (
        md5(json.dumps(res).encode()).hexdigest() == "1e0be2a10306b053e8a41dc3c593399e"
    )
