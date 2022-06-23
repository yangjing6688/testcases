import pymysql
import json

# Mapping of testbed name to new path
new_file_loc_map = {
    "xiq_blr_tb1_exos.yaml": "TestBeds/BANGALORE/Prod/wired",
    "xiq_blr_tb1_voss.yaml": "TestBeds/BANGALORE/Prod/wired",
    "xiq_blr_tb2_exos.yaml": "TestBeds/BANGALORE/Prod/wired",
    "xiq_blr_tb2_voss.yaml": "TestBeds/BANGALORE/Prod/wired",
    "testbed1.yaml": "TestBeds/BANGALORE/Prod/wired_wireless",
    "testbed2.yaml": "TestBeds/BANGALORE/Prod/wired_wireless",
    "adsptestbed1.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "testbed3.yaml": "TestBeds/BANGALORE/Prod/wired_wireless",
    "xiq_blr_tb1_a3.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb1_ap1130.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb1_ap230.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb1_ap305c_mu1.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb1_ap410c_mu1.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb1_ap460c_mu1.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb1_mixed_ap630_sr2348p.yaml": "TestBeds/BANGALORE/Prod/wired_wireless",
    "xiq_blr_tb1_wing.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb1_xr200p.yaml": "TestBeds/BANGALORE/Prod/wired",
    "xiq_blr_tb2_a3.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb2_ap150w.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb2_ap250.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb2_ap302w_mu1.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb2_ap305c_mu1.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb2_ap460c_mu1.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb2_mixed_ap410C_sr2348p.yaml": "TestBeds/BANGALORE/Prod/wired_wireless",
    "xiq_blr_tb2_wing.yaml": "TestBeds/BANGALORE/Prod/wireless",
    "xiq_blr_tb2_xr600.yaml": "TestBeds/BANGALORE/Prod/wired",
    "eni_digitwin_5320stk_1node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320stk_1node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320stk_1node3.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320stk_1node4.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320stk_2node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320stk_2node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320stk_4node.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320_1node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320_1node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320_1node3.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320_1node4.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320_2node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320_2node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5320_4node.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420stk_1node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420stk_1node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420stk_1node3.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420stk_1node4.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420stk_2node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420stk_2node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420stk_4node.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420_1node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420_1node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420_1node3.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420_1node4.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420_2node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420_2node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5420_4node.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520stk_1node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520stk_1node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520stk_1node3.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520stk_1node4.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520stk_2node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520stk_2node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520stk_4node.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520_1node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520_1node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520_1node3.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520_1node4.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520_2node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520_2node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5520_4node.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720stk_1node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720stk_1node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720stk_1node3.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720stk_1node4.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720stk_2node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720stk_2node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720stk_4node.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720_1node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720_1node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720_1node3.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720_1node4.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720_2node1.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720_2node2.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "eni_digitwin_5720_4node.yaml": "TestBeds/CHENNAI/Prod/digital_twin",
    "chn_5420_rack_i17_1_exos.yaml": "TestBeds/CHENNAI/Prod/wired",
    "chn_5420_rack_i17_2_exos.yaml": "TestBeds/CHENNAI/Prod/wired",
    "rdu_exos_twin_rack10_1node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack10_1node2.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack10_1node3.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack10_1node4.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack10_2node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack10_2node2.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack10_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack11_1node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack11_1node2.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack11_1node3.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack11_1node4.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack11_2node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack11_2node2.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack11_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack12_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack13_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack14_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack15_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack16_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack8_1node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack8_1node2.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack8_1node3.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack8_1node4.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack8_2node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack8_2node2.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack8_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack9_1node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack9_1node2.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack9_1node3.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack9_1node4.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack9_2node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack9_2node2.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_exos_twin_rack9_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_vm_pod1_1node1.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_vm_pod1_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_vm_pod2_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_vm_pod3_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_vm_pod4_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_vm_pod5_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_vm_pod6_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_vm_pod7_4node.yaml": "TestBeds/RDU/Prod/digital_twin",
    "rdu_5420_rack1_2node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x460g2_pod1_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x460g2_pod2_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x460g2_pod3_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x460g2_stk_pod1_4node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x460g2_stk_pod2_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x460g2_stk_pod3_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x465_pod1_4node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x465_pod2_4node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x465_pod3_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x465_pod4_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x590_pod1_4node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x590_pod2_4node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x590_pod3_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x590_pod3_3node_rest.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x590_pod4_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x590_pod5_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x590_pod6_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x690_stk_pod1_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x690_stk_pod2_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x870_pod1_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_x870_pod2_3node.yaml": "TestBeds/RDU/Prod/wired",
    "rdu_xiqse_mixed_elems1.yaml": "TestBeds/RDU/Prod/wired_wireless",
    "rdu_xiqse_mixed_elems2.yaml": "TestBeds/RDU/Prod/wired_wireless",
    "rdu_xiqse_mixed_elems3.yaml": "TestBeds/RDU/Prod/wired_wireless",
    "rdu_xiqse_mixed_elems4.yaml": "TestBeds/RDU/Prod/wired_wireless",
    "rdu_xiqse_mixed_elems5.yaml": "TestBeds/RDU/Prod/wired_wireless",
    "rdu_xiqse_xiqintegration_mixed_elems1.yaml": "TestBeds/RDU/Prod/wired_wireless",
    "rdu_xiqse_xiqintegration_licensing_elems1.yaml": "TestBeds/RDU/Prod/other_resources/",
    "rdu_xiq_voss_exos.yaml": "TestBeds/RDU/Prod/wired_wireless",
    "rdu_xiq_ap410_1.yaml": "TestBeds/RDU/Prod/wireless",
    "rdu_xiq_ap650x1.yaml": "TestBeds/RDU/Prod/wireless",
    "rdu_xiq_ap650x2.yaml": "TestBeds/RDU/Prod/wireless",
    "rdu_xiq_ap650x3.yaml": "TestBeds/RDU/Prod/wireless",
    "rdu_xiq_ap650x4.yaml": "TestBeds/RDU/Prod/wireless",
    "dut_a_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5320_rack1/1_node",
    "dut_a_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5320_rack1/1_node",
    "dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5320_rack1/1_node",
    "dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5320_rack1/1_node",
    "dut_a_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack1/1_node",
    "dut_a_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack1/1_node",
    "dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack1/1_node",
    "dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack1/1_node",
    "dut_a_exos_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack1/2_node",
    "dut_a_exos_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack1/2_node",
    "dut_a_voss_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack1/2_node",
    "dut_a_voss_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack1/2_node",
    "dut_a_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack2/1_node",
    "dut_a_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack2/1_node",
    "dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack2/1_node",
    "dut_a_exos_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack2/2_node",
    "dut_a_voss_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack2/2_node",
    "dut_a_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack3/1_node",
    "dut_a_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack3/1_node",
    "dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack3/1_node",
    "dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack3/1_node",
    "dut_a_exos_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack3/2_node",
    "dut_a_exos_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack3/2_node",
    "dut_a_voss_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack3/2_node",
    "dut_a_voss_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5420_rack3/2_node",
    "dut_a_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack1/1_node",
    "dut_a_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack1/1_node",
    "dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack1/1_node",
    "dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack1/1_node",
    "dut_a_exos_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack1/2_node",
    "dut_a_exos_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack1/2_node",
    "dut_a_voss_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack1/2_node",
    "dut_a_voss_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack1/2_node",
    "dut_a_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack2/1_node",
    "dut_a_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack2/1_node",
    "dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack2/1_node",
    "dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack2/1_node",
    "dut_a_exos_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack2/2_node",
    "dut_a_exos_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack2/2_node",
    "dut_a_voss_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack2/2_node",
    "dut_a_voss_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack2/2_node",
    "dut_a_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack3/1_node",
    "dut_a_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack3/1_node",
    "dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack3/1_node",
    "dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack3/1_node",
    "dut_a_exos_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack3/2_node",
    "dut_a_exos_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack3/2_node",
    "dut_a_voss_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack3/2_node",
    "dut_a_voss_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack3/2_node",
    "dut_a_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack4/1_node",
    "dut_a_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack4/1_node",
    "dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack4/1_node",
    "dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack4/1_node",
    "dut_a_exos_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack4/2_node",
    "dut_a_exos_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack4/2_node",
    "dut_a_voss_dut_b_exos.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack4/2_node",
    "dut_a_voss_dut_b_voss.yaml": "TestBeds/SALEM/Prod/wired/slm_5520_rack4/2_node",
    "xiq_sj_tb1_exos.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb1_voss.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb2_exos_1.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb2_exos_2.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb4_exos.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb5_exos.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb6_exos.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb1_460c_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb1_a3.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb1_ap150w.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb1_ap230.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb1_ap410c_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb1_ap630.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb1_ap7532I.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb1_wing.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb1_xr600.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb2_ap305c_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb2_ap460c_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb2_mixed_ap410C_sr2348p.yaml": "TestBeds/SJ/Prod/wired_wireless",
    "xiq_sj_tb3_460c_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb3_ap150w.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb3_ap302w_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb3_mixed_ap410C_sr2348p.yaml": "TestBeds/SJ/Prod/wired_wireless",
    "xiq_sj_tb3_xr200p.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb4_ap150w.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb4_ap230.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb4_ap230_01_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb4_ap460c_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb4_mixed_ap410c_sr2348p.yaml": "TestBeds/SJ/Prod/wired_wireless",
    "xiq_sj_tb4_wing.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb4_xr200p.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb4_xr600p.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb5_ap150w-mu2.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb5_ap410c.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb5_ap550_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb5_sr2208p.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb5_wing.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb5_xr600p.yaml": "TestBeds/SJ/Prod/wired",
    "xiq_sj_tb6_ap130_1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb6_ap130_2.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb6_ap230_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb6_ap410c_sr2348p.yaml": "TestBeds/SJ/Prod/wired_wireless",
    "xiq_sj_tb6_ap460c_mu1.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb6_wing.yaml": "TestBeds/SJ/Prod/wireless",
    "xiq_sj_tb6_xr600p.yaml": "TestBeds/SJ/Prod/wired",
    "demo_salem_1_node_exos.yaml": "TestBeds/SALEM/Demo/wired",
    "demo_salem_1_node_voss.yaml": "TestBeds/SALEM/Demo/wired",
    "demo_salem_2_node_exos_no_tgen.yaml": "TestBeds/SALEM/Demo/wired",
    "demo_salem_2_node.yaml": "TestBeds/SALEM/Demo/wired",

}

test_host = 'econ-test.cluster-ckzwg7t8wthc.us-east-1.rds.amazonaws.com'
prod_host = 'econ-production.cluster-ckzwg7t8wthc.us-east-1.rds.amazonaws.com'

# Connect to the database
connection = pymysql.connect(host=test_host,
                             user='admin',
                             password='UU^7hLQ61$JATRkP#iFZslv6NI30ir$GQ2fGXkfc',
                             database='econ-tbedmgr',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:

    # Dump info from wizardStatus table
    with connection.cursor() as cursor:
        sql = "SELECT `wizardId`, `jobConfig` FROM `wizardStatus`"
        cursor.execute(sql)

        wizard_results = cursor.fetchall()

    # Dump info from testbeds table
    with connection.cursor() as cursor:
        sql = "SELECT `testbed_id`, `configFileName`, `configFilePath` FROM `testbeds`"
        cursor.execute(sql)

        testbeds_results = cursor.fetchall()

    # need to update:
    # wizardStatus table - jobConfig: ui > xiq_arg_testbed
    # wizardStatus table - jobConfig: ui > [ devTestbedPath ]
    # wizardStatus table - jobConfig: ui > testSuiteList > [ devTestbedPath ]
    # testbeds table - configFilePath

    new_wizard_results = []
    for result in wizard_results:
        any_change = False
        job_config = json.loads(result["jobConfig"])

        # This field doesn't appear to be used in any of the saved jobs
        # # wizardStatus table - jobConfig: ui > xiq_arg_testbed
        # if 'xiq_arg_testbed' in job_config['ui'] and job_config['ui']['xiq_arg_testbed']:
        #     # update xiq_arg_testbed
        #     job_config['ui']['xiq_arg_testbed'] = 'testPath2'
        #     any_change = True

        # wizardStatus table - jobConfig: ui > [ devTestbedPath ]
        if 'devTestbedPath' in job_config['ui']:
            for devTestbedPath in job_config['ui']['devTestbedPath']:
                if type(devTestbedPath) is dict:
                    tb_name = devTestbedPath.get('name')
                    if tb_name:
                        try:
                            devTestbedPath['configFilePath'] = new_file_loc_map[tb_name]
                            any_change = True
                        except:
                            # Testbed name was not one of the testbeds that we moved
                            pass


        # wizardStatus table - jobConfig: ui > testSuiteList > [ devTestbedPath ]
        if 'testSuiteList' in job_config['ui']:
            for testSuite in job_config['ui']['testSuiteList']:
                for devTestbedPath in testSuite['devTestbedPath']:
                    if type(devTestbedPath) is dict:
                        tb_name = devTestbedPath.get('name')
                        if tb_name:
                            try:
                                devTestbedPath['configFilePath'] = new_file_loc_map[tb_name]
                                any_change = True
                            except:
                                # Testbed name was not one of the testbeds that we moved
                                pass

        if any_change:
            new_wizard_results.append({
                'wizardId': result['wizardId'],
                'jobConfig': json.dumps(job_config)
                })


    with open('update_testbed_paths_result.json', 'w') as f:
        json.dump(new_wizard_results, f)

    new_testbed_results = []
    for result in testbeds_results:
        any_change = False
        # print(result)
        cfg_name = result['configFileName']
        cfg_path = result['configFilePath']

        # testbeds table - configFilePath
        try:
            cfg_path = new_file_loc_map[cfg_name]
            any_change = True
        except:
            pass

        if any_change:
            new_testbed_results.append({
                'testbed_id': result['testbed_id'],
                'configFileName': cfg_name,
                'configFilePath': cfg_path
                })

    with open('update_testbed_paths_result.json', 'a') as f:
        json.dump(new_testbed_results, f)


    with connection.cursor() as cursor:

        # Update wizardStatus table
        for entry in new_wizard_results:
            sql = f"UPDATE `wizardStatus` SET jobConfig = '{entry['jobConfig']}' WHERE wizardId = {entry['wizardId']};"
            print(f"Now running command: {sql}")
            cursor.execute(sql)
            # break

        # Update testbeds table
        for entry in new_testbed_results:
            sql = f"UPDATE `testbeds` SET configFilePath = '{entry['configFilePath']}' WHERE testbed_id = {entry['testbed_id']};"
            print(f"Now running command: {sql}")
            cursor.execute(sql)
            # break

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

