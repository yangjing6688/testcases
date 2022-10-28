import pytest
import random
from extauto.common.AutoActions import AutoActions
from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R7.XIQ_5498_Add_Support_for_Diagnostics_Page.testbed_1_node.Resources import testcase_base

"""
Script title : This script run the below tests for Add Support for Diagnostics Page according with XIQ-5498 story
Author: icosmineanu - TCXM22209, tpodar - TCXM2211
Description : Check that the Diagnostics option is present in Monitoring Menu and the slot selector dropdown isn't present
Testcases : TCXM22209, TCXM22211
Pre-Requests : None
Comments : Other platform than EXOS is not yet supported
Modified by: icosmineanu
"""
class TCXM22209Tests(testcase_base.xiqBase):

    @pytest.mark.development
    @pytest.mark.testbed_1_node
    @pytest.mark.xim_tcxm_22209
    @pytest.mark.xim_tcxm_22211
    @pytest.mark.p1
    def test_tcxm_22209(self, onboarded_switch):
        """
        TCXM - 22209 - Verify that the Diagnostics option is available under the Monitor Tab
        TCXM - 22211 - Verify that the slot dropdown selector is not present for standalone.

        Step    Description

        1       Onboard the EXOS device
        2       Navigate to Device360
        3       In Monitor Tab check that the Diagnostics option is present in Monitoring Menu
        4       Click on the Diagnostics TAB
        --------------
        5       Verify if the slot selector dropdown isn't present
        """
        self.executionHelper.testSkipCheck()
        dut = onboarded_switch

        D360Flag = 0


        try:
            res = self.xiq.xflowscommonDeviceCommon.go_to_device360_window(dut.mac)
            assert res, "Unable to go to device360 window"
            D360Flag = 1
            res = self.xiq.xflowsmanageDevice360.device360_navigate_to_monitor_diagnostics()
            assert res, "Unable to navigate to Diagnostics TAB"

            print("Verify that the slot dropdown selector is not present")

            stack_dropdown = self.xiq.xflowsmanageDevice360.get_device360_monitor_diagnostics_stack_drop_down()
            assert stack_dropdown == -1, "The stack selector dropdown is present for standalone"

        finally:
            if D360Flag == 1:
                self.xiq.xflowsmanageDevice360.close_device360_window()
