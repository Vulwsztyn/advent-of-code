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

    let number_regex = Regex::new(r"\d+").unwrap();
    let map_regex = Regex::new(r".*map\:\s*$").unwrap();
    let three_numbers_regex = Regex::new(r"(\d+) (\d+) (\d+)").unwrap();

    let lines = contents.lines().collect::<Vec<&str>>();
    let mut list_of_maps: Vec<Vec<(i32,i32,i32)>> = vec![];
    let mut current_map_index = 0;

    let line0 = lines.get(0).unwrap();
    let seeds: Vec<i32> = number_regex
        .find_iter(line0)
        .map(|x| line0[x.0..x.1].parse::<i32>().unwrap())
        .collect::<Vec<i32>>();
    
    let mut not_yet_maps = true;
    for (_line_i, line) in lines.iter().enumerate() {
        let line_is_header= map_regex.is_match(line);
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
        let captures = three_numbers_regex.captures(line);
        if captures.is_none() { continue; }
        let nums_as_str = captures.unwrap();
        let nums_as_vec = nums_as_str.iter().map(
            |x| x.unwrap().parse::<i32>().unwrap()
        ).collect::<Vec<i32>>();
        let nums: (i32,i32,i32) = (
            *nums_as_vec.get(0).unwrap(),
            *nums_as_vec.get(1).unwrap(),
            *nums_as_vec.get(2).unwrap()
        );
        list_of_maps.get(current_map_index).unwrap().push(*&nums);
    }
    seeds.iter().for_each(|x| print!("{}", x));
    println!()
}
