let lib_name
let identifier

// exports
rpc.exports = {
    libinfo: function(name, itf){
        lib_name = name
        identifier = itf
    }
}

// main dumper
let count = 0

function dump() {
    // counter
    count += 1
    if (count !== 1) {
        console.log(`[-] Ignored (${count})`)
        return
    }
    // dump lib
    let lib = Process.findModuleByName(lib_name);
    console.log(`[o] Start dumping ${lib_name}`)
    console.log(`    ${lib.base} - ${lib.base.add(ptr(lib.size))} / size: ${lib.size}`)
    Memory.protect(ptr(lib.base), lib.size, 'rwx');
    let dump = new File(`/data/data/${identifier}/files/dump_${lib_name}`, "wb")
    let lib_buffer = lib.base.readByteArray(lib.size)
    dump.write(lib_buffer)
    dump.close()
    // send info
    send([Process.findModuleByName(lib_name), Process.arch])
}

// Hook lib load
Interceptor.attach(Module.findExportByName(null, 'dlopen'), {
    onEnter: function (args) {
        this.path = Memory.readUtf8String(args[0]);
    },
    onLeave: function () {
        if (this.path !== null && this.path.includes(lib_name)) {
            dump() // target lib loaded
        }
    }
});