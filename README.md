# frida_lib_dumper
dump loaded library (.so) from memory to get decrypted lib for Android

## Basic Usage
1. Put identifier of target Android app and library name in ``dumper.py``
2. Connect to your device through adb and run [frida-server](https://github.com/frida/frida/releases)
3. Run ``dumper.py``

### Sample Usage for Unity Apps
1. Extract dump.cs by [Zygisk-Il2CppDumper](https://github.com/Perfare/Zygisk-Il2CppDumper) or [Auto-Il2CppDumper](https://github.com/AndnixSH/Auto-Il2cppDumper) and save to a folder in which ``label_ida.py`` exists
2. Dump libil2cpp.so using ``dumper.py``
3. Load libil2cpp.so into IDA
4. Go [File] → [Script file] and select ``label_ida.py`` to apply symbols in IDA

## Acknowledgements
- https://github.com/lasting-yang/frida_dump
- https://github.com/F8LEFT/SoFixer

