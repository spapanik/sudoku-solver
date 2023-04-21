use crate::sudoku::constants::*;
use std::collections::{HashMap, HashSet};

pub struct SudokuPuzzle {
    top: String,
    mid: String,
    bottom: String,
    cells: Vec<char>,
    candidates: HashMap<usize, HashSet<char>>,
    constants: SudokuConstants,
}

impl SudokuPuzzle {
    pub fn new(string: String) -> SudokuPuzzle {
        const TOP: &str = "┌─────┬─────┬─────┐";
        const MID: &str = "├─────┼─────┼─────┤";
        const BTM: &str = "└─────┴─────┴─────┘";
        let constants = SudokuConstants::new();
        let mut cells: Vec<char> = string.chars().collect();
        let mut candidates = HashMap::new();
        for i in 0..81 {
            let mut temp_digits = constants.digits.clone();
            if !temp_digits.contains(&cells[i]) {
                cells[i] = '.';
            }
            if cells[i] == '.' {
                for j in &constants.collisions[i] {
                    temp_digits.remove(&cells[*j]);
                }
                candidates.insert(i, temp_digits);
            }
        }
        return SudokuPuzzle {
            top: String::from(TOP),
            mid: String::from(MID),
            bottom: String::from(BTM),
            cells,
            candidates,
            constants,
        };
    }

    pub fn solve(&mut self) -> bool {
        while self.cells.contains(&'.') {
            if !&self.advance() {
                return false;
            }
        }
        return true;
    }

    pub fn matrix(&self) -> String {
        return format!(
            "{}\n{}{}{}{}\n{}{}{}{}\n{}{}{}{}\n",
            self.top,
            self.format_row(0),
            self.format_row(1),
            self.format_row(2),
            self.mid,
            self.format_row(3),
            self.format_row(4),
            self.format_row(5),
            self.mid,
            self.format_row(6),
            self.format_row(7),
            self.format_row(8),
            self.bottom,
        );
    }

    pub fn debug_info(&self) -> String {
        let mut output = format!(
            "cells: {}\ncandidates: {{\n",
            String::from_iter(self.cells.iter())
        );
        for i in 0..81 {
            if self.cells[i] == '.' {
                output += &format!("\t{}:", self.format_cell_id(i));
                if !self.candidates.contains_key(&i) || self.candidates[&i].len() == 0 {
                    output += " no candidates,\n";
                } else {
                    output += " {";
                    let mut sorted = self.candidates[&i].iter().collect::<Vec<&char>>();
                    sorted.sort_unstable();
                    for candidate in sorted {
                        output += &format!("{candidate}, ");
                    }
                    output += "\x08\x08},\n";
                }
            }
        }
        output += "}\n";
        return output;
    }

    fn format_cell_id(&self, cell_index: usize) -> String {
        let row_id = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J'];
        return format!("{}{}", row_id[cell_index / 9], (cell_index % 9) + 1);
    }

    fn format_row(&self, row: usize) -> String {
        let start = 9 * row;
        return format!(
            "│{} {} {}│{} {} {}│{} {} {}│\n",
            self.cells[start],
            self.cells[start + 1],
            self.cells[start + 2],
            self.cells[start + 3],
            self.cells[start + 4],
            self.cells[start + 5],
            self.cells[start + 6],
            self.cells[start + 7],
            self.cells[start + 8]
        );
    }

    fn advance(&mut self) -> bool {
        return self.advance_cells() || self.advance_candidates();
    }

    fn advance_cells(&mut self) -> bool {
        return self.naked_single() || self.hidden_single();
    }

    fn advance_candidates(&mut self) -> bool {
        return self.naked_pair() || self.hidden_pair() || self.pointing_pair();
    }

    fn set_and_clean(&mut self, index: usize, digit: char) {
        self.cells[index] = digit;
        self.candidates.remove(&index);
        for i in &self.constants.collisions[index] {
            if self.candidates.contains_key(i) {
                self.candidates.get_mut(i).unwrap().remove(&digit);
            }
        }
    }

    fn naked_single(&mut self) -> bool {
        let mut advanced = false;

        let candidates = self.candidates.clone();

        for index in candidates.keys() {
            if self.candidates[index].len() == 1 {
                advanced = true;
                self.set_and_clean(*index, *self.candidates[index].iter().next().unwrap());
            }
        }
        return advanced;
    }

    fn hidden_single(&mut self) -> bool {
        let mut advanced = false;
        let candidates = self.candidates.clone();

        for index in candidates.keys() {
            let blocks = vec![
                self.constants.indices_in_same_row[*index].clone(),
                self.constants.indices_in_same_column[*index].clone(),
                self.constants.indices_in_same_box[*index].clone(),
            ];

            for block in blocks.iter() {
                let mut unique = self.candidates[index].clone();
                for i in block.iter() {
                    if self.candidates.contains_key(i) {
                        for digit in self.candidates[i].iter() {
                            unique.remove(digit);
                        }
                    }
                }
                if unique.len() == 1 {
                    advanced = true;
                    self.set_and_clean(*index, *unique.iter().next().unwrap());
                    break;
                }
            }
        }
        return advanced;
    }

    fn naked_pair(&mut self) -> bool {
        /*
            bool Sudoku::naked_pair(unordered_set<int> group) {
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
                advanced |= naked_pair(row);
            }
            for (unordered_set<int> column: constants.columns) {
                advanced |= naked_pair(column);
            }
            for (unordered_set<int> box: constants.boxes) {
                advanced |= naked_pair(box);
            }

            return advanced;
        }

            */
        return false;
    }

    fn hidden_pair(&mut self) -> bool {
        /*
            bool Sudoku::hidden_pair(unordered_set<int> group) {
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
                advanced |= hidden_pair(row);
            }
            for (unordered_set<int> column: constants.columns) {
                advanced |= hidden_pair(column);
            }
            for (unordered_set<int> box: constants.boxes) {
                advanced |= hidden_pair(box);
            }

            return advanced;
        }
            */
        return false;
    }

    fn pointing_pair(&mut self) -> bool {
        /*
                bool advanced = false;
            unordered_set<int> unfilled{};
            for (auto candidate: candidates) {
                unfilled.insert(candidate.first);
            }
            auto common = intersection_set(intersection_set(box, line), unfilled);
            if (common.size() == 0) {
                return false;
            }
            auto outside_line = intersection_set(difference_set(box, line), unfilled);
            auto outside_box = intersection_set(difference_set(line, box), unfilled);
            if ((outside_line.size() == 0) || (outside_box.size() == 0)) {
                return false;
            }

            unordered_set<char> common_digits{};
            for (auto index: common) {
                for (auto digit: candidates[index]) {
                    common_digits.insert(digit);
                }
            }
            unordered_set<char> outside_line_digits{};
            for (auto index: outside_line) {
                for (auto digit: candidates[index]) {
                    outside_line_digits.insert(digit);
                }
            }
            unordered_set<char> outside_box_digits{};
            for (auto index: outside_box) {
                for (auto digit: candidates[index]) {
                    outside_box_digits.insert(digit);
                }
            }

            auto line_only_digits = difference_set(common_digits, outside_line_digits);
            if (intersection_set(line_only_digits, outside_box_digits).size() > 0) {
                advanced = true;
                for (auto index: outside_box) {
                    candidates[index] = difference_set(candidates[index], line_only_digits);
                }
            }

            auto box_only_digits = difference_set(common_digits, outside_box_digits);
            if (intersection_set(box_only_digits, outside_line_digits).size() > 0) {
                advanced = true;
                for (auto index: outside_line) {
                    candidates[index] = difference_set(candidates[index], box_only_digits);
                }
            }

            return advanced;
        }


        bool Sudoku::pointing_pair() {
            bool advanced = false;
            for (unordered_set<int> box: constants.boxes) {
                for (unordered_set<int> row: constants.rows) {
                    advanced |= pointing_pair(box, row);
                }
                for (unordered_set<int> column: constants.columns) {
                    advanced |= pointing_pair(box, column);
                }
            }
            return advanced;
            */
        return false;
    }
}
