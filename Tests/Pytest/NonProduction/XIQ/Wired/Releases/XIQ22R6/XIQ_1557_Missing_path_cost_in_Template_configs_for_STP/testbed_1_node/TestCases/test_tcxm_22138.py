# Author:         vstefan
# Description:    Verify that Path Cost column is present under the STP tab in Switch Template Port Configuration.
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22138
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest

from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM22138Tests(xiqBase):

    @pytest.mark.xim_tcxm_22138
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p2
    @pytest.mark.testbed_1_node
    def test_22138_verify_path_cost_column_is_present(self, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and check
                    that Path Cost Column is present.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22138'
        
        self.utils.print_info(
            f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
            network_policy, template_switch)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        self.suite_udk.click_on_stp_tab(level="template")
        rows = self.suite_udk.get_stp_port_configuration_rows(level="template")

        for index, row in enumerate(rows):
            
            path_cost_element, _ = self.utils.wait_till(
                func=lambda:
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_path_cost_row(row),
                silent_failure=True,
                exp_func_resp=True, 
                delay=1
            )
            
            assert path_cost_element, \
                f"Did not find the path cost element for this row:" \
                f" '{row.text}' (row index: {index})"
            self.utils.print_info(
                f"Successfully found the path cost element (it has "
                f"value='{path_cost_element.get_attribute('value')}') "
                f"for the row with index: {index}")

        self.utils.print_info(
            "Successfully verified that the path cost element is contained"
            "in every row of the STP port configuration table"
        )
