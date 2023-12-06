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

fn gear_values(lines: *const Vec<&str>, numbers: *const Vec<Vec<(usize, usize, usize)>>, max_x: usize, max_y: usize, x: usize, y: usize) -> i32 {
    println!("{} {} {} {} {} {} {}", max_x, max_y, x, y, 0, 0, 0 );
    let yi:i32 = y.try_into().unwrap();
    let xi:i32 = x.try_into().unwrap();
    let y_min= if y>0 {y-1} else {0};
    let x_min = if x>0 {x-1} else {0};
    let mut neighbours: Vec<(usize, usize, usize)> = vec![];
    for i in y_min..y+2 {
        unsafe {&*numbers}.get(i).unwrap().iter().for_each(
            |(y,x1,x2)| 
                if x_min<=*x2 && x+1>=*x1 {
                    println!("{} {} {}", y, x1, x2);
                    neighbours.push((*y,*x1,*x2));
                }
        );
    }
    if neighbours.len() != 2 {
        return 0;
    }
    // let line = unsafe { &*lines }.get(y).unwrap();
    // let symbol = non_symbol_regex.find(&line[x..x+1]);
    let mut val = 1;
    neighbours.iter().for_each(
        |(y,x1,x2)| {
        let line = unsafe { &*lines }.get(*y).unwrap();
        let val_as_str = &line[*x1..*x2+1];
        let val_as_i = val_as_str.parse::<i32>().unwrap();
        val*=val_as_i;
        }
    );
    val
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let lines = contents.lines().collect::<Vec<&str>>();
    let asterisk_regex = Regex::new(r"\*").unwrap();
    let number_regex = Regex::new(r"\d+").unwrap();
    let max_x = lines[0].len()-1;
    let max_y = lines.len()-1;
    let mut sum = 0;
    let numbers_in_lines = lines.iter().enumerate().map(
        |(y, line)| {
            return number_regex
                .find_iter(line)
                .map(|(x1,x2)| (y,x1,x2-1))
                .collect::<Vec<(usize, usize, usize)>>();
        }
    ).collect::<Vec<Vec<(usize, usize, usize)>>>();
    let gear_value = |x,y| gear_values(&lines, &numbers_in_lines, max_x, max_y, x, y);

    numbers_in_lines.iter().for_each(
        |line| line.iter().for_each(|(y,x1,x2)| println!("{} {} {}", y, x1, x2))
    );
    lines.iter().enumerate().for_each(
        |(y, line)| {
            let numbers = asterisk_regex
                .find_iter(line)
                .map(
                    |(x1, _)| gear_value(x1, y)
                )
                .collect::<Vec<i32>>();
            println!("Line {}: {} {:?}", y, line, numbers);
            sum += numbers.iter().sum::<i32>();
        }
    );
    println!("Sum: {}", sum);
}
