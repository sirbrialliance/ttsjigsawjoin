# Creating the TTS workshop mod

To set scripts in a TTS save file:

- Set the global lua script to `require("src/tts/ttsjigsawjoin")`
- Set the global UI XML to `<Include src="src/tts/ttsjigsawjoin.xml"/>`

Then to set or update the scripts using your IDE of choice to upload them into an active TTS file. For example, with Visual Studio Code with the "Tabletop Simulator Lua" plugin installed use the `TTSLua: Save and Play` command with a puzzle (or to-be puzzle) save file loaded in TTS. Your IDE will flatten all the file includes and send the results over to TTS.

The `ttsjigsawjoin_TEMPLATE.json` and `build_json.py` files aren't used in this branch, but they are in the original.

To explain how your new workshop mod will be bootstrapped with a clean scoreboard and other defaults...

The template's `LuaScriptState` field starts blank, so when you first load the full savefile, the Lua script will detect that and set a flag to disable saving game state during that session. When you save in that session (e.g. the upload to the workshop is effectively a save), the Lua script will cause `LuaScriptState` to be just the string "saveDelay" instead of saving any state generated since your load (e.g. the scoreboard with your name in it). Finally, when *that* save is later loaded (e.g. a user loads the mod from the workshop), the Lua script will see that `LuaScriptState` is "saveDelay", and will initialize the desired default state (with a blank scoreboard, though it will quickly detect the user as a player and add them), and enable subsequent normal saves.
