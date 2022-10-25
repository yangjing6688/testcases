# Author:         sstaut@extremenetworks.com
# Description:    Verify that Path Cost for every port is set initially to default value (empty field) on a stack.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22154
# Date Updated:   19-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_stack.Resources.testcase_base import \
    xiqBase


class TCXM22154Tests(xiqBase):

    @pytest.mark.xim_tcxm_22154
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    @pytest.mark.testbed_stack
    def test_22154_verify_default_values_of_path_cost_at_template_level(
            self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go in device's CLI and set Path Cost for all ports to auto (configure stpd s0 ports cost auto [ports]).
        5	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and verify that the field for
                    Path Cost is empty (meaning the Path Cost value is default) for every stack slot.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22154'

        self.utils.print_info(
            f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
            network_policy, template_switch)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        for slot_index in range(1, len(onboarded_switch.stack) + 1):
            self.suite_udk.navigate_to_slot_template(f'{template_switch}-{slot_index}')
            self.suite_udk.check_default_stp_path_cost()
            self.utils.print_info(f"Successfully verified default STP cost in Device Template on slot {slot_index}.")
