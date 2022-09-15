import pytest
from sudoku_solver_py.algorithms import find_single

from sudoku_solver_py.models import Box, Cell, Column, Row


@pytest.mark.parametrize("init_values,expected_values,success", 
    [
        ([0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0], False),
        ([1,0,3,4,5,6,7,0,9],[1,0,3,4,5,6,7,0,9], False),
        ([1,2,3,4,5,6,7,0,9],[1,2,3,4,5,6,7,8,9], True),
    ])
@pytest.mark.parametrize("group_type", [Row, Column, Box])
def test_find_single(group_type: type, init_values: list[int], expected_values: list[int], success: bool):
    
     # arrange
    group_obj = group_type(index=0)
    for init_val in init_values:
        group_obj.cells.append(Cell(value=init_val))
    # act
    was_successful = find_single(group_obj)
    # assert
    assert was_successful == success
    assert expected_values == group_obj.values
