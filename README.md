# poker_ver1

## Poker Game (Terminal Version)

A simple command-line Texas Hold'em poker game written in Python.

## Features
- Heads-up: Player vs Bot
- Bot chooses a random valid action each turn (check / call / raise / fold)
- 52-card deck using a `Card` class, shuffled automatically each hand
- Texas Hold'em flow: pre-flop → flop → turn → river → showdown
- Betting system with blinds, pot, calls, and fixed-size raises
- 7-card hand evaluation (2 hole cards + 5 community cards) supporting:
  - Royal Flush, Straight Flush, Four of a Kind, Full House
  - Flush, Straight, Three of a Kind, Two Pair, One Pair, High Card
- Simple chip stack tracking for both players
- All interaction happens in the terminal via text input

## How to Run

```text
python game.py

This project was developed with the assistance of generative AI tools.

Originally, I had only worked with Python in a procedural style. Through my research, I was introduced to object-oriented languages, and to better understand how classes are used, I created this project using Python with a class-based design.
