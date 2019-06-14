#pragma once

#include <unordered_set>

using namespace ::std;

class SudokuConstants {
	public:
		unordered_set<char> digits;
		unordered_set<int> rows[9];
		unordered_set<int> columns[9];
		unordered_set<int> boxes[9];
		unordered_set<int> indices_in_same_row[81];
		unordered_set<int> indices_in_same_column[81];
		unordered_set<int> indices_in_same_box[81];
		unordered_set<int> collisions[81];

		SudokuConstants();
};
