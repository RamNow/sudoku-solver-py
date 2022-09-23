import pytest
from sudoku_solver_py.algorithms import find_single, reduce_candidates_by_group_constraints, naked_pairs, \
    remove_from_candidates, naked_triplet, exists_triplet_match

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

    group_obj[3].candidates = [8,9]
    group_obj[8].candidates = [8,9]

    # act
    naked_pair_indexes = naked_pairs(group_obj)
    # assert
    assert naked_pair_indexes
    
    for i in [0,1,3,4,6,7,8]:
        assert 2 not in group_obj[i].candidates
        assert 3 not in group_obj[i].candidates

    for j in [0,1,2,4,5,6,7]:
        assert 8 not in group_obj[j].candidates
        assert 9 not in group_obj[j].candidates

    for np in [2,5]:
        assert 2 in group_obj[np].candidates
        assert 3 in group_obj[np].candidates
    
    for np2 in [3,8]:
        assert 8 in group_obj[np2].candidates
        assert 9 in group_obj[np2].candidates

    expected_naked_pair_indexes = [
        group_obj[2].index,
        group_obj[3].index,
        group_obj[5].index,
        group_obj[8].index,
    ]
    assert set(expected_naked_pair_indexes) == set(naked_pair_indexes)



@pytest.mark.parametrize("group_type", [Row, Column, Box])
def test_naked_pair_skip_cells(group_type: type, cell_factory):
    # arrange
    group_obj: GroupModel = group_type(index=0)
    for ci in range(9):
        group_obj.cells.append(cell_factory(value=0, index=ci))

    # naked pair - a pair of candidates in two cells of the group
    group_obj[2].candidates = [2, 3]
    group_obj[5].candidates = [3, 2]

    # act
    naked_pair_indexes = naked_pairs(group_obj, [2, 5])
    # assert
    assert not naked_pair_indexes, 'Naked pair should have been skipped'


@pytest.mark.parametrize("init_values,init_candidates,expected_candidates,expected_naked_pair_indexes", [
    # examples see https://www.learn-sudoku.com/naked-triplets.html
    (  # true triplets
            [0, 0, 7, 2, 3, 4, 0, 0, 0],
            [(1, 5, 9), (1, 5, 9), (), (), (), (), (1, 5, 9), (1, 6, 8, 9), (5, 6, 8, 9)],
            [(1, 5, 9), (1, 5, 9), (), (), (), (), (1, 5, 9), (6, 8), (6, 8)],
            [0, 1, 6],
    ),
    (  # virtual triplets
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [(5, 6), (), (1, 4, 8, 9), (4, 7), (8, 6), (1, 6, 7), (3, 4, 7, 9), (3, 4, 5, 7, 9), (5, 8)],
            [(5, 6), (), (1, 4, 9), (4, 7), (8, 6), (1, 7), (3, 4, 7, 9), (3, 4, 7, 9), (5, 8)],
            [0, 4, 8],
    ),

])
@pytest.mark.parametrize("group_type", [Row, Column, Box])
def test_naked_triplet(group_type: type, init_values, init_candidates, expected_candidates, expected_naked_pair_indexes,
                       cell_factory):
    # arrange
    group_obj: GroupModel = group_type(index=0)

    for init_value in init_values:
        group_obj.cells.append(cell_factory(value=init_value))

    for i in range(9):
        group_obj[i].candidates = list(init_candidates[i])

    # act
    naked_triplet_indexes = naked_triplet(group_obj)
    # assert
    assert naked_triplet_indexes

    for r in range(9):
        assert set(group_obj[r].candidates) == set(expected_candidates[r])

    assert set(naked_triplet_indexes) == set(expected_naked_pair_indexes)


@pytest.mark.parametrize('a,b,c,match_found', [
    ([1, 5], [5, 9], [1, 9], True),
    ([1, 5], [5, 8], [1, 9], False),
    ([1, 5, 9], [1, 5, 9], [1, 5, 9], True),
    ([1, 5, 9], [1, 5, 9], [1, 5, 8], False),
    ([1, 5, 9], [1, 5], [1, 9], True),
    ([1, 5, 9], [1, 5], [5, 9], True),
    ([5, 9], [1, 5, 9], [1, 9], True),
    ([5, 9], [1, 5, 9], [1, 8], False),
])
def test_exists_triplet_match(a: list[int], b: list[int], c: list[int], match_found: bool):
    assert exists_triplet_match(a, b, c) == match_found
