
module adder(
    input wire clk,
    input wire [31:0] a,
    input wire [31:0] b,
    output wire [31:0] out
);
    
    reg [31:0] out_0, out_1, out_2;
    always @(posedge clk) begin
        out_1 <= out_0;
		out_2 <= out_1;
    end
    assign out = out_2;
    
    
    always @(*) begin
        out_0 <= a + b;
    end
    
endmodule
        