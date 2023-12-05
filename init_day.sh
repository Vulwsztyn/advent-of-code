#!/bin/env bash
cargo new day$1
cp ./template.rs ./day$1/src/main.rs
cat ./dependencies.toml >> ./day$1/Cargo.toml
cd day$1
cargo build