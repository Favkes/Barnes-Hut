import numpy as np

from models import Body, TreeNode, vec2, Pos2


def stepBody(body:Body, dt:float = 0.1):
    dx = body.vx * dt
    dy = body.vy * dt

    x_ = body.x + dx
    y_ = body.y + dy

    body.x = x_
    body.y = y_


def r_32vector(body_attracted:Pos2, body_attracting:Pos2, eps:float = 1) -> tuple[vec2, vec2]:
    # returns the `_1byr2 * _1byr` vector also denoted as `_1byr3` or `1/r^3`,
    # multiplied by `[dx, dy]`
    dx = body_attracting.x - body_attracted.x
    dy = body_attracting.y - body_attracted.y

    _1byr2 = 1 / (dx * dx + dy * dy + eps ** 2)
    _1byr = _1byr2 ** 0.5

    _1byr3 = _1byr2 * _1byr

    return _1byr3 * dx, _1byr3 * dy


def calculatePairGravity(body_attracted:Body, body_attracting:Body, eps:float = 1) -> vec2:
    M = body_attracting.m
    _dxbyr3, _dybyr3 = r_32vector(body_attracted, body_attracting, eps)

    ax = _dxbyr3 * M
    ay = _dybyr3 * M

    return ax, ay


def calculateTreeGravity(body:Body, node:TreeNode, theta:float = 1):
    # empty leaf
    if len(node.children) == 0 and len(node.bodies) == 0:
        return 0, 0

    # non-empty leaf
    if 0 < len(node.bodies):
        total_gx, total_gy = 0, 0

        for other in node.bodies:   # leaf can contain multiple bodies if there's a depth limit
            if other is body: continue

            ax, ay = calculatePairGravity(body, other)
            total_gx += ax
            total_gy += ay

        return total_gx, total_gy

    # tree
    x, y = node.bounds.x_int, node.bounds.y_int
    s = max(x.x_hi - x.x_lo, y.x_hi - y.x_lo)

    dx, dy = node.com.x - body.x, node.com.y - body.y
    d2 = dx*dx + dy*dy

    if not node.bounds.contain(body) and s*s < theta**2 * d2:
        gx, gy = r_32vector(body, node.com)
        ax = gx * node.mass
        ay = gy * node.mass
        return ax, ay

    # recursive walk through the tree
    total_gx = total_gy = 0.0
    for child in node.children:
        gx, gy = calculateTreeGravity(body, child, theta)
        total_gx += gx
        total_gy += gy
    return total_gx, total_gy


def calculateTotalGravity(bodies:list[Body], i:int) -> vec2:
    # for body of index `i`
    body = bodies[i]
    total_gx, total_gy = 0, 0

    for other in bodies:
        if other is body: continue

        ax, ay = calculatePairGravity(body, other)
        total_gx += ax
        total_gy += ay

    return total_gx, total_gy



def step(bodies:list[Body], tree:TreeNode, dt:float, theta:float):
    # accelerations = [calculateTotalGravity(bodies, i) for i in range(len(bodies))]
    accelerations = [calculateTreeGravity(body, tree, theta=theta) for body in bodies]

    # x, y, m = np.asarray([(b.x, b.y, b.m) for b in bodies], dtype=float).T
    # dx = x[None, :] - x[:, None]
    # dy = y[None, :] - y[:, None]
    # w = m[None, :] / (dx*dx + dy*dy + 1.0)**1.5 #eps=1
    # accelerations = zip((dx*w).sum(axis=1), (dy*w).sum(axis=1))

    for body, (ax, ay) in zip(bodies, accelerations):
        body.vx += ax * dt
        body.vy += ay * dt
        stepBody(body, dt)

