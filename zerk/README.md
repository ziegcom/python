# Zerk, the Great Underground Umpire

This was thrown together as an excuse to learn about Python classes and regex.  Be nice :-)

# Version History

- 2017-03-31
    - supports Py2.6/2.7/3.x
    - general improvements

- 2017-03-30 
    - first runnable version
    - created GitHub project
    - added color, more monsters/items, etc

- 2017-03-29 - draft Board.py, main.py

# Backlog

## 1.0

- needs "use tool"
- needs "kill monster with the tool"
- needs a goal / exit-condition
- serialize world parameters out of main() into world.json
- flying/climbing monsters should be able to pass rubble
- needs combat system (hit points, hit dice, equipping weapons etc)
- player should have weight limit

## 2.0

- replace Board with World, exchanging the current positional grid with
  a connected graph of nodes ("rooms")

## Complete

- ~~implicit subject~~
- ~~killing Thessalhydra makes you the monster?~~
- ~~monsters stupidly box themselves into corner~~
- ~~occasionally monsters don't appear on initial debug screen~~
- ~~colorize map~~
- ~~add more monsters / items~~
- ~~add wait/sleep~~
- ~~research Python 2.6/2.7/3.x compatibility options~~
