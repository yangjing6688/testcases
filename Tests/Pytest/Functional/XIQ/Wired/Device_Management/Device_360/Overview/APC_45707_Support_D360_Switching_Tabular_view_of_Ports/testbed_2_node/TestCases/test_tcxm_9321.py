# Author:         rvisterineanu
# Description:    To verify hyperlink in LLDP column takes to LLDP neighbor
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9321
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
#                 This test case needs a testbed yaml with two devices.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time


from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_2_node.Resources.testcase_base import xiqBase


class TCXM9321Tests(xiqBase):

    @pytest.mark.tcxm_9321
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_2_node
    def test_9321_verify_hyperlink_in_LLDP_column_takes_to_LLDP_neighbor(self, logger, onboarded_2_switches):
        """
        Step	    Step Description
        1	        Onboard the devices
        2	        Navigate to Device360, Monitor, Overview
        3	        Look in the LLDP Neighbor column for Sysname hyperlinks of LLDP Neighbors
        4	        Click on the first Sysname hyperlink of LLDP Neighbour
        5	        Click on the Sysname hyperlink of LLDP Neighbour of current device in order to access the Device360 page of the first device
        6	        Repeat steps 4-5 for other existing  Sysname Hyperlinks of LLDP Neighbour
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9321'

        dut1, dut2 = onboarded_2_switches

        isl_ports_dut1 = self.suite_udk.get_isl_ports(dut1.isl)
        isl_ports_dut2 = self.suite_udk.get_isl_ports(dut2.isl)

        if len(isl_ports_dut1) < 1:
            pytest.skip(
                "****This testcase doesn't run on single node testbed, it needs at least two nodes for execution. "
                "Hence skipping test****")
        
        if len(isl_ports_dut2) < 1:
            pytest.skip(
                "****This testcase doesn't run on single node testbed, it needs at least two nodes for execution. "
                "Hence skipping test****")

        logger.info("Wait for LLDP NEIGHBORS column to be updated before to start the test (bounce IQAgent)")
        self.suite_udk.bounce_device(self.xiq, dut1)
        self.suite_udk.bounce_device(self.xiq, dut2)

        self.suite_udk.go_to_device360(dut1)

        try:
            
            self.suite_udk.select_max_pagination_size()

            logger.info("Verify if LLDP NEIGHBOR column displays the sysname with hyperlink on all ports connected to "
                        "the onboarded neighbor device as configured in yaml file and click it")
            time.sleep(5)
            hyperlinks_list_dut1 = self.suite_udk.check_device360_LLDP_neighbors_with_hyperlink_dut1(isl_ports_dut1)

            for i in range(len(hyperlinks_list_dut1)):
                
                time.sleep(15)
                hyperlinks_list_dut1 = self.suite_udk.check_device360_LLDP_neighbors_with_hyperlink_dut1(isl_ports_dut1)
                hyper_dut1 = hyperlinks_list_dut1[i]
                
                self.auto_actions.click(hyper_dut1)
                time.sleep(15)
                
                mac_device360 = self.xiq.xflowsmanageDevice360.dev360.get_device_info_mac_address()
                assert "MAC Address:\n" + dut2.mac.upper() == mac_device360.text, "The mac in device360 is not the same as in the yaml file!"
                logger.info(f"The displayed LLDP neighbor is correct and has the mac: {dut2.mac.upper()}")
                
                hyperlinks_list_dut2 = self.suite_udk.check_device360_LLDP_neighbors_with_hyperlink_dut2(isl_ports_dut2)
                time.sleep(15)

                self.auto_actions.click(hyperlinks_list_dut2[i])
                time.sleep(15)
                    
                mac_device360 = self.xiq.xflowsmanageDevice360.dev360.get_device_info_mac_address()
                assert "MAC Address:\n" + dut1.mac.upper() == mac_device360.text, "The mac in device360 is not the same as in the yaml file!"
                
                logger.info(f"The displayed LLDP neighbor is correct and has the mac: {dut1.mac.upper()}")

        finally:

            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
