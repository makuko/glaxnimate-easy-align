from glaxnimate.model.shapes import Group
from glaxnimate.utils import Point
from bounds import get_bounds
from parents import get_parents
from transform import discard_transforms


def main(window, document, settings):
    composition = window.current_composition
    uuid = window.current_shape.uuid
    group = composition.find_by_uuid(uuid)

    if not isinstance(group, Group):
        window.warning("Please select a layer or group")
        return

    bounds = get_bounds(composition, uuid)

    if bounds == None:
        return

    offset = Point(bounds.left, bounds.top)

    if settings["horizontal"] == "Center":
        offset.x += bounds.width / 2
    elif settings["horizontal"] == "Right":
        offset.x += bounds.width

    if settings["vertical"] == "Center":
        offset.y += bounds.height / 2
    elif settings["vertical"] == "Bottom":
        offset.y += bounds.height

    parents = get_parents(composition, uuid)
    position = discard_transforms(parents, offset)
    anchor_point = discard_transforms([*parents, group], offset)

    with document.macro("Align anchor point"):
        group.transform.position.value = position
        group.transform.anchor_point.value = anchor_point
