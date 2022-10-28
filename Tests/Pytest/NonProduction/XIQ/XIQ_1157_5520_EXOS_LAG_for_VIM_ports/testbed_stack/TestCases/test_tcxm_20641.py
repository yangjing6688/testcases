import time
import pytest
import random

from ..Resources.testcase_base import xiqBase
from extauto.common.AutoActions import AutoActions


class TCXM20641Tests(xiqBase):
    @pytest.mark.development
    @pytest.mark.testbed_stack
    @pytest.mark.xim_tcxm_20641
    @pytest.mark.p2
    def test_tcxm_20641(self, network_policy, template_stack):
        """
        Author        : scostache
        TCXM-20641    : https://aerohive.qtestnet.com/p/101323/portal/project#tab=testdesign&object=1&id=55067659
        Description   : Verify that a fixed panel port cannot be added to and existing LACP for VIM ports
        when LACP was created using Aggregate Ports Across Stack button from Switch Template.
        Preconditions : Use EXOS 5520 stack
        No.   	Step Description
        1	    Onboard the EXOS 5520 stack with only one VIM module.
        2	    Create a Network Policy with specific 5520 template.
        3	    Using the Aggregate Ports Across Stack button from Switch Template -> Port Configuration aggregate
                2 VIM ports.
        4	    Check if an error message appears.
        5	    To existing LACP add a fixed panel port from the same stack slot.
            When editing the created LACP, there is no possibility of adding other ports besides the VIM ports from the same
            VIM module.
        6	    To existing LACP add a fixed panel port from different stack slot.
            When editing the created LACP, there is no possibility of adding other ports besides the VIM ports from the same
            VIM module.
        """
        self.xiq.Utils.print_info("---------TEST_TCXM_20641---------")
        self.executionHelper.testSkipCheck()

        try:
            lst_errors = ["You cannot aggregate Ethernet ports with SFP ports.",
                          "Only VIM ports within the same VIM can be part of the same LAG"]
            self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy, template_stack)

            if self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.\
                    get_sw_template_port_configuration_tab() is None:
                AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_template_link
                                    (template=template_stack))

            time.sleep(2)

            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

            # 1. Aggregate 2 VIM ports.
            self.xiq.Utils.print_info("#1. Create a LAG with 2 VIM ports")
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                get_aggr_ports_across_stack_button())
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                get_lacp_toggle_button())

            self.xiq.Utils.print_info("Get all available ports for the first switch")
            all_ports = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_select_ports_available()
            total_number_of_ports = len(all_ports)
            first_vim_port = "1:" + str(total_number_of_ports-3)
            fixed_panel_port = "1:" + str(random.randint(1, total_number_of_ports-4))
            second_vim_port = "1:" + str(random.randint(total_number_of_ports-2, total_number_of_ports))

            self.xiq.Utils.print_info("Add port ", first_vim_port, " to lag group ", first_vim_port)
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_port
                                (port=first_vim_port))
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                get_lag_add_port_button())
            time.sleep(1)
            selected_port = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.\
                get_selected_port(port=first_vim_port)
            assert selected_port is not None, f"Port {first_vim_port} wasn't added"

            self.xiq.Utils.print_info("Add port ", second_vim_port, " to lag group ", first_vim_port)
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                get_available_port(port=second_vim_port))
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                get_lag_add_port_button())
            time.sleep(1)
            selected_port = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.\
                get_selected_port(port=second_vim_port)
            assert selected_port is not None, f"Port {second_vim_port} wasn't added"

            error_message = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_error_message()
            if error_message is not None:
                assert error_message.text not in lst_errors, f"Error message was detected"
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                get_save_port_type_button())
            self.xiq.Utils.\
                print_info("Successfully created LAG with with 2 VIM ports: ", first_vim_port, " and ", second_vim_port)

            # 2. Try adding Fix Panel Port from same stack
            self.xiq.Utils.print_info("#2. Try adding Fix Panel Port from same stack")
            lag_text = first_vim_port + " LAG"
            elements = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_lag_span(lag=first_vim_port)
            is_lag_found = False
            lag_element = None
            for lag_element in elements:
                if lag_element.text == lag_text:
                    is_lag_found = True
                    AutoActions().click(lag_element)
                    break
            assert is_lag_found is True, f"{lag_text} wasn't found"

            self.xiq.Utils.print_info("Try to add port ", second_vim_port, " to lag group ", first_vim_port)
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.\
                get_available_port(port=fixed_panel_port)
            assert element is None, f"Port {fixed_panel_port} is found and it shouldn't"

            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_cancel_button())
            self.xiq.Utils.print_info("Scenario validated: cannot add fixed panel port in VIM Lag")

            # 3. Try adding Fix Panel Port from second stack
            # Stack2 shouldn't be available when editing existing VIM Lag
            self.xiq.Utils.print_info("#3. Try adding Fix Panel Port from second stack")
            AutoActions().click(lag_element)
            self.xiq.Utils.print_info("Try to find if Stack 2 is available for lag group {first_vim_port}")
            element = self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_available_slot(slot=2)
            assert element is None, f"Slot 2 is found and it shouldn't"
            self.xiq.Utils.print_info("Scenario validated: cannot add ports from different stack in VIM Lag")
            AutoActions().click(self.xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.get_cancel_button())
        finally:
            self.xiq.xflowscommonNavigator.navigate_to_devices()
            self.xiq.Utils.print_info("-------END TEST_TCXM_20641-------")
