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
    let sequence = lines[0];
    let map = get_map(lines);

    let mut current_nodes = map.keys().filter(|key| key.ends_with("A")).map(|x| x.clone()).collect::<Vec<String>>();
    // print current
    current_nodes.iter().for_each(
        |node| {
            println!("{}", node);
        }
    );
    let mut sequence_index = 0;
    let mut steps_count = 0;
    println!("");
    while !is_end(&current_nodes) {
        let new_nodes = current_nodes.iter().map(
            |current| {
                let next_choices = map.get(current).unwrap();
                if sequence.chars().nth(sequence_index).unwrap() == 'L' {
                    next_choices.0.clone()
                } else {
                    next_choices.1.clone()
                }
            }
        ).collect::<Vec<String>>();

        // println!("{}", sequence.chars().nth(sequence_index).unwrap());
        steps_count += 1;
        sequence_index += 1;
        if sequence_index == sequence.len() {
            sequence_index = 0;
        }
        // print current
        // new_nodes.iter().for_each(
        //     |node| {
        //         println!("{}", node);
        //     }
        // );
        current_nodes = new_nodes;
        // println!("{}",steps_count);
    }
    println!("{}",steps_count);
}

fn is_end(nodes: &Vec<String>) -> bool {
    nodes.iter().all(|node| node.ends_with("Z"))
}

fn get_map(lines: Vec<&str>) -> HashMap<String, (String, String)> {
    let mut map = HashMap::new();
    let line_regex = Regex::new(r"(\w+)\s\=\s\((\w+)\,\s(\w+)\)").unwrap();
    lines.iter().skip(2).for_each(
        |line| {
            let captures = line_regex.captures(line).unwrap();
            let key = captures.at(1).unwrap();
            println!("{} {} {}", key, captures.at(2).unwrap(), captures.at(3).unwrap());
            map.insert(key.to_string(), (captures.at(2).unwrap().to_string(), captures.at(3).unwrap().to_string()));
        }
    );
    map
}