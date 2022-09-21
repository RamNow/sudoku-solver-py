import pytest
from pytest import fixture
from sudoku_solver_py.models import Cell, Row, Column, Box


@fixture
def cell_index_counter():
    pytest.cell_index_counter = -1


@fixture
def cell_factory(cell_index_counter):
    def _cell_factory(value: int, index: int = None) -> Cell:
        pytest.cell_index_counter += 1
        return Cell(value=value, index=index or pytest.cell_index_counter, row=Row(index=0), column=Column(index=0), box=Box(index=0))

    return _cell_factory
