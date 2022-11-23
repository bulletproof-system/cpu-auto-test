'''
Author: ltt
Date: 2022-10-26 20:16:07
LastEditors: ltt
LastEditTime: 2022-11-22 23:40:30
FilePath: Base.py
'''
import subprocess, os

import modules.Global as Global

def run(command, desc=None, errdesc=None):
    """调用命令"""
    if desc is not None:
        print(desc)

    result = subprocess.run(' '.join(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    if result.returncode != 0:
        message = f"""{errdesc or 'Error running command'}.
Command: {' '.join(command)}
Error code: {result.returncode}
stdout: {result.stdout.decode(encoding="gb2312", errors="ignore") if len(result.stdout)>0 else '<empty>'}
stderr: {result.stderr.decode(encoding="gb2312", errors="ignore") if len(result.stderr)>0 else '<empty>'}
"""
        raise RuntimeError(message)
    return result.stdout.decode(encoding="utf8", errors="ignore")

def test_env(): 
    """测试环境"""
    run([f"java","-version"],errdesc="java not found")
    run(["java", "-jar", Global.MARS_PATH, 'h'], errdesc="mars not found")
    test_type = Global.TEST_TYPE
    if(test_type == "Logisim"):
        try:
            run(["java","-jar",Global.LOGISIM_PATH,"-version"], errdesc="Logisim not found")
        except:
            print("无可用 Logisim.jar")
    elif(test_type == "Verilog"):
        compiler_type = Global.COMPILER_TYPE
        if(compiler_type == "iverilog"):
            try:
                run(["where","iverilog"])
            except:
                print("无可用 verilog 编译器")
                
class CompareError(RuntimeError):
    def __init__(self, arg=[]):
        self.args = arg
        
def list_files(path: str, extension: str):
    '''
    遍历 path 目录下所有文件名以 extension 结尾的文件，返回文件名称列表
    例: list_files('src', '.v')
    '''
    result = []
    for path, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                result.append(os.path.join(path, file))
    return result
# print(list_files('src', '.v'))