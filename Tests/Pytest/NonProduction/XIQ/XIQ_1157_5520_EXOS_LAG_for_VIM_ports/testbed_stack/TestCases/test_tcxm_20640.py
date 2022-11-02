from time import sleep

import pytest

from extauto.common.AutoActions import AutoActions
from ..Resources.testcase_base import xiqBase


class TCXM20640Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_20640
    @pytest.mark.p2
    def test_switch_template(self, onboarded_dut, network_policy, template_stack):
        """
         Author        : gburlacu
         Description   : Verify that LACP cannot be formed between VIM and fixed panel ports using Aggregate Ports
                         Across Stack button from Switch Template.
         Preconditions : Use EXOS 5520 stack
         Step	Step Description
         1	    Onboard the EXOS 5520 stack with only one VIM module.
         2	    Create a Network Policy with specific 5520 template.
         3	    Using the Aggregate Ports Across Stack button from Switch Template -> Port Configuration aggregate
                1 VIM port and 1 fixed panel port from the same stack slot.
         4	    Check if an error message appears.
         5	    Using the Aggregate Ports Across Stack button from Switch Template -> Port Configuration aggregate
                1 VIM port and 1 fixed panel port from different stack slot.
         6	    Check if an error message appears.
         """

        lst_errors = ["You cannot aggregate Ethernet ports with SFP ports.",
                      "Only VIM ports within the same VIM can be part of the same LAG",
                      "Selected ports have different maximum speeds and cannot be part of the same LAG."]
        try:
            self.switch_template.select_sw_template(network_policy, template_stack)

            if self.sw_template_web_elements.get_sw_template_port_configuration_tab() is None:
                AutoActions().click(self.sw_template_web_elements.get_template_link(template=template_stack))

            sleep(2)

            self.switch_template.go_to_port_configuration()

            # 1. aggregate 1 VIM port and 1 fixed panel port from the first stack slot.
            AutoActions().click(self.switch_template.sw_template_web_elements.get_aggr_ports_across_stack_button())
            AutoActions().click(self.sw_template_web_elements.get_lacp_toggle_button())

            print("Get all available ports for the first switch")
            all_ports = self.switch_template.sw_template_web_elements.get_select_ports_available()
            total_number_of_ports = len(all_ports)
            port_fixed = "1:1"
            port_vim = "1:" + str(total_number_of_ports)

            print(f"Add port {port_fixed} to lag group {port_fixed}")
            AutoActions().click(self.sw_template_web_elements.get_available_port(port=port_fixed))
            AutoActions().click(self.sw_template_web_elements.get_lag_add_port_button())
            sleep(1)
            selected_port = self.sw_template_web_elements.get_selected_port(port=port_fixed)
            assert selected_port is not None, f"Port {port_fixed} wasn't added"

            print(f"Add port {port_vim} to lag group {port_fixed}")
            AutoActions().click(self.sw_template_web_elements.get_available_port(port=port_vim))
            AutoActions().click(self.sw_template_web_elements.get_lag_add_port_button())
            sleep(1)
            selected_port = self.sw_template_web_elements.get_selected_port(port=port_vim)
            assert selected_port is None, f"Port {port_vim} was added"

            error_message = self.sw_template_web_elements.get_error_message()
            assert error_message.text in lst_errors, f"No error message was detected"
            AutoActions().click(self.switch_template.sw_template_web_elements.get_cancel_button())

            # 2. aggregate 1 VIM port and 1 fixed panel port from a different stack slot
            AutoActions().click(self.switch_template.sw_template_web_elements.get_aggr_ports_across_stack_button())
            AutoActions().click(self.sw_template_web_elements.get_lacp_toggle_button())

            print(f"Add port {port_vim} to lag group {port_vim}")
            AutoActions().click(self.sw_template_web_elements.get_available_port(port=port_vim))
            AutoActions().click(self.sw_template_web_elements.get_lag_add_port_button())
            sleep(1)
            selected_port = self.sw_template_web_elements.get_selected_port(port=port_vim)
            assert selected_port is not None, f"Port {port_vim} wasn't added"

            AutoActions().click(self.switch_template.sw_template_web_elements.get_available_slot(slot=2))
            port_fixed = "2:1"
            print(f"Add port {port_fixed} to lag group {port_vim}")
            AutoActions().click(self.sw_template_web_elements.get_available_port(port=port_fixed))
            AutoActions().click(self.sw_template_web_elements.get_lag_add_port_button())
            sleep(1)
            selected_port = self.sw_template_web_elements.get_selected_port(port=port_fixed)
            assert selected_port is None, f"Port {port_fixed} was added"
            error_message = self.sw_template_web_elements.get_error_message()
            assert error_message.text in lst_errors, f"No error message was detected"
            AutoActions().click(self.switch_template.sw_template_web_elements.get_cancel_button())
        finally:
            self.navigator.navigate_to_devices()
