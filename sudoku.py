import numpy as np

import dlx


def possibility_index(row, col, val):
    return 81 * row + 9 * col + val


def build_link_matrix(sudoku):
    array = np.zeros((729, 324), dtype=int)
    # Cell constraints
    for row in range(9):
        for col in range(9):
            constraint_idx = 9 * row + col
            for val in range(9):
                array[possibility_index(row, col, val), constraint_idx] = 1
    # Row constraints
    for row in range(9):
        for val in range(9):
            constraint_idx = 81 + 9 * row + val
            for col in range(9):
                array[possibility_index(row, col, val), constraint_idx] = 1
    # Column constraints
    for col in range(9):
        for val in range(9):
            constraint_idx = 162 + 9 * col + val
            for row in range(9):
                array[possibility_index(row, col, val), constraint_idx] = 1
    # Box constraints
    for box_row in range(3):
        for box_col in range(3):
            for val in range(9):
                constraint_idx = 243 + 9 * (3 * box_row + box_col) + val
                for row in range(3 * box_row, 3 * (box_row + 1)):
                    for col in range(3 * box_col, 3 * (box_col + 1)):
                        array[possibility_index(row, col, val), constraint_idx] = 1

    # Get column names
    column_names = np.array(
        [f"R{i+1}C{j+1}" for i in range(9) for j in range(9)]
        + [f"R{i+1}#{j+1}" for i in range(9) for j in range(9)]
        + [f"C{i+1}#{j+1}" for i in range(9) for j in range(9)]
        + [f"B{i+1}#{j+1}" for i in range(9) for j in range(9)]
    )

    return dlx.build_link_matrix(array, column_names)


def solution_as_array(solution):
    array = np.zeros((9, 9), dtype=int)
    for r in solution:
        row, col = int(r.C.N[1]) - 1, int(r.C.N[3]) - 1
        val = r.R.C.N[3]
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