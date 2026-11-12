from glaxnimate.model.shapes import Group, Image, PreCompLayer
from glaxnimate.utils import Point
from bounds import get_bounds
from message import warning
from parents import find_node, get_parents, get_uuid
from transform import discard_transforms


def main(window, document, settings):
    vertical = settings["vertical"]
    horizontal = settings["horizontal"]

    composition = window.current_composition
    uuid = get_uuid(window.current_shape)
    node = find_node(composition, uuid)

    if (
        not isinstance(node, Group)
        and not isinstance(node, Image)
        and not isinstance(node, PreCompLayer)
    ):
        warning(window, "Please select a layer, group, image or precomposition")

        return

    bounds = get_bounds(composition, uuid)

    if bounds == None:
        return

    offset = Point(bounds.left, bounds.top)

    if horizontal == "center":
        offset.x += bounds.width / 2
    elif horizontal == "right":
        offset.x += bounds.width

    if vertical == "center":
        offset.y += bounds.height / 2
    elif vertical == "bottom":
        offset.y += bounds.height

    parents = get_parents(composition, uuid)
    position = discard_transforms(parents, offset)
    anchor_point = discard_transforms([node, *parents], offset)

    with document.macro("Align anchor point"):
        node.transform.position.value = position
        node.transform.anchor_point.value = anchor_point
