import frida
import sys
import os

# setting
identifier = ""
lib_name = ""


def get_script():
    # read javascript code
    with open("dumper.js", "r") as f:
        return f.read()


def fix_lib(arch, base):
    # fix dumped library
    dump_name = "dump_" + lib_name
    # send so fixer
    if arch == "arm":
        os.system("adb push android/SoFixer32 /data/local/tmp/SoFixer")
    elif arch == "arm64":
        os.system("adb push android/SoFixer64 /data/local/tmp/SoFixer")
    os.system("adb shell chmod +x /data/local/tmp/SoFixer")
    # move dump
    os.system(f"adb shell su -c 'chmod 777 /data/data/{identifier}/files/{dump_name}'")
    os.system(f"adb shell su -c 'cp /data/data/{identifier}/files/{dump_name} /data/local/tmp/'")
    # run so fixer
    os.system(f"adb shell /data/local/tmp/SoFixer -m {base} -s /data/local/tmp/{dump_name} -o /data/local/tmp/{dump_name}.fix.so")
    # pull lib
    os.system(f"adb pull /data/local/tmp/{dump_name}.fix.so {lib_name}")
    # remove files
    os.system(f"adb shell rm /data/local/tmp/{dump_name}")
    os.system(f"adb shell rm /data/local/tmp/{dump_name}.fix.so")
    os.system("adb shell rm /data/local/tmp/SoFixer")
    os.system(f"adb shell su -c 'rm /data/data/{identifier}/files/{dump_name}'")


def on_message(message, data):
    # frida message handler
    if "payload" in message:  # dumped
        print("[o] Fix dumped lib")
        info = message["payload"]
        print("----------------------------------------------------")
        fix_lib(info[1], info[0]["base"])
        print("----------------------------------------------------")
        print(f"[o] Successfully dumped {lib_name}")
    else:  # error
        print(message)


if __name__ == "__main__":
    device: frida.core.Device = frida.get_usb_device()
    target = device.spawn(identifier)
    session: frida.core.Session = device.attach(target)
    script = session.create_script(get_script())
    script.on('message', on_message)
    script.load()
    script.exports.libinfo(lib_name, identifier)
    device.resume(target)
    sys.stdin.read()
