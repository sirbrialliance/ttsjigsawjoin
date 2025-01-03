# Jigsaw Join Family Edition for Tabletop Simulator

This is a branch of [Canonelis/ttsjiggys](https://github.com/Canonelis/ttsjigsawjoin) altered for a more family/friends approach to puzzle solving with added features.

## Notable Changes

- No piece movement limitation. (The base mod limits you to only moving one more piece than your total score.)
- Useability improvements to initial puzzle piece positions/rotations.
- Context actions for arranging a selection of pieces in a square, a row, or to a local grid for easy manipulation and handling of pieces. You can also arrange square puzzle pieces based on their general shape (e.g. all tabs in, 3 in 1 out, etc.).
- Cheats (see below).
- No greeting screen.
- Right click the puzzle board and choose "Change table color" to quickly change the table background color.
- Pieces have been regenerated with higher accuracy UV data so the image on pieces isn't distorted when inspected closely.
- The starting puzzle board has been shrunken and moved to the side.

## Cheats

A handful of accessability/cheat features have been added to help make more advanced puzzles more approachable for unskilled players who may be playing with more skilled players.

- Right click the puzzle board and choose...
	- "Cheat: Select Edges" to select all free/unconnected edge pieces. Note that TTS itself has a selection limit, so this may not select all the pieces if there are too many. (Try using it a few times, or make process on the known edges and check again.)
	- "Cheat: Gather Pieces" to make a "mini puzzle" (a small subset of the larger puzzle) for a less skilled player to work on. Start by placing one puzzle piece on the puzzle board, then right-click the puzzle board and select this option. It will ask you for a distance; choose and confirm. If nothing happens, try again. (TTS seems to often not give me the result the first time you use the dialog.) All pieces within the given range of the given piece will be moved to the center of the game area. You now have a subset "circle" of puzzle to work on.
- Right click a puzzle piece (possibly a selection of pieces) and choose...
	- "Cheat: Rotate Right" to correctly orient all pieces as they appear in the final puzzle solution.
	- "Cheat: Puzzle Order" is basically the same as "Arrange: Square", but orders pieces based on their order in the puzzle (rows first, starting from the top-left). Note that items arrange on the same row may not be on the same row in the puzzle.

Use of a cheat is announced to all players.

# Installation

## Playing

toto: I need to upload this to the Steam Workshop.

## Building Code

See [dist/README.md](dist/README.md)

## Generating the pieces

Not well documented, dig around in `src/making pieces`. You'll need to fiddle with hardcoded paths and target actions. Note that you need to use the locally included version of `py2d`, not the normal version available through `pip`.

`generate_square_pieces.py` makes the square pieces, `create_pieces.py` makes the hexagonal ones. Updated pieces need to be hosted somewhere and `PUZZLE_URL` in the main Lua script needs to changed (before generating a puzzle).

`src/blender`, I believe, is an older, unmaintained method for generating the pieces.
