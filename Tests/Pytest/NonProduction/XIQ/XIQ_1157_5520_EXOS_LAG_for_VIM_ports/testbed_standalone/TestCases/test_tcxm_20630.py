import pytest
import time

from ..Resources.testcase_base import xiqBase


class TCXM20630Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_standalone
    @pytest.mark.xim_tcxm_20630
    @pytest.mark.p2
    def test_vim_lag_device_level_config(self, onboarded_dut,):
        """
        Author        : tapostol
        Description   : Verify that different LAGs can be configured across different port modules when LACP is created
                        using Device Level Configuration.
        Preconditions : Use EXOS 5520 devices with 4 ports VIM module.
        Step	Step Description
        1	    Onboard the EXOS 5520 standalone.
        2	    Create a Network Policy with specific 5520 template.
        3	    Assign the previously created Network Policy to the device and update the device.
        4	    Using D360 -> Port Configuration aggregate 2 VIM ports from the VIM module.
        5	    Using D360 -> Port Configuration aggregate 2 VIM ports from the same VIM module.
        6	    Using D360 -> Port Configuration aggregate 2 fixed panel ports.
        7	    Update the device, check the results in CLI and check the number of LACP ports in D360 -> Port
                Configuration table.
        8	    Using D360 -> Port Configuration remove all ports from all LAGs.
        9	    Update the device, check the results in CLI and check the number of LACP ports in D360 -> Port
                Configuration table.
        """
        self.executionHelper.testSkipCheck()
        dut = onboarded_dut
        try:
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            time.sleep(5)

            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = self.xiq.xflowsmanageDevice360.dev360.\
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            self.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
            time.sleep(5)

            # Get list of ports (4 VIM and 2 fixed)
            ports_rows = self.xiq.xflowsmanageDevice360.get_device360_configure_port_rows()
            assert ports_rows, "Could not extract port list from Device360"
            ports_no = len(ports_rows)

            ports_used = [str(ports_no), str(ports_no-1), str(ports_no-2), str(ports_no-3), str(ports_no-4),
                          str(ports_no-5)]

            button_settings = self.xiq.xflowsmanageDevice360.dev360.\
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            self.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
            time.sleep(5)
            # Aggregate 2 VIM ports
            # number_of_aggregated_ports = 0
            assert self.suite_udk.device360_aggregate_ports([ports_used[1], ports_used[0]], True),\
                "Could not aggregate ports n-1, n"
            # number_of_aggregated_ports = number_of_aggregated_ports + 2

            # Aggregate 2 VIM ports
            assert self.suite_udk.device360_aggregate_ports([ports_used[3], ports_used[2]], False),\
                "Could not aggregate ports n-3, n-2"
            # number_of_aggregated_ports = number_of_aggregated_ports + 2

            # Aggregate 2 fixed ports
            assert self.suite_udk.device360_aggregate_ports([ports_used[5], ports_used[4]], False),\
                "Could not aggregate ports n-5, n-4"
            # number_of_aggregated_ports = number_of_aggregated_ports + 2

            # Push changes to the device
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut), "Could not update device"

            # Check aggregation ports added in Device360 and on dut CLI
            # assert self.suite_udk.device360_check_aggregated_ports_number(number_of_aggregated_ports)
            assert self.suite_udk.check_lacp_dut(dut, [ports_used[1] + "-" + ports_used[0],
                                                       ports_used[3] + "-" + ports_used[2],
                                                       ports_used[5] + "-" + ports_used[4]])

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = self.xiq.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            self.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
            time.sleep(5)
            # Remove aggregation for 2 VIM ports
            assert self.suite_udk.device360_remove_port_aggregation([ports_used[1], ports_used[0]], False),\
                "Could not remove ports n-1, n from lacp"
            # number_of_aggregated_ports = number_of_aggregated_ports - 2

            # Remove aggregation for 2 VIM ports
            assert self.suite_udk.device360_remove_port_aggregation([ports_used[3], ports_used[2]], False),\
                "Could not remove ports n-3, n-2 from lacp"
            # number_of_aggregated_ports = number_of_aggregated_ports - 2

            # Remove aggregation for 2 fixed ports
            assert self.suite_udk.device360_remove_port_aggregation([ports_used[5], ports_used[4]], True),\
                "Could not remove ports n-5, n-4 from lacp"
            # number_of_aggregated_ports = number_of_aggregated_ports - 2

            # Push changes to the device
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut), "Could not update device"

            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            # Check aggregation ports removed in Device360 and on dut CLI
            # assert self.suite_udk.device360_check_aggregated_ports_number(number_of_aggregated_ports)
            assert self.suite_udk.check_lacp_dut(dut, [])

        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
            self.xiq.xflowsmanageDevices.revert_device_to_template(dut.serial)
