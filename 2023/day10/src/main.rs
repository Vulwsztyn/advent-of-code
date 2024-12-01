use std::collections::HashMap;
use std::env;
use std::fs;
// use onig::*;

// | is a vertical pipe connecting north and south.
// - is a horizontal pipe connecting east and west.
// L is a 90-degree bend connecting north and east.
// J is a 90-degree bend connecting north and west.
// 7 is a 90-degree bend connecting south and west.
// F is a 90-degree bend connecting south and east.
// . is ground; there is no pipe in this tile.
// S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

#[derive(Eq, PartialEq, Debug, Copy, Clone)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

fn opposite_direction(direction: Direction) -> Direction {
    match direction {
        Direction::Up => Direction::Down,
        Direction::Down => Direction::Up,
        Direction::Left => Direction::Right,
        Direction::Right => Direction::Left,
    }
}

fn get_connections() -> HashMap<char, (Direction, Direction)> {
    return HashMap::from([
        ('|', (Direction::Up, Direction::Down)),
        ('-', (Direction::Left, Direction::Right)),
        ('L', (Direction::Up, Direction::Right)),
        ('J', (Direction::Up, Direction::Left)),
        ('7', (Direction::Down, Direction::Left)),
        ('F', (Direction::Down, Direction::Right)),
    ]);
}

fn next_coords((x, y): (usize, usize), direction: Direction) -> (usize, usize) {
    match direction {
        Direction::Up => (x, y - 1),
        Direction::Down => (x, y + 1),
        Direction::Left => (x - 1, y),
        Direction::Right => (x + 1, y),
    }
}

fn at_coords(map: &Vec<&str>, (x, y): (usize, usize)) -> char {
    return map[y].chars().nth(x).unwrap();
}

fn is_connected(pipe: char, direction: Direction) -> bool {
    let connections = get_connections();
    let directions = connections.get(&pipe);
    if directions.is_none() {
        return false;
    }
    let (first, second) = directions.unwrap();
    return *first == direction || *second == direction;
}

fn get_pipe_shape_from_directions(direction1: Direction, direction2: Direction) -> char {
    let connections = get_connections();
    for (pipe, (d1, d2)) in connections.iter() {
        if (*d1 == direction1 && *d2 == direction2) || (*d1 == direction2 && *d2 == direction1) {
            return *pipe;
        }
    }
    panic!(
        "No pipe shape found for directions {:?} and {:?}",
        direction1, direction2
    );
}

fn next_direction(pipe: char, current_direction: Direction) -> Direction {
    let connections = get_connections();
    let (d1, d2) = connections.get(&pipe).unwrap();
    let incoming_direction = opposite_direction(current_direction);
    if *d1 == incoming_direction {
        return *d2;
    }
    if *d2 == incoming_direction {
        return *d1;
    }
    panic!(
        "Pipe {:?} does not connect to direction {:?}",
        pipe, current_direction
    );
}

fn find_start(map: &Vec<&str>) -> (usize, usize) {
    for (y, line) in map.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == 'S' {
                return (x, y);
            }
        }
    }
    panic!("No start found");
}

fn get_file_path() -> String {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    file_path.to_string()
}

fn get_file_contents(file_path: String) -> String {
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    contents
}

fn main() {
    let file_path = get_file_path();

    println!("Filename: {}", file_path);

    let contents = get_file_contents(file_path);
    let lines = contents.lines().collect::<Vec<&str>>();
    let start = find_start(&lines);
    let start_connections = vec![
        Direction::Up,
        Direction::Down,
        Direction::Left,
        Direction::Right,
    ]
    .iter()
    .map(|&direction| (direction, next_coords(start, direction)))
    .filter(|&(_, (x, y))| x < lines[0].len() && y < lines.len() && x >= 0 && y >= 0)
    .filter(|&(direction, coords)| {
        is_connected(
            at_coords(&lines, coords),
            opposite_direction(direction),
        )
    })
    .collect::<Vec<(Direction, (usize, usize))>>();
    if start_connections.len() != 2 {
        panic!(
            "Expected 2 start_connections, got {:?}. Start_connections: {:?}",
            start_connections.len(),
            start_connections
        );
    }
    let start_pipe = get_pipe_shape_from_directions(start_connections[0].0, start_connections[1].0);
    println!("Start: {:?}", start);
    println!("Start pipe: {:?}", start_pipe);
    let mut current_coords = next_coords(start, start_connections[0].0);
    let mut current_direction = next_direction(at_coords(&lines, current_coords), start_connections[0].0);
    let mut current_distance = 1;
    while (next_coords(current_coords, current_direction) != start) {
        current_distance += 1;
        current_coords = next_coords(current_coords, current_direction);
        let current_pipe = at_coords(&lines, current_coords);
        current_direction = next_direction(current_pipe, current_direction);
        println!("Current coords: {:?}, current pipe: {:?}, current direction: {:?}", current_coords, current_pipe, current_direction);
    }
    println!("Distance: {:?}", (current_distance+1)/2);

}
