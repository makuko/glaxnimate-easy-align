from os import path
from glaxnimate.model.shapes import Group, Shape


basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "target.txt"))


def main(window, document, settings):
    shape = window.current_shape

    if (not isinstance(shape, Group) and not isinstance(shape, Shape)):
        window.warning("Please select a layer, group or shape")

        return

    f = open(filepath, "w")

    f.write(shape.uuid.hex)
    f.close()
