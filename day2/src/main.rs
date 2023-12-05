use std::collections::HashMap;
use std::env;
use std::fs;
use onig::*;

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

fn get_value(line: &str) -> i32 {
    let value_regex = Regex::new(r"^Game (\d+):").unwrap();
    let value_indices = value_regex.captures(line).unwrap().iter_pos().map(|x| x.unwrap()).collect::<Vec<(usize, usize)>>();
    println!("Value indices: {:?}", value_indices);
    let value = line.get(value_indices[1].0..value_indices[1].1).unwrap().parse::<i32>().unwrap();
    value
}

fn line_value(line: &str) -> i32 {
    println!("Line: {}", line);
    let value = get_value(line);
    let balls_regex = Regex::new(r"\d+ [rgb]").unwrap();
    let limits: HashMap<&str, i32> = HashMap::from([
        ("r", 12),
        ("g", 13),
        ("b", 14),
    ]);
    let balls = balls_regex
        .find_iter(line)
        .map(
            |x| line
            .get(x.0..x.1)
            .unwrap()
        )
        .map (
            |x| x
            .split_whitespace()
            .collect::<Vec<&str>>()
        )
        .filter (
            |x| x[0].parse::<i32>().unwrap() > *limits.get(x[1]).unwrap()
        )
        .collect::<Vec<Vec<&str>>>();
    println!("Balls: {:?}", balls);
    if balls.len() == 0 { value } else { 0 }
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let numbers: Vec<i32> = contents.lines().map(|x| line_value(x)).collect();
    println!("Sum: {}", numbers.iter().sum::<i32>());
}
