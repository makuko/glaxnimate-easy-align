import math
from glaxnimate.model.shapes import Group
from glaxnimate.utils import Point, Vector2D


def discard_transforms(groups, point):
    point = Point(point.x, point.y)

    for group in groups:
        if isinstance(group, Group):
            anchor_point = group.transform.anchor_point.value or Point(0, 0)
            position = group.transform.position.value or Point(0, 0)
            scale = group.transform.scale.value
            rotation = group.transform.rotation.value

            transform_point(point, position, anchor_point, Vector2D(1 / scale.x, 1 / scale.y), -rotation)

    return point


def apply_transforms(groups, point):
    point = Point(point.x, point.y)

    for group in groups:
        if isinstance(group, Group):
            anchor_point = group.transform.anchor_point.value or Point(0, 0)
            position = group.transform.position.value or Point(0, 0)
            scale = group.transform.scale.value
            rotation = group.transform.rotation.value

            transform_point(point, anchor_point, position, scale, rotation)

    return point


def transform_point(point, anchor_point, position, scale, rotation):
    x = point.x - anchor_point.x
    y = point.y - anchor_point.y

    rad = rotation / 180 * math.pi

    point.x = (x * math.cos(rad) - y * math.sin(rad)) * scale.x + position.x
    point.y = (y * math.cos(rad) + x * math.sin(rad)) * scale.y + position.y
