
from sudoku_solver_py.models import Grid, GroupModel


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
    