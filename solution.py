import json
from pprint import pprint
import numpy as np
import copy


def import_test_cases(file_name: str) -> list[dict]:
    with open(file_name) as test_cases:
        test_cases = json.load(test_cases)
    return test_cases


class Stonewall:
    def __init__(self, heights: list[int]):
        self.heights = heights
        self.list_view = heights

    @property
    def list_view(self):
        return self._list_view

    @list_view.setter
    def list_view(self, heights: list[int]):
        length = len(self.heights)
        max_height = max(self.heights)
        stone_wall = []
        for i in range(max_height):
            line = []
            for j in range(length):
                line.append(" ")
            stone_wall.append(line)
        column_no = -1
        for height in self.heights:
            column_no += 1
            for k in range(height):
                stone_wall[max_height - 1 - k][column_no] = "x"
        self._list_view = np.array(stone_wall)

    def __repr__(self) -> str:
        return repr(self.heights)

    def looking_horizontally(self, row: int, column: int):
        start_row = self.list_view[row, column:]

        max_block_length = len(start_row)
        if len(block_lengths := np.where(start_row != "x")[0]) > 0:
            max_block_length = max(block_lengths)

        vertical_slice = self.list_view[
            : row + 1, column : column + max_block_length
        ]

        max_block_height = vertical_slice.shape[0]
        if (
            len(
                block_heights := np.where(
                    np.any(vertical_slice != "x", axis=1)
                )[0]
            )
            > 0
        ):
            max_block_height = vertical_slice.shape[0] - max(block_heights) - 1

        return max_block_length, max_block_height

    def looking_vertically(self, row: int, column: int):
        start_column = self.list_view[: row + 1, column]

        max_block_height = len(start_column)
        if len(block_heights := np.where(start_column != "x")[0]) > 0:
            max_block_height = len(start_column) - max(block_heights) - 1

        horizontal_slice = self.list_view[
            row - (max_block_height - 1) : row + 1, column:
        ]

        max_block_length = horizontal_slice.shape[1]

        if (
            len(
                block_lengths := np.where(
                    np.any(horizontal_slice != "x", axis=0)
                )[0]
            )
            > 0
        ):
            max_block_length = min(block_lengths)

        return max_block_length, max_block_height

    def get_outer_coords(
        row: int, column: int, length: int, height: int
    ) -> tuple[tuple[int]]:
        bottom_left_coord = (row, column)
        bottom_right_coord = (row, column + length - 1)
        top_left_coord = (row - (height - 1), column)
        top_right_coord = (row - (height - 1), column + length - 1)
        return (
            top_left_coord,
            top_right_coord,
            bottom_left_coord,
            bottom_right_coord,
        )


# next steps - write function that chooses the bigger out of horizontal and vertical
# to replace the used blocks with 'b' - or incremental letters if possible
# select the next bottom leftest


if __name__ == "__main__":
    first_test_case = import_test_cases("input.json")[0]
    first_input = first_test_case["input"]
    mystonewall = Stonewall(first_input)
    # pprint(mystonewall.list_view)
    looking_vertically(
        mystonewall.list_view.shape[0] - 1, 0, mystonewall.list_view
    )
    looking_horizontally(
        mystonewall.list_view.shape[0] - 1, 0, mystonewall.list_view
    )
