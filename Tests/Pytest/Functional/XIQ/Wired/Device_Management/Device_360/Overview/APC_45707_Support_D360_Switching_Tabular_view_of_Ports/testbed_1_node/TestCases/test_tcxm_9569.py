# Author:         ssandu
# Description:    To verify if the power used is shown correctly in the D360 table
# Story:          APC-45707 Support D360 Switching Tabular view of Ports
# Testcases:      TCXM-9569
# Date Updated:   5-August-2022
# Pre-Requests:   Ideally the EXOS/VOSS device should not contain an on-prem configuration before running any test case of this suite.
#                 Otherwise intermitent failures could appear during test run.
# Comments:       This test case is applicable for the EXOS and VOSS devices that are supported by XIQ.

import pytest
import time

from Tests.Pytest.Functional.XIQ.Wired.Device_Management.Device_360.Overview.APC_45707_Support_D360_Switching_Tabular_view_of_Ports.testbed_1_node.Resources.testcase_base import xiqBase


class TCXM9569Tests(xiqBase):

    @pytest.mark.tcxm_9569
    @pytest.mark.exos
    @pytest.mark.voss
    @pytest.mark.p1
    @pytest.mark.testbed_1_node
    def test_9569_verify_power_usage_column(self, logger, onboarded_switch):
        """ 
        Step	Step Description
        1	    Onboard device
        2	    Navigate to Device360
        3	    Verify the 'Power Used' column if displays values for all the ports
        4	    Verify the values of 'Power Used' in CLI for all the ports
        5	    Compare XIQ vs CLI values of 'Power Used' for all the ports
        6	    Exit Device360
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'test_apc_45707_tcxm_9569'

        column_name = "Power Used"

        try:
            print("Collect the Power Usages values for all ports from CLI!")
            try:
                self.network_manager.connect_to_network_element_name(onboarded_switch.name)
                ports_power_cli = []

                if onboarded_switch.cli_type.upper() == "EXOS":

                    try:
                        output = self.devCmd.send_cmd(onboarded_switch.name, "show inline-power info ports | begin 1",
                                                 max_wait=5, interval=2)[0].return_text
                        time.sleep(1)
                    except Exception as error:
                        print(error)
                        pytest.skip("The device '{}' does not supported the PoE feature!".format(onboarded_switch.name))

                    output_lines = output.splitlines()
                    for line in output_lines:
                        if not (not line
                                or line.startswith("\x1bE")
                                or line.startswith("*")):
                            line = line.split()
                            port_power_value = [line[0], line[-2]]
                            ports_power_cli.append(port_power_value)
                            print("Line CLI: ", port_power_value)

                elif onboarded_switch.cli_type.upper() == "VOSS":

                    self.devCmd.send_cmd(onboarded_switch.name, "enable", max_wait=5, interval=2)
                    self.devCmd.send_cmd(onboarded_switch.name, "configure terminal", max_wait=5, interval=2)
                    output = self.devCmd.send_cmd(onboarded_switch.name, "show poe-power-measurement | begin 1",
                                             max_wait=5, interval=2, ignore_cli_feedback=True)[0].return_text
                    time.sleep(1)
                    if "Device is not a POE device" in output:
                        print(output)
                        pytest.skip("The device '{}' does not supported the PoE feature!".format(onboarded_switch.name))

                    output_lines = output.splitlines()
                    for line in output_lines:
                        if not (not line
                                or line.startswith("\t")
                                or line.startswith("-")
                                or line.startswith("*")
                                or line.endswith("#")):
                            if "does not support" in line:
                                line = line.split()
                                port_power_value = [line[1], "N/A"]
                                print("Line CLI: ", port_power_value)
                            else:
                                line = line.split()
                                port_power_value = [line[0], line[-1]]
                                print("Line CLI: ", port_power_value)
                            ports_power_cli.append(port_power_value)

            finally:
                self.network_manager.close_connection_to_network_element(onboarded_switch.name)

            print("Collect the Power Usages values for all ports from XIQ!")
            self.suite_udk.go_to_device360(onboarded_switch)

            self.suite_udk.select_max_pagination_size()

            checkbox_button = self.xiq.xflowsmanageDevice360.dev360.get_device360_columns_toggle_button()

            self.auto_actions.click(checkbox_button)
            time.sleep(3)

            all_checkboxes = self.xiq.xflowsmanageDevice360.dev360.get_device360_all_checkboxes()
            columns_found_enabled = [k for k, v in all_checkboxes.items() if v["is_selected"] is True]
            logger.info(f"These columns are currently found enabled: {columns_found_enabled}")

            if column_name in columns_found_enabled:
                logger.info(f"{column_name} column is already visible")
            else:
                logger.info(f"{column_name} column is not already visible; click on its checkbox")
                self.auto_actions.click(all_checkboxes[column_name]['element'])
                time.sleep(5)

            ports_power_xiq = []
            ports_table = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            for entry in ports_table:
                assert column_name.upper() in entry, f"Failed to find {column_name} column in table row: {entry}"
                if not (entry['PORT NAME'] == "mgmt"):
                    power_value_port_xiq = entry[column_name.upper()].split()
                    line_xiq = [entry['PORT NAME'], power_value_port_xiq[0]]
                    ports_power_xiq.append(line_xiq)
                    print("Line XIQ: ", line_xiq)

            print("Compare the Power Usages values - XIQ vs CLI!")
            for result in self.suite_udk.check_power_values(ports_power_xiq, ports_power_cli):
                if result[1] != "PASSED":
                    pytest.fail(
                        "For {}, the 'Power Usages' values from XIQ and CLI do NOT match "
                        "- Jira ticket XIQ-5903".format(result[0]))

        finally:
            self.suite_udk.select_pagination_size("10")
            self.xiq.xflowsmanageDevice360.close_device360_window()
