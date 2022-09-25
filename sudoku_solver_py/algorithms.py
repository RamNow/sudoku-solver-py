from typing import Callable

from sudoku_solver_py.models import Grid, GroupModel, Cell


def find_single(group: GroupModel) -> bool:
    """
    Checks for a single candidate in the group.
    If found, it is set.
    Returns true / false depending on whether a single was found.
    """
    if len(group.candidates) != 1:
        return False

    for cell in group.cells:
        if cell.is_vacant:
            cell.value = group.candidates[0]
            return True


def reduce_candidates_by_group_constraints(grid: Grid) -> bool:
    """
    Walks over cell and removes candidates that are violating the constraints by given values in
    - boxes
    - rows
    - columns
    Returns true if any candidate in any cell could be removed.
    """

    some_candidates_reduced = False

    for cell in grid.cells:
        before = cell.candidates.copy()
        cell.candidates = [c for c in cell.candidates
                           if not c in cell.row.values
                           if not c in cell.column.values
                           if not c in cell.box.values
                           ]
        if before != cell.candidates:
            some_candidates_reduced = True

    return some_candidates_reduced


def remove_from_candidates(cell: Cell, values: list | set):
    cell.candidates = [c for c in cell.candidates if c not in values]


def naked_pairs(group: GroupModel, skip_cells_with_index=None) -> list:
    """
    Checks for naked pairs in a group.
    Removes both candidate from all other cells in the group.
    Returns the array of cell indexes for the naked pairs.
    """

    if skip_cells_with_index is None:
        skip_cells_with_index = []
    else:
        # we don't want to change to original list.
        skip_cells_with_index = skip_cells_with_index.copy()

    naked_pair_cell_indexes = []

    for i in range(9):
        cell1 = group[i]
        if cell1.index in skip_cells_with_index:
            continue

        if len(cell1.candidates) == 2:
            pair1 = set(cell1.candidates)
            # find other cell in group with same pair values
            for f in range(i + 1, 9):
                cell2 = group[f]
                if len(cell2.candidates) == 2:
                    pair2 = set(cell2.candidates)
                    if pair1 == pair2:
                        naked_pair_cell_indexes.append(cell1.index)
                        naked_pair_cell_indexes.append(cell2.index)

                        # remove pair from all other cells in group
                        for cleanup_index in (c for c in range(9) if c not in [i, f]):
                            cleanup_cell = group[cleanup_index]
                            remove_from_candidates(cleanup_cell, pair1)

                        break

    return naked_pair_cell_indexes


def naked_triplets(group: GroupModel, skip_cells_with_index=None) -> list:
    """
    Checks for naked triplets in a group.
    Removes all three candidates from all other cells in the group.
    Returns the array of cell indexes for the naked triplets.
    see https://www.learn-sudoku.com/naked-triplets.html
    """

    if skip_cells_with_index is None:
        skip_cells_with_index = []
    else:
        # we don't want to change to original list.
        skip_cells_with_index = skip_cells_with_index.copy()

    naked_triplet_cell_indexes = []

    # iterate over all 3-pack-combinations of cells in this group
    for c1, c2, c3 in ((c1, c2, c3) for c1 in range(9) for c2 in range(c1 + 1, 9) for c3 in range(c2 + 1, 9)):
        cell1 = group[c1]
        cell2 = group[c2]
        cell3 = group[c3]

        if cell1.index in skip_cells_with_index \
                or cell2.index in skip_cells_with_index \
                or cell3.index in skip_cells_with_index:
            continue

        if not (2 <= len(cell1.candidates) <= 3
                and 2 <= len(cell2.candidates) <= 3
                and 2 <= len(cell3.candidates) <= 3):
            # no potential triplet
            continue

        candidates1 = set(cell1.candidates)
        candidates2 = set(cell2.candidates)
        candidates3 = set(cell3.candidates)

        # one of the values of a cells candidate must be found in each of the other cell candidates
        if exists_triplet_match(candidates1, candidates2, candidates3):
            naked_triplet_cell_indexes.append(cell1.index)
            naked_triplet_cell_indexes.append(cell2.index)
            naked_triplet_cell_indexes.append(cell3.index)

            # remove triplets from all other cells in group
            cleanup_values = set(cell1.candidates + cell2.candidates + cell3.candidates)
            for cleanup_index in (c for c in range(9) if c not in [c1, c2, c3]):
                cleanup_cell = group[cleanup_index]
                remove_from_candidates(cleanup_cell, cleanup_values)

    return naked_triplet_cell_indexes


def exists_triplet_match(a: list[int] | set[int], b: list[int] | set[int], c: list[int] | set[int]) -> bool:
    """Checks whether there is a `triplet` in terms of 'Sudoku-Naked-Triplets' in the 3 given lists of values."""

    triplet = set(list(a) + list(b) + list(c))
    return len(triplet) == 3


def naked_quads(group: GroupModel, skip_cells_with_index=None) -> list:
    """
    Checks for naked quads in a group.
    Removes all four candidates from all other cells in the group.
    Returns the array of cell indexes for the naked quads.
    see https://www.sudokuwiki.org/Naked_Candidates
    """

    if skip_cells_with_index is None:
        skip_cells_with_index = []
    else:
        # we don't want to change to original list.
        skip_cells_with_index = skip_cells_with_index.copy()

    naked_quads_cell_indexes = []

    # iterate over all 3-pack-combinations of cells in this group
    for c1, c2, c3, c4 in (
            (c1, c2, c3, c4) for c1 in range(9)
            for c2 in range(c1 + 1, 9)
            for c3 in range(c2 + 1, 9)
            for c4 in range(c3 + 1, 9)):
        cell1 = group[c1]
        cell2 = group[c2]
        cell3 = group[c3]
        cell4 = group[c4]

        if cell1.index in skip_cells_with_index \
                or cell2.index in skip_cells_with_index \
                or cell3.index in skip_cells_with_index \
                or cell4.index in skip_cells_with_index:
            continue

        if not (2 <= len(cell1.candidates) <= 4
                and 2 <= len(cell2.candidates) <= 4
                and 2 <= len(cell3.candidates) <= 4
                and 2 <= len(cell4.candidates) <= 4):
            # no potential triplet
            continue

        candidates1 = set(cell1.candidates)
        candidates2 = set(cell2.candidates)
        candidates3 = set(cell3.candidates)
        candidates4 = set(cell4.candidates)

        # one of the values of a cells candidate must be found in each of the other cell candidates
        if exists_quad_match(candidates1, candidates2, candidates3, candidates4):
            naked_quads_cell_indexes.append(cell1.index)
            naked_quads_cell_indexes.append(cell2.index)
            naked_quads_cell_indexes.append(cell3.index)
            naked_quads_cell_indexes.append(cell4.index)

            # remove triplets from all other cells in group
            cleanup_values = set(cell1.candidates + cell2.candidates + cell3.candidates +  cell4.candidates)
            for cleanup_index in (c for c in range(9) if c not in [c1, c2, c3, c4]):
                cleanup_cell = group[cleanup_index]
                remove_from_candidates(cleanup_cell, cleanup_values)

    return naked_quads_cell_indexes


def exists_quad_match(a: list[int] | set[int],
                      b: list[int] | set[int],
                      c: list[int] | set[int],
                      d: list[int] | set[int]) -> bool:
    """Checks whether there is a `quad` in terms of 'Sudoku-Naked-Quads' in the 4 given lists of values."""

    triplet = set(list(a) + list(b) + list(c) + list(d))
    return len(triplet) == 4


def naked_candidates(grid: Grid, algorithm: Callable, skip_cells_with_index: list = None) -> list:
    if skip_cells_with_index is None:
        skip_cells_with_index = []
    else:
        # we don't want to change the original list
        skip_cells_with_index = skip_cells_with_index.copy()

    naked_candidates_cell_indexes = []

    for row in grid.rows:
        new_naked_candidates = algorithm(row, skip_cells_with_index)
        naked_candidates_cell_indexes += new_naked_candidates
        skip_cells_with_index += new_naked_candidates

    for col in grid.columns:
        new_naked_candidates = algorithm(col, skip_cells_with_index)
        naked_candidates_cell_indexes += new_naked_candidates
        skip_cells_with_index += new_naked_candidates

    for box in grid.boxes:
        new_naked_candidates = algorithm(box, skip_cells_with_index)
        naked_candidates_cell_indexes += new_naked_candidates

    return naked_candidates_cell_indexes
