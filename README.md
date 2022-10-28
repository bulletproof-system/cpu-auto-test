# 利用 python 对 Logisim/Verilog 中搭建的 CPU 进行自动化测试

- 引用自文件 [CPU 自动化测试](..\..\..\blog\CPU 自动化测试.md)
- 主目录下有一个样例文件夹 `example`，其中的两个 `bat` 分别用于测试 `.circ` 和 `.v` 文件
- 选择 python 原因：~~不想写 JAVA~~
- 一人役
- 项目地址 [https://gitee.com/LTT-Repository/cpu-auto-test.git](https://sctrack.sendcloud.net/track/click/eyJuZXRlYXNlIjogImZhbHNlIiwgIm1haWxsaXN0X2lkIjogMCwgInRhc2tfaWQiOiAiIiwgImVtYWlsX2lkIjogIjE2NjY4NTc5MTc2NTBfNDIxMjlfMTkzMDFfMzgzMy5zYy0xMF85XzE3OV8xOTctaW5ib3VuZDAkMTcyODkwMTQwOUBxcS5jb20iLCAic2lnbiI6ICIxNTBhNWI2ZWJhMWVhZTU3ZjU3NGMzYzExYzFiZmEyNCIsICJ1c2VyX2hlYWRlcnMiOiB7fSwgImxhYmVsIjogMCwgInRyYWNrX2RvbWFpbiI6ICJzY3RyYWNrLnNlbmRjbG91ZC5uZXQiLCAicmVhbF90eXBlIjogIiIsICJsaW5rIjogImh0dHBzJTNBLy9naXRlZS5jb20vTFRULVJlcG9zaXRvcnkvY3B1LWF1dG8tdGVzdC5naXQiLCAib3V0X2lwIjogIjEwNi43NS43Mi42MiIsICJjb250ZW50X3R5cGUiOiAzLCAidXNlcl9pZCI6IDQyMTI5LCAib3ZlcnNlYXMiOiAiZmFsc2UiLCAiY2F0ZWdvcnlfaWQiOiAxMjIyNjh9.html)

[toc]

## 0. 测试方案

### 测试过程

1. 初始化

   - 处理命令行参数
   - 指定指令测试
   - 生成指令并测试(未实现)

     - 加载可用指令列表以及指令模板
     - 确定生成指令个数
     - 确定指令执行次数
2. 随机生成指令(未实现)

   - 寄存器运算指令
     - 避免使用未初始化的寄存器
   - 与立即数运算的指令
     - 增大边界数据生成权重
   - 跳转指令
     - 随机生成易导致死循环，一般进行独立测试或套用模板
3. Mars 编译指令为机器码并得到标准输出
4. 导入 Logisim/Verilog 并测试
5. 比对输出数据和标准输出数据

### 环境

- python
  - 版本：`python3` 版本大于等于 3.6
  - 依赖的模块：`sys`、`getopt`、`json` 、`subprocess`、`re`、`hashlib`、`os`
- \Mars.jar 魔改过命令行输入
  - 使用 `n<number>` 指定最大仿真步数
  - 输入 `$pc` 以获取 `pc` 的值
  - 为了交上去 Mars 文件夹中只剩了 Mars.jar
- Logisim.jar
  - 没有改动
  - 为了交上去会删除 Logisim文件夹中 Logisim.jar
- Windows 10
  - 系统默认 shell：`cmd`

## 1. 初始化

### 读取命令行参数

- 命令行参数列表

  |          参数          |       值       |    默认值    |                     作用                     |
  | :--------------------: | :-------------: | :-----------: | :------------------------------------------: |
  |     `-h,--help`     |      None      |     False     |              展示所有参数并退出              |
  |   `-f,--filename`   |    FILE_PATH    |     None     |  使用指定文件中的指令测试，不指定则随机生成  |
  |    `-n,--number`    |    INSTR_NUM    |      32      |              指定生成的指令个数              |
  | `-m,--max-execution` | EXECUTION_TIME |      100      |               指令最多执行次数               |
  |         `-b`         |      None      |     False     |         利用原 std 文件直接比对数据         |
  |      `--force`      |      None      |     False     |     强制重新生成 std 文件，优先于 `-b`     |
  |    `--output-dir`    |   OUTPUT_DIR   |    output/    |                输出所在文件夹                |
  |       `--asm`       |    ASM_NAME    |    asm.asm    |                指令保存文件名                |
  |       `--code`       |    CODE_NAME    |   code.txt   |               机器码保存文件名               |
  |      `--result`      |   RESULT_NAME   |  result.txt  |                 输出比对结果                 |
  |       `--test`       |    TEST_PATH    |     None     |          测试文件路径(*.circ, *.v)          |
  |     `--compiler`     |  COMPILER_TYPE  |   iverilog   |          编译器(iverilog, vcs, ies)          |
  |       `--argv`       |  COMPILER_ARGV  |     None     |              传递给编译器的参数              |
  |       `--std`       |    STD_NAME    |   std.json   |                 标准输出结果                 |
  |       `--out`       |    OUT_NAME    |   out.json   |               测试程序输出结果               |
  |       `--mars`       |    MARS_PATH    | Mars\Mars.jar |                  Mars 路径                  |
  |     `--logisim`     |  LOGISIM_PATH  |  logisim.jar  |                 Logisim 路径                 |
  |   `--jump-enbled`   |   JUMP_ENBLED   |     false     |               是否生成跳转指令               |
  | `--default-setting` | DEFAULT_SETTING | setting.json | 如果指定将使用文件中的配置并忽略其他所有参数 |


  - 默认参数在 `setting.json` 中修改
  - ` --filename` 仅可指定 `.asm` 文件
  - 根据测试文件后缀名进行测试
- `setting.json` 参数列表

  - 同上
  - ```json
      "INSTRUCTION_LIST" : [
          {
              "name" : "add",
              "opcode" : "000000",
              "funct" : "100000",
              "RegWrite" : true,
              "RegAddr" : ["rd"],
              "MemWrite" : false,
              "jump" : false,
              "weight" : 2
          },
          {
              "name" : "sub",
              "opcode" : "000000",
              "funct" : "100010",
              "RegWrite" : true,
              "RegAddr" : ["rd"],
              "MemWrite" : false,
              "jump" : false,
              "weight" : 2
          },
          {
              "name" : "ori",
              "opcode" : "001101",
              "RegWrite" : true,
              "RegAddr" : ["rt"],
              "MemWrite" : false,
              "jump" : false,
              "weight" : 2
          },
          {
              "name" : "lw",
              "opcode" : "100011",
              "RegWrite" : true,
              "RegAddr" : ["rt"],
              "MemWrite" : false,
              "jump" : false,
              "weight" : 2
          },
          {
              "name" : "sw",
              "opcode" : "101011",
              "RegWrite" : false,
              "MemWrite" : true,
              "MemAddr" : ["rt","offset"],
              "jump" : false,
              "weight" : 2
          },
          {
              "name" : "beq",
              "opcode" : "000100",
              "RegWrite" : false,
              "MemWrite" : false,
              "jump" : true,
              "weight" : 2
          },
          {
              "name" : "lui",
              "opcode" : "001111",
              "RegWrite" : true,
              "RegAddr" : ["rt"],
              "MemWrite" : false,
              "jump" : false,
              "weight" : 2
          },
          {
              "name" : "nop",
              "opcode" : "000000",
              "funct" : "000000",
              "RegWrite" : false,
              "MemWrite" : false,
              "jump" : false,
              "weight" : 1
          },
          {
              "name" : "j",
              "opcode" : "000010",
              "RegWrite" : false,
              "MemWrite" : false,
              "jump" : true,
              "weight" : 1
          },
          {
              "name" : "jal",
              "opcode" : "000011",
              "RegWrite" : true,
              "RegAddr" : ["pc"],
              "MemWrite" : false,
              "jump" : true,
              "weight" : 1
          },
          {
              "name" : "jr",
              "opcode" : "000000",
              "funct" : "001000",
              "RegWrite" : false,
              "MemWrite" : false,
              "jump" : true,
              "weight" : 1
          }
      ]
    ```

### 根据 `FILE_PATH` 有无判断是否生成指令

- `FILE_PATH` 有值则跳过 [2. 指令生成](##2. 指令生成)

## 2. 指令生成

pass

## 3.1 Logisim 机器码及 STD 生成

- 当两次输入文件一致时或指定了 `-b` 时会跳过，除非指定了 `--force`
- 调用 `Mars` 从 `ASM_NAME` 文件生成机器码保存至 `CODE_NAME` 中，并同时生成标准输出文件 `STD_NAME`

### 3.1.1 生成机器码

- 生成数据段从 0 开始的机器码

  ```bash
  java -jar Mars\Mars.jar me nc mc CompactDataAtZero dump .text HexText {DATA_PATH} {ASM_PATH}
  ```
- 生成代码段从 0 开始的机器码

  ```bash
  java -jar Mars\Mars.jar me nc mc CompactTextAtZero dump .text HexText {TEXT_PATH} {ASM_PATH}
  ```
- 根据不同指令合并得到所需机器码

### 3.1.2 生成标准输出

- 枚举 0 ~  MAX_EXE，首先获取第 i 次指令的 pc 地址

  ```bash
  java -jar Mars\Mars.jar n{i} nc $pc mc CompactDataAtZero {ASM_PATH}
  ```

  将 pc - 0x00003000 后得到代码段从 0 开始的地址，从而得到当前正在执行的指令 `instr`
- 将 `instr` 转换为二进制 `code`，根据指令可以得到当前指令改变的寄存器编号或者内存地址，再调用 Mars 得到当前指令改变的寄存器值或者内存值，可以形成如下字典

  ```json
  {
      "instr": "",
      "code": "",
      "RegWrite": true,
      "RegAddr": "",
      "RegData": "",
      "MemWrite": false,
      "MemAddr": "",
      "MemData": ""
  },
  ```

  最终得到 std 文件

## 3.2 Verilog 机器码及 STD 生成

- 当两次输入文件一致时或指定了 `-b` 时会跳过，除非指定了 `--force`
- 调用 `Mars` 从 `ASM_NAME` 文件生成机器码保存至 `CODE_NAME` 中，并同时生成标准输出文件 `STD_NAME`

### 3.2.1 生成机器码

- 生成数据段从 0 开始的机器码

  ```bash
  java -jar Mars\Mars.jar me nc mc CompactDataAtZero dump .text HexText {DATA_PATH} {ASM_PATH}
  ```
- 直接得到所需机器码

### 3.2.2 生成标准输出

- 枚举 0 ~  MAX_EXE，首先获取第 i 次指令的 pc 地址

  ```bash
  java -jar Mars\Mars.jar n{i} nc $pc mc CompactDataAtZero {ASM_PATH}
  ```

  将 pc - 0x00003000 后得到代码段从 0 开始的地址，从而得到当前正在执行的指令 `instr`
- 将 `instr` 转换为二进制 `code`，根据指令可以得到当前指令改变的寄存器编号或者内存地址，再调用 Mars 得到当前指令改变的寄存器值或者内存值，可以形成如下字典

  ```json
  {
      "instr": "",
      "code": "",
      "RegWrite": true,
      "RegAddr": "",
      "RegData": "",
      "MemWrite": false,
      "MemAddr": "",
      "MemData": ""
  },
  ```

  最终得到 std 文件

## 4.1 导入 Logisim 测试

- `TEST_PATH` 所指定的文件后缀为 .circ
- Logisim 测试文件在 Logisim 文件夹中
- 使用命令行输出 `out` 文件

## 4.2 导入 Verilog 测试

- `TEST_PATH` 所指定的文件后缀为 .v
- 将 `testbranch.v` 文件与输入的顶层模块一起编译，仿真后得到输出
- 根据输出格式化得到 `out` 文件

## 5.1 Logisim 比对输出

- 对 `code`、`RegWrite`、`RegAddr`、`RegData`、`MemWrite`、`Memaddr`、`MemData` 按 `code` 值不同分情况比对
- 在第一个错误处退出程序并打印 `std` 和 `out` 中对应数据
- 全部相同输出 `Accepted`

## 5.2 Verilog 比对输出

- 对 `pc`、`RegAddr`、`RegData`、`MemAddr`、`MemData` 分情况比对
- 在第一个错误处退出程序并打印 `std` 和 `out` 中对应数据
- 全部相同输出 `Accepted`

## 6 Bug

- 还没完全测试过
- 没有实现汇编代码自动生成，只支持用现有的汇编文件测试
- 由于有时候 Mars 在出错时返回值是 0 可能导致程序继续进行而不终止

## 7 Update

### `2022-10-28`

- Verilog 比对时无视 `$ 0` 的写入数据

### `2022-10-27`

- 重建仓库
- 添加了 `example` 样例文件夹

### `2022-10-26`

- 重构了工程结构
- 支持测试 Verilog，但只支持使用 `iverilog` 编译

### `2022-10-24`

- 修改了向 ROM 数据时的 bug
- 因为多次调用 `Mars` 使得生成 std 文件速度巨慢，现在当输入文件一致时不会重新生成 std 文件，除非指定 `--force` 选项

### `2022-10-23`

- 完成整个框架的搭建，可以实现 Logisim 的测试
