import pytest
from tokenize import group
from sudoku_solver_py.models import Box, Cell, Column, Grid, Row

def test_find_box_index():
    
    assert Grid.find_box_index(0, 0) == 0
    assert Grid.find_box_index(1, 2) == 0
    assert Grid.find_box_index(2, 1) == 0
    assert Grid.find_box_index(0, 3) == 1
    assert Grid.find_box_index(0, 6) == 2
    assert Grid.find_box_index(3, 0) == 3
    assert Grid.find_box_index(4, 0) == 3
    assert Grid.find_box_index(4, 2) == 3
    assert Grid.find_box_index(3, 3) == 4
    assert Grid.find_box_index(3, 6) == 5
    assert Grid.find_box_index(6, 0) == 6
    assert Grid.find_box_index(6, 3) == 7
    assert Grid.find_box_index(6, 6) == 8
    assert Grid.find_box_index(7, 7) == 8
    assert Grid.find_box_index(8, 8) == 8


def test_init_grid():

    # arrange
    numbers = '2,3,7 8,4,1 5,6,9 186795243 594326718 315674892 469582137 728139456 642918375 853467921 971253684'
    # act
    grid = Grid(numbers)
    # assert
    assert len(grid.cells) == 9*9
    assert len(grid.rows) == 9
    assert len(grid.columns) == 9
    assert len(grid.boxes) == 9

    numbers = numbers.replace(' ', '').replace(',', '')
    
    for i in range(9*9):
        val = int(numbers[i])
        assert grid.cells[i] == val

    assert grid.rows[0].cells[0] == 2
    assert grid.rows[0].cells[1] == 3
    assert grid.rows[0].cells[2] == 7
    assert grid.rows[0].cells[3] == 8
    assert grid.rows[1].cells[3] == 7

    assert str(grid.rows[0]) == '237841569'
    assert str(grid.rows[1]) == '186795243'
    assert str(grid.rows[2]) == '594326718'
    assert str(grid.rows[3]) == '315674892'
    assert str(grid.rows[4]) == '469582137'
    assert str(grid.rows[5]) == '728139456'
    assert str(grid.rows[6]) == '642918375'
    assert str(grid.rows[7]) == '853467921'
    assert str(grid.rows[8]) == '971253684'
    
    assert str(grid.columns[0]) == '215347689'
    assert str(grid.columns[1]) == '389162457'
    assert str(grid.columns[2]) == '764598231'
    assert str(grid.columns[3]) == '873651942'
    assert str(grid.columns[4]) == '492783165'
    assert str(grid.columns[5]) == '156429873'
    assert str(grid.columns[6]) == '527814396'
    assert str(grid.columns[7]) == '641935728'
    assert str(grid.columns[8]) == '938276514'

    assert str(grid.boxes[0]) == '237186594'
    assert str(grid.boxes[1]) == '841795326'
    assert str(grid.boxes[2]) == '569243718'
    assert str(grid.boxes[3]) == '315469728'
    assert str(grid.boxes[4]) == '674582139'
    assert str(grid.boxes[5]) == '892137456'
    assert str(grid.boxes[6]) == '642853971'
    assert str(grid.boxes[7]) == '918467253'
    assert str(grid.boxes[8]) == '375921684'

def test_cell_equals(cell_factory):
    c1 = cell_factory(value=2)
    c2 = cell_factory(value=2)
    c3 = cell_factory(value=0)
    assert c1 == 2
    assert 2 == c1
    assert c2 == c1
    assert not c2 == c3
    assert not c3 == 2
    assert c2 != c3
    assert c3 != 2


@pytest.mark.parametrize("value,candidates,is_vacant", [
    (0, [1,2,3,4,5,6,7,8,9], True),
    (1, [], False),
])
def test_cell_initialization(value: int, candidates: list[int], is_vacant: bool, cell_factory):
    cell = cell_factory(value=value)
    assert cell.is_vacant == is_vacant
    assert cell.candidates == candidates


@pytest.mark.parametrize("group_type", [Row, Column, Box])
def test_get_value_by_cell_index(group_type: type, cell_factory):
     # arrange
    group_obj = group_type(index=0)
    for i in range(9):
        group_obj.cells.append(cell_factory(value=i*2))
    # act + assert
    for j in range(9):
        assert group_obj[j] == j*2, 'GroupModel should be subscriptable'


@pytest.mark.parametrize("init_values,values", 
    [
        ([0,0,0,0,0,0,0,0,0],[]),
        ([1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]),
        ([0,1,0,4,0,5,6,0,8],[1,4,5,6,8]),
    ])
@pytest.mark.parametrize("group_type", [Row, Column, Box])
def test_get_values(group_type: type, init_values: list[int], values: list[int], cell_factory):
     # arrange
    group_obj = group_type(index=0)
    for init_value in init_values:
        group_obj.cells.append(cell_factory(value=init_value))
    # act
    actual_values = group_obj.values
    # assert
    assert actual_values == values


@pytest.mark.parametrize("init_values,candidates", 
    [
        ([0,0,0,0,0,0,0,0,0],[1,2,3,4,5,6,7,8,9]),
        ([1,2,3,4,5,6,7,8,9],[]),
        ([0,1,0,4,0,5,6,0,8],[2,3,7,9]),
    ])
@pytest.mark.parametrize("group_type", [Row, Column, Box])
def test_find_group_candidates(group_type: type, init_values: list[int], candidates: list[int], cell_factory):
    # arrange
    group_obj = group_type(index=0)
    for init_val in init_values:
        group_obj.cells.append(cell_factory(value=init_val))
    # act
    actual_candidates = group_obj.candidates
    # assert
    assert actual_candidates == candidates
    