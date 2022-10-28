# Author:         vstefan
# Description:    Verify that Configuration Audit reflects the changes when modifying Path Cost for the second port on each ASIC.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22145
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM22145Tests(xiqBase):

    @pytest.mark.xim_tcxm_22145
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    @pytest.mark.testbed_1_node
    def test_22145_verify_delta_cli(self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration and  click Create Port Typefor
                    the second port on each ASIC ("+" button).
        5	        For Port Name & Usage tab, fill in the Name field for the port.
        6	        Go to the STP tab in Create Port Type window.
        7	        Set a random value between 1 and 200000000 for Path Cost and save the configuration.
        8	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and verify that the value
                    for the modified Path Cost is the random value.
        9	        Check Devices -> Configuration Audit button status and Delta CLI.
        10	        Save the Switch Template, update the device and check the results in CLI (show stpd s0 ports [port]).
        11	        Unassign the previous created Port Types for ports and delete Port Types
                    from Configure -> Common Objects -> Policy -> Port Types.
        12	        Save the Switch Template, update the device and check the results in CLI (show stpd s0 ports [port]).
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22145'

        self.suite_udk.verify_path_cost_at_template_level(
            onboarded_switch=onboarded_switch,
            path_cost="random",
            port_order_in_asic=2,
            template_switch=template_switch,
            network_policy=network_policy,
            verify_delta_cli=True
        )
