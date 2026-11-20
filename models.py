from dataclasses import dataclass


type vec2 = tuple[float, float]


@dataclass
class Pos2:
    x:float
    y:float

    @property
    def val(self):
        return self.x, self.y
    @val.setter
    def val(self, v:vec2):
        self.x, self.y = v

    def __add__(self, other):
        return Pos2(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Pos2(-self.x, -self.y)

    def __sub__(self, other):
        return -other + self

    def __mul__(self, other):
        if isinstance(other, float|int):
            return Pos2(self.x * other, self.y * other)
        elif isinstance(other, Pos2):
            return Pos2(self.x * other.x, self.y * other.y)
        else:
            return None


class Body(Pos2):
    m:float = 1   # [kg]

    vx:float = 0
    vy:float = 0

    def __init__(self, x:float = 0, y:float = 0, m:float = 1, vx:float = 0, vy:float = 0):
        super().__init__(x, y)
        self.m = m
        self.vx = vx
        self.vy = vy


@dataclass
class Interval:
    x_lo:float
    x_hi:float

    def contains(self, x:float):
        return self.x_lo <= x < self.x_hi

    def split(self):
        x_mi = (self.x_lo + self.x_hi) / 2
        return Interval(self.x_lo, x_mi), Interval(x_mi, self.x_hi)


@dataclass
class Bounds2:
    x_int:Interval
    y_int:Interval

    def contain(self, pos:Pos2):
        return self.x_int.contains(pos.x) and self.y_int.contains(pos.y)

    def split(self):
        x_lo, x_hi = self.x_int.split()
        y_lo, y_hi = self.y_int.split()
        return (Bounds2(x_lo, y_lo), Bounds2(x_hi, y_lo),
                Bounds2(x_lo, y_hi), Bounds2(x_hi, y_hi))


class TreeNode:
    bounds:Bounds2
    children:list["TreeNode"]
    bodies:list[Body]

    mass:float
    com:Pos2

    depth:int
    bodycount:int


    def __init__(self, bounds:Bounds2, depth:int = 0):
        self.bounds = bounds
        self.children = []
        self.bodies = []

        self.mass = None
        self.com = None

        self.depth = depth
        self.bodycount = 0

    def sprout(self):
        self.children = [
            TreeNode(bound_quarter, self.depth+1) for bound_quarter in self.bounds.split()
        ]
        for child in self.children:
            for body in self.bodies:
                if child.bounds.contain(body):
                    child.bodies.append(body)
        self.bodycount = len(self.bodies)
        self.bodies = []

    def calculate_properties(self):
        if 0 < len(self.bodies):
            mass = 0
            comx, comy = 0, 0

            for body in self.bodies:
                mass += body.m
                comx += body.x * body.m
                comy += body.y * body.m

            comx /= mass
            comy /= mass

        elif 0 < len(self.children):
            mass = 0
            comx, comy = 0, 0

            for child in self.children:
                mass += child.mass
                comx += child.com.x * child.mass
                comy += child.com.y * child.mass

            comx /= mass
            comy /= mass

        else: # empty leaf
            mass = 0
            comx, comy = 0, 0

        self.mass = mass
        self.com = Pos2(comx, comy)



def build_tree(bounds:Bounds2, bodies:list[Body], max_depth:int = 16):
    root = TreeNode(bounds, 0)
    root.bodies = bodies

    # build the tree structure
    def subdivide(node:TreeNode, remaining_depth:int):
        if len(node.bodies) <= 1 or remaining_depth <= 0:
            return

        node.sprout()

        for child in node.children:
            subdivide(child, remaining_depth - 1)

    subdivide(root, max_depth)

    # calculate node properties like `mass` and `com`
    def properterize(node:TreeNode):
        for child in node.children:
            properterize(child)

        # and go from leaves up
        node.calculate_properties()
    properterize(root)

    return root

