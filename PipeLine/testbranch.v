// `include "mips.v"

module tb (
	
);
	reg clk, reset;
	initial begin
		$dumpfile("wave.vcd");
		$dumpvars();
		clk = 0;
		reset = 1;
		#30 reset = 0;


		#4000 $finish;
	end
	mips mips(.clk(clk), .reset(reset));
	always #20 clk = ~clk;
endmodule //tb