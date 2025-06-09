# Jigsaw Join Family Edition for Tabletop Simulator

This is a custom game for Tabletop Simulator for putting together jigsaw puzzles with friends and family. Unlike TTS's built-in jigsaw mode, pieces stick to each other when placed correctly allowing for more natural puzzle-solving experience. Additionally, there's a ton of other useful and quality-of-life features.

This is a branch of [Canonelis/ttsjiggys](https://github.com/Canonelis/ttsjigsawjoin) altered for a more family/friends approach to puzzle solving with additional updates and features.

## Playing

- Subscribe to the [game in the Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3493402409).
- Load the game like any other from the Steam Workshop.
- Hit "New Puzzle", paste in a URL, choose your options, and hit "Continue" to get started!

## Notable Changes

Notable changes from standard Jigsaw Join include:

- No piece movement limitation beyond TTS's selection limit. No greeting screen.
- Useability improvements to initial puzzle piece positions/rotations. Also, the starting puzzle board has been shrunken and moved to the side.
- Context actions for arranging a selection of pieces in various ways, including based on how each piece's tabs/nubs are arranged (see below).
- Cheats for making puzzle-solving more accessible for less-advanced players (see below).
- Pieces have been regenerated with higher accuracy UV data so the image on pieces isn't distorted when inspected closely.
- Faster piece joining.
- The URL for the current picture is available to select and copy from the scoreboard for display on another monitor if desired.
- New cursed pieces set. You didn't actually need the puzzle to have edges, did you?
- You can change the table color (see below).
- Aspect ratio calculator (see below).

## Feature Details

### Arrange Options

Right click a piece or a selection of pieces for some helpful arrangement options:

- "Arrange: Square" arranges the pieces in a roughly square shape. It also tries to be somewhat smart about larger piece islands that you include.
- "Arrange: Rectangle" is like "Arrange: Square", but arranges things in a wider rectangle.
- "Arrange: By Shape" will group together individual pieces based on the edges of each piece. (Namely, which sides have protruding tabs, which sides accept those tabs, and which sides are straight puzzle edge pieces.) Each row is a group with the same arrangement.
- "Arr & Rot: By Shape" (arrange and rotate by shape) does the same, but additionally will rotate the pieces so there are fewer groups overall. Additionally, it puts all the puzzle edge pieces in a group together.
- "Arrange: Left/Right" does the same as "Arrange: By Shape", but only considers the left and right edges. If you want to do this by top/bottom edges instead, rotate the pieces 90° first, run the command, then rotate them back.
- "Align: Local Grid" tries to arrange the selection so the pieces are grid-aligned with each other. It also tries to avoid putting pieces on top of each other, including larger clusters of pieces, so things may still move around more than a small bit.

Note the some of these options are not available for hexagonal puzzles.

### Cheats

A handful of accessability/cheat features have been added to help make more advanced puzzles more approachable for unskilled players playing with more skilled players.

- Right click the puzzle board and choose...
	- "Cheat: Gather Edges" to move all the free/unconnected edge pieces over the puzzle board.
	- "Cheat: Gather Pieces" to make a "mini puzzle" (a small subset of the larger puzzle) for a less skilled player to work on. Start by placing one puzzle piece on the puzzle board, then right-click the puzzle board and select this option. It will ask you for a distance; choose and confirm. If nothing happens (Tabletop bug), try again. All pieces within the given range of the given piece will be moved to the center of the game area. You now have a subset "circle" of puzzle to work on. Then, begin apologizing for all the pieces you took that others were working on.
- Right click a puzzle piece (or a selection of pieces) and choose...
	- "Cheat: Rotate Solved" to correctly orient all pieces as they appear in the final puzzle solution.
	- "Cheat: Puzzle Order" to arrange pieces based on their order in the puzzle (rows first, starting from the top-left). Note that items arranged on the same row may not be on the same row in the puzzle. Doesn't handle clusters of pieces well.

Decide with your group beforehand when using cheats is acceptable. Use of a cheat is announced to all players.

### Misc

- Right click the puzzle board and choose "Change Table Color" to change the table background color.
- When creating a new puzzle, you may not know your image's aspect ratio offhand. Simply enter the width and height in pixels to the right of "Calculate aspect:" then hit "Calculate". A puzzle board with the closest aspect ratio will be selected for you.

# Development

## Building Code

See [dist/README.md](dist/README.md)

## Generating the pieces

It's kind of a mess. First, go to `src/making pieces`.

`generate_square_pieces.py` makes the square pieces, `create_pieces.py` makes the hexagonal ones. 

You'll need to fiddle with hardcoded paths in those files and the hardcoded target actions. Note that you need to use the locally included version of `py2d`, not the normal version available through `pip`. You can debug "install" it with `pip install -e src/` from the project root.

Updated pieces need to be hosted somewhere and `PUZZLE_URL` in the main Lua script needs to changed (before generating a puzzle).

`src/blender`, I believe, is an older, unmaintained method for generating the pieces.
