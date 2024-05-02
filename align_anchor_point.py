from glaxnimate.model.shapes import Group, Image, PreCompLayer
from glaxnimate.utils import Point
from bounds import get_bounds
from parents import get_parents
from transform import discard_transforms


def main(window, document, settings):
    composition = window.current_composition
    uuid = window.current_shape.uuid
    node = composition.find_by_uuid(uuid)

    if (
        not isinstance(node, Group)
        and not isinstance(node, Image)
        and not isinstance(node, PreCompLayer)
    ):
        window.warning("Please select a layer, group, image or precomposition")

        return

    bounds = get_bounds(composition, uuid)

    if bounds == None:
        return

    dialog = window.create_dialog("align_anchor_point.ui")

    if not dialog:
        return

    if dialog.exec():
        vertical, horizontal = get_setting(dialog)

        if horizontal == "keep" and vertical == "keep":
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
        anchor_point = discard_transforms([*parents, node], offset)

        with document.macro("Align anchor point"):
            node.transform.position.value = position
            node.transform.anchor_point.value = anchor_point


def get_setting(dialog):
    if dialog.get_value("topLeft", "checked"):
        return "top", "left"

    if dialog.get_value("topCenter", "checked"):
        return "top", "center"

    if dialog.get_value("topRight", "checked"):
        return "top", "right"

    if dialog.get_value("centerLeft", "checked"):
        return "center", "left"

    if dialog.get_value("centerCenter", "checked"):
        return "center", "center"

    if dialog.get_value("centerRight", "checked"):
        return "center", "right"

    if dialog.get_value("bottomLeft", "checked"):
        return "bottom", "left"

    if dialog.get_value("bottomCenter", "checked"):
        return "bottom", "center"

    if dialog.get_value("bottomRight", "checked"):
        return "bottom", "right"

    return "keep", "keep"
