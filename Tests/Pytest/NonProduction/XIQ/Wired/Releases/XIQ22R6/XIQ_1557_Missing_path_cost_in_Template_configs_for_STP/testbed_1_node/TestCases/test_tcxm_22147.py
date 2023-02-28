# Author:         vstefan
# Description:    Verify that the Path Cost Value is present and correct in Create Port Type window, Summary tab.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22147
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM22147Tests(xiqBase):

    @pytest.mark.xim_tcxm_22147
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_22147_verify_path_cost_value_in_create_port_type_window(
            self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration and  click Create Port Type
                    for the 4th port on each ASIC ("+" button).
        5	        For Port Name & Usage, fill in the Name field for the port.
        6	        Go to the STP tab in Create Port Type window.
        7	        Set a random value between 1 and 200000000 for Path Cost.
        8	        Go to Summary tab under Create Port Type window and verify the value for Path Cost.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22147'
        dut = self.dut

        ports = self.suite_udk.get_one_port_from_each_asic(dut=onboarded_switch, order=4)

        self.utils.print_info(f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy, template_switch, dut.cli_type)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        self.suite_udk.click_on_port_details_tab()
        
        for port in ports:
        
            port_type_name = self.suite_udk.generate_port_type_name()
            path_cost = self.suite_udk.generate_random_path_cost()
            self.utils.print_info(
                f"Create a new port type '{port_type_name}' with path cost '{path_cost}' for port '{port}'")
            
            try:
                expected_summary = {
                    'STP': 'Enabled', 
                    'Edge Port': 'Enabled', 
                    'BPDU Protection': 'Disabled', 
                    'Priority': '64', 
                    'Path Cost': path_cost
                    }
                self.utils.print_info(f"Expected summary: {expected_summary}")
                
                _, summary = self.xiq.xflowsmanageDevice360.create_port_type_with_stp_settings(
                    port, port_type_name=port_type_name, path_cost=path_cost, description="description", status=True, 
                    port_usage="access", priority=64, bpdu_protection="Disabled", stp_enabled=True, edge_port=True,
                    save=False)
                self.utils.print_info(f"Found summary: {summary}")

                self.utils.print_info("Verify that the configured fields appear correctly in the summary tab")
                assert all(expected_summary[k] == summary[k] for k in expected_summary), \
                    f"Not all the values of the summary are the expected ones. " \
                    f"Expected summary: {expected_summary}\nFound summary: {summary}"
                self.utils.print_info(
                    f"Successfully verified the summary for port type '{port_type_name}' "
                    f"with path cost '{path_cost}' for port '{port}'"
                )
                
            finally:
                self.suite_udk.close_port_type_config()
