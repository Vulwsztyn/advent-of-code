#!/bin/env bash
cargo new day
cp ./template.rs ./day/src/main.rs
cat ./dependencies.toml >> ./day/Cargo.toml
cp -r ./day6/.idea ./day
mv day day$1
cd day$1
cargo build