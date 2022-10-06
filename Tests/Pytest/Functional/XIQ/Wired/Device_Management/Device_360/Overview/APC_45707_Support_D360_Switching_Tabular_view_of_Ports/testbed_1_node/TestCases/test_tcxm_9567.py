# Author:         tpodar
# Description:    To verify if the traffic received rate is shown correctly in the D360 table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9567
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time
import re

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


vlan_a = "10"
vlan_a_name = "VLAN-10"
vlan_b = '11'
vlan_b_name = "VLAN-11"


class TCXM9567Tests(xiqBase):

    @pytest.mark.tcxm_9567
    @pytest.mark.run(order=3)
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_9567(self, onboarded_switch):
        """
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360
        3	    Verify the 'TRAFFIC RECEIVED(RX)' check mark in the columns section
        4	    Verify the ''TRAFFIC RECEIVED(RX)' column displays values for all the ports(the first 10 ports)
        5	    Display and verify the values for 'TRAFFIC RECEIVED(RX)' in CLI for the following ports: 1, 24
        6	    Compare the values from XIQ  to the CLI values of 'TRAFFIC RECEIVED(RX)' for the following ports: 1, 24
        7	    Navigate to the 100 ports option
        8	    Verify the 'TRAFFIC RECEIVED(RX)' column displays values for all the ports(100 ports)
        9	    Display and verify the values for 'TRAFFIC RECEIVED(RX)' in CLI for the following ports: 1, 24
        10	    Compare the values from XIQ  to the CLI values of 'TRAFFIC RECEIVED(RX)' for the following ports: 1, 24
        11	    Setup clean-up - Exit Device360 and logout from XIQ
        
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9567'

        dut = onboarded_switch

        try:

            port_list = [self.tb.dut1_tgen_port_a.ifname, self.tb.dut1_tgen_port_b.ifname]
            first_port, second_port = port_list
            
            self.udks.setupTeardownUdks.Base_Test_Suite_Setup()
            
            self.suite_udk.clear_counters(
                self.tb.dut1, first_port=first_port, second_port=second_port)
            self.suite_udk.bounce_IQAgent(
                dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)

            self.suite_udk.setup_vlans(self.udks, self.tb.dut1, vlan_a, port_list)
            
            packet_a = 'packetA'
            packet_b = 'packetB'
            tgen_port_a = self.tb.createTgenPort(
                self.tb.tgen1_name, self.tb.tgen_dut1_port_a.ifname)
            tgen_port_b = self.tb.createTgenPort(
                self.tb.tgen1_name, self.tb.tgen_dut1_port_b.ifname)
            self.udks.trafficGenerationUdks.Create_Ethernet2_Packet(
                packet_a, '00:22:22:22:22:22', '00:11:11:11:11:11')
            self.udks.trafficGenerationUdks.Create_Ethernet2_Packet(
                packet_b, '00:11:11:11:11:11', '00:22:22:22:22:22')

            self.suite_udk.Transmit_Traffic_Bidirectionally_and_Verify_it_was_Received_tcxm_9567(
                tgen_port_a, tgen_port_b, packet_a, packet_b, packet_b, packet_a, tx_count=5)
            
            try:
                
                self.suite_udk.go_to_device360(onboarded_switch)

                checkboxes_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()
                checkboxes_button.location_once_scrolled_into_view
                self.auto_actions.click(checkboxes_button)
                time.sleep(2)

                checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_marked_checkboxes()
                time.sleep(3)

                print("Checking if the Received Traffic checkbox is marked in the columns section")
                for i in checkboxes:
                    if "Received" in i:
                        print( f"The {i} checkbox is checked")
                        break
                else:
                    assert False, "The received traffic checkbox is not checked"
            
            finally:
                self.xiq.xflowsmanageDevice360.close_device360_window()
                time.sleep(3)
            
            self.suite_udk.bounce_IQAgent(
                dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)
            
            start_time = time.time()
            while time.time() - start_time < 1200:
                
                time.sleep(4)
                self.xiq.xflowscommonDevices.refresh_devices_page()
                time.sleep(4)

                try:
                    traffic_list_from_dut = self.suite_udk.get_received_traffic_list_from_dut(
                        dut, first_port, second_port)
                    self.suite_udk.bounce_IQAgent(
                        dut, connect_to_dut=False, disconnect_from_dut=False, wait=False)
                    
                    time.sleep(30)
                    self.suite_udk.go_to_device360(onboarded_switch)
                    traffic_list_from_xiq = self.suite_udk.device360_display_traffic_received_from_xiq_and_return_traffic_list(
                        dut, first_port, second_port)

                    for i in range(2):
                        
                        match = re.search(r'(\d+(\.\d+)?)', traffic_list_from_xiq[i]).group(1)
                        if "KB" in traffic_list_from_xiq[i]:
                            traffic_list_from_xiq[i] = float(match) * 1024
                        elif "MB" in traffic_list_from_xiq[i]:
                            traffic_list_from_xiq[i] = float(match) * 1024 * 1024
                        else:
                            traffic_list_from_xiq[i] = float(match)

                    print("Traffic list from xiq is: ", traffic_list_from_xiq)
                    print("Traffic list from dut is: ", traffic_list_from_dut)

                    for i in range(2):
                        a = float(traffic_list_from_dut[i])
                        b = float(traffic_list_from_xiq[i])

                        print("Finding the difference in percentage between the traffic values")

                        try:
                            percentage_diff = ((b-a)/a)*100
                        except ZeroDivisionError:
                            percentage_diff = 0
                            
                        print(f"the percentage for index {i} is {percentage_diff}")
                        assert abs(percentage_diff) <= 10, "The difference is more than 10%"
                except Exception as exc:
                    print(exc)
                else:
                    break
                finally:
                    self.suite_udk.select_pagination_size("10")
                    self.xiq.xflowsmanageDevice360.close_device360_window()
                    time.sleep(10)
            else:
                assert False, f"Failed to verify values after {int(time.time()-start_time)} seconds"
                
        finally: 
            self.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(self.tb.dut1.name, vlan_a)
