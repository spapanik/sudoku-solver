#include <string>
#include <iostream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <exception>

#include "sudoku.hpp"
#include "constants.hpp"

using namespace ::std;

Sudoku::Sudoku(const string sudoku_string) {
	cells = sudoku_string;
	constants = SudokuConstants();

	for (int i = 0; i < 81; i++) {
		if (cells[i] == '.') {
			unordered_set<char> temp_digits(constants.digits);
			for (int j: constants.collisions[i]) {
				temp_digits.erase(cells[j]);
			}
			candidates[i] = temp_digits;
		}
	}
}


string Sudoku::str() {
	ostringstream stringStream;
	stringStream
	<< TOP << endl
	<< format_row(0) << format_row(1) << format_row(2) << MID << endl
	<< format_row(3) << format_row(4) << format_row(5) << MID << endl
	<< format_row(6) << format_row(7) << format_row(8) << BTM << endl;
	return stringStream.str();
}


string Sudoku::format_row(int row) {
	int start = 9*row;
	ostringstream stringStream;
	stringStream
			<< "│" << cells[start] << " " << cells[start+1] << " " << cells[start+2]
			<< "│" << cells[start+3] << " " << cells[start+4] << " " << cells[start+5]
			<< "│" << cells[start+6] << " " << cells[start+7] << " " << cells[start+8]
			<< "│\n";
	return stringStream.str();
}


bool Sudoku::solve() {
	while (cells.find('.') != string::npos) {
		if (!advance()) {
			return false;
		}
	}
	return true;
}


bool Sudoku::advance() {
	return advance_cells();
}


bool Sudoku::advance_cells() {
	return naked_single() || hidden_single();
}


template <class type>
type get_element(unordered_set<type> non_empty_set) {
	for (type object: non_empty_set) {
		return object;
	}

	throw runtime_error("get_element called on an empty set.");
}


template <class type> unordered_set<type> intersection_set(unordered_set<type> first, unordered_set<type> second) {
	unordered_set<type> output{};
	for (type object: first) {
		if (second.find(object) != second.end()) {
			output.insert(object);
		}
	}

	return output;
}


template <class type> unordered_set<type> union_set(unordered_set<type> first, unordered_set<type> second) {
	unordered_set<type> output{};
	for (type object: first) {
		output.insert(object);
	}
	for (type object: second) {
		output.insert(object);
	}

	return output;
}


template <class type> unordered_set<type> difference_set(unordered_set<type> first, unordered_set<type> second) {
	unordered_set<type> output{};
	for (type object: first) {
		if (second.find(object) == second.end()) {
			output.insert(object);
		}
	}

	return output;
}


bool Sudoku::naked_single() {
	bool advanced = false;
	vector<int> deleted;

	for (pair<int, unordered_set<char>> candidate_pair: candidates) {
		if (candidate_pair.second.size() == 1) {
			int index = candidate_pair.first;
			char digit = get_element(candidate_pair.second);
			cells[index] = digit;
			deleted.push_back(index);
			for (int i: constants.collisions[index]) {
				if (candidates.find(i) != candidates.end()) {
					candidates[i].erase(digit);
				}
			}
			advanced = true;
		}
	}

	for (int index: deleted) {
		candidates.erase(index);
	}

	return advanced;
}

bool Sudoku::hidden_single() {
	bool advanced = false;
	vector<int> deleted;

	for (pair<int, unordered_set<char>> candidate_pair: candidates) {
			unordered_set<int> blocks[3];
			int index = candidate_pair.first;
			blocks[0] = constants.indices_in_same_row[index];
			blocks[1] = constants.indices_in_same_column[index];
			blocks[2] = constants.indices_in_same_box[index];
			for (unordered_set<int> block: blocks) {
				unordered_set<char> unique(candidates[index]);
				for (int j: block) {
					for (char digit: candidates[j]) {
						unique.erase(digit);
					}
				}
				if (unique.size() == 1) {
					advanced = true;
					char digit = get_element(unique);
					cells[index] = digit;
					deleted.push_back(index);
					for (int i: constants.collisions[index]) {
						if (candidates.find(i) != candidates.end()) {
							candidates[i].erase(digit);
						}
					}
					break;
				}
			}
	}
	for (int index: deleted) {
		candidates.erase(index);
	}

		return advanced;
}
