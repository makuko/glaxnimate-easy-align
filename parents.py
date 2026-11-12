from glaxnimate.model.shapes import Group, PreCompLayer


def get_uuid(node):
    return getattr(node, "uuid", None)


def find_node(composition, uuid):
    if uuid is None:
        return None

    return find_in_children(composition, uuid)


def find_in_children(node, uuid):
    for child in node.shapes:
        if get_uuid(child) == uuid:
            return child

        found = None

        if isinstance(child, Group):
            found = find_in_children(child, uuid)
        elif isinstance(child, PreCompLayer):
            found = find_in_children(child.composition, uuid)

        if found is not None:
            return found

    return None


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
    if get_uuid(node) == uuid:
        return True

    if isinstance(node, Group):
        return visit_children(node, uuid, parents)

    if isinstance(node, PreCompLayer):
        return visit_children(node.composition, uuid, parents)

    return False
