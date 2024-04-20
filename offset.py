from glaxnimate.model.shapes import Group
from parents import get_parents


def get_offset(composition, uuid):
    parents = get_parents(composition, uuid)
    offset = {
        "x": 0,
        "y": 0
    }

    for parent in parents:
        if isinstance(parent, Group):
            offset["x"] += parent.transform.position.value.x - parent.transform.anchor_point.value.x
            offset["y"] += parent.transform.position.value.y - parent.transform.anchor_point.value.y

    return offset
