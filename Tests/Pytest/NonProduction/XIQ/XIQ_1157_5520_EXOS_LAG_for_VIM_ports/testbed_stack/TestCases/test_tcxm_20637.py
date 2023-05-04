import time
import pytest

from ..Resources.testcase_base import xiqBase


class TCXM20637Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_20637
    @pytest.mark.p1
    def test_verify_lacp_for_vim_ports_sw_template(self, onboarded_dut, network_policy, template_stack):
        """
        Author        : rvisterineanu
        Description   : [STACK] Verify that LACP for VIM ports can be created using Aggregate Ports Across Stack button from Switch Template.
        Preconditions : Use EXOS 5520 stack
         Step	Step Description
         1	    Onboard the EXOS 5520 stack with only one VIM module.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using the Aggregate Ports Across Stack button from Switch Template -> Port configuration aggregate 2 VIM ports.
         5	    Update the device, check the results in CLI.
         6	    Using the Switch Template -> Port Configuration add 3rd VIM port to the LACP.
         7      Update the device, check the results in CLI.
         8      Using the Switch Template -> Port Configuration add 4th VIM port to the LACP.
         9      Update the device, check the results in CLI.
         10     Using the Switch Template -> Port Configuration remove all VIM ports from the LACP.
         """

        self.executionHelper.testSkipCheck()
        dut = onboarded_dut

        try:
            #Aggregate 2 VIM ports
            vim_slots_list = self.suite_udk.get_stack_slots_with_vim(dut.stack)
            print(f"Slots with VIM are : {vim_slots_list}")
            self.switch_template.select_sw_template(network_policy, template_stack, dut.cli_type)
            self.auto_actions.click(self.sw_template_web_elements.get_template_link(template=template_stack))

            time.sleep(2)
            self.switch_template.go_to_port_configuration()
            self.auto_actions.click(self.sw_template_web_elements.get_aggr_ports_across_stack_button())
            self.auto_actions.click(self.sw_template_web_elements.get_lacp_toggle_button())

            first_slot_with_vim = vim_slots_list[0]
            self.auto_actions.click(self.sw_template_web_elements.get_available_slot(slot=int(first_slot_with_vim[-1])))
            all_ports = self.switch_template.sw_template_web_elements.get_select_ports_available()
            total_number_of_ports = len(all_ports)
            first_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports)
            second_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports - 1)
            third_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports - 2)
            fourth_vim_port = first_slot_with_vim[-1] + ":" + str(total_number_of_ports - 3)

            assert self.suite_udk.aggregate_vim_ports_tmpl(first_vim_port, second_vim_port) == 1, \
                                            f"Vim ports {first_vim_port} and {second_vim_port} were not aggregated"

            assert self.suite_udk.devices_update_config(dut) == 1, f"Network policy wasn't deployed successfully."

            #Verify the existing LAG and add 3rd VIM port
            first_template_slot_vim = template_stack + "-" + first_slot_with_vim[-1]
            assert self.suite_udk.navigate_to_sw_template(network_policy, template_stack, first_template_slot_vim) == 1, \
                                        f"Could not navigate to switch template"
            self.suite_udk.verify_lag_is_created_and_add_new_port(first_vim_port, third_vim_port)

            assert self.suite_udk.devices_update_config(dut) == 1, f"Network policy wasn't deployed successfully."

            self.suite_udk.check_lag_cli(dut.name, first_vim_port, third_vim_port)

            #Verify the existing LAG and add 4th VIM port
            assert self.suite_udk.navigate_to_sw_template(network_policy, template_stack, first_template_slot_vim) == 1, \
                f"Could not navigate to switch template"
            self.suite_udk.verify_lag_is_created_and_add_new_port(first_vim_port, fourth_vim_port)

            assert self.suite_udk.devices_update_config(dut) == 1, f"Network policy wasn't deployed successfully."

            self.suite_udk.check_lag_cli(dut.name, first_vim_port, fourth_vim_port)

            #Remove all ports from LACP
            assert self.suite_udk.navigate_to_sw_template(network_policy, template_stack, first_template_slot_vim) == 1, \
                f"Could not navigate to switch template"
            aggregated_ports = [first_vim_port, second_vim_port, third_vim_port, fourth_vim_port]
            self.suite_udk.remove_lag(first_vim_port, aggregated_ports)

            assert self.suite_udk.devices_update_config(dut) == 1, f"Network policy wasn't deployed successfully."

            try:
                self.network_manager.connect_to_network_element_name(dut.name)
                output = self.devCmd.send_cmd(dut.name, 'show configuration | i sharing', max_wait=10, interval=2)
                result = output[0].return_text
            finally:
                self.network_manager.close_connection_to_network_element(dut.name)
            assert "enable sharing" not in result, f"Lag is still present in CLI."

        finally:
            self.xiq.xflowscommonNavigator.navigate_to_devices()
            time.sleep(10)
