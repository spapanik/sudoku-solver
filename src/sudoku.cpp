#include <string>
#include <iostream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <exception>

#include "utils.hpp"
#include "constants.hpp"
#include "sudoku.hpp"

using namespace ::std;

Sudoku::Sudoku(const string sudoku_string) {
	cells = sudoku_string;
	constants = SudokuConstants();

	for (int i = 0; i < 81; i++) {
		if (cells[i] == '.') {
			unordered_set<char> temp_digits = constants.digits;
			for (int j: constants.collisions[i]) {
				temp_digits.erase(cells[j]);
			}
			candidates[i] = temp_digits;
		}
	}
}


vector<char> sort_digits(unordered_set<char> digits) {
	vector<char> out{};
	for (char c: {'1', '2', '3', '4', '5', '6', '7', '8', '9'}) {
		if (digits.find(c) != digits.end()) {
			out.push_back(c);
		}
	}
	return out;
}


string Sudoku::debug_str() {
	ostringstream stringStream;
	vector<char> row_id{'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J'};
	stringStream
		<< "cells: " << cells << endl
		<< "candidates: {" << endl;

	for (int i = 0; i < 81; i++) {
		if (candidates.find(i) != candidates.end()) {
			stringStream << "\t";
			stringStream << row_id[i/9];
			stringStream << (i%9) + 1 << ": (";
			for (char c: sort_digits(candidates[i])) {
				stringStream << c << ", ";
			}
			stringStream << "\b\b)," << endl;
		}
	}
	stringStream << "}" << endl;
	return stringStream.str();
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
	return advance_cells() || advance_candidates();
}


bool Sudoku::advance_cells() {
	return naked_single() || hidden_single();
}


bool Sudoku::advance_candidates() {
	return naked_pair() || hidden_pair();
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
			int index = candidate_pair.first;
			unordered_set<int> blocks[3] = {
				constants.indices_in_same_row[index],
				constants.indices_in_same_column[index],
				constants.indices_in_same_box[index],
			};

			for (unordered_set<int> block: blocks) {
				unordered_set<char> unique = candidates[index];
				for (int j: block) {
					if (candidates.find(j) != candidates.end()) {
						for (char digit: candidates[j]) {
							unique.erase(digit);
						}
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


bool Sudoku::naked_pair_group(unordered_set<int> group) {
	bool advanced = false;
	unordered_set<int> unfilled{};
	for (pair<int, unordered_set<char>> candidate: candidates) {
		unfilled.insert(candidate.first);
	}
	unordered_set<int> indices = intersection_set(group, unfilled);
	if (indices.size() <= 2) {
		return false;
	}

	Combinations<unordered_set<int>, int> combinations(indices, 2);
	while (!combinations.completed) {
		vector<int> combination = combinations.next();
		int index_1 = combination[0];
		int index_2 = combination[1];
		unordered_set<char> digits = candidates[index_1];
		if (digits.size() != 2 || digits != candidates[index_2]) {
			continue;
		}
		for (int index: difference_set(indices, {index_1, index_2})) {
			if (intersection_set(digits, candidates[index]).size()) {
				candidates[index] = difference_set(candidates[index], digits);
				advanced = true;
			}
		}
	}

	return advanced;
}


bool Sudoku::naked_pair() {
	bool advanced = false;
	for (unordered_set<int> row: constants.rows) {
		advanced |= naked_pair_group(row);
	}
	for (unordered_set<int> column: constants.columns) {
		advanced |= naked_pair_group(column);
	}
	for (unordered_set<int> box: constants.boxes) {
		advanced |= naked_pair_group(box);
	}

	return advanced;
}


bool Sudoku::hidden_pair_group(unordered_set<int> group) {
	bool advanced = false;
	unordered_set<int> unfilled{};
	for (pair<int, unordered_set<char>> candidate: candidates) {
		unfilled.insert(candidate.first);
	}
	unordered_set<int> indices = intersection_set(group, unfilled);
	if (indices.size() <= 2) {
		return false;
	}

	Combinations<unordered_set<int>, int> combinations(indices, 2);
	while (!combinations.completed) {
		vector<int> combination = combinations.next();
		int index_1 = combination[0];
		int index_2 = combination[1];
		if (union_set(candidates[index_1], candidates[index_2]).size() == 2) {
			continue;
		}
		unordered_set<char> common = intersection_set(candidates[index_1], candidates[index_2]);
		unordered_set<char> other{};
		for (int index: difference_set(indices, {index_1, index_2})) {
			for (char digit: candidates[index]) {
				other.insert(digit);
			}
		}
		unordered_set<char> hidden = difference_set(common, other);
		if (hidden.size() != 2) {
			continue;
		}
		candidates[index_1] = hidden;
		candidates[index_2] = hidden;
		advanced = true;
	}

	return advanced;
}


bool Sudoku::hidden_pair() {
	bool advanced = false;
	for (unordered_set<int> row: constants.rows) {
		advanced |= hidden_pair_group(row);
	}
	for (unordered_set<int> column: constants.columns) {
		advanced |= hidden_pair_group(column);
	}
	for (unordered_set<int> box: constants.boxes) {
		advanced |= hidden_pair_group(box);
	}

	return advanced;
}
