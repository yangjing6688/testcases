import time
import pytest

from ..Resources.testcase_base import xiqBase


class TCXM20636Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_20636
    @pytest.mark.p1
    def test_verify_lacp_for_vim_ports_d360(self, onboarded_dut):
        """
        Author        : rvisterineanu
        Description   : Verify that VIM ports can be removed from the existing LACP.
        Preconditions : Use EXOS 5520 stack
         Step	Step Description
         1	    Onboard the EXOS 5520 stack.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using D360 -> Port configuration aggregate 2 VIM ports.
         5	    Update the device, check the results in CLI and check the number of LACP ports in D360.
         6	    Using D360 -> Port Configuration add 3rd VIM port to the LACP.
         7      Update the device, check the results in CLI and check the number of LACP ports in D360.
         8      Using D360 -> Port Configuration add 4th VIM port to the LACP.
         9      Update the device, check the results in CLI and check the number of LACP ports in D360.
         10     Using D360 -> Port Configuration remove all VIM ports from the LACP.
         11     Update the device, check the results in CLI and check the number of LACP ports in D360.

         """

        self.executionHelper.testSkipCheck()
        dut = onboarded_dut

        try:
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            time.sleep(5)

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.suite_udk.navigate_d360_port_settings_and_aggregation()

            # Select unit from stack with VIM ports
            vim_slots_list = self.suite_udk.get_stack_slots_with_vim(dut.stack)
            print(f"Slots with VIM are : {vim_slots_list}")
            first_slot_with_vim = vim_slots_list[0]
            self.suite_udk.device360_change_slot_view(first_slot_with_vim[-1])

            # Aggregate 2 VIM ports
            number_of_aggregated_ports = 0
            ports_rows = self.xiq.xflowsmanageDevice360.get_device360_configure_port_rows()
            assert ports_rows, "Could not extract port list from Device360"
            ports_no = len(ports_rows)
            first_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no)
            second_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 1)
            third_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 2)
            fourth_vim_port = first_slot_with_vim[-1] + ":" + str(ports_no - 3)
            ports_used = [first_vim_port, second_vim_port]
            number_of_aggregated_ports += 2
            assert self.suite_udk.device360_aggregate_ports(ports_used), \
                f"Could not aggregate ports {ports_used}"

            # Update the device and check LACP in Device360 and CLI
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut) == 1, "Could not update the device"

            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            time.sleep(5)

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.suite_udk.navigate_d360_port_settings_and_aggregation()

            # Select unit from stack with VIM ports
            self.suite_udk.device360_change_slot_view(first_slot_with_vim[-1])
            time.sleep(10)

            lag_rows = self.xiq.xflowsmanageDevice360.\
                get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert len(lag_rows) == number_of_aggregated_ports, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"

            lacp_ports_d360 = [second_vim_port + "-" + str(ports_no)]
            assert self.suite_udk.check_lacp_dut_cli(lacp_ports_d360), "Incorrect number of LACPs from dut"

            # Add 3rd VIM port
            assert self.suite_udk.device360_add_lag_port(second_vim_port,
                                                         third_vim_port) == 1, f"Port {third_vim_port} wasn't added"

            # Update the device and check LACP in Device360 and CLI
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut) == 1, "Could not update the device"

            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            time.sleep(5)

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.suite_udk.navigate_d360_port_settings_and_aggregation()

            # Select unit from stack with VIM ports
            self.suite_udk.device360_change_slot_view(first_slot_with_vim[-1])
            time.sleep(10)

            number_of_aggregated_ports += 1
            lag_rows = self.xiq.xflowsmanageDevice360.\
                get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert len(lag_rows) == number_of_aggregated_ports, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"

            lacp_ports_d360 = [third_vim_port + "-" + str(ports_no)]
            assert self.suite_udk.check_lacp_dut_cli(lacp_ports_d360), "Incorrect number of LACPs from dut"

            # Add 4th VIM port
            assert self.suite_udk.device360_add_lag_port(second_vim_port,
                                                         fourth_vim_port) == 1, f"Port {fourth_vim_port} wasn't added"
            time.sleep(5)

            # Update the device and check LACP in Device360 and CLI
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut) == 1, "Could not update the device"

            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            time.sleep(5)

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.suite_udk.navigate_d360_port_settings_and_aggregation()

            # Select unit from stack with VIM ports
            self.suite_udk.device360_change_slot_view(first_slot_with_vim[-1])
            time.sleep(10)

            number_of_aggregated_ports += 1
            print(f'The no of aggregated ports is {number_of_aggregated_ports}')
            lag_rows = self.xiq.xflowsmanageDevice360.\
                get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert len(lag_rows) == number_of_aggregated_ports, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"

            lacp_ports_d360 = [fourth_vim_port + "-" + str(ports_no)]
            assert self.suite_udk.check_lacp_dut_cli(lacp_ports_d360), "Incorrect number of LACPs from dut"

            # Remove VIM ports from LAG
            assert self.suite_udk.device360_remove_lag(second_vim_port) == 1, f"LAG {second_vim_port} was not removed"
            time.sleep(5)

            # Update the device and check LACP in Device360 and CLI
            self.xiq.xflowsmanageDevice360.close_device360_window()
            assert self.suite_udk.devices_update_config(dut) == 1, "Could not update the device"

            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
            time.sleep(5)

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.suite_udk.navigate_d360_port_settings_and_aggregation()

            # Select unit from stack with VIM ports
            self.suite_udk.device360_change_slot_view(first_slot_with_vim[-1])
            time.sleep(10)

            number_of_aggregated_ports -= 4
            print(f'the no of aggregated ports is {number_of_aggregated_ports}')
            lag_rows = self.xiq.xflowsmanageDevice360.\
                get_device360_configure_aggregated_port_settings_aggregation_rows()
            assert lag_rows is None, \
                f"The number of aggregated ports is not {number_of_aggregated_ports}"

            lacp_ports_d360 = []
            assert self.suite_udk.check_lacp_dut_cli(lacp_ports_d360), "Incorrect number of LACPs from dut"

        finally:
            self.xiq.xflowsmanageDevice360.close_device360_window()
            time.sleep(5)
            self.xiq.xflowsmanageDevices.revert_device_to_template(dut.mac)
            time.sleep(15)
