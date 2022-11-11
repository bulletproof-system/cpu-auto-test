'''
Author: ltt
Date: 2022-10-22 22:12:33
LastEditors: ltt
LastEditTime: 2022-11-09 10:53:47
FilePath: auto_test.py
'''
import modules.Base as Base
import modules.Decode as Decode
import modules.Global as Global
import modules.Generator as Generator
import modules.Comparator as Comparator



def main():
    
    test_type = Global.TEST_TYPE
    if(test_type == "Logisim"):
        Generator.Logisim()
        Comparator.Logisim()
        pass
    elif(test_type == "Verilog"):
        if(Global.P == 4):
            Generator.P4()
        elif (Global.P == 5):
            Generator.P5()
        elif (Global.P == 6):
            Generator.P6() 
        else:
            pass
        Comparator.Verilog()
        pass
    else:
        print("无效测试文件名")
        raise RuntimeError
    return
    
if __name__ == "__main__":
    Decode.init_argv() # 读取参数
    Base.test_env()  # 测试环境
    main() 
 
    