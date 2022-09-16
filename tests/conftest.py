from unittest import mock
from pytest import fixture
from sudoku_solver_py.models import Cell, Row, Column, Box

@fixture
def cell_factory():
    def _cell_factory(value: int) -> Cell:
        return Cell(value=value, row=Row(index=0), column=Column(index=0), box=Box(index=0))

    return _cell_factory