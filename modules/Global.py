'''
Author: ltt
Date: 2022-10-22 22:17:45
LastEditors: ltt
LastEditTime: 2022-11-28 16:14:32
FilePath: Global.py
'''

shortopts = "hf:n:P:"
longopts = ["help","filename=","copy","number=","debug","output-dir=",
            "test=","compiler=","compile-argv=","gen=","gen-argv="]
FILE_PATH = "FILE_PATH"
TEST_NUM = 100
COPY = False
COMPARE = True
DEBUG = "DEBUG"
OUTPUT_DIR = "OUTPUT_DIR"
ASM_NAME = "ASM_NAME"
ASM_PATH = "ASM_PATH"
CODE_NAME = "CODE_NAME"
CODE_PATH = "CODE_PATH"
RESULT_NAME = "RESULT_NAME"
RESULT_PATH = "RESULT_PATH"
TEST = "TEST"
TEST_FILES = []
TEST_CIRC = "TEST_CIRC"
STD_NAME = "STD_NAME"
STD_PATH = "STD_PATH"
OUT_NAME = "OUT_NAME"
OUT_PATH = "OUT_PATH"
MARS_PATH = "MARS_PATH"
MARS_P7_PATH = "MARS_P7_PATH"
LOGISIM_PATH = "LOGISIM_PATH"
P = 5
COMPILER_TYPE = "COMPILER_TYPE"
COMPILER_ARGV = "COMPILER_ARGV"
GENERATOR = ""
GEN_ARGV = ""
CLASSIFY = {}
ENBLED_INSTRUCTION = []
INSTRUCTION_DICT = {}
ENBLED_CLASS = []
CALC_CLASS = []
MEM_CLASS = []
JUMP_CLASS = []
MD_CLASS = []
TEST_TYPE = "TEST_TYPE"
ROM =r"""<comp lib=\"4\" loc=\"\([0-9]*,[0-9]*\)\" name=\"ROM\">
      <a name=\"addrWidth\" val=\"[0-9]*\"\/>
      <a name=\"dataWidth\" val=\"[0-9]*\"\/>
      <a name=\"contents\">addr\/data:[0-9a-zA-Z \n]*
<\/a>
    <\/comp>"""
label_num = 0