use std::env;
use std::fs;
use std::iter::zip;
use std::time::Instant;
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
    let start = Instant::now();

    let [mut left, mut right] = lines.iter().fold([vec![],vec![]],
                                                  |mut acc: [Vec<u32>; 2], line| {
            let split = line.split(" ").filter(|x| x.len() > 0).map(|x| x.parse::<u32>().unwrap()).collect::<Vec<u32>>();
            println!("{:?}", split);
            acc[0].push(split[0]);
            acc[1].push(split[1]);
            acc
        }
    );
    left.sort();
    right.sort();
    let mut sum: u64 = 0;
    let mut index_right: usize = 0;
    for v in left.iter() {
        while index_right< right.len() && right[index_right] < *v {

            index_right += 1;

        }
        let mut to_deduct = 0;
        if index_right >= right.len() {break;}
        while right[index_right] == *v {
            sum += *v as u64;
            index_right += 1;
            to_deduct += 1;
            if index_right >= right.len() {break;}
        }
        index_right -= to_deduct;
    }

    let duration = start.elapsed();
    println!("Time elapsed: {:?}", duration);
    println!("Sum: {}", sum);
}
