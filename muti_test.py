'''
Author: ltt
Date: 2022-11-07 20:52:32
LastEditors: ltt
LastEditTime: 2022-11-28 16:21:23
FilePath: muti_test.py
'''
import modules.Base as Base
import modules.Decode as Decode
import modules.Global as Global
import modules.DataMaker as DataMaker
import modules.InstrGenerator as IG
import auto_test, os


def main():
    wrong_test = []
    if(Global.COMPARE == False):
        print("未指定测试文件，仅在 test_file 文件夹下生成数据")
    for i in range(1, Global.TEST_NUM+1):
        Global.FILE_PATH = os.path.join("test_file", f"P{Global.P}_test_{i}.asm")
        if(Global.DEBUG):
            print(f"generate data file \"{Global.FILE_PATH}\"")
        with open(Global.FILE_PATH, "w") as fp:
            if Global.GENERATOR == "":
                data = DataMaker.makedata(10)
            else:
                data = DataMaker.get_data_from()
            fp.write(data)
        if(Global.COMPARE):
            Global.OUTPUT_DIR = os.path.join("output", f"P{Global.P}_test_{i}")
            Decode.change_dir()
            if not os.path.exists(Global.OUTPUT_DIR):
                os.mkdir(Global.OUTPUT_DIR)
            try:
                auto_test.main()
            except Base.CompareError:
                wrong_test.append(i)
            if(wrong_test != []):
                print("wrong result in test %s" % " ".join(str(x) for x in wrong_test))
            else:
                print("all Accepted")
if __name__ == "__main__":
    Decode.init_argv()  # 读取参数
    Base.test_env()  # 测试环境
    main()
    # Decode.init_argv() # 读取参数
    # IG.print_mips(IG.construct_instr("add",1,2,0))
    # IG.print_mips(IG.construct_instr("nop"))
    # IG.print_mips(IG.construct_instr("beq",1,2,"label"))
    # IG.print_mips(IG.construct_instr("ori",1,2,123213))
    # IG.print_mips(IG.construct_instr("jal","cases"))
