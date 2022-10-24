# Author:         sstaut@extremenetworks.com
# Description:    Verify that a random value between 1 and 200000000 can be set for Path Cost for the third port on each ASIC only on stack slot 2.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22161
# Date Updated:   18-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_stack.Resources.testcase_base import xiqBase


class TCXM22161Tests(xiqBase):

    @pytest.mark.xim_tcxm_22161
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.p2
    @pytest.mark.testbed_stack
    def test_22161_verify_random_value_as_path_cost(self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration -> slot 2 Template and  click Create Port Type for the last port on each ASIC ("+" button)
        5	        For Port Name & Usage, fill in the Name and Description fields for the port.
        6	        Go to the STP tab in Create Port Type window.
        7	        Set a random value between 1 and 200000000 for Path Cost and save the configuration.
        8	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and verify that the value for the modified Path Cost is the random value.
        10	        Save the Switch Template, update the device and check the results in CLI (show stpd s0 ports [port]).
        11	        Unassign the previous created Port Types for ports and delete Port Types from Configure -> Common Objects -> Policy -> Port Types.
        12	        Save the Switch Template, update the device and check the results in CLI (show stpd s0 ports [port]).
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22161'

        self.suite_udk.verify_path_cost_at_template_level(
            onboarded_switch=onboarded_switch,
            path_cost="random",
            port_order_in_asic=3,
            template_switch=template_switch,
            network_policy=network_policy,
            slot="2"
        )
