#!/bin/env bash
cargo new day
cp ./template.rs ./day/src/main.rs
cat ./dependencies.toml >> ./day/Cargo.toml
cp -r ./2023/day01.1/.idea ./day
touch ./day/data.txt
touch ./day/test.txt
mv day 2024/day$1
cd 2024/day$1
cargo build
