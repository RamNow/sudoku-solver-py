from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, validator


class Model(BaseModel, ABC):
    
    @abstractmethod
    def is_valid() -> bool:
        """Checks whether or not all Sudoku rules are followed."""


class Cell(Model):
    """Representation of a single field of a Sudoku puzzle."""
    
    index: int
    value: int
    row: "Row"
    column: "Column"
    box: "Box"

    candidates: list[int] = Field(default_factory=list)

    @validator('candidates', always=True)
    def init_candidates(cls, v, values, **kwargs):
        is_vacant = values['value'] == 0
        if is_vacant:
            # set candidates to all possible values
            return list(range(1,10))
        # set empty candidates
        return list()

    @property
    def is_vacant(self) -> bool:
        return self.value == 0

    def is_valid() -> bool:
        pass

    def __eq__(self, obj):
        return isinstance(obj, Cell) and obj.value == self.value or isinstance(obj, int) and obj == self.value
            


class GroupModel(Model):
    index: int
    cells: list[Cell] = Field(default_factory=list)

    @property
    def candidates(self) -> list[int]:
        """Returns a list of values that are not yet present in this group."""
        taken_values = [v.value for v in self.cells if v != 0]
        return [v for v in range(1, 10) if v not in taken_values]

    @property
    def values(self) -> list[int]:
        """Returns a list of all cell values that are not vacant."""
        return [c.value for c in self.cells if not c.is_vacant]

    def is_valid() -> bool:
        pass

    def __str__(self) -> str:
        cell_values = [str(c.value) for c in self.cells]
        return ''.join(cell_values)

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise ValueError('index must be of type int')
        return self.cells[index]


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
                
                row = self.rows[row_index]
                column = self.columns[col_index]
                box = self.boxes[self.find_box_index(row_index, col_index)]

                val = row_values[col_index]
                cell = Cell(value=int(val), index=row_index*9 + col_index, row=row, column=column, box=box)
                
                self.cells.append(cell)
                row.cells.append(cell)
                column.cells.append(cell)
                box.cells.append(cell)


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
            

Cell.update_forward_refs()
