
from sudoku_solver_py.models import Grid, GroupModel, Cell


def find_single(group: GroupModel) -> bool:
    """
    Checks for a single candidate in the group.
    If found, it is set.
    Returns true / false depending wheter or not a single was found.
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
    

def remove_from_candidates(cell: Cell, values: list|set):
    cell.candidates = [c for c in cell.candidates if c not in values]


def naked_pairs(group: GroupModel) -> bool:
    """
    Checks for naked pairs in a group.
    Removes both candidate from all other cells in the group.
    Returns true / false depending wheter or not a naked pair was found.
    """

    naked_pair_found = False

    for i in range(9):
        cell1 = group[i]
        
        if len(cell1.candidates) == 2:
            pair1 = set(cell1.candidates)
            # find other cell in group with same pair values
            for f in range(i+1, 9):
                cell2 = group[f]
                if len(cell2.candidates) == 2:
                    pair2 = set(cell2.candidates)
                    if pair1 == pair2:
                        naked_pair_found = True
                        # remove pair from all other cells in group
                        for cleanup_index in (c for c in range(9) if c not in [i, f]):
                            cleanup_cell = group[cleanup_index]
                            remove_from_candidates(cleanup_cell, pair1)

                        break
    
    return naked_pair_found
