from uuid import UUID
from os import path
from glaxnimate.model.shapes import Group
from glaxnimate.utils import Point
from bounds import get_bounds
from parents import get_parents
from transform import apply_transforms, discard_transforms


basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "target.txt"))


def main(window, document, settings):
    selected = window.current_shape

    if not isinstance(selected, Group):
        window.warning("Please select a layer or group")

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

    target_bounds = get_bounds(composition, target_uuid)
    selected_bounds = get_bounds(composition, selected.uuid)

    parents = get_parents(composition, selected.uuid)

    position = apply_transforms(parents, selected.transform.position.value or Point(0, 0))
    position.x += target_bounds.left - selected_bounds.left
    position.y += target_bounds.top - selected_bounds.top

    if settings["target_horizontal"] == "Center":
        position.x += target_bounds.width / 2
    elif settings["target_horizontal"] == "Right":
        position.x += target_bounds.width

    if settings["target_vertical"] == "Center":
        position.y += target_bounds.height / 2
    elif settings["target_vertical"] == "Bottom":
        position.y += target_bounds.height

    if settings["selected_horizontal"] == "Center":
        position.x -= selected_bounds.width / 2
    elif settings["selected_horizontal"] == "Right":
        position.x -= selected_bounds.width

    if settings["selected_vertical"] == "Center":
        position.y -= selected_bounds.height / 2
    elif settings["selected_vertical"] == "Bottom":
        position.y -= selected_bounds.height

    with document.macro("Align with target"):
        selected.transform.position.value = discard_transforms(parents, position)
