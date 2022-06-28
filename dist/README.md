# Creating the TTS workshop mod

In `src\tts`, `ttsjigsawjoin_TEMPLATE.json` contains the initial room setup (e.g. extended table) but without the Lua script or UI XML, so those can be source-controlled separately as `ttsjigsawjoin.ttslua` and `ttsjigsawjoin.xml`.

Use `build_json.py` to insert those into the template and build the full savefile here as `ttsjigsawjoin.json`. Then you can copy that over an existing savefile in e.g. `C:\Users\<YOU>\Documents\My Games\Tabletop Simulator\Saves\TS_Save_1.json`, load it in TTS, and upload to the workshop. Alternatively to replacing an existing savefile, you can instead edit e.g. `C:\Users\<YOU>\Documents\My Games\Tabletop Simulator\Saves\SaveFileInfos.json` and insert a reference to the new one.

To explain how your new workshop mod will be bootstrapped with a clean scoreboard and other defaults...

The template's `LuaScriptState` field starts blank, so when you first load the full savefile, the Lua script will detect that and set a flag to disable saving game state during that session. When you save in that session (e.g. the upload to the workshop is effectively a save), the Lua script will cause `LuaScriptState` to be just the string "saveDelay" instead of saving any state generated since your load (e.g. the scoreboard with your name in it). Finally, when *that* save is later loaded (e.g. a user loads the mod from the workshop), the Lua script will see that `LuaScriptState` is "saveDelay", and will initialize the desired default state (with a blank scoreboard, though it will quickly detect the user as a player and add them), and enable subsequent normal saves.
