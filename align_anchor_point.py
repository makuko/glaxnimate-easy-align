from glaxnimate.model.shapes import Group
from glaxnimate.utils import Point
from bounding_box import get_bounding_box
from offset import get_offset


def main(window, document, settings):
    composition = window.current_composition
    uuid = window.current_shape.uuid
    group = composition.find_by_uuid(uuid)

    if not isinstance(group, Group):
        return

    bounding_box = get_bounding_box(composition, uuid)

    if bounding_box == None:
        return

    offset = get_offset(composition, uuid)
    delta_x = group.transform.anchor_point.value.x - group.transform.position.value.x
    delta_y = group.transform.anchor_point.value.y - group.transform.position.value.y
    x = bounding_box["left"] - offset["x"]
    y = bounding_box["top"] - offset["y"]

    if settings["horizontal"] == "Center":
        x += bounding_box["width"] / 2
    elif settings["horizontal"] == "Right":
        x += bounding_box["width"]

    if settings["vertical"] == "Center":
        y += bounding_box["height"] / 2
    elif settings["vertical"] == "Bottom":
        y += bounding_box["height"]

    with document.macro("Align anchor point"):
        group.transform.position.value = Point(x, y)
        group.transform.anchor_point.value = Point(x + delta_x, y + delta_y)
