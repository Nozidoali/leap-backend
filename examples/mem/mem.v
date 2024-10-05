module top (
    input [5:0] array,
    input [3:0] indvar,
    output [5:0] mem_addr,
    output mem_rd_en,
    input [3:0] mem_data,
    output [3:0] result
);
    
    wire [3:0] tmp0;
    wire [5:0] tmp1;
    wire [5:0] tmp2;
    assign tmp0 = indvar + 1;
    assign tmp1 = tmp0 << 2;
    assign tmp2 = array + tmp1;
    assign mem_addr = tmp2;
    assign result = mem_data;
    assign mem_rd_en = 1;
endmodule