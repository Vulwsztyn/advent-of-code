use std::env;
use std::fs;
// use onig::*;

#[derive(PartialOrd, PartialEq)]
enum Type {
    One,
    Pair,
    TwoPair,
    Three,
    House,
    Four,
    Five,
}

struct PartialHand {
    cards: str,
    bid: u128,
}

struct Hand {
    cards: str,
    bid: u128,
    hand_type: Type,
    card_values: Vec<u128>,
}

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
}
