from glaxnimate.model.shapes import Group, PreCompLayer


def get_parents(composition, uuid):
    parents = []

    visit_children(composition, uuid, parents)

    return parents


def visit_children(node, uuid, parents):
    for child in node.shapes:
        if visit_node(child, uuid, parents):
            parents.append(node)

            return True

    return False


def visit_node(node, uuid, parents):
    if node.uuid == uuid:
        return True

    if isinstance(node, Group):
        return visit_children(node, uuid, parents)

    if isinstance(node, PreCompLayer):
        return visit_children(node.composition, uuid, parents)

    return False
