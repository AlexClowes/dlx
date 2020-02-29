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

    # Get row names
    row_names = [f"R{r}C{c}#{v}" for r, c, v in product(range(1, 10), repeat=3)]

    return dlx.build_link_matrix(array, row_names=row_names)


def solution_as_array(solution):
    array = np.zeros((9, 9), dtype=int)
    for r in solution:
        row, col, val = int(r.N[1]) - 1, int(r.N[3]) - 1, int(r.N[5])
        array[row, col] = val
    return array


def solve(sudoku):
    link_matrix = build_link_matrix(sudoku)
    yield from map(solution_as_array, dlx.search(link_matrix, []))


def main():
    sudoku = np.zeros((9, 9), dtype=int)
    for solution in solve(sudoku):
        print(solution)
        break


if __name__ == "__main__":
    main()
