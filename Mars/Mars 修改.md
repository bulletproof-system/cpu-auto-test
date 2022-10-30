# Mars 修改方案

## 0 全局变量

`venus/Globals.java`

- 添加
	- 静态变量 `public static boolean outPutStd = false;` 是否输出 std 信息到命令行

## 1 命令行

### `venus/MarsLaunch.java`

- `private boolean parseCommandArgs(String[] args)`

	- 添加输出 std 信息的参数，优化最大仿真步数参数的输入为 `n<number>`

	- 添加

		```java
		// 输出 std 信息
		if (args[i].toLowerCase().equals("std")) { 
		    Globals.outPutStd = true;
		    continue;
		}
		// Check for stand-alone integer, which is the max execution steps option
		if (args[i].toLowerCase().indexOf("n")==0) {
		    String s = args[i].substring(1);					   
		    try {
		        maxSteps = Integer.decode(s).intValue(); // if we got here, it has to be OK 
		        continue;
		    }             
		    catch (NumberFormatException nfe) {
		    }
		    continue;
		}
		```

		

## 2 仿真器

### `simulator\Simulator.java`

- `synchronized (Globals.memoryAndRegistersLock)` 同步块中

	- 输出当前 pc 值，以及指令

	- 添加

		``` java
		if(GLOBAL.outPutStd){
		    System.out.print("\npc: "+Binary.intToHexString(pc));
		    System.out.print("instr: "+Binary.intToHexString(statement.getBinaryStatement()));
		}
		instruction.getSimulationCode().simulate(statement); // 原有语句
		if(Globals.outPutStd)
		    System.out.print(" asm:"+statement.getPrintableBasicAssemblyStatement()+" ");
		```
		
		

## 3 寄存器堆、数据储存器

### `mips\hardware\RegisterFile.java`

- `public static Register getUserRegister(String Rname)` 方法

	- 增加对 `pc` 的判断

	- 添加

		```java
		if(Rname.compareTo("$pc") == 0){
		    reg = programCounter;
		}
		```

- `public static int updateRegister(int num, int val)` 方法

	- 更改寄存器时输出值

	- 添加

		```java
		if(Globals.outPutStd)
			System.out.print(String.format("$%2d <= %08x", num, val));
		```

- `public static void updateRegister(String reg, int val)` 方法

	- 更改寄存器时输出值

	- 添加

		```java
		if(Globals.outPutStd)
			System.out.print(String.format("$ 0 <= %08x", val));
		```

### `mips\hardware\Memory.java`

- `public int set(int address, int value, int length)` 方法

	- 更改内存时输出值

	- 添加

		```java
		if(Globals.outPutStd) System.out.print(String.format("*0x%08x <= %08x", address, value));
		```

		
