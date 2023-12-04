use std::env;
use std::fs;

fn get_file_patb() -> String {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    file_path.to_string()
}

fn get_file_contents(file_path: String) -> String {
    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    contents
}

fn first_digit<T: std::iter::Iterator<Item=char>>(chars: T) -> i32 {
    for c in chars {
        if c.is_digit(10) {
            return c.to_digit(10).unwrap() as i32;
        }
    }
    0
}

fn code_from_line(line: &str) -> i32 {
    let first = first_digit(line.chars());
    let last = first_digit(line.chars().rev());
    println!("First: {}, Last: {}", first, last);
    first*10 + last
}

fn main() {
    let file_path = get_file_patb();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let numbers: Vec<i32> = contents.lines().map(|x| code_from_line(x)).collect();
    println!("Sum: {}", numbers.iter().sum::<i32>());
}