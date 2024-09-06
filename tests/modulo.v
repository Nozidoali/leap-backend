
module modulo(
    input wire clk,
    input wire [31:0] a,
    input wire [31:0] b,
    output wire [31:0] out
);
    
    reg [31:0] out_0, out_1, out_2, out_3, out_4, out_5, out_6, out_7, out_8, out_9, out_10, out_11, out_12, out_13, out_14, out_15, out_16, out_17, out_18, out_19, out_20, out_21, out_22, out_23, out_24, out_25, out_26, out_27, out_28, out_29, out_30, out_31, out_32, out_33, out_34, out_35, out_36, out_37, out_38, out_39, out_40, out_41, out_42, out_43, out_44, out_45, out_46, out_47, out_48, out_49;
    always @(posedge clk) begin
        out_1 <= out_0;
		out_2 <= out_1;
		out_3 <= out_2;
		out_4 <= out_3;
		out_5 <= out_4;
		out_6 <= out_5;
		out_7 <= out_6;
		out_8 <= out_7;
		out_9 <= out_8;
		out_10 <= out_9;
		out_11 <= out_10;
		out_12 <= out_11;
		out_13 <= out_12;
		out_14 <= out_13;
		out_15 <= out_14;
		out_16 <= out_15;
		out_17 <= out_16;
		out_18 <= out_17;
		out_19 <= out_18;
		out_20 <= out_19;
		out_21 <= out_20;
		out_22 <= out_21;
		out_23 <= out_22;
		out_24 <= out_23;
		out_25 <= out_24;
		out_26 <= out_25;
		out_27 <= out_26;
		out_28 <= out_27;
		out_29 <= out_28;
		out_30 <= out_29;
		out_31 <= out_30;
		out_32 <= out_31;
		out_33 <= out_32;
		out_34 <= out_33;
		out_35 <= out_34;
		out_36 <= out_35;
		out_37 <= out_36;
		out_38 <= out_37;
		out_39 <= out_38;
		out_40 <= out_39;
		out_41 <= out_40;
		out_42 <= out_41;
		out_43 <= out_42;
		out_44 <= out_43;
		out_45 <= out_44;
		out_46 <= out_45;
		out_47 <= out_46;
		out_48 <= out_47;
		out_49 <= out_48;
    end
    assign out = out_49;
    
    
    always @(*) begin
        out_0 <= a % b;
    end
    
endmodule
        