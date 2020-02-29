from itertools import product

import numpy as np

import dlx


def possibility_index(row, col, val):
    return 81 * row + 9 * col + val


def build_link_matrix(sudoku):
    array = np.zeros((729, 324), dtype=int)
    # Cell constraints
    for row, col in product(range(9), repeat=2):
        constraint_idx = 9 * row + col
        for val in range(9):
            array[possibility_index(row, col, val), constraint_idx] = 1
    # Row constraints
    for row, val in product(range(9), repeat=2):
        constraint_idx = 81 + 9 * row + val
        for col in range(9):
            array[possibility_index(row, col, val), constraint_idx] = 1
    # Column constraints
    for col, val in product(range(9), repeat=2):
        constraint_idx = 162 + 9 * col + val
        for row in range(9):
            array[possibility_index(row, col, val), constraint_idx] = 1
    # Box constraints
    for box_row, box_col in product(range(3), repeat=2):
        for val in range(9):
            constraint_idx = 243 + 9 * (3 * box_row + box_col) + val
            for row in range(3 * box_row, 3 * (box_row + 1)):
                for col in range(3 * box_col, 3 * (box_col + 1)):
                    array[possibility_index(row, col, val), constraint_idx] = 1

    # Get column, row names
    column_names = (
        [f"R{r}C{c}" for r, c, in product(range(1, 10), repeat=2)]
        + [f"R{r}#{v}" for r, v, in product(range(1, 10), repeat=2)]
        + [f"C{c}#{v}" for c, v in product(range(1, 10), repeat=2)]
        + [f"B{b}#{v}" for b, v in product(range(1, 10), repeat=2)]
    )
    row_names = [f"R{r}C{c}#{v}" for r, c, v in product(range(1, 10), repeat=3)]

    link_matrix = dlx.build_link_matrix(
        array, column_names=column_names, row_names=row_names
    )

    # Apply given values from sudoku
    satisfied_constraints = set()
    for row, col in product(range(9), repeat=2):
        if sudoku[row, col] != 0:
            val = sudoku[row, col]
            box = 3 * (row // 3) + (col // 3)
            satisfied_constraints |= {
                f"R{row+1}C{col+1}", f"R{row+1}#{val}", f"C{col+1}#{val}", f"B{box+1}#{val}"
            }
    for header in dlx.linked_list_iter(link_matrix, "R"):
        if header.N in satisfied_constraints:
            dlx.cover(header)

    return link_matrix


def solution_as_array(solution):
    array = np.zeros((9, 9), dtype=int)
    for r in solution:
        row, col, val = int(r.N[1]) - 1, int(r.N[3]) - 1, int(r.N[5])
        array[row, col] = val
    return array


def solve(sudoku):
    link_matrix = build_link_matrix(sudoku)
    yield from (sudoku + solution_as_array(sol) for sol in dlx.search(link_matrix, []))


def main():
    sudoku = np.array([
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 2, 0, 0, 3],
        [0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 0, 0],
        [4, 0, 1, 6, 0, 0, 0, 0, 0],
        [0, 0, 7, 1, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 4, 0],
        [0, 3, 0, 9, 1, 0, 0, 0, 0],
    ])
    for solution in solve(sudoku):
        print(solution)


if __name__ == "__main__":
    main()
