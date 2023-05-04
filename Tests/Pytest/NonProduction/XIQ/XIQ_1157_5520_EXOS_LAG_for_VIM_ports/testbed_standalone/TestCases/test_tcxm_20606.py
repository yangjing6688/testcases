from time import sleep

import pytest

from extauto.common.AutoActions import AutoActions
from ..Resources.testcase_base import xiqBase


class TCXM20606Tests(xiqBase):

    @pytest.mark.development
    @pytest.mark.testbed_standalone
    @pytest.mark.xim_tcxm_20606
    @pytest.mark.p2
    def test_vim_switch_template_with_aggregate_button(self, onboarded_dut, network_policy, template_switch):
        """
        Author        : gburlacu
        Description   : Verify that LACP for VIM ports can be created using Aggregate Ports button from Switch Template
                        for EXOS 5520.
        Preconditions : Use EXOS 5520 devices with 4 ports VIM module.
        Step	Step Description
        1	    Onboard the EXOS 5520 standalone.
        2	    Create a Network Policy with specific 5520 template.
        3	    Assign the previously created Network Policy to the device and update the device.
        4	    Using the Aggregate Ports button from Switch Template -> Port configuration aggregate 2 VIM ports.
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
        main_lag_port = 0
        all_vim_ports_added_to_lacp = False
        try:
            self.switch_template.select_sw_template(network_policy, template_switch, dut.cli_type)
            self.switch_template.go_to_port_configuration()
            self.auto_actions.click(self.sw_template_web_elements.get_aggr_ports_standalone_button())

            print("Get all available ports")
            all_ports = self.sw_template_web_elements.get_select_ports_available()
            total_number_of_ports = len(all_ports)
            main_lag_port = total_number_of_ports - 3
            for i in range(nr_vim_ports):
                vim_ports.insert(0, total_number_of_ports - i)
            self.auto_actions.click(self.sw_template_web_elements.get_cancel_button())

            self.suite_udk.add_ports_to_lag(dut, main_lag_port, vim_ports[0:2], False)

            self.switch_template.select_sw_template(network_policy, template_switch, dut.cli_type)
            self.suite_udk.go_to_switch_template(template_switch)
            self.suite_udk.add_ports_to_lag(dut, main_lag_port, [vim_ports[2]], True)

            self.switch_template.select_sw_template(network_policy, template_switch, dut.cli_type)
            self.suite_udk.go_to_switch_template(template_switch)
            self.suite_udk.add_ports_to_lag(dut, main_lag_port, [vim_ports[3]], True)
            all_vim_ports_added_to_lacp = True

        finally:
            if main_lag_port != 0:
                self.switch_template.select_sw_template(network_policy, template_switch, dut.cli_type)
                self.suite_udk.go_to_switch_template(template_switch)
                lag_text = str(main_lag_port) + " LAG"
                print(f"Remove all ports from {lag_text}")
                labels = self.sw_template_web_elements.get_lag_span(lag=main_lag_port)
                for i in labels:
                    if i.text == lag_text:
                        self.auto_actions.click(i)
                        while True:
                            ports_in_agg = self.sw_template_web_elements.get_port_in_agg()
                            if ports_in_agg is None:
                                break
                            AutoActions().click(ports_in_agg[-1])
                            self.auto_actions.click(
                                self.sw_template_web_elements.get_lag_remove_port_button())
                            sleep(1)

                        if all_vim_ports_added_to_lacp is True:
                            self.suite_udk.save_and_upload(dut)
                            lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
                            if str(main_lag_port) in lacp_config:
                                self.suite_udk.cleanup_lacp_on_dut(dut, main_lag_port)
                                pytest.fail(f'Lag {main_lag_port} was not removed from switch')
                        else:
                            self.suite_udk.save_configuration()
                            lacp_config = self.suite_udk.get_lacp_configuration_from_device(dut)
                            if str(main_lag_port) in lacp_config:
                                self.suite_udk.cleanup_lacp_on_dut(dut, main_lag_port)
                        break
            self.xiq.xflowscommonNavigator.navigate_to_devices()
