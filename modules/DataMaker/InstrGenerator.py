'''
Author: ltt
Date: 2022-11-07 17:05:01
LastEditors: ltt
LastEditTime: 2022-11-07 20:45:58
FilePath: InstrGenerator.py
'''

import modules.Global as Global
import modules.Decode as Decode


def construct_instr(name, *argv):
    ret = {}
    ret["type"] = "instr"
    ret["name"] = name
    ret["calss"] = instr_class = Global.INSTRUCTION_DICT[name]
    mips = Global.CLASSIFY[instr_class]["mips"].copy()
    i = 0
    for a in mips:
        if(a in (", ","(",")")): ret[a] = a
        else:
            ret[a] = argv[i]
            i += 1
    
def print_mips(*src):
    if(src["type"] == "label"): print(mips["label"])
    else:
        mips = Global.CLASSIFY[mips["class"]]["mips"]
        ret = [src[x] for x in mips]
        print(''.join(ret))
        
if __name__ == "__main__":
    Decode.init_argv() # 读取参数
    instr = construct_instr("add",1,2,0)
    print_mips(instr)