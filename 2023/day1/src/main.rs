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


fn text_to_digit(text: &str) -> i32 {
    match text {
        "o" => 1,
        "t" => 2,
        "th" => 3,
        "f" => 4,
        "fi" => 5,
        "s" => 6,
        "se" => 7,
        "e" => 8,
        "n" => 9,
        _ => text.parse::<i32>().unwrap(),
    }
}

fn code_from_line(line: &str) -> i32 {
    println!("Line: {}", line);
    let re_digits = Regex::new(r"(\d|o(?=ne)|t(?=wo)|th(?=ree)|f(?=our)|fi(?=ve)|s(?=ix)|se(?=ven)|e(?=ight)|n(?=ine))").unwrap();
    let all_digits = re_digits.find_iter(line).into_iter().map(|x| text_to_digit(line.get(x.0..x.1).unwrap())).collect::<Vec<i32>>();
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
