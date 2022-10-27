'''
Author: ltt
Date: 2022-10-22 22:12:33
LastEditors: ltt
LastEditTime: 2022-10-27 14:16:55
FilePath: auto_test.py
'''
import re
import modules.Base as Base
import modules.Decode as Decode
import modules.Constants as Const
import modules.Generator as Generator
import modules.Comparator as Comparator

def test_env(setting): 
    """测试环境"""
    Base.run([f"java","-version"],errdesc="java not found")
    Base.run(["java", "-jar", setting[Const.MARS_PATH], 'h'], errdesc="mars not found")
    test_type = setting[Const.TEST_TYPE]
    if(test_type == "Logisim"):
        try:
            Base.run(["java","-jar",setting[Const.LOGISIM_PATH],"-version"], errdesc="Logisim not found")
        except:
            print("无可用 Logisim.jar")
    elif(test_type == "Verilog"):
        compiler_type = setting[Const.COMPILER_TYPE]
        if(compiler_type == "iverilog"):
            try:
                Base.run(["where","iverilog"])
            except:
                print("无可用 verilog 编译器")

def main():
    setting = Decode.init_argv() # 读取参数
    test_env(setting)  # 测试环境
    
    test_path = setting[Const.TEST_PATH]
    test_type = setting[Const.TEST_TYPE]
    if(test_type == "Logisim"):
        Generator.Logisim(setting)
        Comparator.Logisim(setting)
        pass
    elif(test_type == "Verilog"):
        Generator.Verilog(setting)
        Comparator.Verilog(setting)
        pass
    else:
        print("无效测试文件名")
        raise RuntimeError
    return
    
if __name__ == "__main__":
	main() 
 
    