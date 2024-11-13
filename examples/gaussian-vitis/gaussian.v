module top(
i_0_in_reg_76_enablePhi_BB_2, 
j_0_reg_64_enablePhi_BB_1, 
k_0_reg_85_enablePhi_BB_3, 
ni_0_in_reg_76_pi_BB_2, 
nj_0_reg_64_pi_BB_1, 
nk_0_reg_85_pi_BB_3, 
loaddd_A_0_0_fromMem, 
loaddd_A_0_1_fromMem, 
loaddd_c_0_0_fromMem, 
clk, 
rst, 
endCircuit_endCircuitPI, 
endCircuit, 
n278_ctrlOut_BB_3, 
n273_ctrlOut_BB_2, 
ni_reg_216_po_BB_2, 
nj_fu_141_p2_po_BB_1, 
nk_reg_247_po_BB_3, 
storeee_A_0_0_toMem, 
storeee_A_0_0_addr, 
loaddd_A_0_0_addr, 
loaddd_A_0_1_addr, 
loaddd_c_0_0_addr, 
n268_ctrlOut_BB_1, 
src_j_0_reg_64_dst_zext_ln13_fu_96_p1_anchorPo_BB_1_BB_2, 
src_A_addr_reg_237_dst_storeee_A_0_0_addr_anchorPo_BB_3_BB_4, 
src_A_addr_reg_237_dst_loaddd_A_0_0_addr_anchorPo_BB_3_BB_4, 
src_c_addr_reg_206_dst_loaddd_c_0_0_addr_anchorPo_BB_1_BB_4, 
src_shl_ln_reg_211_dst_239_anchorPo_BB_1_BB_3, 
src_shl_ln24_reg_224_dst_242_anchorPo_BB_2_BB_3, 
src_loaddd_A_0_1_fromMem_dst_237_anchorPo_BB_3_BB_4
);
input i_0_in_reg_76_enablePhi_BB_2;
input j_0_reg_64_enablePhi_BB_1;
input k_0_reg_85_enablePhi_BB_3;
input [31:0] ni_0_in_reg_76_pi_BB_2;
input [4:0] nj_0_reg_64_pi_BB_1;
input [4:0] nk_0_reg_85_pi_BB_3;
input [31:0] loaddd_A_0_0_fromMem;
input [31:0] loaddd_A_0_1_fromMem;
input [31:0] loaddd_c_0_0_fromMem;
input clk;
input rst;
input endCircuit_endCircuitPI;
output endCircuit;
output n278_ctrlOut_BB_3;
output n273_ctrlOut_BB_2;
output [31:0] ni_reg_216_po_BB_2;
output [4:0] nj_fu_141_p2_po_BB_1;
output [4:0] nk_reg_247_po_BB_3;
output [31:0] storeee_A_0_0_toMem;
output [7:0] storeee_A_0_0_addr;
output [7:0] loaddd_A_0_0_addr;
output [7:0] loaddd_A_0_1_addr;
output [3:0] loaddd_c_0_0_addr;
output n268_ctrlOut_BB_1;
output [4:0] src_j_0_reg_64_dst_zext_ln13_fu_96_p1_anchorPo_BB_1_BB_2;
output [7:0] src_A_addr_reg_237_dst_storeee_A_0_0_addr_anchorPo_BB_3_BB_4;
output [7:0] src_A_addr_reg_237_dst_loaddd_A_0_0_addr_anchorPo_BB_3_BB_4;
output [3:0] src_c_addr_reg_206_dst_loaddd_c_0_0_addr_anchorPo_BB_1_BB_4;
output [7:0] src_shl_ln_reg_211_dst_239_anchorPo_BB_1_BB_3;
output [31:0] src_shl_ln24_reg_224_dst_242_anchorPo_BB_2_BB_3;
output [31:0] src_loaddd_A_0_1_fromMem_dst_237_anchorPo_BB_3_BB_4;
wire [31:0] i_0_in_reg_76;
wire [31:0] i_reg_216;
wire [31:0] zext_ln13_fu_96_p1;
wire [4:0] j_0_reg_64;
wire [4:0] j_fu_141_p2;
wire [4:0] k_0_reg_85;
wire [7:0] zext_ln22_fu_147_p1;
wire [31:0] zext_ln22_1_fu_151_p1;
wire [4:0] k_reg_247;
wire [7:0] A_addr_reg_237;
wire [31:0] A_load_1_reg_252;
wire [3:0] c_addr_reg_206;
wire [7:0] shl_ln_reg_211;
wire [7:0] shl_ln_fu_115_p3;
wire [31:0] i_fu_123_p2;
wire [31:0] mul_ln24_reg_257;
wire [31:0] shl_ln24_reg_224;
wire [31:0] shl_ln24_fu_135_p2;
wire [63:0] zext_ln24_1_fu_176_p1;
wire [31:0] mul_ln24_fu_187_p0;
wire [3:0] trunc_ln24_fu_111_p1;
assign i_0_in_reg_76 = i_0_in_reg_76_enablePhi_BB_2 ? zext_ln13_fu_96_p1 : ni_0_in_reg_76_pi_BB_2;
assign i_reg_216 = i_fu_123_p2;
assign zext_ln13_fu_96_p1 = j_0_reg_64;
assign j_0_reg_64 = j_0_reg_64_enablePhi_BB_1 ? 5'd1 : nj_0_reg_64_pi_BB_1;
assign j_fu_141_p2 = (j_0_reg_64 + 5'd1);
assign k_0_reg_85 = k_0_reg_85_enablePhi_BB_3 ? 5'd1 : nk_0_reg_85_pi_BB_3;
assign zext_ln22_fu_147_p1 = k_0_reg_85;
assign zext_ln22_1_fu_151_p1 = k_0_reg_85;
assign k_reg_247 = (k_0_reg_85 + 5'd1);
assign A_addr_reg_237 = (zext_ln22_1_fu_151_p1 + shl_ln24_reg_224);
assign A_load_1_reg_252 = loaddd_A_0_0_fromMem;
assign c_addr_reg_206 = j_0_reg_64;
assign shl_ln_reg_211 = ({4'b0000,shl_ln_fu_115_p3[7:4]});
assign shl_ln_fu_115_p3 = ({4'd0,trunc_ln24_fu_111_p1});
assign i_fu_123_p2 = (i_0_in_reg_76 + 32'd1);
assign mul_ln24_reg_257 = (A_load_1_reg_252 * mul_ln24_fu_187_p0);
assign shl_ln24_reg_224 = ({4'b0000,shl_ln24_fu_135_p2[31:4]});
assign shl_ln24_fu_135_p2 = (i_fu_123_p2 << 32'd4);
assign zext_ln24_1_fu_176_p1 = (zext_ln22_fu_147_p1 + shl_ln_reg_211);
assign mul_ln24_fu_187_p0 = loaddd_c_0_0_fromMem;
assign trunc_ln24_fu_111_p1 = j_0_reg_64[3:0];
assign endCircuit = endCircuit_endCircuitPI;
assign n278_ctrlOut_BB_3 = ((k_0_reg_85 == 5'd16) ? 1'b1 : 1'b0);
assign n273_ctrlOut_BB_2 = ((i_0_in_reg_76 == 32'd15) ? 1'b1 : 1'b0);
assign ni_reg_216_po_BB_2 = i_reg_216;
assign nj_fu_141_p2_po_BB_1 = j_fu_141_p2;
assign nk_reg_247_po_BB_3 = k_reg_247;
assign storeee_A_0_0_toMem = (mul_ln24_reg_257 - loaddd_A_0_1_fromMem);
assign storeee_A_0_0_addr = A_addr_reg_237;
assign loaddd_A_0_0_addr = A_addr_reg_237;
assign loaddd_A_0_1_addr = zext_ln24_1_fu_176_p1;
assign loaddd_c_0_0_addr = c_addr_reg_206;
assign n268_ctrlOut_BB_1 = ((j_0_reg_64 == 5'd16) ? 1'b1 : 1'b0);
assign src_j_0_reg_64_dst_zext_ln13_fu_96_p1_anchorPo_BB_1_BB_2 = j_0_reg_64;
assign src_A_addr_reg_237_dst_storeee_A_0_0_addr_anchorPo_BB_3_BB_4 = A_addr_reg_237;
assign src_A_addr_reg_237_dst_loaddd_A_0_0_addr_anchorPo_BB_3_BB_4 = A_addr_reg_237;
assign src_c_addr_reg_206_dst_loaddd_c_0_0_addr_anchorPo_BB_1_BB_4 = c_addr_reg_206;
assign src_shl_ln_reg_211_dst_239_anchorPo_BB_1_BB_3 = shl_ln_reg_211;
assign src_shl_ln24_reg_224_dst_242_anchorPo_BB_2_BB_3 = shl_ln24_reg_224;
assign src_loaddd_A_0_1_fromMem_dst_237_anchorPo_BB_3_BB_4 = loaddd_A_0_1_fromMem;
endmodule