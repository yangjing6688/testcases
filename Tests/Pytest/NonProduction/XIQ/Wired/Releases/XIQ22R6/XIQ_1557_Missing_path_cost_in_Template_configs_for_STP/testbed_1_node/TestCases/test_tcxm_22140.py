# Author:         vstefan
# Description:    Verify that Path Cost field is present under the STP tab when creating Port Type
#                 for the second port on each ASIC and has an editable field.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22140
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from collections import defaultdict
from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM22140Tests(xiqBase):

    @pytest.mark.xim_tcxm_22140
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_22140_verify_path_cost_field_is_editable_template_level(self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration and  click Create Port Type
                    for the second port on each ASIC ("+" button).
        5	        For Port Name & Usage, fill in the Name and Description fields for the port.
        6	        Go to the STP tab in Create Port Type window.
        7           In the STP tab verify that Path Cost is present and it has an editable field.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22140'
        dut = self.dut

        ports = self.suite_udk.get_one_port_from_each_asic(dut=onboarded_switch, order=2)
        port_config = defaultdict(lambda: {})
        
        for port in ports:
            port_config[port]["port_type_name"] = self.suite_udk.generate_port_type_name()
            port_config[port]["path_cost"] = self.suite_udk.generate_random_path_cost()
        self.utils.print_info(f"Port Type Configuration: {port_config}")

        self.utils.print_info(f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy, template_switch, dut.cli_type)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        self.suite_udk.click_on_port_details_tab()

        for port, port_info in port_config.items():
            
            self.utils.print_info(f"Configuring port '{port}' with {port_info}")
            
            port_type_name = port_info["port_type_name"]
            path_cost = port_info["path_cost"]
            
            try:
                self.suite_udk.open_new_port_type_editor(port=port)
                self.suite_udk.configure_port_name_usage_tab(port_type_name=port_type_name, port_type="access")
                self.suite_udk.go_to_stp_settings_tab_in_honeycomb()
                self.suite_udk.verify_path_cost_field_is_editable()
                self.suite_udk.configure_stp_settings_tab_in_honeycomb(
                    stp_enabled=True,
                    edge_port=True,
                    bpdu_protection="Disabled",
                    path_cost=path_cost,
                    priority=64
                )
                self.suite_udk.go_to_last_page()

                expected_summary = {
                    'STP': 'Enabled', 
                    'Edge Port': 'Enabled', 
                    'BPDU Protection': 'Disabled', 
                    'Priority': '64',
                    'Path Cost': path_cost
                    }
                self.utils.print_info(f"Expected summary: {expected_summary}")
                
                summary = self.suite_udk.get_stp_settings_summary()
                self.utils.print_info(f"Found summary: {summary}")

                self.utils.print_info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                self.utils.print_info("Successfully verified the summary")
            
            finally:
                self.suite_udk.close_port_type_config()
