'''
Author: ltt
Date: 2022-11-07 11:14:05
LastEditors: ltt
LastEditTime: 2022-11-08 13:43:33
FilePath: DataMaker.py
'''

import modules.InstrGenerator as IG
import modules.Global as Global
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

def generate_group(id, num = 10, prefix='', name="case"):
    ret = []
    class_list = [key for key, value in Global.CLASSIFY.items() if value["enbled"] != []]
    label = f"{name}_{id}"
    begin_label =  label+"_begin"
    end_label = label+"_end"
    used_reg = list(range(1,31))
    random.shuffle(used_reg)
    used_reg = sorted(used_reg[0:3]+[0,31])
    ret.append({"type" : "label", "label" : begin_label})
    for _ in range(num):
        ret.append(IG.construct_instr())
    
    ret.append({"type" : "label", "label" : end_label})
    
    
    