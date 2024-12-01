use std::env;
use std::fs;
use onig::*;
use std::iter::zip;

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
    let times = get_numbers(&lines, 0);
    let limits = get_numbers(&lines, 1);
    let numbers = zip(times, limits).map(
        |(time, limit)| {
            let mut number_of_ways = 0;
            for velocity in 1..time - 1 {
                let time_left = time - velocity;
                let distance = velocity * time_left;
                if distance > limit {
                    // println!("{} {} {} {}", time, limit, velocity, time_left);
                    number_of_ways += 1;
                }
            }
            number_of_ways
        }
    ).collect::<Vec<u128>>();
    println!("{:?}", numbers);
    let product = numbers.iter().product::<u128>();
    println!("{}", product);
}

fn get_numbers(lines: &Vec<&str>, index: usize) -> Vec<u128> {
    let number_regex = Regex::new(r"\d+").unwrap();

    number_regex.find_iter(&lines[index]).map(
        |(start, end)| {
            lines[index][start..end].parse::<u128>().unwrap()
        }
    ).collect::<Vec<u128>>()

}
