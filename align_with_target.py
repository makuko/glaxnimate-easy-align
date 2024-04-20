from uuid import UUID
from os import path
from glaxnimate import log
from glaxnimate.model.shapes import Group, Shape, Path
from glaxnimate.utils import Point
from glaxnimate.utils.bezier import Bezier, Point as BezierPoint, PointType
from bounding_box import get_bounding_box

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "target.txt"))


def main(window, document, settings):
    selected = window.current_shape

    if isinstance(selected, Path):
        window.warning("Aligning a path currently requires a parent group and aligning that instead")

        return

    if (not isinstance(selected, Group) and not isinstance(selected, Shape)):
        window.warning("Please select a layer, group or shape")

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

    target_bounding_box = get_bounding_box(composition, target_uuid)
    selected_bounding_box = get_bounding_box(composition, selected.uuid)

    x = target_bounding_box["left"] - selected_bounding_box["left"]
    y = target_bounding_box["top"] - selected_bounding_box["top"]

    if settings["target_horizontal"] == "Center":
        x += target_bounding_box["width"] / 2
    elif settings["target_horizontal"] == "Right":
        x += target_bounding_box["width"]

    if settings["target_vertical"] == "Center":
        y += target_bounding_box["height"] / 2
    elif settings["target_vertical"] == "Bottom":
        y += target_bounding_box["height"]

    if settings["selected_horizontal"] == "Center":
        x -= selected_bounding_box["width"] / 2
    elif settings["selected_horizontal"] == "Right":
        x -= selected_bounding_box["width"]

    if settings["selected_vertical"] == "Center":
        y -= selected_bounding_box["height"] / 2
    elif settings["selected_vertical"] == "Bottom":
        y -= selected_bounding_box["height"]

    with document.macro("Align with target"):
        if isinstance(selected, Group):
            move_position(selected.transform.position, x, y)
        elif isinstance(selected, Path):
            move_points(selected, x, y)
        else:
            move_position(selected.position, x, y)


def move_position(position, x, y):
    position.value = Point(position.value.x + x, position.value.y + y) if position.value else Point(x, y)


def move_points(path, x, y):
    bezier = Bezier()
    i = 0

    if path.shape.value.closed == True:
        bezier.close()

    for point in path.shape.value:
        bezier.insert_point(i, BezierPoint(
            Point(point.pos.x + x, point.pos.y + y),
            Point(point.tan_in.x + x, point.tan_in.y + y),
            Point(point.tan_out.x + x, point.tan_out.y + y),
            point.type
        ))

        i += 1

    path.shape.value = bezier
