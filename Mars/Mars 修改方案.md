# Mars 修改方案

## 1. 优化最大仿真步数参数的输入为 `n<number>`

- `venus/MarsLaunch.java`

	- `private boolean parseCommandArgs(String[] args)` 方法

		```java
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

## 2. 增加输出 PC 寄存器的功能

- `mips\hardware\RegisterFile.java`

	- `public static Register getUserRegister(String Rname)` 方法

		```java
		if(Rname.compareTo("$pc") == 0){
		    reg = programCounter;
		}
		```

## 3. 添加命令行参数 `std` 以输出标准输出

- `venus/Globals.java`

	- ```java
		public static boolean outPutStd = false;
		```

- `venus/MarsLaunch.java`

	- `private boolean parseCommandArgs(String[] args)` 方法

		```java
		// 输出 std 信息
		if (args[i].toLowerCase().equals("std")) { 
		    Globals.outPutStd = true;
		    continue;
		}
		```

- `simulator\Simulator.java`

	- `synchronized (Globals.memoryAndRegistersLock)` 同步块中

		输出 pc 值，机器码，汇编码

		```java
		if(GLOBAL.outPutStd){
		    System.out.print("\npc: "+Binary.intToHexString(pc));
		    System.out.print("instr: "+Binary.intToHexString(statement.getBinaryStatement()));
		}
		instruction.getSimulationCode().simulate(statement); // 原有语句
		if(Globals.outPutStd)
		    System.out.print(" asm:"+statement.getPrintableBasicAssemblyStatement()+" ");
		```

- `mips\hardware\RegisterFile.java`

	- `public static int updateRegister(int num, int val)` 方法

		更改寄存器时输出值，忽略 `$0` 寄存器的改变

		```java
		if(Globals.outPutStd)
			System.out.print(String.format("$%2d <= %08x", num, val));
		```

- `mips\hardware\Memory.java`

	- `public int set(int address, int value, int length)` 方法

		内存改变时输出值

		```java
		if(Globals.outPutStd) System.out.print(String.format("*0x%08x <= %08x", address, value));
		```

## 4. add 与 sub 不检测溢出

- `mars\mips\instructions\InstructionSet.java`

	- 注释掉判断溢出的部分

		```java
		instructionList.add(
		                new BasicInstruction("add $t1,$t2,$t3",
		            	 "Addition with overflow : set $t1 to ($t2 plus $t3)",
		                BasicInstructionFormat.R_FORMAT,
		                "000000 sssss ttttt fffff 00000 100000",
		                new SimulationCode()
		               {
		                   public void simulate(ProgramStatement statement) throws ProcessingException
		                  {
		                     int[] operands = statement.getOperands();
		                     int add1 = RegisterFile.getValue(operands[1]);
		                     int add2 = RegisterFile.getValue(operands[2]);
		                     int sum = add1 + add2;
		                  // overflow on A+B detected when A and B have same sign and A+B has other sign.
		                     // if ((add1 >= 0 && add2 >= 0 && sum < 0)
		                     //    || (add1 < 0 && add2 < 0 && sum >= 0))
		                     // {
		                     //    throw new ProcessingException(statement,
		                     //        "arithmetic overflow",Exceptions.ARITHMETIC_OVERFLOW_EXCEPTION);
		                     // }
		                     RegisterFile.updateRegister(operands[0], sum);
		                  }
		               }));
		instructionList.add(
		                new BasicInstruction("sub $t1,$t2,$t3",
		            	 "Subtraction with overflow : set $t1 to ($t2 minus $t3)",
		                BasicInstructionFormat.R_FORMAT,
		                "000000 sssss ttttt fffff 00000 100010",
		                new SimulationCode()
		               {
		                   public void simulate(ProgramStatement statement) throws ProcessingException
		                  {
		                     int[] operands = statement.getOperands();
		                     int sub1 = RegisterFile.getValue(operands[1]);
		                     int sub2 = RegisterFile.getValue(operands[2]);
		                     int dif = sub1 - sub2;
		                  // overflow on A-B detected when A and B have opposite signs and A-B has B's sign
		                     // if ((sub1 >= 0 && sub2 < 0 && dif < 0)
		                     //    || (sub1 < 0 && sub2 >= 0 && dif >= 0))
		                     // {
		                     //    throw new ProcessingException(statement,
		                     //        "arithmetic overflow",Exceptions.ARITHMETIC_OVERFLOW_EXCEPTION);
		                     // }
		                     RegisterFile.updateRegister(operands[0], dif);
		                  }
		               }));
		```

		
