# Author:         vstefan
# Description:    Verify that port Path Cost can be set to default for the 4th port on each ASIC.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22144
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM22144Tests(xiqBase):

    @pytest.mark.xim_tcxm_22144
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_22144_verify_default_value_for_path_cost(self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration and  click Create Port Type
                    for the 4th port on each ASIC ("+" button).
        5	        For Port Name & Usage, fill in the Name and Description fields for the port.
        6	        Go to the STP tab in Create Port Type window.
        7	        Set a random value between 1 and 200000000 for Path Cost and save the configuration.
        8	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and verify that the value
                    for the modified Path Cost is the random value.
        9	        Save the Switch Template, update the device and check the results in CLI (show stpd s0 ports [port]).
        10	        Go to Network Policy -> Switch Template -> Port Configuration and  click Edit Port Type
                    for the 4th port on each ASIC.
        11	        Go to the STP tab in Edit Port Type window.
        12	        Leave the Path Cost field empty (default value) and save the configuration.
        13	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and verify that the value
                    for the modified Path Cost is the default value.
        14	        Save the Switch Template, update the device and check the results in CLI (show stpd s0 ports [port]).
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22144'

        self.suite_udk.verify_path_cost_at_template_level(
            onboarded_switch=onboarded_switch,
            path_cost="random",
            port_order_in_asic=4,
            template_switch=template_switch,
            network_policy=network_policy,
            revert_mode="edit_honeycomb_with_empty_path_cost"
        )
