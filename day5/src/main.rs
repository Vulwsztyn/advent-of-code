use std::env;
use std::fs;
use onig::*;

struct Mapping {
    destination_range_start: u128,
    source_range_start: u128,
    length: u128,
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

fn line_to_entry(line: &str) -> Option<Mapping> {
    let three_numbers_regex = Regex::new(r"(\d+) (\d+) (\d+)").unwrap();
    let captures = three_numbers_regex.captures(line);
    if captures.is_none() {
        return None;
    }
    let nums_as_str = captures.unwrap();
    let nums_as_vec = nums_as_str.iter_pos().skip(1).map(
        |x| {
            let (start, end) = x.unwrap();
            line[start..end].parse::<u128>().unwrap()
        }
    ).collect::<Vec<u128>>();
    // println!("");
    Some(Mapping {
        destination_range_start: *nums_as_vec.get(0).unwrap(),
        source_range_start: *nums_as_vec.get(1).unwrap(),
        length: *nums_as_vec.get(2).unwrap(),
    })        
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);


    let lines = contents.lines().collect::<Vec<&str>>();
    let seeds = get_seeds(&lines);


    let list_of_maps = get_list_of_maps(lines);
    seeds.iter().for_each(|x| print!("{} ", x));
    println!();
    let mapped = seeds.iter().map(|&seed|
        list_of_maps.iter().fold(
            seed,
            |acc, map| {
                apply_map(acc, map)
            },
        )
    ).collect::<Vec<u128>>();
    mapped.iter().for_each(|&x| print!("{} ", x));
    println!();
    let minimum = mapped.iter().min().unwrap();
    println!("Minimum: {}", minimum);
}

fn apply_map(seed: u128, mappings: &Vec<Mapping>) -> u128 {
    let maybe_mapping = mappings.iter().find(|x| x.source_range_start <= seed && seed < x.source_range_start + x.length);
    if maybe_mapping.is_none() {
        return seed;
    }
    let mapping = maybe_mapping.unwrap();
    let offset = seed - mapping.source_range_start;
    mapping.destination_range_start + offset
}

fn get_list_of_maps(lines: Vec<&str>) -> Vec<Vec<Mapping>> {
    let map_regex = Regex::new(r".*map\:\s*$").unwrap();



    let mut list_of_maps: Vec<Vec<Mapping>> = vec![];
    let mut current_map_index = 0;


    let mut not_yet_maps = true;
    for (_line_i, &line) in lines.iter().enumerate() {
        let line_is_header = map_regex.is_match(line);
        if line_is_header {
            current_map_index += 1;
            if not_yet_maps {
                not_yet_maps = false;
                current_map_index = 0;
            }
            list_of_maps.push(vec![])
        }
        if not_yet_maps || line_is_header {
            continue;
        }
        let maybe_entry = line_to_entry(line);
        if maybe_entry.is_none() {
            continue;
        }
        let entry = maybe_entry.unwrap();
        list_of_maps.get_mut(current_map_index).unwrap().push(entry);
    }
    list_of_maps
}

fn get_seeds(lines: &Vec<&str>) -> Vec<u128> {
    let number_regex = Regex::new(r"\d+").unwrap();

    let line0 = lines.get(0).unwrap();
    let seeds: Vec<u128> = number_regex
        .find_iter(line0)
        .map(|x| line0[x.0..x.1].parse::<u128>().unwrap())
        .collect::<Vec<u128>>();
    seeds
}
