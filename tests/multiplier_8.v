
module multiplier(
    input wire clk,
    input wire [31:0] a,
    input wire [31:0] b,
    output wire [31:0] out
);
    
    reg [31:0] out_0, out_1, out_2, out_3, out_4, out_5, out_6, out_7;
    always @(posedge clk) begin
        out_1 <= out_0;
		out_2 <= out_1;
		out_3 <= out_2;
		out_4 <= out_3;
		out_5 <= out_4;
		out_6 <= out_5;
		out_7 <= out_6;
    end
    assign out = out_7;
    
    
    always @(*) begin
        out_0 <= a * b;
    end
    
endmodule
        