import json
from hashlib import md5

import numpy as np


def test_dot_product():
    from speedup import dot_product

    res = dot_product(1, 2, 3, 4, 4, 5)
    assert res == 27


def test_cross_product():
    from speedup import cross_product

    res = cross_product(1, 2, 3, 4, 4, 5)
    assert res == (-2, 7, -4)


def test_generate_faces(read_data):
    from speedup import generate_faces

    data = read_data("triangles.json")
    res = generate_faces(np.array(data), 320, 320)
    return (
        md5(json.dumps(res).encode()).hexdigest() == "1e0be2a10306b053e8a41dc3c593399e"
    )
