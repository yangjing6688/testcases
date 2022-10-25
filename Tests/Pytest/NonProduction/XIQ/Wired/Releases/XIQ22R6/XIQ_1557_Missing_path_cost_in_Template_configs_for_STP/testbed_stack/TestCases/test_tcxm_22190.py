# Author:         rvisterineanu
# Description:    Verify you cannot set a negative value, 0, 200000001 or a character for Path Cost
#                 for the 3rd port on each ASIC on both stack slots.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22190
# Date Updated:   18-August-2022
# Pre-Requests:   Ideally the EXOS and SR device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and SR devices that are supported by XIQ.

import pytest


from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_stack.Resources.testcase_base import xiqBase


class TCXM22190Tests(xiqBase):

    @pytest.mark.xim_tcxm_22190
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.p2
    @pytest.mark.testbed_stack
    def test_22190_verify_not_valid_path_cost_values_in_honeycomb(
            self, onboarded_switch, network_policy, template_switch):
        """
        TCXM-22190 - Verify you cannot set a negative value, 0, 200000001 or a character for Path Cost
                    for the 3rd port on each ASIC on both stack slots.
        Step        Step Description
        1	        Onboard the EXOS/SR stack.
        2	        Create a Network Policy with specific EXOS/SR device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration and  click Create Port Type
                    for the 3rd port on each ASIC ("+" button).
        5	        For Port Name & Usage tab, fill in the Name field for the port.
        6	        Go to the STP tab in Create Port Type window.
        7	        Set by turn a negative value, 0, 200000001 and a character (e.g. #,%,*)
                    for Path Cost and save the configuration.
        8           Repeat steps 4-6 for slot 2 template.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22190'

        self.suite_udk.verify_path_cost_wrong_value(
            template_switch=template_switch,
            network_policy=network_policy,
            dut=onboarded_switch,
            order=3,
            slot="1"
        )

        self.suite_udk.verify_path_cost_wrong_value(
            template_switch=template_switch,
            network_policy=network_policy,
            dut=onboarded_switch,
            order=3,
            slot="2"
        )
