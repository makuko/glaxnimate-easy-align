from uuid import UUID
from os import path
from glaxnimate.model.shapes import Group, Image, PreCompLayer
from glaxnimate.utils import Point
from bounds import get_bounds
from parents import get_parents
from transform import apply_transforms, discard_transforms


basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "target.txt"))


def main(window, document, settings):
    selected = window.current_shape

    if (
        not isinstance(selected, Group)
        and not isinstance(selected, Image)
        and not isinstance(selected, PreCompLayer)
    ):
        window.warning("Please select a layer, group, image or precomposition")

        return

    try:
        f = open(filepath, "r")
    except:
        window.warning("Please set a target first")

        return

    target_uuid = UUID(f.read())

    f.close()

    composition = window.current_composition
    target = composition.find_by_uuid(target_uuid)

    if target == None:
        window.warning("Please set a target first")

        return

    dialog = window.create_dialog("align_with_target.ui")

    if not dialog:
        return

    if dialog.exec():
        selected_horizontal, target_horizontal = get_horizontal(dialog)
        selected_vertical, target_vertical = get_vertical(dialog)

        if selected_horizontal == "keep" and selected_vertical == "keep":
            return

        target_bounds = get_bounds(composition, target_uuid)
        selected_bounds = get_bounds(composition, selected.uuid)

        if target_bounds is None:
            window.warning("Target shape is empty and has no size")

            return

        if selected_bounds is None:
            window.warning("Selected shape is empty and has no size")

            return

        parents = get_parents(composition, selected.uuid)
        position = apply_transforms(parents, selected.transform.position.value or Point(0, 0))

        if selected_horizontal != "keep":
            position.x += target_bounds.left - selected_bounds.left

            if target_horizontal == "center":
                position.x += target_bounds.width / 2
            elif target_horizontal == "right":
                position.x += target_bounds.width

            if selected_horizontal == "center":
                position.x -= selected_bounds.width / 2
            elif selected_horizontal == "right":
                position.x -= selected_bounds.width

        if selected_vertical != "keep":
            position.y += target_bounds.top - selected_bounds.top

            if target_vertical == "center":
                position.y += target_bounds.height / 2
            elif target_vertical == "bottom":
                position.y += target_bounds.height

            if selected_vertical == "center":
                position.y -= selected_bounds.height / 2
            elif selected_vertical == "bottom":
                position.y -= selected_bounds.height

        with document.macro("Align with target"):
            selected.transform.position.value = discard_transforms(parents, position)


def get_horizontal(dialog):
    if dialog.get_value("hRightLeft", "checked"):
        return "right", "left"

    if dialog.get_value("hCenterLeft", "checked"):
        return "center", "left"

    if dialog.get_value("hLeftLeft", "checked"):
        return "left", "left"

    if dialog.get_value("hRightCenter", "checked"):
        return "right", "center"

    if dialog.get_value("hCenterCenter", "checked"):
        return "center", "center"

    if dialog.get_value("hLeftCenter", "checked"):
        return "left", "center"

    if dialog.get_value("hRightRight", "checked"):
        return "right", "right"

    if dialog.get_value("hCenterRight", "checked"):
        return "center", "right"

    if dialog.get_value("hLeftRight", "checked"):
        return "left", "right"

    return "keep", "keep"


def get_vertical(dialog):
    if dialog.get_value("vBottomTop", "checked"):
        return "bottom", "top"

    if dialog.get_value("vCenterTop", "checked"):
        return "center", "top"

    if dialog.get_value("vTopTop", "checked"):
        return "top", "top"

    if dialog.get_value("vBottomCenter", "checked"):
        return "bottom", "center"

    if dialog.get_value("vCenterCenter", "checked"):
        return "center", "center"

    if dialog.get_value("vTopCenter", "checked"):
        return "top", "center"

    if dialog.get_value("vBottomBottom", "checked"):
        return "bottom", "bottom"

    if dialog.get_value("vCenterBottom", "checked"):
        return "center", "bottom"

    if dialog.get_value("vTopBottom", "checked"):
        return "top", "bottom"

    return "keep", "keep"
