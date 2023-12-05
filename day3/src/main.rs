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
fn has_symbol_in_neighbourhood(lines: *const Vec<&str>, max_x: usize, max_y: usize, x1: usize, x2: usize, y: usize) -> bool {
    let non_symbol_regex = Regex::new(r"[\d\.]").unwrap();
    let is_symbol = |x: usize,y:usize| -> bool {
        println!("{} {}", x, y);
        let line = unsafe { &*lines }.get(y).unwrap();
        let symbol = non_symbol_regex.find(&line[x..x+1]);
        symbol.is_none()
    };
    let range_start = if x1>0 {x1-1} else {x1};
    let range_end = if x2<max_x {x2+1} else {x2};
    println!("{} {} {} {} {} {} {}", max_x, max_y, x1, x2, y, range_start, range_end);

    // TODO: make better
    let mut ys: Vec<usize> = vec![];
    if y>0 {
        ys.push(y-1);
    }
    if y<max_y {
        ys.push(y+1);
    }

    for y in ys {
        for x in range_start..range_end+1 {
            if is_symbol(x, y) {
                return true;
            }
        }
    }
    if x1>0 && is_symbol(x1-1, y) {
        return true;
    }
    if x2<max_x && is_symbol(x2+1, y) {
        return true;
    }
    false
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let lines = contents.lines().collect::<Vec<&str>>();
    let number_regex = Regex::new(r"\d+").unwrap();
    let max_x = lines[0].len()-1;
    let max_y = lines.len()-1;
    let has_symbol = |x1,x2,y| has_symbol_in_neighbourhood(&lines, max_x, max_y, x1, x2, y);
    let mut sum = 0;
    lines.iter().enumerate().for_each(
        |(y, line)| {
            let numbers = number_regex
                .find_iter(line)
                .filter(
                    |(x1, x2)| has_symbol(*x1, *x2-1, y)
                )
                .map(|x| line.get(x.0..x.1).unwrap().parse::<i32>().unwrap())
                .collect::<Vec<i32>>();
            println!("Line {}: {} {:?}", y, line, numbers);
            sum += numbers.iter().sum::<i32>();
        }
    );
    println!("Sum: {}", sum);
}
