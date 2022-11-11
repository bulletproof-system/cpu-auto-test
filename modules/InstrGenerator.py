'''
Author: ltt
Date: 2022-11-07 17:05:01
LastEditors: ltt
LastEditTime: 2022-11-08 13:55:51
FilePath: InstrGenerator.py
'''

import modules.Global as Global
import modules.Decode as Decode
import random


def construct_instr(name, *argv):
    ret = {}
    ret["type"] = "instr"
    ret["name"] = name
    instr_class = Global.INSTRUCTION_DICT[name]
    ret["class"] = instr_class["class"]
    mips = Global.CLASSIFY[ret["class"]]["mips"].copy()
    i = 0
    for a in mips:
        if(a in (", ","(",")")): ret[a] = a
        else:
            ret[a] = argv[i]
            i += 1
            
    return ret
    
def rand_instr(instr_class, *argv):
    choice = Global.CLASSIFY[instr_class]["enbled"]
    return construct_instr(random.choice(choice), argv)
    
def rand_argv(str, argv=[]):
    """生成随机参数"""
    if(argv != []): return random.choice(argv)
    if str in ("rs","rt","rd","base"): 
        return random.randint(0,31)
    elif str in ("offset", "immediate"):
        return random.randint(-100, 100)
    else:
        return 0
    
def rand_assign(*argv, word_aligned=False):
    """对所给寄存器随机赋值"""
    ret = []
    value = {0 : 0}
    init_reg = [0]
    uninit_reg = argv.copy()
    random.shuffle(uninit_reg)
    for x in argv:
        op = random.randint(0,1)
        if op == 0:
            ret.append(rand_instr("cal_ri", x, random.choice(init_reg), rand_argv("immediate")))
        else:
            ret.append()
    pass
    
def print_mips(src, prefix='', suffix=''):
    """输出指令"""
    if(src["type"] == "label"): print(src["label"]+':')
    else:
        ret = [prefix ,src["name"]," "]
        mips = Global.CLASSIFY[src["class"]]["mips"]
        for x in mips:
            if x in ("rs","rt","rd"): 
                ret.append("$%-2d" % src[x])
            elif x in ("base"):
                ret.append("$%d" % src[x])
            elif x in ("offset","immediate"):
                ret.append("%d" % src[x])
            else:
                ret.append(src[x])
        ret.append(suffix)
        print(''.join(ret))
        
if __name__ == "__main__":
    pass