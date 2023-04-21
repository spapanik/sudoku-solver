use std::collections::HashSet;

pub struct SudokuConstants {
    pub digits: HashSet<char>,
    pub rows: Vec<HashSet<usize>>,
    pub columns: Vec<HashSet<usize>>,
    pub boxes: Vec<HashSet<usize>>,
    pub indices_in_same_row: Vec<HashSet<usize>>,
    pub indices_in_same_column: Vec<HashSet<usize>>,
    pub indices_in_same_box: Vec<HashSet<usize>>,
    pub collisions: Vec<HashSet<usize>>,
}

impl SudokuConstants {
    pub fn new() -> SudokuConstants {
        let digits = HashSet::from(['1', '2', '3', '4', '5', '6', '7', '8', '9']);
        let mut rows = vec![HashSet::new(); 9];
        let mut columns = vec![HashSet::new(); 9];
        let mut boxes = vec![HashSet::new(); 9];
        let mut indices_in_same_row = vec![HashSet::new(); 81];
        let mut indices_in_same_column = vec![HashSet::new(); 81];
        let mut indices_in_same_box = vec![HashSet::new(); 81];
        let mut collisions = vec![HashSet::new(); 81];

        for i in 0..9 {
            for j in 0..9 {
                rows[i].insert(9 * i + j);
                columns[i].insert(9 * j + i);
                boxes[i].insert(27 * (i / 3) + 3 * (i % 3) + j % 3 + 9 * (j / 3));
            }
        }

        for i in 0..81 {
            for j in 0..i {
                if i / 9 == j / 9 {
                    indices_in_same_row[i].insert(j);
                    indices_in_same_row[j].insert(i);
                    collisions[i].insert(j);
                    collisions[j].insert(i);
                }
                if (i - j) % 9 == 0 {
                    indices_in_same_column[i].insert(j);
                    indices_in_same_column[j].insert(i);
                    collisions[i].insert(j);
                    collisions[j].insert(i);
                }
                if i / 27 == j / 27 && (i % 9) / 3 == (j % 9) / 3 {
                    indices_in_same_box[i].insert(j);
                    indices_in_same_box[j].insert(i);
                    collisions[i].insert(j);
                    collisions[j].insert(i);
                }
            }
        }

        return SudokuConstants {
            digits,
            rows,
            columns,
            boxes,
            indices_in_same_row,
            indices_in_same_column,
            indices_in_same_box,
            collisions,
        };
    }
}
