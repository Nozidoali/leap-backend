module top (
    input [1:0] a,
    input [1:0] b,
    input [1:0] c,
    output [3:0] out
);
    assign out = a + b + c;
endmodule