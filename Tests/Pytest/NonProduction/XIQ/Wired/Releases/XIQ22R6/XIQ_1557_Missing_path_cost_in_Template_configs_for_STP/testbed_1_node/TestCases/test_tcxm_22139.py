# Author:         vstefan
# Description:    Verify that Path Cost for every port is set initially to default value (empty field).
# Story:          XIQ 1557 Missing path cost in Template configs for STP
# Testcases:      TCXM-22139
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermittent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import re

from collections import defaultdict
from Tests.Pytest.NonProduction.XIQ.Wired.Releases.XIQ22R6.XIQ_1557_Missing_path_cost_in_Template_configs_for_STP.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM22139Tests(xiqBase):

    @pytest.mark.xim_tcxm_22139
    @pytest.mark.development
    @pytest.mark.EXOS
    @pytest.mark.VOSS
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_22139_verify_default_values_of_path_cost_at_template_level(self, network_policy, template_switch):
        """
        Step        Step Description
        1	        Onboard the EXOS device.
        2	        Create a Network Policy with specific EXOS device template.
        3	        Assign the previously created Network Policy to the device and update the device.
        4	        Go in device's CLI and set Path Cost for all ports to auto (configure stpd s0 ports cost auto [ports]).
        5	        Go to Network Policy -> Switch Template -> Port Configuration -> STP tab and verify that the field for
                    Path Cost is empty (meaning the Path Cost value is default).
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_XIQ_1557_TCXM_22139'

        self.utils.print_info(
            f"Go to the port configuration of '{template_switch}' template")
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(
            network_policy, template_switch)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        self.suite_udk.click_on_stp_tab(level="template")
        rows = self.suite_udk.get_stp_port_configuration_rows(level="template")

        results = defaultdict(lambda: {"msg": "", "status": False})
        
        for row in rows:
            
            port_match = re.search(r"^(.*)\n", row.text)
            assert port_match, f"Failed to get the port from '{row.text}'"
            port = port_match.group(1)
            
            path_cost_element, _ = self.utils.wait_till(
                func=lambda:
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_sw_template_path_cost_row(row),
                exp_func_resp=True,
                delay=1
            )
            
            path_cost_value = path_cost_element.get_attribute("value")
            results[port]["status"] = path_cost_value == ""
            results[port]["msg"] = f"Expected the path cost value to be '' but found '{path_cost_value}'" \
                                   f" for row with port='{port}'" if path_cost_value != "" else \
                f"Successfully verified the default value of path cost for row with port={port}"
        
        for port, data in {port: data for port, data in results.items() if data["status"] is True}.items():
            self.utils.print_info(data["msg"])
        
        failed_verifications = {port: data for port, data in results.items() if data["status"] is False}
        
        if failed_verifications:
            for port, data in failed_verifications.items():
                self.utils.print_error(data["msg"])
            pytest.fail("\n".join(list(data["msg"] for data in failed_verifications.values())))
        
        self.utils.print_info("Successfully verified that the default path cost values are '' at template level")
