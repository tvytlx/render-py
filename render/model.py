from .core import Vec4d


class Model:
    def __init__(self, filename):
        """
        https://en.wikipedia.org/wiki/Wavefront_.obj_file#Vertex_normal_indices
        """
        vertices = []
        indices = []
        with open(filename) as f:
            for line in f:
                if line.startswith("v "):
                    x, y, z = [float(d) for d in line.strip("v").strip().split(" ")]
                    vertices.append(Vec4d(x, y, z, 1))
                elif line.startswith("f "):
                    indices.append(
                        [
                            int(d.split("/")[0])
                            for d in line.strip("f").strip().split(" ")
                        ]
                    )
        self.vertices, self.indices = vertices, indices
