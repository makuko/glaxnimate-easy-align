from uuid import UUID
from os import path
from glaxnimate.model.shapes import Group, Image, PreCompLayer
from glaxnimate.utils import Point
from bounds import get_bounds
from message import warning
from parents import find_node, get_parents
from transform import apply_transforms, discard_transforms


basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "target.txt"))


def main(window, document, settings):
    selected_horizontal = settings["horizontal"]
    target_horizontal = settings["target_horizontal"]
    selected_vertical = settings["vertical"]
    target_vertical = settings["target_vertical"]

    if selected_horizontal == "keep" and selected_vertical == "keep":
        return

    selected = window.current_shape

    if (
        not isinstance(selected, Group)
        and not isinstance(selected, Image)
        and not isinstance(selected, PreCompLayer)
    ):
        warning(window, "Please select a layer, group, image or precomposition")

        return

    try:
        f = open(filepath, "r")
    except:
        warning(window, "Please set a target first")

        return

    target_uuid = UUID(f.read())

    f.close()

    composition = window.current_composition
    target = find_node(composition, target_uuid)

    if target == None:
        warning(window, "Please set a target first")

        return

    target_bounds = get_bounds(composition, target_uuid)
    selected_bounds = get_bounds(composition, selected.uuid)

    if target_bounds is None:
        warning(window, "Target shape is empty and has no size")

        return

    if selected_bounds is None:
        warning(window, "Selected shape is empty and has no size")

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
