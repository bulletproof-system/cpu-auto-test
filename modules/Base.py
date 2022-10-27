'''
Author: ltt
Date: 2022-10-26 20:16:07
LastEditors: ltt
LastEditTime: 2022-10-26 23:19:59
FilePath: Base.py
'''
import subprocess

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