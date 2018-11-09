import json
from hashlib import md5


def test_generate_faces_with_z_buffer(read_data):
    from render.speedup import generate_faces_with_z_buffer

    data = read_data("triangles.json")
    res = generate_faces_with_z_buffer(data)
    return (
        md5(json.dumps(res).encode()).hexdigest() == "1e0be2a10306b053e8a41dc3c593399e"
    )
