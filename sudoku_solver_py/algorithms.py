
from sudoku_solver_py.models import GroupModel


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
    