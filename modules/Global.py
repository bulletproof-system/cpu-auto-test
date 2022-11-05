'''
Author: ltt
Date: 2022-10-22 22:17:45
LastEditors: ltt
LastEditTime: 2022-11-04 23:00:47
FilePath: Global.py
'''

shortopts = "hf:n:m:b"
longopts = ["help","filename=","number=","max-execution=","force","debug","output-dir=",
            "asm=","code=","result=","test=","compiler=","argv=","std=","out=","mars=",
            "logisim=","delay-enbled=","default-setting="]
FILE_PATH = "FILE_PATH"
INSTR_NUM = "INSTR_NUM"
EXECUTION_TIME = "EXECUTION_TIME"
SKIP = "SKIP"
FORCE = "FORCE"
DEBUG = "DEBUG"
OUTPUT_DIR = "OUTPUT_DIR"
ASM_NAME = "ASM_NAME"
ASM_PATH = "ASM_PATH"
CODE_NAME = "CODE_NAME"
CODE_PATH = "CODE_PATH"
RESULT_NAME = "RESULT_NAME"
RESULT_PATH = "RESULT_PATH"
TEST_PATH = "TEST_PATH"
TEST_CIRC = "TEST_CIRC"
STD_NAME = "STD_NAME"
STD_PATH = "STD_PATH"
OUT_NAME = "OUT_NAME"
OUT_PATH = "OUT_PATH"
MARS_PATH = "MARS_PATH"
LOGISIM_PATH = "LOGISIM_PATH"
DELAY_ENBLED = "DELAY_ENBLED"
COMPILER_TYPE = "COMPILER_TYPE"
COMPILER_ARGV = "COMPILER_ARGV"
INSTRUCTION_LIST = "INSTRUCTION_LIST"
TEST_TYPE = "TEST_TYPE"
ROM =r"""<comp lib=\"4\" loc=\"\([0-9]*,[0-9]*\)\" name=\"ROM\">
      <a name=\"addrWidth\" val=\"[0-9]*\"\/>
      <a name=\"dataWidth\" val=\"[0-9]*\"\/>
      <a name=\"contents\">addr\/data:[0-9a-zA-Z \n]*
<\/a>
    <\/comp>"""
# INSTRUCTION_LIST = [
# 	{
# 			"name" : "add",
# 			"type" : "R",
# 			"jump" : False,
# 			"weight" : 2
# 		},
# 		{
# 			"name" : "sub",
# 			"type" : "R",
# 			"jump" : False,
# 			"weight" : 2
# 		},
# 		{
# 			"name" : "ori",
# 			"type" : "I",
# 			"jump" : False,
# 			"weight" : 2
# 		},
# 		{
# 			"name" : "lw",
# 			"type" : "I",
# 			"jump" : False,
# 			"weight" : 2
# 		},
# 		{
# 			"name" : "sw",
# 			"type" : "I",
# 			"jump" : False,
# 			"weight" : 2
# 		},
# 		{
# 			"name" : "beq",
# 			"type" : "I",
# 			"jump" : True,
# 			"weight" : 2
# 		},
# 		{
# 			"name" : "lui",
# 			"type" : "I",
# 			"jump" : False,
# 			"weight" : 2
# 		},
# 		{
# 			"name" : "nop",
# 			"type" : "S",
# 			"jump" : False,
# 			"weight" : 1
# 		}
# ]
