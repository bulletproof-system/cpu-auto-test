'''
Author: ltt
Date: 2022-10-26 20:19:34
LastEditors: ltt
LastEditTime: 2023-01-04 17:26:48
FilePath: Generator.py
'''
import re, json, os, shutil
from functools import cmp_to_key

import modules.Base as Base
import modules.Global as Global
import modules.Decode as Decode


def generate_code_P3():
    """生成 Logisim 机器码和标准输出"""
    """生成机器码"""
    asm, mars = Global.ASM_PATH, Global.MARS_PATH
    code_path = Global.CODE_PATH
    debug = Global.DEBUG
    data, text = "temp/data.txt", "temp/text.txt"
    if(debug): print("generating code (Logisim)")
    Base.run(["java", "-jar", mars,"ae1", "me", "nc", "mc",
             "CompactDataAtZero", "dump", ".text", "HexText", data, asm])
    Base.run(["java", "-jar", mars,"ae1", "me", "nc", "mc",
             "CompactTextAtZero", "dump", ".text", "HexText", text, asm])
    with open(data, "r") as DataAtZeroFile:
        DataAtZero = DataAtZeroFile.readlines()
    with open(text, "r") as TextAtZeroFile:
        TextAtZero = TextAtZeroFile.readlines()
    codes = Decode.merge(DataAtZero, TextAtZero,
                         Global.INSTRUCTION_DICT)
    with open(code_path, "w") as code_file:
        code_file.write("v2.0 raw\n")
        code_file.writelines(codes)  # 合并后机器码储存在 code_path 对应文件中
    if(debug): print("generating code finish (Logisim)")
    """生成标准输出"""
    std_path = Global.STD_PATH
    codes += ["00000000"]
    std = []
    if(debug): print("generating std (Logisim)")
    ret = Base.run(["java","-jar",mars,"me","nc","std","mc","CompactDataAtZero",asm]).split('\n')
    
    for str in ret:
        ans = {}
        if(str[0:2] != "pc"): continue
        # 获取 pc 及指令
        pc = ans["pc"] = "0x"+str[6:14]
        instr = ans["instr"] = str[24:32]
        ans["asm"] = re.search("asm:[^\r^\n]*",str).group()[5:]
        if(debug): print(f"generating {str}")
        
        # 根据指令获取输出
        attr,code = Global.INSTRUCTION_DICT.get(ans["asm"].split(' ')[0]),Decode.toBin(instr)
        if(attr == None):
            raise RuntimeError("指令集中没有该指令:"+ans["asm"])
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
    if(debug): print("generating std finish (Logisim)")
    return
def generate_out_P3():
    """获取 Logisim 输出文件"""
    debug = Global.DEBUG
    test_path, test_circ = Global.TEST, Global.TEST_CIRC
    logisim = Global.LOGISIM_PATH
    code_path, out_path = Global.CODE_PATH, Global.OUT_PATH
    if(debug): print("generating out (Logisim)")
    Base.run(["copy", test_path, test_circ])
    with open(test_circ, "r+") as fp:
        with open(code_path, "r") as code_file:
            code_str = code_file.readlines()[1:]
            circ_str = fp.read()
            rom_str = re.search(Global.ROM, circ_str)
            if (rom_str == None):
                print("无 ROM 组件")
                raise RuntimeError
            # print(rom_str.group())
            rom_str = re.sub(r"\n([0-9a-zA-Z ]*\n*)*</a>",
                             f"\n{' '.join(code_str)}</a>", rom_str.group())
            # print(rom_str)
            circ_str = re.sub(Global.ROM, rom_str, circ_str)
            fp.seek(0, 0)
            fp.truncate()
            fp.write(circ_str)

    ret = Base.run(["java", "-jar", logisim, "Logisim/auto_test.circ",
                   "-tty", "table", "-sub", "Logisim/CPU.circ", test_circ])

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
    if(debug): print("generating out finish (Logisim)")
    return
def P3():
    """测试 Logisim"""
    Base.run(["copy", Global.FILE_PATH, Global.ASM_PATH])
    generate_code_P3()
    if(Global.COMPARE):
        generate_out_P3()


def generate_code_P4():
    """生成单周期机器码和标准输出"""
    """生成机器码"""
    asm, mars = Global.ASM_PATH, Global.MARS_PATH
    code_path = Global.CODE_PATH
    debug = Global.DEBUG
    if(debug): print("generating code (P4)")
    Base.run(["java", "-jar", mars,"ignore","ae1", "me", "nc", "mc", "CompactDataAtZero", "dump", ".text", "HexText", code_path, asm])
    with open(code_path, "r") as code_file:
        codes = code_file.readlines()
    if(debug): print("generating code finish(P4)")
    """生成标准输出"""
    std_path = Global.STD_PATH
    codes += ["00000000"]
    std = []
    if(debug): print("generating std (P4)")
    if(Global.COPY):
        test_path = Global.TEST
        shutil.copy(code_path, test_path)
    ret = Base.run(["java","-jar",mars,"ignore","ae1","me","nc","std","mc","CompactDataAtZero",asm]).split('\n')
    for str in ret:
        ans = {}
        if(str[0:2] != "pc"): continue
        # 获取 pc 及指令
        pc = ans["pc"] = "0x"+str[6:14]
        instr = ans["instr"] = str[24:32]
        ans["asm"] = re.search("asm:[^\r^\n]*",str).group()[5:]
        if(debug): print(f"generating {str}")
        
        # 根据指令获取输出
        attr,code = Global.INSTRUCTION_DICT.get(ans["asm"].split(' ')[0]),Decode.toBin(instr)
        if(attr == None):
            raise RuntimeError("指令集中没有该指令:"+ans["asm"])
        ans["code"] = code
        if (attr["RegWrite"] == True):
            ans["RegWrite"] = True
            ans["RegAddr"] = str[34:36]
            ans["RegData"] = "0x"+str[40:48]
            if(ans["RegAddr"] == " 0"): continue # 过滤 $0 寄存器
        else:
            ans["RegWrite"] = False   
        if (attr["MemWrite"] == True):
            ans["MemWrite"] = True
            ans["MemAddr"] = str[34:44]
            ans["MemData"] = "0x"+str[48:56]
        else:
            ans["MemWrite"] = False
    
        # if (attr["RegWrite"] or attr["MemWrite"]):
        std.append(ans)
    with open(std_path, "w") as std_file:
        std_file.write(json.dumps(std, sort_keys=False, indent=4, separators=(',', ': ')))
    if(debug): print("generating code finish (P4)")    
    return
def generate_out_P4():
    """获取P4 CPU 输出文件"""
    debug = Global.DEBUG
    if(debug): print("generating out (P4)")
    compiler,argv = Global.COMPILER_TYPE,Global.COMPILER_ARGV
    out_path = Global.OUT_PATH
    code_path = Global.CODE_PATH
    test_branch = os.path.join("Verilog", "P4.v")
    shutil.rmtree("mips_files")
    os.mkdir("mips_files")
    with open("mips_files/.gitignore", "w") as fp:
        fp.write("!.gitignore")
    for file_path in Global.TEST_FILES:
        shutil.copy(file_path, "mips_files")
    shutil.copy(test_branch, "mips_files")
    shutil.copy(code_path, "mips_files")
    if(compiler == "iverilog"):
        ret = Base.run(["cd", "mips_files",
                        "&&", "iverilog",argv,"-o","out", "-s", "tb_P4", "*.v", 
                        "&&", "vvp", "out"], errdesc="编译错误")
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
                if(ans["RegAddr"] == " 0"): continue # 过滤 $0 寄存器
            else:
                ans["MemWrite"] = True
                ans["RegWrite"] = False
                ans["MemAddr"] = "0x"+s[12:20]
                ans["MemData"] = "0x"+s[-10:-2]
            out.append(ans)
        
    else:
        pass
    with open(out_path,"w") as out_file:
        out_file.write(json.dumps(out, sort_keys=False,
                        indent=4, separators=(',', ': ')))
    if(debug): print("generating out finish (P4)")
    return
def P4():
    """测试单周期CPU"""
    Base.run(["copy", Global.FILE_PATH, Global.ASM_PATH])
    generate_code_P4()
    if(Global.COMPARE):
        generate_out_P4()
            
def comp(a, b):
    """排序函数"""
    if(int(a["time"]) < int(b["time"])): return -1
    if(int(a["time"]) > int(b["time"])): return 1
    if(a["RegWrite"]): return -1
    if(b["RegWrite"]): return 1
    return 0       
def generate_code_P5():
    """生成 P5 机器码和标准输出"""
    """生成机器码"""
    asm, mars = Global.ASM_PATH, Global.MARS_PATH
    code_path = Global.CODE_PATH
    debug = Global.DEBUG
    if(debug): print("generating code (P5)")
    Base.run(["java", "-jar", mars,"ignore","ae1","db", "me", "nc", "mc", "CompactDataAtZero", "dump", ".text", "HexText", code_path, asm])
    with open(code_path, "r") as code_file:
        codes = code_file.readlines()
    if(debug): print("generating code finish(P5)")
    if(Global.COPY):
        test_path = Global.TEST
        shutil.copy(code_path, test_path)
    """生成标准输出"""
    std_path = Global.STD_PATH
    codes += ["00000000"]
    std = []
    if(debug): print("generating std (P5)")
    ret = Base.run(["java","-jar",mars,"ignore","ae1","db","me","nc","std","mc","CompactDataAtZero",asm]).split('\n')
    for str in ret:
        ans = {}
        if(str[0:2] != "pc"): continue
        # 获取 pc 及指令
        pc = ans["pc"] = "0x"+str[6:14]
        instr = ans["instr"] = str[24:32]
        ans["asm"] = re.search(r"asm:[^\r^\n]*",str).group()[5:]
        if(debug): print(f"generating {str}")
        
        # 根据指令获取输出
        attr,code = Global.INSTRUCTION_DICT.get(ans["asm"].split(' ')[0]),Decode.toBin(instr)
        if(attr == None):
            raise RuntimeError("指令集中没有该指令:"+ans["asm"])
        ans["code"] = code
        if(code == "0"*32): continue
        if (attr["RegWrite"] == True):
            ans["RegWrite"] = True
            ans["RegAddr"] = str[34:36]
            ans["RegData"] = "0x"+str[40:48]
            if(ans["RegAddr"] == " 0"): continue # 过滤 $0 寄存器
        else:
            ans["RegWrite"] = False   
        if (attr["MemWrite"] == True):
            ans["MemWrite"] = True
            ans["MemAddr"] = str[34:44]
            ans["MemData"] = "0x"+str[48:56]
        else:
            ans["MemWrite"] = False
    
        # if (attr["RegWrite"] or attr["MemWrite"]):
        std.append(ans)
    with open(std_path, "w") as std_file:
        std_file.write(json.dumps(std, sort_keys=False, indent=4, separators=(',', ': ')))
    if(debug): print("generating code finish (P5)")    
    return
def generate_out_P5():
    """获取P5 CPU 输出文件"""
    debug = Global.DEBUG
    if(debug): print("generating out (P5)")
    compiler,argv = Global.COMPILER_TYPE,Global.COMPILER_ARGV
    out_path = Global.OUT_PATH
    code_path = Global.CODE_PATH
    test_branch = os.path.join("Verilog", "P5.v")
    shutil.rmtree("mips_files")
    os.mkdir("mips_files")
    with open("mips_files/.gitignore", "w") as fp:
        fp.write("!.gitignore")
    for file_path in Global.TEST_FILES:
        shutil.copy(file_path, "mips_files")
    shutil.copy(code_path, "mips_files")
    shutil.copy(test_branch, "mips_files")
    if(compiler == "iverilog"):
        ret = Base.run(["cd", "mips_files",
                        "&&", "iverilog",argv,"-o","out", "-s", "tb_P5", "*.v", 
                        "&&", "vvp", "out"], errdesc="编译错误")
        match = re.findall(r"[0-9]*@.*\n",ret)
        # print(match)
        out = []
        for s in match:
            ans = {}
            ans["time"] = re.search(r"[0-9]*@", s).group()[:-1]
            if(re.search(r"@.{10}\$.{14}[\r\n]+", s) != None):
                s = re.search(r"@.{10}\$.{14}[\r\n]+", s).group()
                ans["pc"] = "0x"+s[1:9]
                ans["RegWrite"] = True
                ans["MemWrite"] = False
                ans["RegAddr"] = s[12:14]
                ans["RegData"] = "0x"+s[-10:-2]
                if(ans["RegAddr"] == " 0"): continue # 过滤 $0 寄存器
            else:
                s = re.search(r"@.{10}\*.{20}[\r\n]+", s).group()
                ans["pc"] = "0x"+s[1:9]
                ans["MemWrite"] = True
                ans["RegWrite"] = False
                ans["MemAddr"] = "0x"+s[12:20]
                ans["MemData"] = "0x"+s[-10:-2]
            out.append(ans)
    else:
        pass
    out.sort(key=cmp_to_key(comp))
    with open(out_path,"w") as out_file:
            out_file.write(json.dumps(out, sort_keys=False,
                           indent=4, separators=(',', ': ')))
    if(debug): print("generating out finish (P5)")
    return        
def P5():
    """测试P5 CPU"""
    Base.run(["copy", Global.FILE_PATH, Global.ASM_PATH])
    generate_code_P5()
    if(Global.COMPARE):
        generate_out_P5()
    pass


def generate_code_P6():
    """生成 P6 机器码和标准输出"""
    """生成机器码"""
    asm, mars = Global.ASM_PATH, Global.MARS_PATH
    code_path = Global.CODE_PATH
    debug = Global.DEBUG
    if(debug): print("generating code (P6)")
    Base.run(["java", "-jar", mars,"ignore","ae1","db", "me", "nc", "mc", "CompactDataAtZero", "dump", ".text", "HexText", code_path, asm])
    with open(code_path, "r") as code_file:
        codes = code_file.readlines()
    if(debug): print("generating code finish(P6)")
    if(Global.COPY):
        test_path = Global.TEST
        shutil.copy(code_path, test_path)
    """生成标准输出"""
    std_path = Global.STD_PATH
    codes += ["00000000"]
    std = []
    if(debug): print("generating std (P6)")
    ret = Base.run(["java","-jar",mars,"ignore","ae1","db","me","nc","std","mc","CompactDataAtZero",asm]).split('\n')
    for str in ret:
        ans = {}
        if(str[0:2] != "pc"): continue
        # 获取 pc 及指令
        pc = ans["pc"] = "0x"+str[6:14]
        instr = ans["instr"] = str[24:32]
        ans["asm"] = re.search(r"asm:[^\r^\n]*",str).group()[5:]
        if(debug): print(f"generating {str}")
        
        # 根据指令获取输出
        attr,code = Global.INSTRUCTION_DICT.get(ans["asm"].split(' ')[0]),Decode.toBin(instr)
        if(attr == None):
            raise RuntimeError("指令集中没有该指令:"+ans["asm"])
        ans["code"] = code
        if(code == "0"*32): continue
        if (attr["RegWrite"] == True):
            ans["RegWrite"] = True
            ans["RegAddr"] = str[34:36]
            ans["RegData"] = "0x"+str[40:48]
            if(ans["RegAddr"] == " 0"): continue # 过滤 $0 寄存器
        else:
            ans["RegWrite"] = False   
        if (attr["MemWrite"] == True):
            ans["MemWrite"] = True
            ans["MemAddr"] = str[34:44]
            ans["MemData"] = "0x"+str[48:56]
        else:
            ans["MemWrite"] = False
    
        # if (attr["RegWrite"] or attr["MemWrite"]):
        std.append(ans)
    with open(std_path, "w") as std_file:
        std_file.write(json.dumps(std, sort_keys=False, indent=4, separators=(',', ': ')))
    if(debug): print("generating code finish (P6)")    
    return
def generate_out_P6():
    """获取 P6 CPU 输出文件"""
    debug = Global.DEBUG
    if(debug): print("generating out (P6)")
    compiler,argv = Global.COMPILER_TYPE,Global.COMPILER_ARGV
    out_path = Global.OUT_PATH
    code_path = Global.CODE_PATH
    test_branch = os.path.join("Verilog", "P6.v")
    shutil.rmtree("mips_files")
    os.mkdir("mips_files")
    with open("mips_files/.gitignore", "w") as fp:
        fp.write("!.gitignore")
    for file_path in Global.TEST_FILES:
        shutil.copy(file_path, "mips_files")
    shutil.copy(test_branch, "mips_files")
    shutil.copy(code_path, "mips_files")
    if(compiler == "iverilog"):
        ret = Base.run(["cd", "mips_files",
                        "&&", "iverilog",argv,"-o","out", "-s", "tb_P6", "*.v", 
                        "&&", "vvp", "out"], errdesc="编译错误")
        match = re.findall(r"[0-9]*@.*\n",ret)
        # print(match)
        out = []
        for s in match:
            ans = {}
            ans["time"] = re.search(r"[0-9]*@", s).group()[:-1]
            if(re.search(r"@.{10}\$.{14}[\r\n]+", s) != None):
                s = re.search(r"@.{10}\$.{14}[\r\n]+", s).group()
                ans["pc"] = "0x"+s[1:9]
                ans["RegWrite"] = True
                ans["MemWrite"] = False
                ans["RegAddr"] = s[12:14]
                ans["RegData"] = "0x"+s[-10:-2]
                if(ans["RegAddr"] == " 0"): continue # 过滤 $0 寄存器
            else:
                s = re.search(r"@.{10}\*.{20}[\r\n]+", s).group()
                ans["pc"] = "0x"+s[1:9]
                ans["MemWrite"] = True
                ans["RegWrite"] = False
                ans["MemAddr"] = "0x"+s[12:20]
                ans["MemData"] = "0x"+s[-10:-2]
            out.append(ans)
    else:
        pass
    out.sort(key=cmp_to_key(comp))
    with open(out_path,"w") as out_file:
            out_file.write(json.dumps(out, sort_keys=False,
                           indent=4, separators=(',', ': ')))
    if(debug): print("generating out finish (P6)")
    return  
def P6():
    """测试P6 CPU"""
    Base.run(["copy", Global.FILE_PATH, Global.ASM_PATH])
    generate_code_P6()
    if(Global.COMPARE):
        generate_out_P6()

def generate_code_P7():
    """生成 P7 机器码和标准输出"""
    """生成机器码"""
    asm, mars = Global.ASM_PATH, Global.MARS_P7_PATH
    code_path = Global.CODE_PATH 
    ktext_path, text_path = os.path.join("temp", "ktext.txt"), os.path.join("temp", "text.txt")
    debug = Global.DEBUG
    if(debug): print("generating code (P7)")
    Base.run(["java", "-jar", mars,"ae1","db", "a","me", "nc", "mc", "CompactDataAtZero", "dump", ".text", "HexText", text_path, asm])
    Base.run(["java", "-jar", mars,"ae1","db", "a","me", "nc", "mc", "CompactDataAtZero", "dump", "0x4180-0x6ffc", "HexText", ktext_path, asm])
    with open(text_path, "r") as text_file:
        text = text_file.readlines()
    with open(ktext_path, "r") as ktext_file:
        ktext = ktext_file.readlines()
    with open(code_path, "w") as code_file:
        codes = ["00000000\n" for _ in range(4096)]
        for (i, text_code) in zip(range(len(text)), text):
            codes[i] = text_code
        for (i, ktext_code) in zip(range((0x4180-0x3000)//4, (0x4180-0x3000)//4+len(ktext)), ktext):
            codes[i] = ktext_code
        code_file.write(''.join(codes))
    # with open(code_path, "w") as code_file:
    #     codes = code_file.readlines()
    if(debug): print("generating code finish(P7)")
    if(Global.COPY):
        test_path = Global.TEST
        shutil.copy(code_path, test_path)
    # return
    """生成标准输出"""
    std_path = Global.STD_PATH
    codes += ["00000000"]
    std = []
    if(debug): print("generating std (P7)")
    ret = Base.run(["java","-jar",mars,"ae1", "10000", "ex","db","me","nc","lg","mc","LargeText",asm]).split('\n')
    for str in ret:
        ans = {}
        if(str == ""): break
        ans["instr"] = ans["asm"] = "unknown"
        ans["pc"] = "0x" + str[1:9]
        if(str[11] == "$"):
            ans["RegWrite"] = True
            ans["MemWrite"] = False
            ans["RegAddr"] = str[12:14]
            ans["RegData"] = "0x" + str[18:26]
        else:
            ans["RegWrite"] = False
            ans["MemWrite"] = True
            ans["MemAddr"] = "0x" + str[12:20]
            ans["MemData"] = "0x" + str[24:33]
        std.append(ans)
    with open(std_path, "w") as std_file:
        std_file.write(json.dumps(std, sort_keys=False, indent=4, separators=(',', ': ')))
    if(debug): print("generating code finish (P7)")    
    return  
def generate_out_P7():
    """获取 P7 CPU 输出文件"""
    debug = Global.DEBUG
    if(debug): print("generating out (P7)")
    compiler,argv = Global.COMPILER_TYPE,Global.COMPILER_ARGV
    out_path = Global.OUT_PATH
    code_path = Global.CODE_PATH
    test_branch = os.path.join("Verilog", "P7.v")
    shutil.rmtree("mips_files")
    os.mkdir("mips_files")
    with open("mips_files/.gitignore", "w") as fp:
        fp.write("!.gitignore")
    for file_path in Global.TEST_FILES:
        shutil.copy(file_path, "mips_files")
    shutil.copy(test_branch, "mips_files")
    shutil.copy(code_path, "mips_files")
    if(compiler == "iverilog"):
        ret = Base.run(["cd", "mips_files",
                        "&&", "iverilog",argv,"-o","out", "-s", "tb_P7", "*.v", 
                        "&&", "vvp", "out"], errdesc="编译错误")
        match = re.findall(r"[0-9]*@.*\n",ret)
        # print(match)
        out = []
        for s in match:
            ans = {}
            ans["time"] = re.search(r"[0-9]*@", s).group()[:-1]
            if(re.search(r"@.{10}\$.{14}[\r\n]+", s) != None):
                s = re.search(r"@.{10}\$.{14}[\r\n]+", s).group()
                ans["pc"] = "0x"+s[1:9]
                ans["RegWrite"] = True
                ans["MemWrite"] = False
                ans["RegAddr"] = s[12:14]
                ans["RegData"] = "0x"+s[-10:-2]
                if(ans["RegAddr"] == " 0"): continue # 过滤 $0 寄存器
            else:
                s = re.search(r"@.{10}\*.{20}[\r\n]+", s).group()
                ans["pc"] = "0x"+s[1:9]
                ans["MemWrite"] = True
                ans["RegWrite"] = False
                ans["MemAddr"] = "0x"+s[12:20]
                ans["MemData"] = "0x"+s[-10:-2]
            out.append(ans)
    else:
        pass
    out.sort(key=cmp_to_key(comp))
    with open(out_path,"w") as out_file:
            out_file.write(json.dumps(out, sort_keys=False,
                           indent=4, separators=(',', ': ')))
    if(debug): print("generating out finish (P7)")
    return    
def P7():
    """测试P7 CPU"""
    Base.run(["copy", Global.FILE_PATH, Global.ASM_PATH])
    generate_code_P7()
    if(Global.COMPARE):
        generate_out_P7()

def generate_code_P8():
    """生成 P8 机器码和标准输出"""
    """生成机器码"""
    asm, mars = Global.ASM_PATH, Global.MARS_P7_PATH
    code_path, coe_path = Global.CODE_PATH, Global.COE_PATH
    ktext_path, text_path = os.path.join("temp", "ktext.txt"), os.path.join("temp", "text.txt")
    debug = Global.DEBUG
    if(debug): print("generating code (P8)")
    Base.run(["java", "-jar", mars,"ae1","db", "a","me", "nc", "mc", "CompactDataAtZero", "dump", ".text", "HexText", text_path, asm])
    Base.run(["java", "-jar", mars,"ae1","db", "a","me", "nc", "mc", "CompactDataAtZero", "dump", "0x4180-0x6ffc", "HexText", ktext_path, asm])
    with open(text_path, "r") as text_file:
        text = text_file.readlines()
    with open(ktext_path, "r") as ktext_file:
        ktext = ktext_file.readlines()
    codes = ["00000000\n" for _ in range(4096)]
    coes =  ["00000000,\n" for _ in range(4096)]
    for (i, text_code) in zip(range(len(text)), text):
        codes[i] = text_code
        coes[i] = text_code[:-1] + ",\n"
    for (i, ktext_code) in zip(range((0x4180-0x3000)//4, (0x4180-0x3000)//4+len(ktext)), ktext):
        codes[i] = ktext_code
        coes[i] = ktext_code[:-1] + ",\n"
    with open(code_path, "w") as code_file:
        code_file.write(''.join(codes))
    coes = ["memory_initialization_radix=16;\n","memory_initialization_vector=\n"]+coes[:-1]+[coes[-1][:-2]+";\n"]
    with open(coe_path, "w") as coe_file:
        coe_file.write(''.join(coes))
    if(debug): print("generating code finish(P8)")
    if(Global.COPY):
        test_path = Global.TEST
        shutil.copy(code_path, test_path)
        shutil.copy(coe_path, test_path)
        shutil.copy(Global.FILE_PATH, test_path)
    return

def P8():
    """测试P8 CPU"""
    Base.run(["copy", Global.FILE_PATH, Global.ASM_PATH])
    generate_code_P8()