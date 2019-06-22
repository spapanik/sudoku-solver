#include <cstdlib>
#include <string>
#include <iostream>

#include "sudoku.hpp"
#include "utils.hpp"

using namespace ::std;

int main(int argc, char** argv) {
	if (argc == 1) {
		cerr << "No sudoku strings passed\n";
	}

	for (int i = 1; i < argc; i ++) {
		string sudoku_string = clean_string(argv[i]);
		if (sudoku_string.length() != 81) {
			cerr << "Invalid sudoku length for: " << argv[i] << endl;
			continue;
		}
		cout << "Solving sudoku: " << sudoku_string << endl;
		Sudoku sudoku(sudoku_string);
		bool success = sudoku.solve();
		if (success) {
			cout << "Solution:" << endl << sudoku.str();
		} else {
			cout
				<< "Couldn't solve sudoku, last step:" << endl << sudoku.str()
				<< "Debug info:" << endl << sudoku.debug_str();
		}
	}
	return EXIT_SUCCESS;
}
