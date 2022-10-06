# Author:         icosmineanu
# Description:    To verify if the port name is shown correctly in the D360 table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9562
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9562Tests(xiqBase):

    @pytest.mark.tcxm_9562
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_tcxm_9562(self, onboarded_switch):
        """
        Step            Step Description
         1              Onboard the device
         2              Navigate to Device360, Monitor, Overview
         3              Go to the ports table
         4              Verify that the ports available in this table are the ports also available on the onboarded EXOS/VOSS dut
         5              Choose the first column(which contains the name of the port)
         6              Check if the port name from XIQ is the same as the one from CLI
         7              Delete the onboarded device and logout from XIQ(Teardown)
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9562'

        dut = onboarded_switch

        try:
            self.suite_udk.go_to_device360(onboarded_switch)

            self.suite_udk.select_max_pagination_size()

            try:
                
                self.network_manager.connect_to_network_element_name(dut.name)
                dut_list_of_ports = self.suite_udk.get_port_list_from_dut(dut)
                assert dut_list_of_ports != -1, f"Unable to get ports from dut!"
                table_list_of_ports = self.suite_udk.device360_switch_get_current_page_port_name_list()
                for port in table_list_of_ports:
                    if port in dut_list_of_ports:
                        dut_list_of_ports.remove(port)
                assert len(dut_list_of_ports) == 0, "Some ports were not displayed in the table"
            finally:
                self.network_manager.close_connection_to_network_element(dut.name)

        finally:
            self.suite_udk.select_pagination_size("10")

            self.xiq.xflowsmanageDevice360.close_device360_window()
            time.sleep(3)
