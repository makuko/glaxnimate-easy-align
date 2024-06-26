import math
from glaxnimate.model.shapes import Group, Image, PreCompLayer
from glaxnimate.utils import Point, Vector2D


def discard_transforms(nodes, point):
    point = Point(point.x, point.y)

    for node in nodes:
        if (
            isinstance(node, Group)
            or isinstance(node, Image)
            or isinstance(node, PreCompLayer)
        ):
            anchor_point, position, scale, rotation = get_transform_values(node.transform)

            transform_point(point, position, anchor_point, Vector2D(1 / scale.x, 1 / scale.y), -rotation)

    return point


def apply_transforms(nodes, point):
    point = Point(point.x, point.y)

    for node in nodes:
        if (
            isinstance(node, Group)
            or isinstance(node, Image)
            or isinstance(node, PreCompLayer)
        ):
            anchor_point, position, scale, rotation = get_transform_values(node.transform)

            transform_point(point, anchor_point, position, scale, rotation)

    return point


def get_transform_values(transform):
    return (
        transform.anchor_point.value or Point(0, 0),
        transform.position.value or Point(0, 0),
        transform.scale.value,
        transform.rotation.value
    )


def transform_point(point, anchor_point, position, scale, rotation):
    x = point.x - anchor_point.x
    y = point.y - anchor_point.y

    rad = rotation / 180 * math.pi

    point.x = (x * math.cos(rad) - y * math.sin(rad)) * scale.x + position.x
    point.y = (y * math.cos(rad) + x * math.sin(rad)) * scale.y + position.y
