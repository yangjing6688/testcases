import time
import pytest

from ..Resources.testcase_base import xiqBase


class TCXM20604Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_standalone
    @pytest.mark.xim_tcxm_20604
    @pytest.mark.p1
    def test_vim_verify_lacp_sw_template(self, onboarded_dut, network_policy, template_switch):
        """
        Author        : rvisterineanu
        Description   : Verify that VIM ports can be removed from the existing LACP.
        Preconditions : Use EXOS 5520 standalone
         Step	Step Description
         1	    Onboard the EXOS 5520 standalone.
         2	    Create a Network Policy with specific 5520 template.
         3	    Assign the previously created Network Policy to the device and update the device.
         4	    Using the Assign Button from Switch Template -> Port configuration aggregate 4 VIM ports.
         5	    Update the device, check the results in CLI and check the number of LACP ports in Switch Template
         6	    Using the Switch Template -> Port configuration remove 2 VIM ports from the LACP.
         7      Update the device, check the results in CLI and check the number of LACP ports in Switch Template
         8      Using the Switch Template remove all VIM ports from the LACP.
         9      Update the device, check the results in CLI and check the number of LACP ports in Switch Template
         """

        self.executionHelper.testSkipCheck()
        dut = onboarded_dut
        main_lag_port = 0
        # Aggregate 4 VIM ports
        try:
            self.switch_template.select_sw_template(network_policy, template_switch)
            self.switch_template.go_to_port_configuration()

            self.auto_actions.click(self.sw_template_web_elements.get_sw_template_assign_button())
            time.sleep(3)
            self.auto_actions.move_to_element(self.sw_template_web_elements.get_sw_template_assign_advanced_actions())
            time.sleep(3)
            self.auto_actions.click(self.sw_template_web_elements.get_sw_template_assign_advanced_actions_aggr())
            time.sleep(3)
            self.auto_actions.click(self.sw_template_web_elements.get_lacp_toggle_button())

            all_ports = self.switch_template.sw_template_web_elements.get_select_ports_available()
            assert all_ports is not None, f"Can't get all ports."
            total_number_of_ports = len(all_ports)
            main_lag_port = total_number_of_ports
            for i in range(0, 4):
                self.auto_actions.click(self.sw_template_web_elements.get_available_port(port=main_lag_port - i))
                time.sleep(1)
                self.auto_actions.click(self.sw_template_web_elements.get_lag_add_port_button())
            time.sleep(5)
            save_and_deploy_nw_policy = self.suite_udk.save_and_upload(dut)
            assert save_and_deploy_nw_policy == 1, f"Network policy wasn't deployed successfully."

            lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
            assert str(main_lag_port) in lacp_config, f"Lag {main_lag_port} is not present in CLI"

        # Verify the existing LAG and remove 2 VIM ports
            self.suite_udk.remove_lag_ports(network_policy, template_switch, main_lag_port, 2)

            save_and_deploy_nw_policy = self.suite_udk.save_and_upload(dut)
            assert save_and_deploy_nw_policy == 1, f"Network policy wasn't deployed successfully."

            lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
            assert str(main_lag_port) not in lacp_config, f"Lag {main_lag_port} is still present in CLI"
            main_lag_port = total_number_of_ports - 3
        finally:
            # remove the remaining ports from LAG
            if main_lag_port > 0:
                self.suite_udk.remove_lag_ports(network_policy, template_switch, main_lag_port, 4)

                save_and_deploy_nw_policy = self.suite_udk.save_and_upload(dut)
                assert save_and_deploy_nw_policy == 1, f"Network policy wasn't deployed successfully."

                lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
                assert lacp_config == "" or str(main_lag_port) not in lacp_config, \
                    f"Lag {main_lag_port} wasn't removed from switch "
            self.xiq.xflowscommonNavigator.navigate_to_devices()
