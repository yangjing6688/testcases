# Author:         rvisterineanu
# Description:    Verify that rebooting the stack doesn't affect the configured Path Cost values
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22171
# Date Updated:   18-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_stack.Resources.testcase_base import    xiqBase


class TCXM22171Tests(xiqBase):

    @pytest.mark.xim_tcxm_22171
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.p2
    @pytest.mark.stack
    def test_22171_verify_path_cost_value_after_reboot_of_device(self, onboarded_switch, network_policy,
                                                                 template_switch):
        """
        TCXM-22171 - Verify that rebooting the stack doesn't affect the configured Path Cost values
        Step        Step Description
        1	        Onboard the EXOS/SR stack.
        2	        Create a Network Policy with specific EXOS/SR device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration and  click Create Port Type
                    for the middle port from each ASIC on wach unit ("+" button).
        5	        For Port Name & Usage tab, fill in the Name field for the port.
        6	        Go to the STP tab in Create Port Type window.
        7	        Set a random value between 1 and 200000000 for Path Cost and save the configuration.
        8	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and verify that the value
                    for the modified Path Cost is the random value.
        9	        Save the Switch Template, update the device and check the results in CLI (show stpd s0 ports [port]).
        10	        Reboot the device
        11	        After the device reboots, go to Network Policy -> Switch Template -> Port Configuration ->
                    STP tab and verify that the value for the modified Path Cost is the random value.
        12	        Unassign the previous created Port Types for ports and delete
                    Port Types from Configure -> Common Objects -> Policy -> Port Types.
        13	        Save the Switch Template, update the device and check the results in CLI (show stpd s0 ports [port]).
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22171'
        dut = onboarded_dut

        ports_slot1 = self.suite_udk.get_one_port_from_each_asic_stack(
            onboarded_switch, order=8, slot="1")
        ports_slot2 = self.suite_udk.get_one_port_from_each_asic_stack(
            onboarded_switch, order=8, slot="2")
        path_cost = self.suite_udk.generate_random_path_cost()

        try:
            self.suite_udk.verify_path_cost_at_template_level(
                onboarded_switch=onboarded_switch,
                path_cost=path_cost,
                template_switch=template_switch,
                network_policy=network_policy,
                revert_configuration=False,
                ports=ports_slot1,
                slot="1"
            )

            self.suite_udk.verify_path_cost_at_template_level(
                onboarded_switch=onboarded_switch,
                path_cost=path_cost,
                template_switch=template_switch,
                network_policy=network_policy,
                revert_configuration=False,
                ports=ports_slot2,
                slot="2"
            )
            self.suite_udk.reboot_dut(onboarded_switch)

            self.xiq.xflowscommonDevices.wait_until_device_online(
                onboarded_switch.mac)
            res = self.xiq.xflowscommonDevices.get_device_status(
                device_serial=onboarded_switch.mac)
            assert res == 'green', \
                f"The device did not come up successfully in the XIQ;" \
                f"Device: {onboarded_switch}"
            self.utils.print_info("Device come up successfully in the XIQ")

            for port in ports_slot1:
                self.suite_udk.verify_path_cost_in_port_configuration_stp_tab(
                    template_switch, network_policy, port, path_cost, slot="1")
                self.suite_udk.verify_path_cost_on_dut(
                    onboarded_switch,
                    port=port,
                    expected_path_cost=path_cost
                )

            for port in ports_slot2:
                self.suite_udk.verify_path_cost_in_port_configuration_stp_tab(
                    template_switch, network_policy, port, path_cost, slot="2")
                self.suite_udk.verify_path_cost_on_dut(
                    onboarded_switch,
                    port=port,
                    expected_path_cost=path_cost
                )

        finally:

            try:
                self.utils.print_info(
                    f"Go to the port configuration of"
                    f" '{template_switch}' template"
                )

                self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
                    network_policy, template_switch, dut.cli_type)
                self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                self.suite_udk.click_on_port_details_tab(level="template")

                self.suite_udk.revert_port_configuration_template_level("Access Port")

            finally:
                self.suite_udk.save_template_config()
                self.utils.print_info(
                    "Saved the port type configuration,"
                    "now push the changes to the dut"
                )
                self.suite_udk.update_and_wait_switch(
                    policy_name=network_policy, dut=onboarded_switch)
