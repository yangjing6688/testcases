import pytest
import time
from ..Resources.testcase_base import xiqBase


class TCXM20658Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_20658
    @pytest.mark.p2
    def test_stack_lag_device_level_config(self, onboarded_dut, network_policy, template_stack):
        """
        Author        : tapostol
        Description   : Verify that different LAGs can be configured across different port modules when LACP is
        created using Device Level Configuration.
        Preconditions : Use EXOS 5520 devices with 4 ports VIM module.
        Step	Step Description
        1	    Onboard the EXOS 5520 stack with 2 VIM modules.
        2	    Create a Network Policy with specific 5520 template.
        3	    Assign the previously created Network Policy to the device and update the device.
        4	    Using D360 -> Port Configuration aggregate 2 VIM ports from one VIM module.
        5	    Using D360 -> Port Configuration aggregate 2 VIM ports from the same VIM module.
        6	    Using D360 -> Port Configuration aggregate 2 VIM ports from the other VIM module.
        7	    Using D360 -> Port Configuration aggregate 2 fixed panel ports from different stack slots.
        8	    Update the device, check the results in CLI and check the number of LACP ports in D360 ->
                Port Configuration table.
        9	    Using D360 -> Port Configuration remove all ports from all LAGs.
        10      Update the device, check the results in CLI and check the number of LACP ports in D360 ->
                Port Configuration table.
        """
        self.executionHelper.testSkipCheck()
        self.network_manager.connect_to_network_element_name(onboarded_dut.name)
        try:
            time.sleep(5)
            self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=onboarded_dut.mac)
            time.sleep(5)
            assert self.suite_udk.device360_update_device(), "Could not update the device"

            # Get number of slots:
            number_of_slots = self.suite_udk.device360_get_number_of_slots()
            assert number_of_slots, "[FAIL] Could not get the number of slots"

            # Check if the slots have VIMs
            vim_ports = self.suite_udk.device360_get_vims(number_of_slots)
            assert vim_ports, "[FAIL] No VIM ports found"

            # Navigate to Device360->Port Configuration->Port Settings & Aggregation
            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            button_settings = self.xiq.xflowsmanageDevice360.dev360.\
                get_d360_configure_port_settings_aggregation_tab_button()
            assert button_settings, "Could not find port settings & aggregation button"
            self.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
            time.sleep(5)

            reference_dut_lacp = []

            # Aggregate 2 VIM ports from the first slot
            number_of_aggregated_ports = 0
            assert self.suite_udk.device360_aggregate_stack_ports_slots([vim_ports[0], vim_ports[1]], True),\
                "[FAIL] Could not aggregate first two VIM ports from first slot"
            number_of_aggregated_ports = number_of_aggregated_ports + 2
            reference_dut_lacp.append(vim_ports[0])
            reference_dut_lacp.append(vim_ports[1])

            # Aggregate 2 VIM ports from the first slot
            assert self.suite_udk.device360_aggregate_stack_ports_slots([vim_ports[2], vim_ports[3]], True),\
                "[FAIL] Could not aggregate second two VIM ports from first slot"
            number_of_aggregated_ports = number_of_aggregated_ports + 2
            reference_dut_lacp.append(vim_ports[2])
            reference_dut_lacp.append(vim_ports[3])

            # Try to aggregate 2 VIM ports from another VIM module
            if len(vim_ports) >= 6:
                assert self.suite_udk.device360_aggregate_stack_ports_slots([vim_ports[4], vim_ports[5]], True),\
                    "[FAIL] Could not aggregate first two VIM ports from second slot"
                number_of_aggregated_ports = number_of_aggregated_ports + 2
                reference_dut_lacp.append(vim_ports[4])
                reference_dut_lacp.append(vim_ports[5])
            else:
                self.xiq.xflowsmanageDevice360.utils.print_info("[WARNING]: Couldn't find more than one VIM SLOT")

            aggregate_other_slot = self.\
                suite_udk.device360_aggregate_two_ports_from_different_slots(number_of_slots)

            assert aggregate_other_slot, "Could not aggregate ports from different slots"
            if aggregate_other_slot != 1:
                reference_dut_lacp.append(aggregate_other_slot[0])
                reference_dut_lacp.append(aggregate_other_slot[1])
                number_of_aggregated_ports = number_of_aggregated_ports + 2

            time.sleep(10)

            # Push changes to the device
            assert self.suite_udk.device360_update_device(), "Could not update device"
            time.sleep(15)

            # Check aggregation ports added in Device360 and on dut CLI
            assert self.suite_udk.device360_check_aggregated_ports_number(number_of_aggregated_ports),\
                "[FAIL] Incorrect number of LACP ports"
            assert self.suite_udk.check_lacp_dut(reference_dut_lacp), "Incorrect number of LACPs from dut"

            # Remove aggregation from 2 VIM ports from the first slot
            assert self.suite_udk.device360_remove_stack_ports_slots([vim_ports[0], vim_ports[1]]),\
                "[FAIL] Could not remove aggregation from first VIM ports from first slot"
            number_of_aggregated_ports = number_of_aggregated_ports - 2

            # Remove aggregation from 2 VIM ports from the first slot
            assert self.suite_udk.device360_remove_stack_ports_slots([vim_ports[2], vim_ports[3]]),\
                "[FAIL] Could not remove aggregation from second VIM ports from first slot"
            number_of_aggregated_ports = number_of_aggregated_ports - 2

            # Remove aggregation if exists
            if len(vim_ports) >= 6:
                assert self.suite_udk.device360_remove_stack_ports_slots([vim_ports[4], vim_ports[5]]),\
                    "[FAIL] Could not remove aggregation from first VIM ports from second slot"
                number_of_aggregated_ports = number_of_aggregated_ports - 2

            if aggregate_other_slot != 1:
                assert self.suite_udk.device360_remove_stack_ports_slots(aggregate_other_slot),\
                    "[FAIL] Could not remove aggregation ports 1 from slot 1 and 1 from slot 2"

            time.sleep(10)

            # Push changes to the device
            assert self.suite_udk.device360_update_device(), "Could not update device"
            time.sleep(15)

            # Check aggregation ports removed in Device360 and on dut CLI
            assert self.suite_udk.device360_check_aggregated_ports_number(0),\
                "[FAIL] Incorrect number of LACP ports"
            assert self.suite_udk.check_lacp_dut([]),\
                "[FAIL] Incorrect number of LACPs from dut"

        finally:
            self.network_manager.close_connection_to_network_element(onboarded_dut.name)
            self.xiq.xflowsmanageDevice360.close_device360_window()
            time.sleep(5)
            self.xiq.xflowsmanageDevices.revert_device_to_template(onboarded_dut.mac)
            time.sleep(10)
