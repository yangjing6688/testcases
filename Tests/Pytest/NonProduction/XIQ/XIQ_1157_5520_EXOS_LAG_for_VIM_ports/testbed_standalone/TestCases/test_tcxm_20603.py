import pytest
import time

from ..Resources.testcase_base import xiqBase


class TCXM20603Tests(xiqBase):

    @pytest.mark.development
    @pytest.mark.testbed_standalone
    @pytest.mark.xim_tcxm_20603
    @pytest.mark.p2
    def test_vim_switch_template_assign_button(self, onboarded_dut, network_policy, template_switch):
        """
        Author        : sstaut@extremenetworks.com
        Description   : Verify that LACP for VIM ports can be created using Assign button from Switch Template
                        for EXOS 5520.
        Preconditions : Use EXOS 5520 devices with 4 ports VIM module.
        Step	Step Description
        1	    Onboard the EXOS 5520 standalone.
        2	    Create a Network Policy with specific 5520 template.
        3	    Assign the previously created Network Policy to the device.
        4	    Using the Assign button from Switch Template -> Port configuration aggregate 2 VIM ports.
        5	    Update the device, check the results in CLI.
        6	    Using the Switch Template -> Port Configuration add the 3rd VIM port to the LACP.
        7	    Update the device, check the results in CLI.
        8	    Using the Switch Template -> Port Configuration add the 4rd VIM port to the LACP.
        9	    Update the device, check the results in CLI.
        10	    Using the Switch Template -> Port Configuration remove all VIM ports from the LACP.
        11      Update the device, check the results in CLI.
        """
        self.executionHelper.testSkipCheck()
        dut = onboarded_dut
        vim_ports = []
        nr_vim_ports = 4
        main_lag_port = ""
        try:
            self.switch_template.select_sw_template(network_policy, template_switch)
            self.switch_template.go_to_port_configuration()
            print("Click on Assign button to aggregate ports.")
            time.sleep(1)
            self.auto_actions.click(self.switch_template.sw_template_web_elements.get_sw_template_assign_button())
            time.sleep(1)
            self.auto_actions.move_to_element(self.switch_template.sw_template_web_elements.
                                              get_sw_template_assign_advanced_actions())
            time.sleep(1)
            self.auto_actions.move_to_element(self.switch_template.sw_template_web_elements.
                                              get_sw_template_assign_advanced_actions_aggr())
            time.sleep(1)
            self.auto_actions.click(self.switch_template.sw_template_web_elements.
                                    get_sw_template_assign_advanced_actions_aggr())
            time.sleep(1)

            print("Get all available ports.")
            all_ports = self.switch_template.sw_template_web_elements.get_select_ports_available()
            total_number_of_ports = len(all_ports)
            main_lag_port = total_number_of_ports - 3
            for i in range(nr_vim_ports):
                vim_ports.insert(0, total_number_of_ports - i)
            self.auto_actions.click(self.switch_template.sw_template_web_elements.get_cancel_button())

            self.suite_udk.add_ports_to_lag(dut, main_lag_port, vim_ports[0:2], False)

            self.switch_template.select_sw_template(network_policy, template_switch)
            self.suite_udk.go_to_switch_template(template_switch)
            self.suite_udk.add_ports_to_lag(dut, main_lag_port, [vim_ports[2]], True)

            self.switch_template.select_sw_template(network_policy, template_switch)
            self.suite_udk.go_to_switch_template(template_switch)
            self.suite_udk.add_ports_to_lag(dut, main_lag_port, [vim_ports[3]], True)
        finally:
            if main_lag_port != "":
                self.switch_template.select_sw_template(network_policy, template_switch)
                self.suite_udk.go_to_switch_template(template_switch)

                lag_text = str(main_lag_port) + " LAG"
                print(f"Remove all ports from {lag_text}.")
                labels = self.switch_template.sw_template_web_elements.get_lag_span(lag=main_lag_port)
                if labels is not None:
                    found_label = False
                    for i in labels:
                        if i.text == lag_text:
                            self.auto_actions.click(i)
                            found_label = True
                            break
                    if found_label:
                        vim_ports.reverse()
                        for port in vim_ports:
                            print(f"Remove port {port} from lag.")
                            selected_port = self.switch_template.sw_template_web_elements.get_selected_port(port=port)
                            if selected_port is not None:
                                if port == vim_ports[0]:
                                    self.auto_actions.click(selected_port)
                                self.auto_actions.click(self.switch_template.sw_template_web_elements.
                                                        get_lag_remove_port_button())
                                selected_port = self.switch_template.sw_template_web_elements.\
                                    get_selected_port(port=port)
                            assert selected_port is None, f"Port {port} wasn't removed."
                        self.suite_udk.save_and_upload(dut)
                        lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
                        assert lacp_config == "" or str(main_lag_port) not in lacp_config, \
                            f"Lag {main_lag_port} wasn't removed from switch."
            self.xiq.xflowscommonNavigator.navigate_to_devices()
