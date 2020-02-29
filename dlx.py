from itertools import repeat

import numpy as np


class Node:
    __slots__ = "L", "R", "U", "D", "C", "N"

    def __init__(self, name=None):
        self.N = name


class ListHeader(Node):
    __slots__ = "S"

    def __init__(self, name=None):
        self.N = name
        self.S = 0


def build_row(length, name):
    # Build one row of nodes
    root = last_node = Node(name)
    for _ in range(length - 1):
        next_node = Node(name)
        last_node.R, next_node.L = next_node, last_node
        last_node = next_node
    last_node.R, root.L = root, last_node
    return root


def build_link_matrix(array, column_names=None, row_names=None):
    # Build list headers
    root = ListHeader()
    last_node = root
    for name in column_names or repeat(None, array.shape[1]):
        next_node = ListHeader(name)
        next_node.U = next_node.D = next_node
        last_node.R, next_node.L = next_node, last_node
        last_node = next_node
    next_node.R, root.L = root, next_node

    # Build rows
    for i, name in enumerate(row_names or repeat(None, array.shape[0])):
        row = build_row(np.sum(array[i]), name)
        # Hang new row from headers
        header = root
        node = row
        for j in range(array.shape[1]):
            header = header.R
            if array[i, j]:
                header.U.D, node.U = node, header.U
                header.U, node.D = node, header
                node.C = header
                header.S += 1
                node = node.R
    return root


def linked_list_iter(start, direction, include_start=False):
    if include_start:
        yield start
    node = getattr(start, direction)
    while node != start:
        yield node
        node = getattr(node, direction)


def cover(column):
    column.R.L, column.L.R = column.L, column.R
    for i in linked_list_iter(column, "D"):
        for j in linked_list_iter(i, "R"):
            j.D.U, j.U.D = j.U, j.D
            j.C.S -= 1


def uncover(column):
    for i in linked_list_iter(column, "U"):
        for j in linked_list_iter(i, "R"):
            j.D.U, j.U.D = j, j
            j.C.S += 1
    column.R.L, column.L.R = column, column


def search(root, solution):
    if root.R == root:
        yield solution
    else:
        c = root.R
        cover(c)
        for r in linked_list_iter(c, "D"):
            solution.append(r)
            for j in linked_list_iter(r, "R"):
                cover(j.C)
            yield from search(root, solution)
            for j in linked_list_iter(r, "L"):
                uncover(j.C)
            solution.pop()
        uncover(c)


def solve(array, column_names):
    if len(column_names) != array.shape[1]:
        raise ValueError(
            f"Array has {array.shape[1]} columns, but {len(column_names)} "
            "column names were provided."
        )
    root = build_link_matrix(array, column_names)
    yield from search(root, [])


def solution_names(solution):
    return [
        tuple(node.C.N for node in linked_list_iter(row, "R", include_start=True))
        for row in solution
    ]


def main():
    array = np.array([
        [0, 0, 1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 1],
    ])
    column_names = "ABCDEFG"
    for solution in solve(array, column_names):
        print(solution_names(solution))


if __name__ == "__main__":
    main()
