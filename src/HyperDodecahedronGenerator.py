import itertools
import json
import os
import numpy as np


class HyperDodecahedronGenerator:

    @staticmethod
    def generate_120cell():
        phi = (1 + np.sqrt(5)) / 2
        inv_phi = 1 / phi

        bases = [
            *itertools.product([-1, 1], repeat=4),

            *[(2, 0, 0, 0), (-2, 0, 0, 0),
              (0, 2, 0, 0), (0, -2, 0, 0),
              (0, 0, 2, 0), (0, 0, -2, 0),
              (0, 0, 0, 2), (0, 0, 0, -2)],

            *[(x, y, z, w) for x, y, z, w in itertools.product([-1, 1], repeat=4)
              if abs(x) == 1 and abs(y) == 1 and abs(z) == 1 and abs(w) == phi],

            *[(x, y, z, 0) for x, y, z in itertools.product([-1, 1], repeat=3)
              if abs(x) == 1 and abs(y) == phi and abs(z) == inv_phi],
        ]

        vertices = set()
        for base in bases:
            for perm in itertools.permutations(base):
                vertices.add(perm)

        vertices = [tuple(np.array(v) / np.linalg.norm(v)) for v in vertices]

        print(f"Número de vértices gerados: {len(vertices)}")

        edges = set()
        threshold = 1.05

        for i, v1 in enumerate(vertices):
            for j, v2 in enumerate(vertices):
                if i < j:
                    dist = np.linalg.norm(np.array(v1) - np.array(v2))
                    if dist < threshold:
                        edges.add((i, j))

        vertices_list = [list(vertex) for vertex in vertices]
        edges_list = [list(edge_tuple) for edge_tuple in edges]

        HyperDodecahedronGenerator.append_to_json(vertices_list, edges_list)

    @staticmethod
    def append_to_json(vertices, edges, filename="hyper_shapes.json"):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        if "hyper_dodecahedron" not in data:
            data["hyper_dodecahedron"] = {}

            data["hyper_dodecahedron"]["vertices"] = vertices
            data["hyper_dodecahedron"]["edges"] = edges

            n_data = data

            with open(filename, "w") as f:
                json.dump(n_data, f, indent=2)
        else:
            print("Hyper dodecahedron already exists in the file.")

