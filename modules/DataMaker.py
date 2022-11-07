'''
Author: ltt
Date: 2022-11-07 11:14:05
LastEditors: ltt
LastEditTime: 2022-11-08 00:00:03
FilePath: DataMaker.py
'''

import modules.InstrGenerator as IG
import random

# def rand

def add_nop(source):
    """在每条指令间添加 nop 以测试单条指令正确性"""
    ret = []
    for s in source:
        if(s["type"] == "label"):
            ret.append(s)
        else:
            ret.append(IG.construct_instr("nop"))
            ret.append(IG.construct_instr("nop"))
            ret.append(IG.construct_instr("nop"))
            ret.append(IG.construct_instr("nop"))
            ret.append(IG.construct_instr("nop"))
            ret.append(s)
    return ret

def generate_case(num):
    ret = []
    case_label =  f"case_{num}"
    ret.append({"type" : "label", "label" : case_label})
    
    