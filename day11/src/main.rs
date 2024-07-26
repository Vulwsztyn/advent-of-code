use std::collections::{BTreeSet, HashMap, HashSet};
use std::env;
use std::fs;
// use onig::*;

fn get_file_path() -> String {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    file_path.to_string()
}

fn get_file_contents(file_path: String) -> String {
    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    contents
}

fn main() {
    let addendum = 1000000; // 2 for part 1
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let lines = contents.lines().collect::<Vec<&str>>();
    lines.iter().enumerate().for_each(
        |(line_i, line)| {
            println!("{} {}", line_i, line);
        }
    );
    let mut galaxies: Vec<(usize,usize)> = Vec::new();
    let mut rows_without_galaxies: BTreeSet<usize> = BTreeSet::new();
    let mut cols_without_galaxies: BTreeSet<usize> = BTreeSet::new();
    // fill rows_without_galaxies and cols_without_galaxies with all possibles
    for i in 0..lines.len() {
        rows_without_galaxies.insert(i);
    }
    for i in 0..lines[0].len() {
        cols_without_galaxies.insert(i);
    }
    lines.iter().enumerate().for_each(
        |(line_i, line)| {
            line.chars().enumerate().for_each(
                |(char_i, char)| {
                    if char == '#' {
                        galaxies.push((line_i, char_i));
                        rows_without_galaxies.remove(&line_i);
                        cols_without_galaxies.remove(&char_i);
                    }
                }
            )
        }
    );
    println!("{:?}", galaxies);
    println!("{:?}", rows_without_galaxies);
    println!("{:?}", cols_without_galaxies);
    let mut row_mapping: HashMap<usize, usize> = HashMap::new();
    let mut col_mapping: HashMap<usize, usize> = HashMap::new();
    let mut previous: usize = 0;
    let mut offset: usize = 0;
    for row in rows_without_galaxies.iter() {
        for i in previous..*row {
            row_mapping.insert(i, i+offset);
        }
        offset += addendum-1;
        previous = *row+1;
    }
    for i in previous..lines.len() {
        row_mapping.insert(i, i+offset);
    }
    previous = 0;
    offset = 0;
    for col in cols_without_galaxies.iter() {
        for i in previous..*col {
            col_mapping.insert(i, i+offset);
        }
        offset += addendum-1;
        previous = *col+1;
    }
    for i in previous..lines[0].len() {
        col_mapping.insert(i, i+offset);
    }
    // println!("{:?}", row_mapping);
    // println!("{:?}", col_mapping);
    let mut new_galaxies: Vec<(usize,usize)> = galaxies.iter().map(|(row, col)| {
        (row_mapping.get(row).unwrap().clone(), col_mapping.get(col).unwrap().clone())
    }).collect();
    println!("{:?}", new_galaxies);
    let mut distance_sum: usize = 0;
    for i in 0..new_galaxies.len() {
        for j in i+1..new_galaxies.len() {
            let (row1, col1) = new_galaxies[i];
            let (row2, col2) = new_galaxies[j];
            let distance = (row1 as i32 - row2 as i32).abs() as usize + (col1 as i32 - col2 as i32).abs() as usize;
            distance_sum += distance;
        }
    }
    println!("{}", distance_sum);
}
