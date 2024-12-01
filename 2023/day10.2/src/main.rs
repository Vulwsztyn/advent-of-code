use std::collections::{HashMap, HashSet};
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

#[derive(Eq, PartialEq, Debug, Copy, Clone)]
enum Corner {
    TopLeft,
    TopRight,
    BottomLeft,
    BottomRight,
}

type Coord = (usize, usize);

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

fn shape_to_group_of_corners(shape: char) -> (Vec<Corner>, Vec<Corner>) {
    match shape {
        'L' => (vec![Corner::TopLeft, Corner::BottomLeft, Corner::BottomRight], vec![Corner::TopRight]),
        'J' => (vec![Corner::TopRight, Corner::BottomLeft, Corner::BottomRight], vec![Corner::TopLeft]),
        '7' => (vec![Corner::TopLeft, Corner::TopRight, Corner::BottomRight], vec![Corner::BottomLeft]),
        'F' => (vec![Corner::TopLeft, Corner::TopRight, Corner::BottomLeft], vec![Corner::BottomRight]),
        '|' => (vec![Corner::TopLeft, Corner::BottomLeft], vec![Corner::TopRight, Corner::BottomRight]),
        '-' => (vec![Corner::TopLeft, Corner::TopRight], vec![Corner::BottomLeft, Corner::BottomRight]),
        _ => panic!("Shape {:?} does not have corners", shape),
    }
}

fn corner_and_shape_to_group(corner: Corner, shape: char) -> Vec<Corner> {
    let (group1, group2) = shape_to_group_of_corners(shape);
    if group2.contains(&corner) {
        return group2;
    }
    return group1;
}

fn next_coords((x, y): Coord, direction: Direction) -> Coord {
    match direction {
        Direction::Up => (x, y - 1),
        Direction::Down => (x, y + 1),
        Direction::Left => (x - 1, y),
        Direction::Right => (x + 1, y),
    }
}

fn corner_to_next_direction_and_corner(corner: Corner) -> ((Direction, Corner), (Direction, Corner)) {
    match corner {
        Corner::TopLeft => ((Direction::Left, Corner::TopRight), (Direction::Up, Corner::BottomLeft)),
        Corner::TopRight => ((Direction::Right, Corner::TopLeft), (Direction::Up, Corner::BottomRight)),
        Corner::BottomLeft => ((Direction::Left, Corner::BottomRight), (Direction::Down, Corner::TopLeft)),
        Corner::BottomRight => ((Direction::Right, Corner::BottomLeft), (Direction::Down, Corner::TopRight)),
    }
}

fn next_coords_unsigned((x, y): Coord, direction: Direction) -> (i32, i32) {
    match direction {
        Direction::Up => (x as i32, (y as i32 - 1)),
        Direction::Down => (x as i32, (y as i32 + 1)),
        Direction::Left => ((x as i32 - 1), y as i32),
        Direction::Right => ((x as i32 + 1), y as i32),
    }
}

fn at_coords(map: &Vec<&str>, (x, y): Coord) -> char {
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

fn find_start(map: &Vec<&str>) -> Coord {
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
        .map(|&direction| (direction, next_coords_unsigned(start, direction)))
        .filter(|&(_, (x, y))| x < lines[0].len() as i32 && y < lines.len() as i32 && x >= 0 && y >= 0)
        .map(|(direction, (x, y))| (direction, (x as usize, y as usize)))
        .filter(|&(direction, coords)| {
            is_connected(
                at_coords(&lines, coords),
                opposite_direction(direction),
            )
        })
        .collect::<Vec<(Direction, Coord)>>();
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
    let mut pipes: HashMap<Coord, char> = HashMap::new();
    let mut top_left = start;
    pipes.insert(start, start_pipe);
    pipes.insert(current_coords, at_coords(&lines, current_coords));
    while (next_coords(current_coords, current_direction) != start) {
        current_coords = next_coords(current_coords, current_direction);
        let current_pipe = at_coords(&lines, current_coords);
        current_direction = next_direction(current_pipe, current_direction);
        pipes.insert(current_coords, current_pipe);
        if current_coords.0 < top_left.0 || (current_coords.0 == top_left.0 && current_coords.1 < top_left.1) {
            top_left = current_coords;
        }
        println!("Current coords: {:?}, current pipe: {:?}, current direction: {:?}", current_coords, current_pipe, current_direction);
    }
    let mut visited: HashSet<Coord> = HashSet::new();
    let mut has_spread: HashSet<Coord> = HashSet::new();
    let mut inside_count = 0;
    println!("Pipes: {:?}", pipes);
    println!("Top left: {:?}", top_left);
    let mut stack: Vec<(Coord, Corner)> = Vec::new();
    stack.push((top_left, Corner::BottomRight));
    while (stack.len() > 0) {
        let (current_coords, current_corner) = stack.pop().unwrap();
        println!("Current coords: {:?}, current corner: {:?}", current_coords, current_corner);
        if !visited.contains(&current_coords) {
            visited.insert(current_coords);
            let is_pipe = pipes.contains_key(&current_coords);
            if !is_pipe {
                inside_count += 1;
                println!("Inside count: {:?}", inside_count);
            }
            let corner_group = if is_pipe { corner_and_shape_to_group(current_corner, *pipes.get(&current_coords).unwrap()) } else { vec![Corner::TopLeft, Corner::TopRight, Corner::BottomLeft, Corner::BottomRight] };
            for corner in corner_group {
                let ((dir1, corner1), (dir2, corner2)) = corner_to_next_direction_and_corner(corner);
                let next_coords1 = next_coords(current_coords, dir1);
                let next_coords2 = next_coords(current_coords, dir2);
                stack.push((next_coords1, corner1));
                stack.push((next_coords2, corner2));
                println!("Corner: {:?}", corner);
                println!("Next coords 1: {:?}, corner 1: {:?}, dir1: {:?}", next_coords1, corner1, dir1);
                println!("Next coords 2: {:?}, corner 2: {:?}, dir2: {:?}", next_coords2, corner2, dir2);
            }
            println!();
        }
    }
    let pipes_unvisited = pipes.iter().filter(|(coords, _)| !visited.contains(coords)).collect::<HashMap<&Coord, &char>>();
    println!("Inside count: {:?}", inside_count);
    println!("Pipes unvisited: {:?}", pipes_unvisited);
}
