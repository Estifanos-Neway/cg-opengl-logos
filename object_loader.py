import numpy as np
import itertools


def loadObject(filename, swapyz=False):
    vertices = []
    texcoords = []
    faces = []

    f = open(filename, "r")
    for line in f:
        if line.startswith("#"):
            continue

        values = line.split()

        if not values:
            continue

        if values[0] == "v":
            v = list(map(float, values[1:4]))
            if swapyz:
                v = v[0], v[2], v[1]
            vertices.append(v)

        elif values[0] == "vt":
            texcoords.append(list(map(float, values[1:3])))

        elif values[0] == "f":
            face = []
            texs = []

            for v in values[1:]:
                w = v.split("/")
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    texs.append(int(w[1]))
                else:
                    texs.append(0)

            vert0, vert1, vert2 = list(map(lambda x: vertices[x - 1], face))
            tex0, tex1, tex2 = list(map(lambda x: texcoords[x - 1], texs))

            faces += itertools.chain(vert0, tex0, [0, 0, 0], vert1, tex1, [0, 0, 0], vert2, tex2, [0, 0, 0])

    f.close()
    return len(faces) // 9, np.array(faces, dtype='float32')
