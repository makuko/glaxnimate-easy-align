import math
from glaxnimate.model.shapes import Layer, Group, Shape, Image, PreCompLayer, ShapeElement
from glaxnimate.utils import Point
from parents import get_parents
from transform import get_transform_values, transform_point


class Curve:
    def __init__(self, p0, c0, c1, p1):
        self.p0 = p0
        self.c0 = c0
        self.c1 = c1
        self.p1 = p1

    def __str__(self):
        return "p0: " + str(curve.p0) + ", c0: " +  str(curve.c0) + ", c1: " + str(curve.c1) + ", p1: " + str(curve.p1)


class Bounds:
    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.width = right - left
        self.height = bottom - top

    def __str__(self):
        return "t:" + str(self.top) + ", b: " + str(self.bottom) + ", l: " + str(self.left) + ", r: " + str(self.right)


def get_bounds(composition, uuid):
    node = composition.find_by_uuid(uuid)
    parents = get_parents(composition, uuid)

    return get_node_bounds(node, parents)


def get_node_bounds(node, parents):
    if isinstance(node, ShapeElement) and not node.visible:
        return None

    if isinstance(node, Layer):
        if not node.animation.time_visible:
            return None

        return get_parent_bounds(node, parents)

    if isinstance(node, Group):
        return get_parent_bounds(node, parents)

    if isinstance(node, PreCompLayer):
        return get_precomposition_bounds(node, parents)

    if isinstance(node, Image):
        return get_image_bounds(node, parents)

    if isinstance(node, Shape):
        return get_shape_bounds(node, parents)

    return None


def get_parent_bounds(parent, parents):
    parents = [parent, *parents]

    top = math.inf
    bottom = -math.inf
    left = math.inf
    right = -math.inf

    for node in parent.shapes:
        bounds = get_node_bounds(node, parents)

        if bounds == None:
            continue

        top = min(bounds.top, top)
        bottom = max(bounds.bottom, bottom)
        left = min(bounds.left, left)
        right = max(bounds.right, right)

    if math.isinf(top) or math.isinf(bottom) or math.isinf(left) or math.isinf(right):
        return None

    return Bounds(top, bottom, left, right)


def get_precomposition_bounds(precomposition, parents):
    if not precomposition.composition.visible:
        return None

    return get_parent_bounds(precomposition.composition, [precomposition, *parents])


def get_image_bounds(image, parents):
    a = Point(0, 0)
    b = Point(image.image.width, 0)
    c = Point(image.image.width, image.image.height)
    d = Point(0, image.image.height)

    for parent in [image, *parents]:
        if (
            isinstance(parent, Group)
            or isinstance(parent, Image)
            or isinstance(parent, PreCompLayer)
        ):
            anchor_point, position, scale, rotation = get_transform_values(parent.transform)

            transform_point(a, anchor_point, position, scale, rotation)
            transform_point(b, anchor_point, position, scale, rotation)
            transform_point(c, anchor_point, position, scale, rotation)
            transform_point(d, anchor_point, position, scale, rotation)

    return Bounds(
        min(a.y, b.y, c.y, d.y),
        max(a.y, b.y, c.y, d.y),
        min(a.x, b.x, c.x, d.x),
        max(a.x, b.x, c.x, d.x)
    )


def get_shape_bounds(shape, parents):
    path = shape.to_path()
    bezier = path.shape.value

    n = len(bezier) - int(not bezier.closed)

    curves = []

    for i in range(n):
        curves.append(Curve(
            bezier[i].pos,
            bezier[i].tan_out,
            bezier[(i + 1) % n].tan_in,
            bezier[(i + 1) % n].pos
        ))

    for parent in parents:
        if (
            isinstance(parent, Group)
            or isinstance(parent, Image)
            or isinstance(parent, PreCompLayer)
        ):
            anchor_point, position, scale, rotation = get_transform_values(parent.transform)

            for curve in curves:
                transform_point(curve.p0, anchor_point, position, scale, rotation)
                transform_point(curve.c0, anchor_point, position, scale, rotation)
                transform_point(curve.c1, anchor_point, position, scale, rotation)
                transform_point(curve.p1, anchor_point, position, scale, rotation)

    top = math.inf
    bottom = -math.inf
    left = math.inf
    right = -math.inf

    for curve in curves:
        bounds = get_curve_bounds(curve.p0, curve.c0, curve.c1, curve.p1)

        top = min(bounds.top, top)
        bottom = max(bounds.bottom, bottom)
        left = min(bounds.left, left)
        right = max(bounds.right, right)

    return Bounds(top, bottom, left, right)


def get_curve_bounds(p0, c0, c1, p1):
    left, right = get_axis_bounds(p0.x, c0.x, c1.x, p1.x)
    top, bottom = get_axis_bounds(p0.y, c0.y, c1.y, p1.y)

    return Bounds(top, bottom, left, right)


def get_axis_bounds(p0, c0, c1, p1):
    a = 3 * p1 - 9 * c1 + 9 * c0 - 3 * p0
    b = 6 * p0 - 12 * c0 + 6 * c1
    c = 3 * c0 - 3 * p0

    lo = min(p0, p1)
    hi = max(p0, p1)

    f = lambda t: (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * c0 + 3 * (1 - t) * t ** 2 * c1 + t ** 3 * p1

    if a == 0:
        if b == 0:
            return lo, hi

        t = -c / b;

        if t > 0 and t < 1:
            v = f(t)
            lo = min(v, lo)
            hi = max(v, hi)

        return lo, hi

    disc = b ** 2 - 4 * a * c

    if disc >= 0:
        t1 = (-b + math.sqrt(disc)) / (2 * a)

        if t1 > 0 and t1 < 1:
            v = f(t1)
            lo = min(v, lo)
            hi = max(v, hi)

        t2 = (-b - math.sqrt(disc)) / (2 * a)

        if t2 > 0 and t2 < 1:
            v = f(t2)
            lo = min(v, lo)
            hi = max(v, hi)

    return lo, hi
