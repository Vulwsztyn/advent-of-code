use std::env;
use std::fs;
use regex::Regex;

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


fn text_to_digit(text: &str) -> i32 {
    match text {
        "one" => 1,
        "two" => 2,
        "three" => 3,
        "four" => 4,
        "five" => 5,
        "six" => 6,
        "seven" => 7,
        "eight" => 8,
        "nine" => 9,
        _ => text.parse::<i32>().unwrap(),
    }
}

fn code_from_line(line: &str) -> i32 {
    println!("Line: {}", line);
    let re_digits = Regex::new(r"(\d|one|two|three|four|five|six|seven|eight|nine)").unwrap();
    let all_digits = re_digits.find_iter(line).map(|x| text_to_digit(x.as_str())).collect::<Vec<i32>>();
    println!("All digits: {:?}", all_digits);
    let first = all_digits.first().unwrap();
    let last = all_digits.last().unwrap();
    println!("First: {}, Last: {}", first, last);
    first*10 + last
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let numbers: Vec<i32> = contents.lines().map(|x| code_from_line(x)).collect();
    println!("Sum: {}", numbers.iter().sum::<i32>());
}
