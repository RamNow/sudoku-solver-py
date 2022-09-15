from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
from pydantic import BaseModel, Field


class Model(BaseModel, ABC):
    @abstractmethod
    def is_valid() -> bool:
        """Checks whether or not all Sudoku rules are followed."""


class Cell(Model):
    value: int

    def is_valid() -> bool:
        pass

    def __eq__(self, obj):
        return isinstance(obj, Cell) and obj.value == self.value or isinstance(obj, int) and obj == self.value
            


class GroupModel(Model):
    index: int
    cells: list[Cell] = Field(default_factory=list)

    def is_valid() -> bool:
        pass

    def __str__(self) -> str:
        cell_values = [str(c.value) for c in self.cells]
        return ''.join(cell_values)


class Row(GroupModel):
   pass


class Column(GroupModel):
    pass


class Box(GroupModel):
    pass 
    
    # Box index within a Grid, and cell index within a box are counting from left to right and from top to bottom: 
    # 0 1 2
    # 3 4 5
    # 6 7 8
   


class Grid(Model):
    """Representation of a Sudoku board."""
    
    cells: list[Cell] = Field(default_factory=list)
    rows: list[Row] = Field(default_factory=list)
    columns: list[Column] = Field(default_factory=list)
    boxes: list[Box] = Field(default_factory=list)

    def __init__(self, numbers: str) -> None:
        super().__init__()

        self.init_groups()

        # removed unwanted chars
        numbers = numbers.replace(',','').replace(' ', '')
    
        for row_index in range(9):

            row_values = numbers[row_index*9:(row_index*9)+9]
            
            for col_index in range(9):
                
                val = row_values[col_index]
                cell = Cell(value=int(val))
                self.cells.append(cell)
                self.rows[row_index].cells.append(cell)
                self.columns[col_index].cells.append(cell)

                # figure out to which box the cell belongs
                box_index = self.find_box_index(row_index, col_index)
                self.boxes[box_index].cells.append(cell)

    @staticmethod
    def find_box_index(row: int, col: int) -> int:
        return row // 3 * 3 + col // 3


    def init_groups(self):
        for i in range(9):
            self.rows.append(Row(index=i))
            self.columns.append(Column(index=i))
            self.boxes.append(Box(index=i))

    def is_valid() -> bool:
        pass
            
