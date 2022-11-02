import pytest
from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R7.XIQ_5498_Add_Support_for_Diagnostics_Page.testbed_stack.Resources import testcase_base

"""
Script title : This script run the below test for Add Support for Diagnostics Page according with XIQ-5498 story
Author: tpodar - TCXM22223
Description : Hover over each item from the seven icons in the port diagnostics section.
Testcases : TCXM2223
Pre-Requests : None
Comments : Other platform than STACK is not yet supported
Modified by: icosmineanu
"""
class TCXM22223Tests(testcase_base.xiqBase):

    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_22223
    @pytest.mark.p1
    def test_tcxm_22223(self,onboarded_stack):
        """
        TCXM - 22223 - Verify if it's possible to hover over the first 7 icons
                       in the port diagnostics section(CPU Usage, Memory, Temperature etc)
                       and the opened box displays correctly the information(Master Unit).

        Step    Description

        1	Onboard the EXOS stack.
        2	Navigate to Device360.
        3	Navigate to the Monitor Tab --> Diagnostics TAB.
        4	Hover over each item from the seven icons in the port diagnostics section.
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

            print("Verify the first seven icons from the top bar (Master Unit)")
            self.localsuiteudks.device360_get_top_bar_information_stack()

            # print("Verify the first seven icons from the top bar for each other unit")
            # self.localsuiteudks.navigate_to_unit_1_n_and_hover_over_top_bar_information_stack(dut)

        finally:
            if D360Flag == 1:
                self.xiq.xflowsmanageDevice360.close_device360_window()