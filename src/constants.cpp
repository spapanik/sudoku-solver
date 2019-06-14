#include "constants.hpp"

#include <unordered_set>

using namespace ::std;

SudokuConstants::SudokuConstants() {
	digits = {'1', '2', '3', '4', '5', '6', '7', '8', '9'};

	for (int i = 0; i < 9; i++) {
		int row[9];
		int column[9];
		int box[9];

		for (int j = 0; j < 9; j++) {
			row[j] = 9 * i + j;
			column[j] = 9 * j + i;
			box[j] = 27 * (i/3) + 3 * (i%3) +  j % 3 + 9 * (j/3);
		}

		unordered_set<int> temp_row(row, row+9);
		rows[i] = temp_row;
		unordered_set<int> temp_column(column, column+9);
		columns[i] = temp_column;
		unordered_set<int> temp_box(box, box+9);
		boxes[i] = temp_box;
	}

	for (int i = 0; i < 81; i++) {
		bool colliding;
		int same_row[8];
		int row_counter = 0;
		int same_column[8];
		int column_counter = 0;
		int same_box[8];
		int box_counter = 0;
		int collision[20];
		int collision_counter = 0;

		for (int j = 0; j < 81; j++) {
			colliding = false;
			if (i / 9 == j / 9 && i != j) {
				same_row[row_counter++] = j;
				colliding = true;
			}
			if ((i - j) % 9 == 0 && i != j) {
				same_column[column_counter++] = j;
				colliding = true;
			}
			if (i / 27 == j / 27 && (i % 9) / 3 == (j % 9) / 3 && i != j) {
				same_box[box_counter++] = j;
				colliding = true;
			}
			if (colliding) {
				collision[collision_counter++] = j;
			}
		}

		unordered_set<int> temp_row(same_row, same_row+8);
		indices_in_same_row[i] = temp_row;
		unordered_set<int> temp_column(same_column, same_column+8);
		indices_in_same_column[i] = temp_column;
		unordered_set<int> temp_box(same_box, same_box+8);
		indices_in_same_box[i] = temp_box;
		unordered_set<int> temp_collision(collision, collision+20);
		collisions[i] = temp_collision;
	}
}
