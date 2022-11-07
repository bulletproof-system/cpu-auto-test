'''
Author: ltt
Date: 2022-10-22 22:12:33
LastEditors: ltt
LastEditTime: 2022-11-07 20:47:47
FilePath: auto_test.py
'''
import re
import modules.Base as Base
import modules.Decode as Decode
import modules.Global as Global
import modules.Generator as Generator
import modules.Comparator as Comparator

def test_env(): 
    """测试环境"""
    Base.run([f"java","-version"],errdesc="java not found")
    Base.run(["java", "-jar", Global.MARS_PATH, 'h'], errdesc="mars not found")
    test_type = Global.TEST_TYPE
    if(test_type == "Logisim"):
        try:
            Base.run(["java","-jar",Global.LOGISIM_PATH,"-version"], errdesc="Logisim not found")
        except:
            print("无可用 Logisim.jar")
    elif(test_type == "Verilog"):
        compiler_type = Global.COMPILER_TYPE
        if(compiler_type == "iverilog"):
            try:
                Base.run(["where","iverilog"])
            except:
                print("无可用 verilog 编译器")

def main():
    Decode.init_argv() # 读取参数
    test_env()  # 测试环境
    
    test_type = Global.TEST_TYPE
    if(test_type == "Logisim"):
        Generator.Logisim()
        Comparator.Logisim()
        pass
    elif(test_type == "Verilog"):
        if(Global.DELAY_ENBLED == False):
            Generator.Single_Cycle()
        else:
            Generator.PipeLine()
        Comparator.Verilog()
        pass
    else:
        print("无效测试文件名")
        raise RuntimeError
    return
    
if __name__ == "__main__":
	main() 
 
    