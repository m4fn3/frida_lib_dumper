# frida_lib_dumper
dump loaded library (.so) from memory to get decrypted lib for Android

## Usage
1. Put identifier of target Android app and library name in ``dumper.py``

2. Connect to your device through adb and run [frida-server](https://github.com/frida/frida/releases)

3. Run ``dumper.py``

## Acknowledgements
- https://github.com/lasting-yang/frida_dump
- https://github.com/F8LEFT/SoFixer

