# Author:         rvisterineanu
# Description:    Verify that the Path Cost Value is present and correct in Edit Port Type window Summary tab for the second port on
#                 each ASIC on both stack slots.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22167
# Date Updated:   18-August-2022
# Pre-Requests:   Ideally the EXOS and SR device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and SR devices that are supported by XIQ.

import pytest


from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_stack.Resources.testcase_base import xiqBase


class TCXM22167Tests(xiqBase):

    @pytest.mark.xim_tcxm_22167
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.p2
    @pytest.mark.testbed_stack
    def test_22167_verify_random_value_as_path_cost(self, onboarded_switch, network_policy, template_switch):
        """
        TCXM-22167 - Verify that the Path Cost Value is present and correct in Edit Port Type window Summary tab for the second port on
        each ASIC on both stack slots.
               Step        Step Description
               1	        Onboard the EXOS/SR stack.
               2	        Create a Network Policy with specific EXOS/SR device template.
               3	        Assign the previously created Network Policy to the device and update the device.
               4	        Go to Network Policy -> Switch Template -> Port Configuration -> slot 1 Template and
                            click Create Port Type for the second port on each ASIC ("+" button).
               5	        For Port Name & Usage, fill in the Name field for the port.
               6	        Go to the STP tab in Create Port Type window.
               7	        Set a random value between 1 and 200000000 for Path Cost and save the configuration.
               8	        Go to Network Policy -> Switch Template -> Port Configuration and  click Edit Port Type ("Edit" button).
               9	        Go to Summary tab under Edit Port Type window and check the value for Path Cost.
               10           Repeat steps 4-9 for slot 2 template.

               """

        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22167'

        try:
            self.suite_udk.verify_path_cost_edit_summary(
                template_switch=template_switch,
                network_policy=network_policy,
                dut=onboarded_switch,
                order=2,
                slot="1"
                )

            self.suite_udk.verify_path_cost_edit_summary(
                template_switch=template_switch,
                network_policy=network_policy,
                dut=onboarded_switch,
                order=2,
                slot="2"
            )
        finally:

            self.utils.print_info(f"Go to the port configuration of '{template_switch}' template")
            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
                network_policy, template_switch)
            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            self.suite_udk.revert_port_configuration_template_level("Access Port")
            self.suite_udk.save_template_config()