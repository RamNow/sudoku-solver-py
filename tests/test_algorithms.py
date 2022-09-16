import pytest
from sudoku_solver_py.algorithms import find_single, reduce_candidates_by_group_constraints

from sudoku_solver_py.models import Box, Cell, Column, Grid, Row


@pytest.mark.parametrize("init_values,expected_values,success", 
    [
        ([0,0,0,0,0,0,0,0,0],[], False),
        ([1,0,3,4,5,6,7,0,9],[1,3,4,5,6,7,9], False),
        ([1,2,3,4,5,6,7,0,9],[1,2,3,4,5,6,7,8,9], True),
    ])
@pytest.mark.parametrize("group_type", [Row, Column, Box])
def test_find_single(group_type: type, init_values: list[int], expected_values: list[int], success: bool, cell_factory):
    
     # arrange
    group_obj = group_type(index=0)
    for init_val in init_values:
        group_obj.cells.append(cell_factory(value=init_val))
    # act
    was_successful = find_single(group_obj)
    # assert
    assert was_successful == success
    assert expected_values == group_obj.values


def test_reduce_candidates_by_group_constraint_empty_grid():
    # arrange
    numbers = '0' * 81 
    empty_grid = Grid(numbers)
    # act 
    was_successful = reduce_candidates_by_group_constraints(empty_grid)
    # assert
    assert not was_successful
    for cell in empty_grid.cells:
        assert cell.candidates == list(range(1,10)), 'Each vacant cell should have all possible candidates in it'


def test_reduce_candidates_by_group_constraint():
    # arrange
    numbers = '000 801 000' \
              '000 000 043' \
              '500 000 000' \
              '000 070 800' \
              '000 000 100' \
              '020 030 000' \
              '600 000 075' \
              '003 400 000' \
              '000 200 600'

    grid = Grid(numbers)
    # act  
    was_successful = reduce_candidates_by_group_constraints(grid)
    # assert
    assert was_successful

    assert grid.rows[0][0].candidates == [2,3,4,7,9]
    assert grid.rows[0][1].candidates == [3,4,6,7,9]
    assert grid.rows[0][2].candidates == [2,4,6,7,9]
    assert grid.rows[5][6].candidates == [4,5,7,9]
    assert grid.rows[5][7].candidates == [5,6,9]
    assert grid.rows[5][8].candidates == [4,6,7,9]
