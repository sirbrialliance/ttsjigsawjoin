import json

src = '..\\src\\tts\\'

with open(src + 'ttsjigsawjoin_TEMPLATE.json', 'r') as template_file, \
     open(src + 'ttsjigsawjoin.ttslua', 'r') as ttslua_file, \
     open(src + 'ttsjigsawjoin.xml', 'r') as xml_file, \
     open('ttsjigsawjoin.json', 'w') as savefile_file:
    template = json.load(template_file)
    template['LuaScript'] = ttslua_file.read()
    template['LuaScriptState'] = ''  # just to be explicit
    template['XmlUI'] = xml_file.read()
    json.dump(template, savefile_file, indent=2)
