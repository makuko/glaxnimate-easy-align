from glaxnimate.model.shapes import Group, Shape
from offset import get_offset


def get_bounding_box(composition, uuid):
    node = composition.find_by_uuid(uuid)

    if isinstance(node, Group):
        return get_group_bounding_box(composition, uuid)

    if isinstance(node, Shape):
        return get_shape_bounding_box(composition, uuid)

    return None


def get_group_bounding_box(composition, uuid):
    group = composition.find_by_uuid(uuid)
    top = None
    bottom = None
    left = None
    right = None

    for node in group.shapes:
        bounding_box = get_bounding_box(composition, node.uuid)

        if bounding_box == None:
            continue

        if (top == None or bounding_box["top"] < top):
            top = bounding_box["top"]

        if (left == None or bounding_box["left"] < left):
            left = bounding_box["left"]

        if (bottom == None or bounding_box["top"] + bounding_box["height"] > bottom):
            bottom = bounding_box["top"] + bounding_box["height"]

        if (right == None or bounding_box["left"] + bounding_box["width"] > right):
            right = bounding_box["left"] + bounding_box["width"]

    if (
        top == None or
        bottom == None or
        left == None or
        right == None
    ):
        return None

    return {
        "width": right - left,
        "height": bottom - top,
        "top": top,
        "left": left
    }


def get_shape_bounding_box(composition, uuid):
    offset = get_offset(composition, uuid)
    node = composition.find_by_uuid(uuid)
    path = node.to_path()
    bounding_box = path.shape.value.bounding_box()

    return {
        "width": bounding_box.size.width,
        "height": bounding_box.size.height,
        "top": offset["y"] + bounding_box.top,
        "left": offset["x"] + bounding_box.left
    }
