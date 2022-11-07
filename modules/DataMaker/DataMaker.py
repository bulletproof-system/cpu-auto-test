'''
Author: ltt
Date: 2022-11-07 11:14:05
LastEditors: ltt
LastEditTime: 2022-11-07 16:20:04
FilePath: DataMaker.py
'''

nop = {
    "type" : "instr",
    "name" : "nop",
    "class" : "cal_ri",
    "opcode" : 0,
    "rs" : 0,
    "rt" : 0,
    "rd" : 0,
    "10:6" : 0,
    "funct" : 0
}

def add_nop(source):
    """在每条指令间添加 nop 以测试单条指令正确性"""
    ret = []
    for s in source:
        if(s["type"] == "label"):
            ret.append(s)
        else:
            ret.append(nop.copy())
            ret.append(nop.copy())
            ret.append(nop.copy())
            ret.append(nop.copy())
            ret.append(nop.copy())
            ret.append(s)
    return ret

