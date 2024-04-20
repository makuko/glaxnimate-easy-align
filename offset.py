from glaxnimate.model.shapes import Group
from glaxnimate.utils import Point
from parents import get_parents
import glaxnimate


def get_offset(composition, uuid):
    parents = get_parents(composition, uuid)
    offset = {
        "x": 0,
        "y": 0
    }

    for parent in parents:
        if isinstance(parent, Group):
            position = parent.transform.position.value if parent.transform.position.value else Point(0, 0)
            anchor_point = parent.transform.anchor_point.value if parent.transform.anchor_point.value else Point(0, 0)

            offset["x"] += position.x - anchor_point.x
            offset["y"] += position.y - anchor_point.y

    return offset
