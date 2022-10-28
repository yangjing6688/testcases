import time
import pytest

from ..Resources.testcase_base import xiqBase


class TCXM20605Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_standalone
    @pytest.mark.xim_tcxm_20605
    @pytest.mark.p1
    def test_vim_verify_lacp_for_vim_ports_d360(self, onboarded_dut):
        """
        Author        : rvisterineanu
        Description   : Verify that LACP for VIM ports can be created using Device Level Configuration.
        Preconditions : Use EXOS 5520 standalone
         Step	Step Description
         1	    Onboard the EXOS 5520 standalone.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using D360 -> Port configuration aggregate 2 VIM ports.
         5	    Update the device, check the results in CLI and check the number of LACP ports in D360.
         6	    Using D360 -> Port Configuration add 3rd VIM port to the LACP.
         7      Update the device, check the results in CLI and check the number of LACP ports in D360.
         8      Using D360 -> Port Configuration add 4th VIM port to the LACP.
         9      Update the device, check the results in CLI and check the number of LACP ports in D360.
         10     Using D360 -> Port Configuration remove all VIM ports from the LACP.
         """

        self.executionHelper.testSkipCheck()
        dut = onboarded_dut
        try:
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            time.sleep(1)
            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            self.auto_actions.click(self.xiq.xflowsmanageDevice360.get_device360_refresh_page_button())

            button_settings = self.xiq.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            self.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
            time.sleep(5)

            # Aggregate 2 VIM ports
            ports_rows = self.xiq.xflowsmanageDevice360.get_device360_configure_port_rows()
            assert ports_rows, "Could not extract port list from Device360"
            ports_no = len(ports_rows)

            ports_used = [str(ports_no), str(ports_no - 1), str(ports_no - 2), str(ports_no - 3)]

            assert self.suite_udk.device360_aggregate_ports([ports_used[1], ports_used[0]], False), \
                f"Could not aggregate ports {ports_used[1]} and {ports_used[0]}"

            # Update the device and check LACP in Device360 and CLI
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut), "Could not update the device"

            # assert self.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports_used[1]), \
            #     f"LAG {ports_used[1]} is not present."
            lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
            assert str(ports_used[1]) in lacp_config, f"Lag {ports_used[1]} is not present in CLI"

        # Aggregate 3rd VIM port
            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = self.xiq.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            self.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
            time.sleep(5)
            assert self.suite_udk.device360_add_lag_port(ports_used[1], ports_used[2]) == 1, \
                f"Port {ports_used[2]} wasn't added to LAG."

        # Update the device and check LACP in Device360 and CLI
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut), "Could not update the device"

            # assert self.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports_used[1]), \
            #     f"LAG {ports_used[1]} is not present."
            lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
            assert str(ports_used[1]) in lacp_config, f"Lag {ports_used[1]} is not present in CLI"

        # Aggregate 4th VIM port
            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = self.xiq.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            self.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
            time.sleep(5)
            assert self.suite_udk.device360_add_lag_port(ports_used[1], ports_used[3]) == 1, \
                f"Port {ports_used[3]} wasn't added to LAG."

        # Update the device and check LACP in Device360 and CLI
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut), "Could not update the device"

            # assert self.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports_used[1]), \
            #     f"LAG {ports_used[1]} is not present."
            lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
            assert str(ports_used[1]) in lacp_config, f"Lag {ports_used[1]} is not present in CLI"

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = self.xiq.xflowsmanageDevice360.dev360. \
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            self.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
            time.sleep(5)
            # Remove LAG
            assert self.suite_udk.device360_remove_lag(ports_used[1]) == 1, f"LAG {ports_used[1]} was not removed"

            # Update the device and check LACP in Device360 and CLI
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut), "Could not update the device"

            # assert self.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports_used[1]) is None, \
            #     f"LAG {ports_used[1]} is still present."
            lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
            assert str(ports_used[1]) not in lacp_config, f"Lag {ports_used[1]} is still present in CLI"
        finally:
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            self.xiq.xflowsmanageDevices.revert_device_to_template(dut.serial)
