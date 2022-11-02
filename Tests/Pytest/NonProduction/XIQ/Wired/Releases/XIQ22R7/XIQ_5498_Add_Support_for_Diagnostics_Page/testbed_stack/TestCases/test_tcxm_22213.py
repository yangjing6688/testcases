import pytest
from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R7.XIQ_5498_Add_Support_for_Diagnostics_Page.testbed_stack.Resources import testcase_base

"""
Script title : This script run the below tests for Add Support for Diagnostics Page according with XIQ-5498 story
Author: icosmineanu - TCXM22213, TCXM2221
Description : Check if Diagnostics option is available for a stack and check if the device information from the header side is displayed correctly according to the cli
Testcases : TCXM22213, TCXM22221
Pre-Requests : None
Comments : Other platform than STACK is not yet supported
"""
class TCXM22213Tests(testcase_base.xiqBase):

    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_22213
    @pytest.mark.xim_tcxm_22221
    @pytest.mark.p1
    def test_tcxm_22213(self, onboarded_stack):
        """
        TCXM - 22213 - Verify that the Diagnostics option is available under the Monitor Tab for a stack (Step 1-4)
        TCXM - 22221 - Verify if the device information(ip, mac address, software version, model, serial, make, iqagent version) from the header side is displayed correctly according to the cli (Master Unit) (Step 1-5)

        Step    Description

        1       Onboard the EXOS device
        2       Navigate to Device360
        3       In Monitor Tab check that the Diagnostics option is present in Monitoring Menu
        4       Click on the Diagnostics TAB
        --------------
        5       For each value displayed in the header part(device information), verify if it coincides with the cli value
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

            print("Navigate to master unit")
            stacking_info_cli = self.localsuiteudks.get_stacking_details_cli(dut)
            print(f"Print a list with mac add, number of slot and role for each stack unit: {stacking_info_cli}")
            res = self.localsuiteudks.navigate_to_unit_options_from_xiq_diagnostics_page(stacking_info_cli[0][0][1],
                                                                          stacking_info_cli[0][0][2].upper())

            print("Verify if the device information from the header side is displayed correctly according to the CLI - Master Unit")
            res = self.localsuiteudks.match_info_stack_cli_with_xiq(dut, stacking_info_cli[0][0][1])
            assert res != -1, "Unable to verify if the device information from the header side is displayed correctly according to the CLI"

        finally:
            if D360Flag == 1:
                self.xiq.xflowsmanageDevice360.close_device360_window()