

import re



def operandaddr(s, addrs):
    setpatt = r'ld \((0x[0-9a-f]*)\).*, (.*)' # e.g. ld (0x4222), a
    res = re.match(setpatt, s)
    if res:
        resstr = res.group(1)
        addr = int(resstr, 16)
        if resstr in addrs:
            var = addrs[resstr]
            return f'set {var} = {res.group(2)}'

    getpatt = r'ld ([a-z]+), \((0x[0-9a-f]*)\)' # e.g. ld a, (0x409c)
    res = re.match(getpatt, s)

    if res:
        resstr = res.group(2)
        addr = int(resstr, 16)
        if resstr in addrs:
            var = addrs[resstr]
            return f'get {res.group(1)} = {var}'
    return ""


if __name__ == "__main__":
    addrs = {
        "0x48f" : "Test",
        "0x408f" : "HEXX",
        "0x4093" : "CURSE",
        "0x4094" : "UNDER",
        "0x4095" : "KSIZ",
        "0x4098" : "ACTK"
    }

    # res = re.match(r'ld (.*), \(?(0x[0-9a-f]*)\)?', "ld hl, (0x408f)")
    # print(res)

    res = operandaddr("ld (0x408f), a", addrs)
    assert res == "set HEXX = a"
    res = operandaddr("ld (0x48f), a", addrs)
    assert res == "set Test = a"
    res = operandaddr("ld a, (0x408f)", addrs)
    assert res == "get a = HEXX"
    res = operandaddr("ld a, (0x4f)", addrs)
    assert res == ""