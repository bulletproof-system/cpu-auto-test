'''
Author: ltt
Date: 2022-11-07 20:52:32
LastEditors: ltt
LastEditTime: 2022-11-07 22:07:23
FilePath: muti_test.py
'''
import modules.Base as Base
import modules.Decode as Decode
import modules.Global as Global
import modules.DataMaker as DataMaker
import modules.InstrGenerator as IG
import auto_test

def main():
    # auto_test.main()
    pass

if __name__ == "__main__":
    Decode.init_argv() # 读取参数
    Base.test_env() # 测试环境
    main()
    # Decode.init_argv() # 读取参数
    # IG.print_mips(IG.construct_instr("add",1,2,0))
    # IG.print_mips(IG.construct_instr("nop"))
    # IG.print_mips(IG.construct_instr("beq",1,2,"label"))
    # IG.print_mips(IG.construct_instr("ori",1,2,123213))
    # IG.print_mips(IG.construct_instr("jal","cases"))