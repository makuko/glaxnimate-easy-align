from os import path
from glaxnimate.model.shapes import Group, Shape, Image, PreCompLayer


basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "target.txt"))


def main(window, document, settings):
    node = window.current_shape

    if (
        not isinstance(node, Group)
        and not isinstance(node, Shape)
        and not isinstance(node, Image)
        and not isinstance(node, PreCompLayer)
    ):
        window.warning("Please select a layer, group, shape, image or precomposition")

        return

    f = open(filepath, "w")

    f.write(node.uuid.hex)
    f.close()
