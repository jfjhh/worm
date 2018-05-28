import numpy as np

vec = np.array
mat = np.array


def homogenize(vec3, h=1.):
    return vec([*vec3, h])


def heterogenize(vec4):
    return vec([*[x/vec4[3] for x in vec4]])


def roll_push(x, a):
    x.pop(0); x.append(a);


def mean(x):
    return sum(x) / len(x)

