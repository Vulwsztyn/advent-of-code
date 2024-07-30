use std::cmp::min;
use std::env;
use std::fs;
use std::time::Instant;
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
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let lines = contents.lines().collect::<Vec<&str>>();
    lines.iter().enumerate().for_each(
        |(line_i, line)| {
            println!("{} {}", line_i, line);
        }
    );
    // split at empty line
    let maps: Vec<Vec<&str>> = contents.split("\n\n").map(|x| x.lines().collect()).collect();
    let mut result = 0;
    let start = Instant::now();
    maps.iter().for_each(
        |map| {
            let width = map[0].len();
            for i in 0..width-1 {
                let mut valid = true;
                let how_many_to_check = min(i+1, width - i-1);
                for row in map.iter() {
                    for j in 0..how_many_to_check {
                        let left = i - j;
                        let right = i + j+1;
                        // println!("{} {} {} {}", i, j, left, right);
                        let left_char = row.chars().nth(left).unwrap();
                        let right_char = row.chars().nth(right).unwrap();
                        if left_char != right_char {
                            valid = false;
                            break;
                        }
                    }
                    if (!valid) {
                        break;
                    }
                }
                if valid {
                    println!("{} is valid - vertical", i+1);
                    result +=i+1;
                    break;
                }
            }
            let height = map.len();
            for i in 0..height-1 {
                let mut valid = true;
                let how_many_to_check = min(i+1, height - i-1);
                for col_i in 0..width {
                    for j in 0..how_many_to_check {
                        let top = i - j;
                        let bottom = i + j+1;
                        println!("{} {} {} {} {} {}x{}", i, j, top, bottom, col_i, width, height);
                        let top_char = map[top].chars().nth(col_i).unwrap();
                        let bottom_char = map[bottom].chars().nth(col_i).unwrap();
                        if top_char != bottom_char {
                            valid = false;
                            break;
                        }
                    }
                    if (!valid) {
                        break;
                    }
                }
                if valid {
                    println!("{} is valid - horizontal", i+1);
                    result += (i+1)*100;
                    break;
                }
            }
        }
    );
    let duration = start.elapsed();
    println!("Time elapsed: {:?}", duration);
    println!("Result: {}", result);
}
