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
	bool advance_candidates();
	// region: Advance sudoku.cells
	bool naked_single();
	bool hidden_single();
	// endregion
	// region: Advance sudoku.candidates
	bool naked_pair();
	bool naked_pair_group(unordered_set<int> group);
	bool hidden_pair();
	bool hidden_pair_group(unordered_set<int> group);
	// endregion

	public:
		Sudoku(const string sudoku_initial);
		string str();
		bool solve();
};
