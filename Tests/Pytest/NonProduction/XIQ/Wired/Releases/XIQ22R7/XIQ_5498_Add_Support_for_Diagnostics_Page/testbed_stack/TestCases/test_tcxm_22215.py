import pytest
from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R7.XIQ_5498_Add_Support_for_Diagnostics_Page.testbed_stack.Resources import testcase_base

"""
Script title : This script run the below tests for Add Support for Diagnostics Page according with XIQ-5498 story
Author: tpodar - TCXM22215, TCXM22217, TCXM22219
Description : Check if the dropdown at the top of the page is present and correctly displays all the devices in the stack and verify Select/Deselect All Ports buttons
Testcases : TCXM22215, TCXM22217, TCXM22219
Pre-Requests : None
Comments : Other platform than STACK is not yet supported
Modified by: icosmineanu
"""
class TCXM22215Tests(testcase_base.xiqBase):

    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_22215
    @pytest.mark.xim_tcxm_22217
    @pytest.mark.xim_tcxm_22219
    @pytest.mark.p1
    def test_tcxm_22215(self, onboarded_stack):
        """
        TCXM - 22215 - Verify that the slot dropdown selector is present and contains all the individual
                       devices in the stack(also each option in the dropdown is clickable)
        TCXM - 22217 - Verify if the Select All Ports button is present and clickable
        TCXM - 22219 - Verify if the DeSelect All Ports button is present and clickable

        Step    Description

        1	Onboard the EXOS stack.
        2	Navigate to Device360.
        3	Navigate to the Monitor Tab --> Diagnostics TAB.
        --------------
        4	Check if the dropdown at the top of the page is present and correctly displays all the devices in the stack
        5   Click on each item in the dropdown in order to verify that it redirects the user to the correct option
        --------------
        6	Verify if the select all ports button is present.
        7	Click on the select all ports button.
        --------------
        8	Verify if the DeSelect all ports button is present.
        9	Click on the DeSelect all ports button.

        """
        self.executionHelper.testSkipCheck()
        dut = onboarded_stack
        D360Flag = 0


        try:
            res = self.xiq.xflowscommonDeviceCommon.go_to_device360_window(dut.mac)
            assert res != -1, "Unable to go to device360 window"
            D360Flag = 1
            res = self.xiq.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            assert res != -1, "Unable to navigate to Diagnostics TAB"

            print("Check if the dropdown at the top of the page is present")
            stack_dropdown = self.xiq.xflowsmanageDevice360.get_device360_monitor_diagnostics_stack_drop_down()
            assert stack_dropdown != -1, "The stack selector dropdown isn't present"

            print("Check each item in the dropdown in order to verify that it redirects the user to the correct option")
            res = self.localsuiteudks.check_all_the_individual_devices_in_the_stack_monitor_diagnostics(dut)
            assert res != -1, "Unable to check each item in the dropdown"

            print("Verify if the select all ports button is present and click on it")
            select = self.localsuiteudks.select_all_port_diagnostics_page()
            assert select != -1, "unable to verify if the select all ports button is present and click on it"

            print("Verify if the dselect all ports button is present and click on it")
            deselect =self.localsuiteudks.deselect_all_port_diagnostics_page()
            assert deselect != -1, "Unable to verify if the dselect all ports button is present and click on it"

        finally:
            if D360Flag == 1:
                self.xiq.xflowsmanageDevice360.close_device360_window()