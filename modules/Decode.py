'''
Author: ltt
Date: 2022-10-23 10:45:14
LastEditors: ltt
LastEditTime: 2022-11-28 16:17:41
FilePath: Decode.py
'''

import sys, getopt, json, os

import modules.Global as Global
import modules.Base as Base

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

def merge(DataAtZero, TextAtZero, instructions):
    """合并两个机器码文件"""
    n = len(DataAtZero)
    codes = []
    for i in range(n):
        data_str = DataAtZero[i]
        text_str = TextAtZero[i]
        code = toBin(data_str)
        opcode  = code[::-1][26:32][::-1]
        funct   = code[::-1][0:6][::-1]
        ret = (opcode == "000100")
        codes.append(text_str if ret else data_str)
    return codes

def signextend(code):
    """符号扩展"""
    code = code[0]*(32-len(code)) + code
    if(code[0] == '1'):
        return int(code, 2)-(1<<32)
    else:
        return int(code, 2)

def load_setting(setting):
    """加载配置"""
    Global.FILE_PATH = setting["FILE_PATH"]
    Global.TEST_NUM = setting["TEST_NUM"]
    Global.DEBUG = (setting["DEBUG"] == "true")
    Global.COMPARE = (setting["COMPARE"] == "true")
    Global.OUTPUT_DIR = setting["OUTPUT_DIR"]
    Global.ASM_NAME = setting["ASM_NAME"]
    Global.CODE_NAME  = setting["CODE_NAME"]
    Global.RESULT_NAME  = setting["RESULT_NAME"]
    Global.TEST  = setting["TEST"] 
    Global.TEST_CIRC  = setting["TEST_CIRC"]
    Global.STD_NAME  = setting["STD_NAME"]
    Global.OUT_NAME  = setting["OUT_NAME"]
    Global.MARS_PATH  = setting["MARS_PATH"]
    Global.MARS_P7_PATH  = setting["MARS_P7_PATH"]
    Global.LOGISIM_PATH  = setting["LOGISIM_PATH"]
    Global.P  = setting["P"]
    Global.COMPILER_TYPE  = setting["COMPILER_TYPE"]
    Global.COMPILER_ARGV  = setting["COMPILER_ARGV"]
    Global.CLASSIFY = setting["CLASSIFY"]
    Global.COPY = (setting["COPY"] == "false")
    # Global.ENBLED_INSTRUCTION = setting["ENBLED_INSTRUCTION"]
    # Global.INSTRUCTION_DICT  = setting["INSTRUCTION_DICT"]
    # Global = setting[""]
    
def init_argv():
    """读取参数"""
    setting_file_name = "setting.json"
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], Global.shortopts, Global.longopts)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    try:
        with open(setting_file_name) as setting_file:
            setting = json.load(setting_file)
    except:
        print(f"找不到 {setting_file_name}")
        sys.exit(2)
    if(args != []):
        print(f"多余参数 {args}")
    load_setting(setting)
    for option, value in opts:
        if option in ("-h","--help"):
            print("没写")
            sys.exit(0)
        if option in ("-f","--filename"):
            Global.FILE_PATH = value
        if option in ("-n","--number"):
            Global.TEST_NUM = int(value)
        if option == "--debug":
            Global.DEBUG = True
        if option == "--output-dir":
            Global.OUTPUT_DIR = value
        if option == "--test":
            Global.TEST = value
        if option == "--compilor":
            Global.COMPILER_TYPE = value
        if option == "--compile-argv":
            Global.COMPILER_ARGV = value
        if option == "-P":
            Global.P = int(value)
        if option == "--gen":
            Global.GENERATOR = value
        if option == "--gen-argv":
            Global.GEN_ARGV = value
        if option == "--copy":
            Global.COPY = True
    change_dir()
    Global.ENBLED_INSTRUCTION = setting[f"ENBLED_INSTRUCTION_P{Global.P}"]
    if(Global.P != 3):
        if(Global.TEST != ""):
            Global.TEST_FILES = Base.list_files(Global.TEST, ".v") 
    construct_instruction_dict()
    return setting

def construct_instruction_dict():
    """构造指令字典"""
    for instr in Global.ENBLED_INSTRUCTION:
        Global.INSTRUCTION_DICT[instr] = {}
    for class_name, class_value  in Global.CLASSIFY.items():
        class_value["enbled"] = []
        for instr_name, instr_value in Global.INSTRUCTION_DICT.items():
            if instr_name in class_value["include"]:
                class_value["enbled"].append(instr_name)
                instr_value["class"] = class_name
                instr_value["RegWrite"] = class_value["RegWrite"]
                instr_value["MemWrite"] = class_value["MemWrite"]
                instr_value["jump"] = class_value["jump"]
        if class_value["enbled"] != [] :
            Global.ENBLED_CLASS.append(class_name)
            if(class_name in ("cal_rr", "cal_ri", "mv_to","cal_ru","shift")):
                Global.CALC_CLASS.append(class_name)
            if(class_name in ("load", "store")):
                Global.MEM_CLASS.append(class_name)
            if(class_name in ("br_r1", "br_r2", "jal", "j")):
                Global.JUMP_CLASS.append(class_name)
            if(class_name in ("mul_div")):
                Global.MD_CLASS.append(class_name)
            
def change_dir():
    Global.ASM_PATH = os.path.join(Global.OUTPUT_DIR,Global.ASM_NAME)
    Global.CODE_PATH = os.path.join(Global.OUTPUT_DIR, Global.CODE_NAME)
    Global.RESULT_PATH = os.path.join(Global.OUTPUT_DIR, Global.RESULT_NAME)
    Global.STD_PATH = os.path.join(Global.OUTPUT_DIR, Global.STD_NAME)
    Global.OUT_PATH = os.path.join(Global.OUTPUT_DIR, Global.OUT_NAME)
    Global.TEST_CIRC = os.path.join(Global.OUTPUT_DIR, Global.TEST_CIRC)
    
if __name__ == "__main__":
	print(signextend("1111001100"))