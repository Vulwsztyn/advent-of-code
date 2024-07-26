use std::env;
use std::fs;
// use onig::*;

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
    let mut result = 0;

    for line in lines.iter() {
        // println!("line: {}", line);
        let mut line_result = 0;
        let split = line.split_whitespace().collect::<Vec<&str>>();
        let map = split[0];
        let expected_str = split[1];
        let expected = expected_str.split(',').map(|x| x.parse::<i32>().unwrap()).collect::<Vec<i32>>();
        // println!("map: {}", map);
        // println!("expected: {:?}", expected);
        let mut stack: Vec<String> = Vec::new();
        stack.push(map.to_string());
        while (stack.len()>0) {
            // println!("stack: {:?}", stack);
            let current = stack.pop().unwrap();
            let first_unknown = current.find('?');
            // println!("first_unknown: {:?}", first_unknown);
            if first_unknown.is_none() {
                let consecutive_hashes = current.split('.').filter(|x| x.len()>0).map(|x| x.len() as i32).collect::<Vec<i32>>();
                // println!("consecutive_hashes: {:?}", consecutive_hashes);
                if consecutive_hashes.len() == expected.len() {
                    let mut valid = true;
                    for i in 0..consecutive_hashes.len() {
                        if consecutive_hashes[i] != expected[i] {
                            valid = false;
                            break;
                        }
                    }
                    if valid {
                        line_result += 1;
                    }
                }
                continue;
            }
            let version1= current.replacen("?", "#", 1);
            let version2= current.replacen("?", ".", 1);
            stack.push(version1);
            stack.push(version2);
        }
        // println!("line: {} result: {}", line, line_result);
        result += line_result;
    }
    println!("result: {}", result);
}
