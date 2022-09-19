# Author:         tapostol
# Description:    To verify that the rows other than the row length can be viewed using hyperlink
#                 in the bottom of the page (pagination)
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9318
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9318Tests(xiqBase):

    @pytest.mark.xim_tcxm_9318
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.development       
    @pytest.mark.p2
    @pytest.mark.testbed_1_node
    def test_9318_verify_other_rows_display_using_pagination_hyperlink(self, onboarded_switch):
        """
        Step	Step Description
        1	    Onboard the device
        2	    Navigate to Device360
        3	    Generate initial empty reference list
        4	    Get port list from the current table page
        5	    Check if the elements from the new page are different from reference
        6	    Navigate to the page 2 hyperlink
        7	    Click on the page 2 hyperlink
        8	    Check highlighted page number is 2
        9	    Replace reference list with port list from page 1
        10	    Repeat steps 4-9 for all pages
        11	    Delete the onboarded device and logout from XIQ
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9318'
        
        current_page_number = 1
        try:
            self.suite_udk.go_to_device360(onboarded_switch)

            ports_list_current_page = []
            more_pages = 1
            
            while more_pages == 1:
                assert self.suite_udk.device360_confirm_current_page_number(current_page_number),\
                    f"Wrong page"
                ports_list_reference = ports_list_current_page
                ports_list_current_page = self.suite_udk.device360_switch_get_current_page_port_name_list()
                assert ports_list_current_page != -1, f"Unable get the port name list"
                assert len(list(set(ports_list_reference).intersection(ports_list_current_page))) == 0,\
                    f"Table on new page share ports with the previous page"
                more_pages = self.suite_udk.device360_monitor_overview_pagination_next_page_by_number()
                assert more_pages != -1, f"Failed to manage pagination"
                current_page_number = current_page_number + 1

        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
