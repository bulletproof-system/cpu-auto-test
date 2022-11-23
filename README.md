# 利用 python 对 Logisim/Verilog 中搭建的 CPU 进行自动化测试

- 这个项目现在支持对 P3~P6 的数据生成以及自动化测试
- 支持指定汇编文件测试和生成多组数据并测试
- 内置一个数据可以生成 P3~P6 数据的数据生成器，但是数据不是很强，[生成方案](docs\数据生成方案.md) 
- 支持外接其他数据生成器，`DataMakers` 文件夹中引用了评论区的一些数据生成器，见[外接数据生成器](docs\外接数据生成器.md)，侵删
- ~~可能会等到本人写过 P7 才会更新~~
- [项目地址](https://gitee.com/LTT-Repository/cpu-auto-test) 
- [github 同步仓库](https://github.com/bulletproof-system/cpu-auto-test/)

[toc]

## 测试方案

### 测试过程

1. 初始化

   - 处理命令行参数
   - 指定汇编文件测试或生成多组数据并测试
3. Mars 编译指令为机器码并得到标准输出
4. 导入 Logisim/Verilog 并测试
5. 比对输出数据和标准输出数据

### 环境

- python
  - 版本：`python3` 版本大于等于 3.6
  - 依赖的模块：`sys`、`getopt`、`json` 、`subprocess`、`re`、`hashlib`、`os`、`shutil`
- Mars\Mars.jar 魔改过命令行输入
  - 使用 `n<number>` 指定最大仿真步数
  - 输入 `$pc` 以获取 `pc` 的值
  - 输入 `std` 可以打印每条指令的执行信息
  - 忽略 `add` 和 `sub` 溢出
  - 寄存器堆中所有寄存器初值都为 `0` 
  - 忽略地址对齐
  - 修改内容见 [Mars 修改方案](docs/Mars 修改方案.md)
- Logisim.jar
  - 没有改动
- Verilog 环境
  - 支持 `iverilog` 
- Windows 10
  - 系统默认 shell：`cmd`
- Linux 下没有测试过，~~也许可以用~~  

### 注意事项

- 使用 `-P` 指定测试的 Project， `--debug` 输出调试信息
- 对于 P3 使用 `--test` 指定测试文件，如 `D:\LTT\repository\cscore\CPU\P3\P3.circ`
- 对于其他 P 使用 `--test` 指定测试文件夹，如 `D:\LTT\repository\cscore\CPU\P6\code`
- 测试 Logisim 时不会改动源文件，会复制一份到 `output\test.circ` 中再修改该文件的 ROM 以进行测试
- 测试 Verilog 时需要使用 `iverilog` 进行仿真
- 测试 Verilog 时会复制指定测试文件夹下的所有 `.v` 文件到 `mips_files` 文件夹下，除引用公用的宏文件外无需 `include` 其他模块，测试文件夹中可以有无关 `.v` 文件，比如 `tb.v`，但是不能在其中 `include` 其他模块。例如，直接指定向平台提交的文件夹。

#### 指定汇编文件测试

- 使用 `-f` 或 `--filename` 指定测试用的 .asm 文件

- 会在命令行打印比对信息，同时输出到文件，默认在 `output` 文件夹中

- example

	```bash
	echo "test P3"
	python auto_test.py -f example\test_circ.asm --test D:\LTT\repository\cscore\CPU\P3\P3.circ -P 3 --debug 
	
	echo "test P4"
	python auto_test.py -f example\test_P4.asm --test D:\LTT\repository\cscore\CPU\P4 -P 4 --debug 
	
	echo "test P5"
	python auto_test.py -f example\test_P5.asm --test D:\LTT\repository\cscore\CPU\P5 -P 5 --debug 
	
	echo "test P6"
	python auto_test.py -f example\test_P6.asm --test D:\LTT\repository\cscore\CPU\P6 -P 6 --debug 
	```

	

#### 生成多组数据并测试

- 使用 `--gen` 指定数据生成器，`--gen-argv` 提供数据生成器参数，如果数据生成器将数据输出到文件，请指定文件名为 `asm.asm`，如果将数据输出到命令行，则无需更改。

- 支持 `.exe` 以及 `.py` 的数据生成器

- 不指定内置生成器时会调用项目内置的数据生成器

- 使用 `-n` 或 `--number` 指定测试组数，默认 10 组

- 会在命令行打印比对信息，同时输出到文件夹，默认在 `output` 文件夹中

- example

	```bash
	echo "test P3"
	python muti_test.py --test D:\LTT\repository\cscore\CPU\P3\P3.circ -P 3 --debug 
	
	echo "test P4"
	python muti_test.py --test D:\LTT\repository\cscore\CPU\P4 -P 4 --debug 
	
	echo "test P5 内置生成器"
	python muti_test.py --test D:\LTT\repository\cscore\CPU\P5 -P 5 --debug
	
	echo "test P5 外接生成器 P5_Maker_1"
	python muti_test.py --test D:\LTT\repository\cscore\CPU\P5 -P 5 --debug --gen DataMakers\P5_Maker_1\Maker_1.exe
	
	echo "test P5 外接生成器 COgenerator"
	python muti_test.py --test D:\LTT\repository\cscore\CPU\P5 -P 5 --debug --gen DataMakers\COgenerator\COgenerator.exe --gen-argv "asm.asm 200"
	
	echo "test P6 50组数据"
	python muti_test.py --test D:\LTT\repository\cscore\CPU\P6 -P 6 --debug -n 50
	```



​	

## 命令行参数

- 命令行参数列表

  |          参数          |       值       |    默认值    |                     作用                     |
  | :--------------------: | :-------------: | :-----------: | :------------------------------------------: |
  |     `-h,--help`     |      None      |     False     |              展示所有参数并退出              |
  |   `-f,--filename`   |    FILE_PATH    |     None     |  使用指定文件中的指令测试，不指定则随机生成  |
  |    `-n,--number`    |    INSTR_NUM    |      32      |              指定生成的指令个数              |
  | `--debug` | DEBUG | False | 输出调试信息 |
  |    `--output-dir`    |   OUTPUT_DIR   |    output    |                输出所在文件夹                |
  |       `--test`       |    TEST_PATH    |     None     |          P3：测试文件, other：测试文件夹          |
  |     `--compiler`     |  COMPILER_TYPE  |   iverilog   |          编译器(iverilog, vcs, ies)，现在只支持 iverilog          |
  |       `--compile-argv`       |  COMPILER_ARGV  |     None     |              传递给编译器的参数              |
  |   `-P`   |   P   |     5     |               指定测试的 Project               |
  | `--gen` | GENERATOR | None | 指定数据生成器，不指定将使用内置生成器 |
  | `--gen-argv` | GEN_ARGV | None | 传递给数据生成器的参数 |


  - 默认参数在 `setting.json` 中修改
  - ` --filename` 仅可指定 `.asm` 文件

## Bug

- P3 年久失修，使用内置生成器的数据可能会炸
- 不保证外接数据生成器的数据正确性

## Update

### `2022-11-22`

- 参数列表更改
- 支持外接数据生成器
- 优化编译 Verilog 方案，现在只用指定文件夹
- 修复了 `$gp` 、`$sp` 初始值不为 0 的 bug

### `2022-11-14`

- 完成数据生成器

### `2022-11-9`

- 为分别测试 P5 P6，将 `--delay-enbled` 参数改为 `-p n` 的形式，用于指定测试形式
- Mars 添加 `ignore` 参数以忽略溢出和字对齐

### `2022-11-6`

- 增加对流水线 CPU 的对拍功能，使用 `--delay-enbled` 参数
- Mars 寄存器初值全为 0
- Mars 编译错误时会结束程序

### `2022-10-30`

- 进一步魔改 Mars，现在用命令行运行 Mars 时添加 `std` 参数可以输出每条指令执行时的信息，用于生成 std
- 由于生成 std 所需的时间大幅减少，去掉了 MD5 比对
- 重构了 std 生成函数
- 现在会将比对结果同时在 `result.txt` 以及控制台输出
- 在 `Mars/` 目录下添加 Mars 的改动记录文件 `Mars 修改方案.md` 
- 增加 `--debug` 参数

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
