'''
Author: ltt
Date: 2022-10-26 20:19:34
LastEditors: ltt
LastEditTime: 2022-10-30 17:04:20
FilePath: Generator.py
'''
from __future__ import barry_as_FLUFL
from asyncio import base_tasks
import hashlib, re, json, os
from pyexpat.errors import codes

import modules.Base as Base
import modules.Constants as Const
import modules.Decode as Decode


def generate_instruction(setting):
    """生成指令"""
    pass

def generate_code_Logisim(setting):
    """生成 Logisim 机器码和标准输出"""
    """生成机器码"""
    asm, mars = setting[Const.ASM_PATH], setting[Const.MARS_PATH]
    code_path = setting[Const.CODE_PATH]
    data, text = "temp\\data.txt", "temp\\text.txt"
    Base.run(["java", "-jar", mars, "me", "nc", "mc",
             "CompactDataAtZero", "dump", ".text", "HexText", data, asm])
    Base.run(["java", "-jar", mars, "me", "nc", "mc",
             "CompactTextAtZero", "dump", ".text", "HexText", text, asm])
    with open(data, "r") as DataAtZeroFile:
        DataAtZero = DataAtZeroFile.readlines()
    with open(text, "r") as TextAtZeroFile:
        TextAtZero = TextAtZeroFile.readlines()
    codes = Decode.merge(DataAtZero, TextAtZero,
                         setting[Const.INSTRUCTION_LIST])
    with open(code_path, "w") as code_file:
        code_file.write("v2.0 raw\n")
        code_file.writelines(codes)  # 合并后机器码储存在 code_path 对应文件中
    # print(''.join(codes))
    """生成标准输出"""
    max_exe = setting[Const.EXECUTION_TIME]
    std_path = setting[Const.STD_PATH]
    codes += ["00000000"]
    std = []
    ret = Base.run(["java","-jar",mars,"me","nc","std","mc","CompactDataAtZero",asm]).split('\n')
    
    for str in ret:
        ans = {}
        if(str[0:2] != "pc"): continue
        # 获取 pc 及指令
        pc = ans["pc"] = "0x"+str[6:14]
        instr = ans["instr"] = str[24:32]
        ans["asm"] = re.search("asm:[^\r^\n]*",str).group()[5:]
        
        # 根据指令获取输出
        attr,code = Decode.findInList(instr, setting[Const.INSTRUCTION_LIST]),Decode.toBin(instr)
        ans["code"] = code
        if (attr["RegWrite"] == True):
            ans["RegWrite"] = True
            ans["RegAddr"] = "0x%08x" % int(str[34:36])
            ans["RegData"] = "0x"+str[40:48]
        else:
            ans["RegWrite"] = False   
        if (attr["MemWrite"] == True):
            ans["MemWrite"] = True
            ans["MemAddr"] = "0x%08x" % (int(str[34:44], 16)>>2)
            ans["MemData"] = "0x"+str[48:56]
        else:
            ans["MemWrite"] = False
        std.append(ans)

    with open(std_path, "w") as std_file:
        std_file.write(json.dumps(std, sort_keys=False, indent=4, separators=(',', ': ')))
    return
def generate_out_Logisim(setting):
    """获取 Logisim 输出文件"""
    test_path, test_circ = setting[Const.TEST_PATH], setting[Const.TEST_CIRC]
    logisim = setting[Const.LOGISIM_PATH]
    code_path, out_path = setting[Const.CODE_PATH], setting[Const.OUT_PATH]

    Base.run(["copy", test_path, test_circ])
    with open(test_circ, "r+") as fp:
        with open(code_path, "r") as code_file:
            code_str = code_file.readlines()[1:]
            circ_str = fp.read()
            rom_str = re.search(Const.ROM, circ_str)
            if (rom_str == None):
                print("无 ROM 组件")
                raise RuntimeError
            # print(rom_str.group())
            rom_str = re.sub(r"\n([0-9a-zA-Z ]*\n*)*</a>",
                             f"\n{' '.join(code_str)}</a>", rom_str.group())
            # print(rom_str)
            circ_str = re.sub(Const.ROM, rom_str, circ_str)
            fp.seek(0, 0)
            fp.truncate()
            fp.write(circ_str)

    ret = Base.run(["java", "-jar", logisim, "Logisim\\auto_test.circ",
                   "-tty", "table", "-sub", "Logisim\\CPU.circ", test_circ])

    ret = ret.replace(' ', '').replace('\t', '').split('\n')
    out = []
    for s in ret:
        if (len(s) < 108):
            break
        ans = {}
        ans["code"] = s[0:32]
        ans["RegWrite"] = True if s[32] == '1' else False
        ans["RegAddr"] = "0x%08x" % int(s[33:38], 2)
        ans["RegData"] = "0x%08x" % int(s[38:70], 2)
        ans["MemWrite"] = True if s[70] == '1' else False
        ans["MemAddr"] = "0x%08x" % int(s[71:76], 2)
        ans["MemData"] = "0x%08x" % int(s[76:108], 2)
        out.append(ans)
    with open(out_path, "w") as out_file:
        out_file.write(json.dumps(out, sort_keys=False,
                       indent=4, separators=(',', ': ')))
    return
def Logisim(setting):
    """测试 Logisim"""
    skip = setting[Const.SKIP]
    if (skip == False):
        if (setting[Const.FILE_PATH] == ""):
            generate_instruction(setting)
        else:
            Base.run(["copy", setting[Const.FILE_PATH], setting[Const.ASM_PATH]])
            generate_code_Logisim(setting)
    generate_out_Logisim(setting)


def generate_code_Verilog(setting):
    """生成 Verilog 机器码和标准输出"""
    """生成机器码"""
    asm, mars = setting[Const.ASM_PATH], setting[Const.MARS_PATH]
    code_path = setting[Const.CODE_PATH]
    Base.run(["java", "-jar", mars, "me", "nc", "mc", "CompactDataAtZero", "dump", ".text", "HexText", code_path, asm])
    with open(code_path, "r") as code_file:
        codes = code_file.readlines()
    """生成标准输出"""
    max_exe = setting[Const.EXECUTION_TIME]
    std_path = setting[Const.STD_PATH]
    codes += ["00000000"]
    std = []
    ret = Base.run(["java","-jar",mars,"me","nc","std","mc","CompactDataAtZero",asm]).split('\n')
    for str in ret:
        ans = {}
        if(str[0:2] != "pc"): continue
        # 获取 pc 及指令
        pc = ans["pc"] = "0x"+str[6:14]
        instr = ans["instr"] = str[24:32]
        ans["asm"] = re.search("asm:[^\r^\n]*",str).group()[5:]
        
        # 根据指令获取输出
        attr,code = Decode.findInList(instr, setting[Const.INSTRUCTION_LIST]),Decode.toBin(instr)
        ans["code"] = code
        if (attr["RegWrite"] == True):
            ans["RegWrite"] = True
            ans["RegAddr"] = str[34:36]
            ans["RegData"] = "0x"+str[40:48]
        else:
            ans["RegWrite"] = False   
        if (attr["MemWrite"] == True):
            ans["MemWrite"] = True
            ans["MemAddr"] = str[34:44]
            ans["MemData"] = "0x"+str[48:56]
        else:
            ans["MemWrite"] = False
    
        if (attr["RegWrite"] or attr["MemWrite"]):
            std.append(ans)
    with open(std_path, "w") as std_file:
        std_file.write(json.dumps(std, sort_keys=False, indent=4, separators=(',', ': ')))
    pass
def generate_out_Verilog(setting):
    """获取 Verilog 输出文件"""
    compiler,argv = setting[Const.COMPILER_TYPE],setting[Const.COMPILER_ARGV]
    test_path,out_path = setting[Const.TEST_PATH],setting[Const.OUT_PATH]
    code_path = f"{os.getcwd()}\\" + setting[Const.CODE_PATH]
    temp = f"{os.getcwd()}\\temp\\out"
    test_branch = f"{os.getcwd()}\\Verilog\\testbranch.v"
    if(compiler == "iverilog"):
        (test_path, test_name) = os.path.split(test_path)
        Base.run(["cd",test_path,"&&","copy",code_path,"code.txt"])
        ret = Base.run(["cd",test_path,
                        "&&","iverilog",argv,"-o",temp,test_name,test_branch, 
                        "&&", "vvp", temp], errdesc="编译错误")
        match = re.findall(r"@.*\n",ret)
        # print(match)
        out = []
        for s in match:
            ans = {}
            ans["pc"] = "0x"+s[1:9]
            if(re.search(r"@.{10}\$.{14}[\r\n]+", s) != None):
                ans["RegWrite"] = True
                ans["MemWrite"] = False
                ans["RegAddr"] = s[12:14]
                ans["RegData"] = "0x"+s[-10:-2]
            else:
                ans["MemWrite"] = True
                ans["RegWrite"] = False
                ans["MemAddr"] = "0x"+s[12:20]
                ans["MemData"] = "0x"+s[-10:-2]
            out.append(ans)
        with open(out_path,"w") as out_file:
            out_file.write(json.dumps(out, sort_keys=False,
                           indent=4, separators=(',', ': ')))
    else:
        pass


def Verilog(setting):
    """测试 Verilog"""
    skip = setting[Const.SKIP]
    if (skip == False):
        if (setting[Const.FILE_PATH] == ""):
            generate_instruction(setting)
        else:
            Base.run(["copy", setting[Const.FILE_PATH], setting[Const.ASM_PATH]])
            generate_code_Verilog(setting)
    generate_out_Verilog(setting)
            