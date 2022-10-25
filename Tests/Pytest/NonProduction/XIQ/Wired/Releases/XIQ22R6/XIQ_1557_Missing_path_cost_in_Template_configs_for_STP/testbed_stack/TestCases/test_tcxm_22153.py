# Author:         sstaut@extremenetworks.com
# Description:    Verify that Path Cost column is present under the STP tab in Switch Template Port Configuration on a stack.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22153
# Date Updated:   17-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_stack.Resources.testcase_base import \
    xiqBase


class TCXM22153Tests(xiqBase):

    @pytest.mark.xim_tcxm_22153
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    @pytest.mark.testbed_stack
    def test_22153_verify_path_cost_column_is_present(
            self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and check
                    that Path Cost Column is present on a stack for slot 1 and slot 2.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22153'

        self.utils.print_info(
            f"Go to the port configuration of '{template_switch}' template.")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
            network_policy, template_switch)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        for slot_index in range(1, len(onboarded_switch.stack) + 1):
            self.suite_udk.navigate_to_slot_template(f'{template_switch}-{slot_index}')
            self.suite_udk.check_stp_path_cost_column()
            self.utils.print_info(f"Successfully verified on slot {slot_index}.")
