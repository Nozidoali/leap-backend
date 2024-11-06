module top(
arg_c_reg, 
arg_A_reg, 
gaussian_loopexitloopexit_1_reg_enablePhi_BB_1, 
gaussian_lrph_indvar4_reg_enablePhi_BB_4, 
LOOP22_1_inductionVar_stage0_enablePhi_BB_5, 
ngaussian_loopexitloopexit_1_reg_pi_BB_1, 
nLOOP22_1_inductionVar_stage0_pi_BB_5, 
ngaussian_lrph_indvar4_reg_pi_BB_4, 
loaddd_A_a_0_fromMem, 
loaddd_A_b_0_fromMem, 
loaddd_c_a_0_fromMem, 
legup_mult_gaussian_11_17_result, 
clk, 
rst, 
endCircuit_endCircuitPI, 
endCircuit, 
n282_ctrlOut_BB_6, 
ngaussian_loopexitloopexit_8_reg_po_BB_1, 
n386_po_BB_5, 
ngaussian_20_21_po_BB_4, 
storeee_A_a_0_toMem, 
storeee_A_a_0_addr, 
loaddd_A_a_0_addr, 
loaddd_A_b_0_addr, 
loaddd_c_a_0_addr, 
legup_mult_gaussian_11_17_in1, 
legup_mult_gaussian_11_17_in2, 
n217_ctrlOut_BB_1, 
n382_ctrlOut_BB_5, 
gaussian_loopexitloopexit_3_reg_anchorPo_BB_1_BB_4, 
gaussian_loopexitloopexit_5_reg_anchorPo_BB_1_BB_6, 
gaussian_loopexitloopexit_6_reg_anchorPo_BB_1_BB_5, 
gaussian_loopexitloopexit_scevgep11_reg_anchorPo_BB_1_BB_5, 
gaussian_20_21_anchorPo_BB_4_BB_6, 
gaussian_lrph_10_reg_anchorPo_BB_4_BB_5
);
input [31:0] arg_c_reg;
input [31:0] arg_A_reg;
input gaussian_loopexitloopexit_1_reg_enablePhi_BB_1;
input gaussian_lrph_indvar4_reg_enablePhi_BB_4;
input LOOP22_1_inductionVar_stage0_enablePhi_BB_5;
input [3:0] ngaussian_loopexitloopexit_1_reg_pi_BB_1;
input [31:0] nLOOP22_1_inductionVar_stage0_pi_BB_5;
input [31:0] ngaussian_lrph_indvar4_reg_pi_BB_4;
input [31:0] loaddd_A_a_0_fromMem;
input [31:0] loaddd_A_b_0_fromMem;
input [31:0] loaddd_c_a_0_fromMem;
input [63:0] legup_mult_gaussian_11_17_result;
input clk;
input rst;
input endCircuit_endCircuitPI;
output endCircuit;
output n282_ctrlOut_BB_6;
output [3:0] ngaussian_loopexitloopexit_8_reg_po_BB_1;
output [31:0] n386_po_BB_5;
output [31:0] ngaussian_20_21_po_BB_4;
output [31:0] storeee_A_a_0_toMem;
output [7:0] storeee_A_a_0_addr;
output [7:0] loaddd_A_a_0_addr;
output [7:0] loaddd_A_b_0_addr;
output [3:0] loaddd_c_a_0_addr;
output [63:0] legup_mult_gaussian_11_17_in1;
output [63:0] legup_mult_gaussian_11_17_in2;
output n217_ctrlOut_BB_1;
output n382_ctrlOut_BB_5;
output [9:0] gaussian_loopexitloopexit_3_reg_anchorPo_BB_1_BB_4;
output [6:0] gaussian_loopexitloopexit_5_reg_anchorPo_BB_1_BB_6;
output [9:0] gaussian_loopexitloopexit_6_reg_anchorPo_BB_1_BB_5;
output [31:0] gaussian_loopexitloopexit_scevgep11_reg_anchorPo_BB_1_BB_5;
output [31:0] gaussian_20_21_anchorPo_BB_4_BB_6;
output [31:0] gaussian_lrph_10_reg_anchorPo_BB_4_BB_5;
wire [3:0] gaussian_loopexitloopexit_1_reg;
wire [4:0] gaussian_loopexitloopexit_8_reg;
wire [8:0] gaussian_loopexitloopexit_2;
wire [9:0] gaussian_loopexitloopexit_3_reg;
wire [5:0] gaussian_loopexitloopexit_4;
wire [6:0] gaussian_loopexitloopexit_5_reg;
wire [9:0] gaussian_loopexitloopexit_6_reg;
wire [4:0] gaussian_loopexitloopexit_7_reg;
wire [31:0] gaussian_loopexitloopexit_scevgep11;
wire [31:0] gaussian_loopexitloopexit_scevgep11_reg;
wire [31:0] gaussian_lrph_indvar4_reg;
wire [31:0] gaussian_20_21;
wire [31:0] gaussian_lrph_9;
wire [31:0] gaussian_lrph_10_reg;
wire [31:0] gaussian_11_12_reg_stage0;
wire [31:0] LOOP22_1_inductionVar_stage0;
wire [31:0] gaussian_11_scevgep6;
wire [31:0] gaussian_11_scevgep6_reg_stage1;
wire [31:0] gaussian_11_13_reg_stage0;
wire [31:0] gaussian_11_scevgep;
wire [31:0] gaussian_11_14;
wire [31:0] gaussian_11_15;
wire [31:0] gaussian_11_15_reg_stage1;
wire [31:0] gaussian_11_16;
wire [31:0] legup_mult_1_unsigned_32_32_1_0_datab;
wire [31:0] gaussian_11_17;
wire [31:0] legup_mult_gaussian_11_17_out;
wire [31:0] gaussian_11_18;
wire [31:0] legup_mult_1_unsigned_32_32_1_0_dataa;
assign gaussian_loopexitloopexit_1_reg = gaussian_loopexitloopexit_1_reg_enablePhi_BB_1 ? 32'd0 : ngaussian_loopexitloopexit_1_reg_pi_BB_1;
assign gaussian_loopexitloopexit_8_reg = (({1'd0,gaussian_loopexitloopexit_1_reg}) + 32'd1);
assign gaussian_loopexitloopexit_2 = (({5'd0,gaussian_loopexitloopexit_1_reg}) * 32'd16);
assign gaussian_loopexitloopexit_3_reg = (({1'd0,gaussian_loopexitloopexit_2}) + 32'd33);
assign gaussian_loopexitloopexit_4 = (({2'd0,gaussian_loopexitloopexit_1_reg}) * (-32'd1));
assign gaussian_loopexitloopexit_5_reg = (({({1{gaussian_loopexitloopexit_4[5]}}),gaussian_loopexitloopexit_4}) + 32'd14);
assign gaussian_loopexitloopexit_6_reg = (({1'd0,gaussian_loopexitloopexit_2}) + 32'd17);
assign gaussian_loopexitloopexit_7_reg = (({1'd0,gaussian_loopexitloopexit_1_reg}) + 32'd1);
assign gaussian_loopexitloopexit_scevgep11 = (arg_c_reg + (({27'd0,gaussian_loopexitloopexit_7_reg}) * 4));
assign gaussian_loopexitloopexit_scevgep11_reg = gaussian_loopexitloopexit_scevgep11;
assign gaussian_lrph_indvar4_reg = gaussian_lrph_indvar4_reg_enablePhi_BB_4 ? 32'd0 : ngaussian_lrph_indvar4_reg_pi_BB_4;
assign gaussian_20_21 = (gaussian_lrph_indvar4_reg + 32'd1);
assign gaussian_lrph_9 = (gaussian_lrph_indvar4_reg * 32'd16);
assign gaussian_lrph_10_reg = (({22'd0,gaussian_loopexitloopexit_3_reg}) + gaussian_lrph_9);
assign gaussian_11_12_reg_stage0 = (gaussian_lrph_10_reg + LOOP22_1_inductionVar_stage0);
assign LOOP22_1_inductionVar_stage0 = LOOP22_1_inductionVar_stage0_enablePhi_BB_5 ? 0 : nLOOP22_1_inductionVar_stage0_pi_BB_5;
assign gaussian_11_scevgep6 = (arg_A_reg + (gaussian_11_12_reg_stage0 * 4));
assign gaussian_11_scevgep6_reg_stage1 = gaussian_11_scevgep6;
assign gaussian_11_13_reg_stage0 = (({22'd0,gaussian_loopexitloopexit_6_reg}) + LOOP22_1_inductionVar_stage0);
assign gaussian_11_scevgep = (arg_A_reg + (gaussian_11_13_reg_stage0 * 4));
assign gaussian_11_14 = loaddd_A_a_0_fromMem;
assign gaussian_11_15 = loaddd_c_a_0_fromMem;
assign gaussian_11_15_reg_stage1 = gaussian_11_15;
assign gaussian_11_16 = loaddd_A_b_0_fromMem;
assign legup_mult_1_unsigned_32_32_1_0_datab = gaussian_11_16;
assign gaussian_11_17 = legup_mult_gaussian_11_17_out;
assign legup_mult_gaussian_11_17_out = legup_mult_gaussian_11_17_result[31:0];
assign gaussian_11_18 = (gaussian_11_14 - gaussian_11_17);
assign legup_mult_1_unsigned_32_32_1_0_dataa = gaussian_11_15_reg_stage1;
assign endCircuit = endCircuit_endCircuitPI;
assign n282_ctrlOut_BB_6 = (gaussian_loopexitloopexit_5_reg == gaussian_20_21);
assign ngaussian_loopexitloopexit_8_reg_po_BB_1 = gaussian_loopexitloopexit_8_reg;
assign n386_po_BB_5 = (LOOP22_1_inductionVar_stage0 + 1'd1);
assign ngaussian_20_21_po_BB_4 = gaussian_20_21;
assign storeee_A_a_0_toMem = (gaussian_11_scevgep6_reg_stage1 >>> 3'd2);
assign storeee_A_a_0_addr = gaussian_11_18;
assign loaddd_A_a_0_addr = (gaussian_11_scevgep6_reg_stage1 >>> 3'd2);
assign loaddd_A_b_0_addr = (gaussian_11_scevgep >>> 3'd2);
assign loaddd_c_a_0_addr = (gaussian_loopexitloopexit_scevgep11_reg >>> 3'd2);
assign legup_mult_gaussian_11_17_in1 = legup_mult_1_unsigned_32_32_1_0_datab;
assign legup_mult_gaussian_11_17_in2 = legup_mult_1_unsigned_32_32_1_0_dataa;
assign n217_ctrlOut_BB_1 = (gaussian_loopexitloopexit_1_reg == 32'd14);
assign n382_ctrlOut_BB_5 = (LOOP22_1_inductionVar_stage0 == 14);
assign gaussian_loopexitloopexit_3_reg_anchorPo_BB_1_BB_4 = gaussian_loopexitloopexit_3_reg;
assign gaussian_loopexitloopexit_5_reg_anchorPo_BB_1_BB_6 = gaussian_loopexitloopexit_5_reg;
assign gaussian_loopexitloopexit_6_reg_anchorPo_BB_1_BB_5 = gaussian_loopexitloopexit_6_reg;
assign gaussian_loopexitloopexit_scevgep11_reg_anchorPo_BB_1_BB_5 = gaussian_loopexitloopexit_scevgep11_reg;
assign gaussian_20_21_anchorPo_BB_4_BB_6 = gaussian_20_21;
assign gaussian_lrph_10_reg_anchorPo_BB_4_BB_5 = gaussian_lrph_10_reg;
endmodule
