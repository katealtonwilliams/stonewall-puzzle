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
        self.block_number = 0
        self.row = self.list_view.shape[0] - 1
        self.column = 0

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

    def find_largest_h_block(self) -> tuple[int]:
        start_row = self.list_view[self.row, self.column :]

        max_block_length = len(start_row)
        if len(block_lengths := np.where(start_row != "x")[0]) > 0:
            max_block_length = max(block_lengths)

        vertical_slice = self.list_view[
            : self.row + 1, self.column : self.column + max_block_length
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

        return (
            max_block_height * max_block_length,
            max_block_length,
            max_block_height,
        )

    def find_largest_v_block(self) -> tuple[int]:
        start_column = self.list_view[: self.row + 1, self.column]

        max_block_height = len(start_column)
        if len(block_heights := np.where(start_column != "x")[0]) > 0:
            max_block_height = len(start_column) - max(block_heights) - 1

        horizontal_slice = self.list_view[
            self.row - (max_block_height - 1) : self.row + 1, self.column :
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

        return (
            max_block_height * max_block_length,
            max_block_length,
            max_block_height,
        )

    def get_outer_coords(self, length: int, height: int) -> tuple[tuple[int]]:
        bottom_left_coord = (self.row, self.column)
        bottom_right_coord = (self.row, self.column + length - 1)
        top_left_coord = (self.row - (height - 1), self.column)
        top_right_coord = (self.row - (height - 1), self.column + length - 1)
        return (
            top_left_coord,
            top_right_coord,
            bottom_left_coord,
            bottom_right_coord,
        )

    def find_largest_block(self) -> tuple[int]:
        h_block_area, _, _ = self.find_largest_h_block()
        v_block_area, _, _ = self.find_largest_v_block()
        if h_block_area > v_block_area:
            return self.find_largest_h_block()
        return self.find_largest_v_block()

    def draw_block(self, length: int, height: int):
        self.list_view[
            self.row - (height - 1) : self.row + 1,
            self.column : self.column + length,
        ] = str(self.block_number)
        self.block_number += 1

    def find_and_draw_biggest_block(self):
        _, length, height = self.find_largest_block()
        self.draw_block(length, height)


if __name__ == "__main__":
    first_test_case = import_test_cases("input.json")[0]
    first_input = first_test_case["input"]
    mystonewall = Stonewall(first_input)
    pprint(mystonewall.list_view)
    mystonewall.find_and_draw_biggest_block()
    pprint(mystonewall.list_view)
