use std::collections::HashMap;
use std::env;
use std::fs;
// use onig::*;
use std::time::Instant;

fn get_file_path() -> String {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    file_path.to_string()
}

fn get_file_contents(file_path: String) -> String {
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    contents
}

fn get_number_of_ways(map: String, expected: Vec<usize>,  memo: &mut HashMap<String, u128>) -> u128 {
    let key = format!("{}-{}", map, expected.iter().map(|x| x.to_string()).collect::<Vec<String>>().join(","));
    if memo.contains_key(&key) {
        return *memo.get(&key).unwrap();
    }
    if expected.len() == 0 {
        if map.find('#').is_none() {
            return 1;
        }
        return 0;
    }
    let first_expected = expected[0];
    if map.len() < first_expected {
        return 0;
    }
    let map_slice = &map[0..first_expected];
    let is_none = map_slice.find('.').is_none();
    let ends_with_dot =
        (map.len() == first_expected || map.chars().nth(first_expected).unwrap() != '#');
    let possible_to_fill_at_beginning = map_slice.find('.').is_none()
        && (map.len() == first_expected || map.chars().nth(first_expected).unwrap() != '#');
    let result = if map.chars().nth(0).unwrap() != '#' {get_number_of_ways(map[1..].to_owned(), expected.clone(), memo)} else {0}
        + if possible_to_fill_at_beginning {
            get_number_of_ways(
                if map.len() == first_expected {
                    "".to_owned()
                } else {
                    map[first_expected + 1..].to_owned()
                },
                expected[1..].to_vec(), memo
            )
        } else {
            0
        };
    memo.insert(key, result);
    return result;
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let lines = contents.lines().collect::<Vec<&str>>();
    lines.iter().enumerate().for_each(|(line_i, line)| {
        println!("{} {}", line_i, line);
    });
    let mut result = 0;
    let start = Instant::now();
    for (line_i, line) in lines.iter().enumerate() {
        // println!("line: {}", line);
        let split = line.split_whitespace().collect::<Vec<&str>>();
        let map = (split[0].to_owned()+"?").repeat(4) + split[0];
        let expected_str = (split[1].to_owned()+",").repeat(4) + split[1];
        // let map = split[0];
        // let expected_str = split[1];
        let expected = expected_str
            .split(',')
            .map(|x| x.parse::<usize>().unwrap())
            .collect::<Vec<usize>>();
        // println!("map: {}", map);
        // println!("expected: {:?}", expected);
        let line_result = get_number_of_ways(map.to_owned(), expected, &mut HashMap::new());
        // println!("line_i: {}, line_result: {}", line_i, line_result);
        result += line_result;
    }
    let duration = start.elapsed();
    println!("Time elapsed: {:?}", duration);
    println!("result: {}", result);
}
