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
    let number_regex = Regex::new(r"\d+").unwrap();
    let mut sum = 0;
    lines.iter().enumerate().for_each(
        |(line_i, line)| {
            println!("{} {}", line_i, line);
            let split = line.split('|').collect::<Vec<&str>>();
            let left_with_header = split.get(0).unwrap();
            let left_split = left_with_header.split(':').collect::<Vec<&str>>();
            let left = left_split.get(1).unwrap();
            let right = split.get(1).unwrap();

            println!(" left: {}", left);
            println!("right: {}", right);
            
            let part_to_nums = |part| number_regex
                .find_iter(part)
                .map(|(x,x2)| {
                    part[x..x2].parse::<i32>().unwrap()
                    }
                )
                .collect::<Vec<i32>>();

            let left_nums = part_to_nums(left);
            let right_nums = part_to_nums(right);
            // left_nums.iter().for_each(|x| print!("{} ", x));
            // println!("");
            // right_nums.iter().for_each(|x| print!("{} ", x));
            // println!("");
            let in_both = right_nums
                .iter()
                .filter(|x|
                    left_nums.contains(x)
                ).collect::<Vec<&i32>>();
            in_both.iter().for_each(|x| print!("{} ", x));
            println!("");
            if in_both.len()==0 {
                return;
            }
            let mut additive = 1;
            let pow = in_both.len()-1;
            for _ in 0..pow {
                additive *= 2;
            }
            println!("{}", additive);
            sum+=additive;
        }
    );
    println!("{}", sum);
}
