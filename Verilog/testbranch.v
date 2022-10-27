`timescale 1ns / 1ps

module tb;

	// Inputs
	reg clk;
	reg reset;

	// Instantiate the Unit Under Test (UUT)
	mips uut (
		.clk(clk), 
		.reset(reset)
	);

	initial begin
		// Initialize Inputs
		// $dumpfile("wave.vcd");
		// $dumpvars();
		clk = 0;
		reset = 1;
		#30 reset = 0;

		#4000 $finish;
	end
    always #20 clk = ~clk;
endmodule

