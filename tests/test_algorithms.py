import pytest
from sudoku_solver_py.algorithms import find_single, reduce_candidates_by_group_constraints, naked_pairs, remove_from_candidates

from sudoku_solver_py.models import Box, Cell, Column, Grid, Row, GroupModel


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


def test_remove_from_candidates(cell_factory):
    # arrange
    cell: Cell = cell_factory(value=0)
    assert set(cell.candidates) == set(range(1,10))
    # act
    remove_from_candidates(cell, [2,3,9])
    # assert
    assert cell.candidates == [1,4,5,6,7,8]
    


@pytest.mark.parametrize("group_type", [Row, Column, Box])
def test_naked_pair(group_type: type, cell_factory):
    # arrange
    group_obj: GroupModel = group_type(index=0)
    for _ in range(9):
        group_obj.cells.append(cell_factory(value=0))

    # naked pair - a pair of candidates in two cells of the group
    group_obj[2].candidates = [2,3]
    group_obj[5].candidates = [3,2]

    # act
    was_successful = naked_pairs(group_obj)
    # assert
    assert was_successful
    
    for i in [0,1,3,4,6,7,8]:
        assert 2 not in group_obj[i].candidates
        assert 3 not in group_obj[i].candidates

    for np in [2,5]:
        assert 2 in group_obj[np].candidates
        assert 3 in group_obj[np].candidates
