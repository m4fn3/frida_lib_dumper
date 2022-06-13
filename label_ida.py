#############################################
# *** Load dump.cs and apply data to IDA ***#
#############################################

with open("dump.cs", encoding="utf-8") as f:
    lines = f.readlines()

metadata = []  # function addr and name
addresses = []  # function addresses

#  *** load dump.cs *** #
print("[o] Loading dump.cs")
dll_name = ""
name_space = ""
class_name = ""
for idx in range(len(lines)):
    line = lines[idx].replace("\n", "")
    if line.startswith("// Dll : "):
        dll_name = line.replace("// Dll : ", "")
    elif line.startswith("// Namespace: "):  # current namespace
        name_space = line.replace("// Namespace: ", "")
    elif line.startswith(("public", "protected", "internal", "private")):  # current class name
        class_name = line.split(":")[0].split()[-1].strip()
    elif line.startswith("	// RVA:"):  # dump method data
        offset_hex = line.split(":")[1].split()[0]
        if offset_hex == "0x":
            continue
        offset = int(offset_hex, 0)
        addresses.append(offset)
        symbol = lines[idx + 1].split("{")[0]
        names = symbol.split("(")[0].split()
        func_name = f"{names[-2]} {name_space}$${class_name}$${names[-1]}({symbol.split('(')[1]}"  # format symbol
        metadata.append({
            "addr": offset,
            "symbol": func_name
        })
print(f"[o] total {len(addresses)} symbols found")

addresses.sort()  # sort addr list
# *** Check *** #
# count = 0
# for idx in range(len(addresses) - 1):
#     start = addresses[idx]
#     end = addresses[idx + 1]
#     ida_start = idc.get_func_attr(start, FUNCATTR_START)
#     # if ida_start != start:
#     #     print(f"{hex(start)} {hex(ida_start)}")
#     ida_end = idc.get_func_attr(start, FUNCATTR_END)
#     if ida_end == idaapi.BADADDR:  # auto detect
#         continue
#     if ida_end > end:  # end addr checker
#         count += 1
#         print(f"{ida_end} {end}")
# print(f"{count} / {len(addresses)}")

# *** adjust function boundaries *** #
for idx in range(len(addresses) - 1):
    start = addresses[idx]
    end = addresses[idx + 1]
    ida_funcs.add_func(start)
    ida_end = idc.get_func_attr(start, FUNCATTR_END)
    if ida_end == idaapi.BADADDR:  # auto detect
        continue
    if ida_end > end:  # limit range
        idc.set_func_end(start, end)
print("[o] Function Adjustment done")

# *** rename functions *** #
for meta in metadata:
    ret = idc.set_name(meta["addr"], meta["symbol"], SN_NOWARN | SN_NOCHECK)
    if ret == 0:  # in case same name function exists
        new_name = meta["symbol"] + '_' + str(meta["addr"])
        ret = idc.set_name(meta["addr"], new_name, SN_NOWARN | SN_NOCHECK)

print("[o] Successfully renamed function")
