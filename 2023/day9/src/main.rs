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

fn line_to_numbers(line: &str) -> Vec<i64> {
    line.split_whitespace().map(
        |number| {
            number.parse::<i64>().unwrap()
        }
    ).collect::<Vec<i64>>()
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
    let mut sum: i64 = 0;
    lines.iter().for_each(
        |line| {
            let mut vectors: Vec<Vec<i64>> = vec![];
            vectors.push(line_to_numbers(line));
            let mut last: &Vec<i64> = vectors.last().unwrap();
            while !last.iter().all(|&x| x == 0) {
                let mut new_vec = vec![];
                for (i, number) in last.iter().enumerate() {
                    if i == last.len() -1 {
                        break;
                    }
                    new_vec.push(last[i+1]-number);
                }
                vectors.push(new_vec);
                last = vectors.last().unwrap();
            }
            // vectors.last().unwrap().push(0);
            let mut acc: i64 = 0;
            let mut index = vectors.len() - 2;
            while true {
                let current_last = vectors[index].last().unwrap();
                acc += current_last;
                println!("{} {} {}", index, current_last, acc);

                if index == 0 {
                    break;
                }
                index -= 1;
            }
            sum += acc;
            println!("Sum: {}", sum);
        }
    );
    println!("Sum: {}", sum);
}
