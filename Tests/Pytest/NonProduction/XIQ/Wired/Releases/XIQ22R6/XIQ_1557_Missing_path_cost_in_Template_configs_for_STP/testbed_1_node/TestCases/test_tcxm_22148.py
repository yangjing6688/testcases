# Author:         vstefan
# Description:    Verify that the Path Cost Value is present and correct in Edit Port Type window, Summary tab.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22148
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from collections import defaultdict
from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM22140Tests(xiqBase):

    @pytest.mark.xim_tcxm_22148
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    @pytest.mark.testbed_1_node
    def test_22148_verify_path_cost_value_in_edit_port_type_window(
            self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration and  click Create Port Type
                    for the 5th port on each ASIC ("+" button).
        5	        For Port Name & Usage, fill in the Name field for the port.
        6	        Go to the STP tab in Create Port Type window.
        7	        Set a random value between 1 and 200000000 for Path Cost and save the configuration.
        8	        Go to Network Policy -> Switch Template -> Port Configuration and  click Edit Port Type ("Edit" button).
        9	        Go to Summary tab under Edit Port Type window and check the value for Path Cost.
        10	        Unassign the previous created Port Types for ports and delete Port Types
                    from Configure -> Common Objects -> Policy -> Port Types.
        """
        self.executionHelper.testSkipCheck()
        self.tb = PytestConfigHelper(config)
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22148'
        dut = onboarded_switch

        ports = self.suite_udk.get_one_port_from_each_asic(dut=onboarded_switch, order=5)
        port_config = defaultdict(lambda: {})
        for port in ports:
            port_config[port]["port_type_name"] = self.suite_udk.generate_port_type_name()
            port_config[port]["path_cost"] = self.suite_udk.generate_random_path_cost()
        self.utils.print_info(f"Port Type Configuration: {port_config}")

        self.utils.print_info(f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy, template_switch, self.tb.dut1.cli_type)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        self.suite_udk.click_on_port_details_tab()

        try:
            for port, port_info in port_config.items():
                
                port_type_name = port_info["port_type_name"]
                path_cost = port_info["path_cost"]
                self.utils.print_info(
                    f"Create a new port type '{port_type_name}' with path cost '{path_cost}' for port '{port}'")
                
                expected_summary = {
                    'STP': 'Enabled', 
                    'Edge Port': 'Enabled', 
                    'BPDU Protection': 'Disabled', 
                    'Priority': '64', 
                    'Path Cost': path_cost
                    }
                self.utils.print_info(f"Expected summary: {expected_summary}")
                
                _, create_port_type_summary = self.xiq.xflowsmanageDevice360.create_port_type_with_stp_settings(
                    port, port_type_name=port_type_name, path_cost=path_cost, description="description", status=True, 
                    port_usage="access", priority=64, bpdu_protection="Disabled", stp_enabled=True, edge_port=True)
                self.utils.print_info(
                    f"Summary from create port type in honeycom (port {port}): {create_port_type_summary}")

                self.utils.print_info(
                    f"Verify that the configured fields appear correctly in the summary tab (port {port})")
                assert all(expected_summary[k] == create_port_type_summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones (port {port}). " \
                    f"Expected summary: {expected_summary}\nFound summary: {create_port_type_summary}"
                self.utils.print_info(
                    f"Successfully verified the summary at port type creation in honeycomb (port {port})")
                
                self.utils.wait_till(timeout=10)
                _, edit_port_type_summary = self.xiq.xflowsmanageDevice360.edit_stp_settings_in_honeycomb_port_editor(
                    port, port_type_name)
                self.utils.print_info(
                    f"Summary from edit port type in honeycomb (port {port}): {create_port_type_summary}")
        
                self.utils.print_info(
                    f"Verify that the configured fields appear correctly in the summary tab (port {port})")
                assert all(expected_summary[k] == edit_port_type_summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones (port {port}). " \
                    f"Expected summary: {expected_summary}\nFound summary: {edit_port_type_summary}"
                self.utils.print_info(
                    f"Successfully verified the summary at port type edit in honeycomb (port {port})")

        finally:
            
            self.utils.print_info(f"Go to the port configuration of '{template_switch}' template")
            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
                network_policy, template_switch, dut.cli_type)
            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                    
            self.suite_udk.revert_port_configuration_template_level(
                "Auto-sense Port" if onboarded_switch.cli_type.upper() == "VOSS" else "Access Port")
            self.suite_udk.save_template_config()
