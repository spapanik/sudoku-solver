mod sudoku;

use std::env;
use std::time::Instant;
use std::process::ExitCode;
use crate::sudoku::puzzle::*;

fn format_time(mut raw_time: f64) -> String {
    if raw_time < 1000.0 {
        return format!("{:.0} ns", raw_time);
    }
    raw_time /= 1000.0;
    if raw_time < 1000.0 {
        return format!("{:.1} µs", raw_time);
    }
    raw_time /= 1000.0;
    if raw_time < 1000.0 {
        return format!("{:.1} ms", raw_time);
    }
    raw_time /= 1000.0;
    return format!("{:.2} s", raw_time);
}

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    let mut show_timings = false;
    let mut skip = 1;
    let mut total_time: u64 = 0;

    if args.len() == 1 {
        eprintln!("No arguments provided");
        return ExitCode::FAILURE;
    }

    if args[1] == "-t" {
    if args.len() == 2 {
        eprintln!("No arguments provided");
        return ExitCode::FAILURE;
    }
        show_timings = true;
        skip = 2;
    }

    for sudoku_string in args.iter().skip(skip) {
        if sudoku_string.len() != 81 {
            eprintln!("Invalid sudoku string length");
            continue;
        }
        let now = Instant::now();
        let mut sudoku_puzzle = SudokuPuzzle::new(sudoku_string.to_string());
        let elapsed = now.elapsed();
        total_time += 1000000000 * (elapsed.as_secs() as u64) + (elapsed.subsec_nanos() as u64);
        println!("Solving sudoku:\n{}", sudoku_puzzle.matrix());
        let success = sudoku_puzzle.solve();
        if success {
            println!("Solved sudoku:\n{}", sudoku_puzzle.matrix());
        } else {
            eprintln!("Failed to solve sudoku:\n{}", sudoku_puzzle.matrix());
            eprintln!("Debug info:\n{}", sudoku_puzzle.debug_info());
        }
    }

    if show_timings {
        println!("Total time: {}", format_time(total_time as f64));
    }
    return ExitCode::SUCCESS;
}
