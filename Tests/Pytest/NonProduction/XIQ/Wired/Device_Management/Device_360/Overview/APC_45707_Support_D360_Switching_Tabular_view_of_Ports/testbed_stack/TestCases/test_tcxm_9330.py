# Author:         tapostol
# Description:    [STACK] To verify that port details of other slots can be viewed using hyperlink in the bottom of the page
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9330
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS stack should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable only for the EXOS stack devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_stack.Resources.testcase_base import xiqBase


class TCXM9330Tests(xiqBase):

    @pytest.mark.STACK
    @pytest.mark.development       
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_9330
    @pytest.mark.p1
    def test_9330_verify_other_slot_ports_displayed(self, onboarded_stack):
        """
        Step	Step Description
        1	    Onboard the device (stack)
        2	    Navigate to Device360
        3	    CLI - show ports information
        4	    Check ports in list
        5	    Navigate to the page 2 hyperlink
        6	    Click on the page 2 hyperlink
        7	    Repeat steps 4-6 for all the pages
        8	    Check all ports displayed
        9	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9330'
        
        current_page_number = 1

        try:
            self.suite_udk.go_to_device360(onboarded_stack)

            try:
                self.network_manager.connect_to_network_element_name(onboarded_stack.name)
                dut_list_of_ports = self.suite_udk.get_port_list_from_dut(onboarded_stack)
                assert dut_list_of_ports != -1, f"Unable to get ports from dut"
            finally:
                self.network_manager.close_connection_to_network_element(onboarded_stack.name)
                
            more_pages = 1

            while more_pages == 1:
                assert self.suite_udk.device360_confirm_current_page_number(current_page_number),\
                    f"Wrong page"

                table_list_of_ports = self.suite_udk.device360_switch_get_current_page_port_name_list()
                assert table_list_of_ports != -1, f"Failed to get ports from Device360"
                for port in table_list_of_ports:
                    if port in dut_list_of_ports:
                        dut_list_of_ports.remove(port)
                more_pages = self.suite_udk.device360_monitor_overview_pagination_next_page_by_number()
                assert more_pages != -1, f"Failed to manage pagination"
                current_page_number = current_page_number + 1
            assert len(dut_list_of_ports) == 0, f"Some ports wre not displayed in the table"

        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
