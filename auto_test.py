'''
Author: ltt
Date: 2022-10-22 22:12:33
LastEditors: ltt
LastEditTime: 2022-11-23 00:20:36
FilePath: auto_test.py
'''
import modules.Base as Base
import modules.Decode as Decode
import modules.Global as Global
import modules.Generator as Generator
import modules.Comparator as Comparator



def main():
    
    P = Global.P
    if(P == 3):
        Generator.P3()
        Comparator.P3()
    if(Global.P == 4):
        Generator.P4()
        Comparator.Verilog()
    elif (Global.P == 5):
        Generator.P5()
        Comparator.Verilog()
    elif (Global.P == 6):
        Generator.P6() 
        Comparator.Verilog()
    else:
        pass
    return 0
    
if __name__ == "__main__":
    Decode.init_argv() # 读取参数
    Base.test_env()  # 测试环境
    main() 
 
    