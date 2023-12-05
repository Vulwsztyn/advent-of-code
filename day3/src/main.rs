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
fn surrounding_coords_with_limits(max_x: usize, max_y: usize, x1: i32, x2: i32, y: i32) -> Vec<(i32, i32)> {
    let mut coords = vec![];
    
    coords
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let lines = contents.lines().collect::<Vec<&str>>();
    let number_regex = Regex::new(r"\d+").unwrap();
    let max_x = lines[0].len();
    let max_y = lines.len();
    let surrounding_coords = |x1,x2,y| surrounding_coords_with_limits(max_x, max_y, x1, x2, y);
    lines.iter().enumerate().for_each(
        |(y, line)| {
            let numbers = number_regex
                .find_iter(line)
                .filter(
                    |(x1, x2)| true
                )
                .map(|x| line.get(x.0..x.1).unwrap().parse::<i32>().unwrap())
                .collect::<Vec<i32>>();
            println!("Line {}: {} {:?}", y, line, numbers);
        }
    );
    // println!("Contents: {}", contents);
}
