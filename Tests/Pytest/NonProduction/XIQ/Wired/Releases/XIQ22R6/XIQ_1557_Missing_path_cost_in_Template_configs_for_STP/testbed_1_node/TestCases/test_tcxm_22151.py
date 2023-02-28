# Author:         vstefan
# Description:    Verify you cannot set a negative value, 0, 200000001 or a character for Path Cost for the second port on each ASIC.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22151
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM22151Tests(xiqBase):

    @pytest.mark.xim_tcxm_22151
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_22151_verify_not_valid_path_cost_values_in_honeycomb(
            self, onboarded_switch, network_policy, template_switch):
        """
        Step        Step Description    
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration and  click Create Port Type
                    for the second port on each ASIC ("+" button).
        5	        For Port Name & Usage tab, fill in the Name field for the port.
        6	        Go to the STP tab in Create Port Type window.
        7	        Set by turn a negative value, 0, 200000001 and a character (e.g. #,%,*)
                    for Path Cost and save the configuration.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22151'
        dut = onboarded_switch

        wrong_values = [-1, 200000001, "#", "b"]
        ports = self.suite_udk.get_one_port_from_each_asic(
            dut=onboarded_switch, order=2)
        port_type_name = self.suite_udk.generate_port_type_name()
        
        self.utils.print_info(
            f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
            network_policy, template_switch, dut.cli_type)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        self.suite_udk.click_on_port_details_tab()

        for port in ports:
            self.utils.print_info(
                f"Verifying that the wrong values ('{wrong_values}') cannot be"
                f"set as path cost in honeycomb port editor for port '{port}'"
            )
            
            try:
                self.suite_udk.open_new_port_type_editor(port=port)
                self.suite_udk.configure_port_name_usage_tab(
                    port_type_name=port_type_name,
                    port_type="access"
                )
                self.suite_udk.go_to_stp_settings_tab_in_honeycomb()
                
                for value in wrong_values:
                    
                    self.utils.print_info(
                        f"Try to set '{value}' as path_cost for port '{port}'")
                    self.suite_udk.set_path_cost_in_honeycomb(value)
                    self.suite_udk.go_to_next_editor_tab()
                    
                    try:
                        self.suite_udk.verify_port_type_editor_still_in_stp_tab()
                    
                    except AssertionError as err:
                        msg = f"Failed! Expected the honeycomb editor to " \
                              f"still be in the STP tab after " \
                              f"clicking NEXT TAB when path_cost='{value}'"
                        self.utils.print_info(msg)
                        self.utils.print_info(repr(err))
                        pytest.fail(msg)
                    
                self.utils.print_info(
                    f"Successfully verified that these values cannot be set"
                    f" (port '{port}'): '{wrong_values}'"
                )
            
            finally:
                self.suite_udk.close_port_type_config()
