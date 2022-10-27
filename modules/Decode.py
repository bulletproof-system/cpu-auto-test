'''
Author: ltt
Date: 2022-10-23 10:45:14
LastEditors: ltt
LastEditTime: 2022-10-27 11:11:09
FilePath: Decode.py
'''

import sys, getopt, json, re, hashlib

import modules.Constants as Const

def toBin(string):
    """十六进制字符串转二进制"""
    ret = ""
    for c in string:
        if(c == '0'): ret += "0000"
        if(c == '1'): ret += "0001"
        if(c == '2'): ret += "0010"
        if(c == '3'): ret += "0011"
        if(c == '4'): ret += "0100"
        if(c == '5'): ret += "0101"
        if(c == '6'): ret += "0110"
        if(c == '7'): ret += "0111"
        if(c == '8'): ret += "1000"
        if(c == '9'): ret += "1001"
        if(c == 'a'): ret += "1010"
        if(c == 'b'): ret += "1011"
        if(c == 'c'): ret += "1100"
        if(c == 'd'): ret += "1101"
        if(c == 'e'): ret += "1110"
        if(c == 'f'): ret += "1111"
    return ret.strip(' ')

def findInList(instr,instructions):
    """在表中查找特定指令"""
    code = toBin(instr)
    opcode  = code[::-1][26:32][::-1]
    funct   = code[::-1][0:6][::-1]
    for x in instructions:
        if x["opcode"] == opcode:
            if opcode == "000000":
                if x["funct"] != funct:
                    continue
            return x
    message = f"指令集中找不到对应指令 {instr} {code}"
    raise RuntimeError(message) 

def merge(DataAtZero, TextAtZero, instructions):
    """合并两个机器码文件"""
    n = len(DataAtZero)
    codes = []
    for i in range(n):
        data_str = DataAtZero[i]
        text_str = TextAtZero[i]
        ret = findInList(data_str, instructions)
        codes.append(text_str if ret["jump"] else data_str)
    return codes

def signextend(code):
    """符号扩展"""
    code = code[0]*(32-len(code)) + code
    if(code[0] == '1'):
        return int(code, 2)-(1<<32)
    else:
        return int(code, 2)

def init_argv():
    """读取参数"""
    setting_file_name = "setting.json"
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], Const.shortopts, Const.longopts)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for option, value in opts:
        if option in ("--default-setting"):
            setting_file_name = value
            try:
                with open(setting_file_name) as setting_file:
                    setting = json.load(setting_file)
            except:
                print(f"找不到 {setting_file_name}")
                sys.exit(2)
            return setting
    try:
        with open(setting_file_name) as setting_file:
            setting = json.load(setting_file)
    except:
        print(f"找不到 {setting_file_name}")
        sys.exit(2)
    if(args != []):
        print(f"多余参数 {args}")
    for option, value in opts:
        if option in ("-h","--help"):
            print("没写")
            sys.exit(0)
        if option in ("-f","--filename"):
            setting[Const.FILE_PATH] = value
        if option in ("-n","--number"):
            setting[Const.INSTR_NUM] = value
        if option in ("-m","--max-execution"):
            setting[Const.EXECUTION_TIME] = value
        if option in ("-b"):
            setting[Const.SKIP] = True
        if option == "--force":
            setting[Const.FORCE] = True
        if option in ("--output-dir"):
            setting[Const.OUTPUT_DIR] = value
        if option in ("--asm"):
            setting[Const.ASM_NAME] = value
        if option in ("--code"):
            setting[Const.ASM_NAME] = value
        if option in ("--result"):
            setting[Const.RESULT_NAME] = value
        if option in ("--test"):
            setting[Const.TEST_PATH] = value
        if option in ("--compilor"):
            setting[Const.COMPILER_TYPE] = value
        if option in ("--argv"):
            setting[Const.COMPILER_ARGV] = value
        if option in ("--std"):
            setting[Const.STD_NAME] = value
        if option in ("--out"):
            setting[Const.OUT_NAME] = value
        if option in ("--mars"):
            setting[Const.MARS_PATH] = value
        if option in ("--logisim"):
            setting[Const.LOGISIM_PATH] = value
        if option in ("--jump-enbled"):
            setting[Const.JUMP_ENBLED] = value
    setting[Const.ASM_PATH] = f"{setting[Const.OUTPUT_DIR]}"+"\\"+f"{setting[Const.ASM_NAME]}"
    setting[Const.CODE_PATH] = f"{setting[Const.OUTPUT_DIR]}"+"\\"+f"{setting[Const.CODE_NAME]}"
    setting[Const.RESULT_PATH] = f"{setting[Const.OUTPUT_DIR]}"+"\\"+f"{setting[Const.RESULT_NAME]}"
    setting[Const.STD_PATH] = f"{setting[Const.OUTPUT_DIR]}"+"\\"+f"{setting[Const.STD_NAME]}"
    setting[Const.OUT_PATH] = f"{setting[Const.OUTPUT_DIR]}"+"\\"+f"{setting[Const.OUT_NAME]}"
    test_path = setting[Const.TEST_PATH]
    if(re.search(".circ",test_path) != None):
        setting[Const.TEST_TYPE] = "Logisim"
    elif(re.search(".v",test_path) != None):
        setting[Const.TEST_TYPE] = "Verilog"
    else:
        pass
    if(setting[Const.FORCE]): 
        setting[Const.SKIP] = False
        return setting
    if(setting[Const.FILE_PATH]):
        try:
            file_md5_path = setting[Const.FILE_MD5]
            code_md5_path = setting[Const.CODE_MD5]
            std_md5_path = setting[Const.STD_MD5]
            last_md5_path = setting[Const.LAST_MD5]
            file_path = setting[Const.FILE_PATH]
            code_path = setting[Const.CODE_PATH]
            std_path = setting[Const.STD_PATH]
            last_md5 = setting[Const.TEST_TYPE]
            with open(file_md5_path, "r") as fp:
                file_md5_old = fp.read()
            with open(code_md5_path, "r") as fp:
                code_md5_old = fp.read()
            with open(std_md5_path, "r") as fp:
                std_md5_old = fp.read()
            with open(last_md5_path, "r") as fp:
                last_md5_old = fp.read()
            with open(file_path, "r", encoding="utf-8") as fp:
                file_str = fp.read()
                file_md5 = hashlib.md5(file_str.encode("utf-8")).hexdigest()
            with open(code_path, "r", encoding="utf-8") as fp:
                code_str = fp.read()
                code_md5 = hashlib.md5(code_str.encode("utf-8")).hexdigest()
            with open(std_path, "r", encoding="utf-8") as fp:
                std_str = fp.read()
                std_md5 = hashlib.md5(std_str.encode("utf-8")).hexdigest()
            if(file_md5 == file_md5_old and code_md5 == code_md5_old and std_md5 == std_md5_old and last_md5_old == last_md5):
                setting[Const.SKIP] = True
                print("输入文件相同，直接进行比对")
        except:
            pass
    
    if(re.search(".circ",test_path) != None):
        setting[Const.TEST_TYPE] = "Logisim"
    elif(re.search(".v",test_path) != None):
        setting[Const.TEST_TYPE] = "Verilog"
    else:
        pass
    return setting

if __name__ == "__main__":
	print(signextend("1111001100"))