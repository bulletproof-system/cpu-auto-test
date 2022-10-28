'''
Author: ltt
Date: 2022-10-26 20:22:43
LastEditors: ltt
LastEditTime: 2022-10-28 21:04:59
FilePath: Comparator.py
'''
import json

import modules.Constants as Const

def Logisim(setting):
    """比对 Logisim"""
    def print_wrong():
        print(f"wrong instruction is found on line {i+1}")
        print(f"we got:\n {json.dumps(out, sort_keys=False, indent=4, separators=(',', ': '))}")
        print(f"we expected:\n {json.dumps(std, sort_keys=False, indent=4, separators=(',', ': '))}")
        return
    std_path = setting[Const.STD_PATH]
    out_path = setting[Const.OUT_PATH]
    with open(std_path) as std_file:
        with open(out_path) as out_file:
            stds = json.load(std_file)
            outs = json.load(out_file)
            for i in range(len(stds)):
                std, out = stds[i], outs[i]
                print("checking %s" % std["instr"])
                if(std["code"] != out["code"]):
                    print_wrong()
                    return
                if(std["code"] == '0'*32):
                    if(out["MemWrite"]):
                        print_wrong()
                        return
                    if(out["RegWrite"] and out["RegAddr"]!="0x00000000"):
                        print_wrong()
                        return
                    continue
                if(std["RegWrite"]!=out["RegWrite"]):
                    print_wrong()
                    return
                if(std["MemWrite"]!=out["MemWrite"]):
                    print_wrong()
                    return
                if(std["RegWrite"]):
                    if(std["RegAddr"]!=out["RegAddr"] or std["RegData"]!=out["RegData"]):
                        print_wrong()
                        return
                if(std["MemWrite"]):
                    if(std["MemAddr"]!=out["MemAddr"] or std["MemData"]!=out["MemData"]):
                        print_wrong()
                        return
    print("Accepted")
    
def Verilog(setting):
    """比对 Verilog"""
    def print_wrong():
        print(f"wrong instruction is found on line {i+1}")
        print(f"we got:\n {json.dumps(out, sort_keys=False, indent=4, separators=(',', ': '))}")
        print(f"we expected:\n {json.dumps(std, sort_keys=False, indent=4, separators=(',', ': '))}")
        return
    std_path = setting[Const.STD_PATH]
    out_path = setting[Const.OUT_PATH]
    with open(std_path) as std_file:
        with open(out_path) as out_file:
            stds = json.load(std_file)
            outs = json.load(out_file)
            for i in range(len(stds)):
                std, out = stds[i], outs[i]
                print("checking %s" % std["instr"])
                if(std["pc"] != out["pc"]):
                    print_wrong()
                    return
                if(std["RegWrite"]!=out["RegWrite"]):
                    print_wrong()
                    return
                if(std["MemWrite"]!=out["MemWrite"]):
                    print_wrong()
                    return
                if(std["RegWrite"]):
                    if(std["RegAddr"] == out["RegAddr"] and out["RegAddr"] == " 0"):
                        continue
                    if(std["RegAddr"]!=out["RegAddr"] or std["RegData"]!=out["RegData"]):
                        print_wrong()
                        return
                if(std["MemWrite"]):
                    if(std["MemAddr"]!=out["MemAddr"] or std["MemData"]!=out["MemData"]):
                        print_wrong()
                        return
    print("Accepted")