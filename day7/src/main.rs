use std::env;
use std::fs;
// use onig::*;
use std::collections::HashMap;
use core::cmp::Ordering;
#[derive(PartialOrd, PartialEq, Debug, Eq, Ord)]
enum Type {
    One,
    Pair,
    TwoPair,
    Three,
    House,
    Four,
    Five,
}

struct PartialHand {
    cards: String,
    bid: u128,
}
#[derive(Debug, Eq, PartialEq, Ord)]
struct Hand {
    cards: String,
    bid: u128,
    hand_type: Type,
    card_values: Vec<u8>,
}

impl PartialOrd for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        if self.hand_type == other.hand_type {
            return self.card_values.partial_cmp(&other.card_values);
        }
        self.hand_type.partial_cmp(&other.hand_type)
    }
}

fn card_to_value(card: char) -> u8 {
    match card {
        'A' => 14,
        'K' => 13,
        'Q' => 12,
        'J' => 11,
        'T' => 10,
        _ => card.to_digit(10).unwrap() as u8,
    }
}

fn hand_to_type(hand: &str) -> Type {
    let counts = hand.chars().fold(
        HashMap::new(),
        |mut counts, card| {
            let count = counts.entry(card).or_insert(0);
            *count += 1;
            counts
        }
    );

    let num_unique_cards = counts.len();

    match num_unique_cards {
        1 => Type::Five,
        2 => {
            for (_, value) in &counts {
                if *value == 4 || *value == 1 {
                    return Type::Four;
                }
                return Type::House;
            }
            panic!("Should not have gotten here")
        }
        3 => {
            for (_, value) in &counts {
                if *value == 1 {
                    continue;
                }
                if *value == 3 {
                    return Type::Three;
                }
                return Type::TwoPair;
            }
            panic!("Should not have gotten here")
        }
        4 => Type::Pair,
        5 => Type::One,
        _ => panic!("Invalid number of cards"),
    }
}

fn hand_from_partial(partial_hand: &PartialHand) -> Hand {
    let hand_type = hand_to_type(&partial_hand.cards);
    let card_values = partial_hand.cards.chars().map(card_to_value).collect::<Vec<u8>>();
    Hand {
        cards: partial_hand.cards.clone(),
        bid: partial_hand.bid,
        hand_type,
        card_values,
    }
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
    let partial_hands = lines.iter().map(
        |line| {
            let mut split = line.split_whitespace();
            let cards = split.next().unwrap();
            let bid = split.next().unwrap().parse::<u128>().unwrap();
            PartialHand {
                cards: cards.to_string(),
                bid,
            }
        }
    ).collect::<Vec<PartialHand>>();
    let mut hands = partial_hands.iter().map(hand_from_partial).collect::<Vec<Hand>>();
    hands.sort();
    hands.iter().for_each(
        |hand| {
            println!("{:?}", hand);
        }
    );
    let values = hands.iter().enumerate().map(
        |(i, hand)| {
            let value = hand.bid * (i + 1) as u128;
            println!("{} {} {}", i, hand.bid, value);
            value
        }
    ).collect::<Vec<u128>>();
    let sum = values.iter().sum::<u128>();
    println!("{}", sum);
}
