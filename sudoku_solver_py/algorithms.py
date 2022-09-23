
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
            for f in range(i+1, 9):
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


def naked_pairs_grid(grid: Grid, skip_cells_with_index: list = None) -> list:

    if skip_cells_with_index is None:
        skip_cells_with_index = []
    else:
        # we don't want to change the original list
        skip_cells_with_index = skip_cells_with_index.copy()

    naked_pair_cell_indexes = []
     
    for row in grid.rows:
        new_naked_pairs = naked_pairs(row, skip_cells_with_index)
        naked_pair_cell_indexes += new_naked_pairs
        skip_cells_with_index += new_naked_pairs

    for col in grid.columns:
        new_naked_pairs = naked_pairs(col, skip_cells_with_index)
        naked_pair_cell_indexes += new_naked_pairs
        skip_cells_with_index += new_naked_pairs

    for box in grid.boxes:
        new_naked_pairs = naked_pairs(box, skip_cells_with_index)
        naked_pair_cell_indexes += new_naked_pairs

    return naked_pair_cell_indexes


def naked_triplet(group: GroupModel, skip_cells_with_index=None) -> list:
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

        if not(2 <= len(cell1.candidates) <= 3
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


def naked_triplets_grid(grid: Grid, skip_cells_with_index: list = None) -> list:
    if skip_cells_with_index is None:
        skip_cells_with_index = []
    else:
        # we don't want to change the original list
        skip_cells_with_index = skip_cells_with_index.copy()

    naked_triplets_cell_indexes = []

    for row in grid.rows:
        new_naked_triplets = naked_pairs(row, skip_cells_with_index)
        naked_triplets_cell_indexes += new_naked_triplets
        skip_cells_with_index += new_naked_triplets

    for col in grid.columns:
        new_naked_triplets = naked_pairs(col, skip_cells_with_index)
        naked_triplets_cell_indexes += new_naked_triplets
        skip_cells_with_index += new_naked_triplets

    for box in grid.boxes:
        new_naked_triplets = naked_pairs(box, skip_cells_with_index)
        naked_triplets_cell_indexes += new_naked_triplets

    return naked_triplets_cell_indexes
