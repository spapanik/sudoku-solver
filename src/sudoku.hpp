#pragma once

#include <string>
#include <unordered_set>
#include <unordered_map>

#include "constants.hpp"

using namespace ::std;

class Sudoku {
	const string TOP = "┌─────┬─────┬─────┐";
	const string MID = "├─────┼─────┼─────┤";
	const string BTM = "└─────┴─────┴─────┘";

	string cells;
	SudokuConstants constants;
	unordered_map<int, unordered_set<char>> candidates;

	string format_row(int row);
	bool advance();
	bool advance_cells();
	bool naked_single();
	bool hidden_single();

	public:
		Sudoku(const string sudoku_initial);
		string str();
		bool solve();
};
