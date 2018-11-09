def test_get_light_intensity(read_data):
    from render.core import get_light_intensity, Vec3d

    data = read_data("w_vertices.json")
    res = get_light_intensity([Vec3d(*d) for d in data])
    assert res == 0.22493567506582834
