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

struct MapInfo {
    map: HashMap<String, (String, String)>,
    seq: String,
}

struct Runner {
    first_end_value: String,
    first_end_steps: usize,
    cycle_length: usize,
    other_ends_at: Vec<usize>,
}

fn get_runner(start: &String, map_info: &MapInfo) -> Runner {
    let (first_end_value, first_end_steps) = get_first_end(start, map_info, 0);
    let (cycle_length, other_ends_at) = get_cycle(&first_end_value, map_info, first_end_steps, 0, &first_end_value, &vec![]);
    return Runner {
        first_end_value,
        first_end_steps,
        cycle_length,
        other_ends_at,
    };
}

fn get_cycle(end: &String, map_info: &MapInfo, end_index: usize, steps: usize, current: &String, other_ends: &Vec<usize>) -> (usize, Vec<usize>) {
    if steps > 0 && current == end {
        return (steps, other_ends.clone());
    }
    let mut new_other_ends = other_ends.clone();
    if steps>0 && is_end(&current) {
        new_other_ends.push(steps);
    }
    let next = next_node(current, map_info, end_index + steps);

    return get_cycle(end, map_info, end_index, steps + 1, &next, &new_other_ends);
}

fn next_node(current: &String, map_info: &MapInfo, sequence_index: usize) -> String {
    let maybe_next_choices = map_info.map.get(current);
    let next_choices = maybe_next_choices.unwrap();
    let index = sequence_index % map_info.seq.len();
    if map_info.seq.chars().nth(index).unwrap() == 'L' {
        next_choices.0.clone()
    } else {
        next_choices.1.clone()
    }
}

fn get_first_end(start: &String, map_info: &MapInfo, steps: usize) -> (String, usize) {
    if is_end(start) {
        return (start.clone(), steps);
    }
    return get_first_end(&next_node(start, map_info, steps), map_info, steps + 1);
}

fn gcd(a: usize, b: usize) -> usize {
    if b == 0 {
        return a;
    }
    return gcd(b, a % b);
}

fn lcm(a: usize, b: usize) -> usize {
    return a * b / gcd(a, b);
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let lines = contents.lines().collect::<Vec<&str>>();
    let map_info = get_map_info(&lines);

    let starting_nodes = map_info.map.keys().filter(|key| key.ends_with("A")).map(|x| x.clone()).collect::<Vec<String>>();
    // print current
    starting_nodes.iter().for_each(
        |node| {
            println!("{}", node);
        }
    );
    println!();
    let runners = starting_nodes.iter().map(
        |node| {
            get_runner(node, &map_info)
        }
    ).collect::<Vec<Runner>>();
    runners.iter().for_each(
        |runner| {
            println!("{} {} {}", runner.first_end_value, runner.first_end_steps, runner.cycle_length);
            runner.other_ends_at.iter().for_each(
                |other_end| {
                    println!("{}", other_end);
                }
            );
        }
    );
    let lcm_of_cycles = runners.iter().fold(1, |acc, runner| lcm(acc, runner.cycle_length));

    println!();

    println!("{}", lcm_of_cycles);
}

fn get_map_info(lines: &Vec<&str>) -> MapInfo {
    MapInfo {
        map: get_map(lines),
        seq: lines[0].to_string(),
    }
}


fn is_end_all(nodes: &Vec<String>) -> bool {
    nodes.iter().all(|node| is_end(node))
}

fn is_end(node: &String) -> bool {
    node.ends_with("Z")
}

fn get_map(lines: &Vec<&str>) -> HashMap<String, (String, String)> {
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