import re
import time
import pytest

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from extauto.common.AutoActions import AutoActions
from extauto.common.Utils import Utils


class SuiteUdk:

    def __init__(self, setup_cls_obj):
        self.defaultLibrary = DefaultLibrary()
        self.setup_cls_obj = setup_cls_obj
        self.utils = Utils()

    def get_stack_slots_with_vim(self, slots_vim_dict):
        """
        Used for retrieving slots with vim modules:
        vim_slots = ["slot1", "slot2", ...]
        """
        vim_slots = []
        for slot_key in slots_vim_dict.keys():
            vim = slots_vim_dict[slot_key]
            if vim and 'vim_model' in vim:
                if vim['vim_model'] is not None:
                    vim_slots.append(slot_key)
        return vim_slots

    def devices_update_config(self, dut):
        """
        This keyword is used to do a config push for a switch ${dut}.
        """
        xiq = self.setup_cls_obj.xiq
        try:
            xiq.xflowscommonNavigator.navigate_to_devices()
            retry = 0
            while retry < 30:
                time.sleep(2)
                res = xiq.xflowscommonDevices.get_device_status(dut.mac)
                if res == 'config audit mismatch':
                    break
                retry += 1

            if retry >= 30:
                self.utils.print_info('Error: Audit icon not yellowed: {}')
                return -1

            if xiq.xflowscommonDevices.update_switch_policy_and_configuration(dut.mac) == -1:
                self.utils.print_info("Error: Failed to update switch")
                return -1
            xiq.xflowscommonDevices.refresh_devices_page()
            time.sleep(2)
            res = xiq.xflowscommonDevices.get_device_status(dut.mac)
            if res != 'green':
                self.utils.print_info('Error: Status not equal to Green: {}')
                return -1
        except Exception as e:
            self.utils.print_info(e)
            return -1
        return 1

    """Switch template"""
    def navigate_to_sw_template(self, network_policy, template_stack, slot_vim):
        """
        This keyword is navigate to ${network_policy} and ${template_stack} and select the ${slot_vim}.
        """
        try:
            self.setup_cls_obj.switch_template.select_sw_template(network_policy, template_stack)
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_template_link(template=template_stack))

            time.sleep(2)
            self.setup_cls_obj.switch_template.go_to_port_configuration()
            template_slot = self.setup_cls_obj.switch_template.sw_template_web_elements.get_template_slot(slot=slot_vim)
            AutoActions().click(template_slot)
            time.sleep(5)
        except Exception as e:
            print(f"Error Exception: {e}")
            return -1
        return 1

    def aggregate_vim_ports_tmpl(self, main_lag_port, port):
        """
                This keyword is aggregate  ${main_lag_port} and another ${port}.
                """
        try:
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_available_port(port=main_lag_port))
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lag_add_port_button())
            time.sleep(2)
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_available_port(port=port))
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lag_add_port_button())
            time.sleep(2)
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_save_port_type_button())
            time.sleep(5)
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_switch_temp_save_button())
            time.sleep(1)
        except Exception as e:
            print(f"Error Exception: {e}")
            return -1
        return 1

    def verify_lag_is_created_and_add_new_port(self, main_lag_port, port):
        """
        This keyword is used to verify in Switch Template that LAG is created and add a new port
        :param main_lag_port: Master port
        :param port: other vim port
        """
        main_lag_port_string = str(main_lag_port)
        lag_text = main_lag_port_string + " LAG"
        labels = self.setup_cls_obj.sw_template_web_elements.get_lag_span(lag=main_lag_port_string)
        is_lag_found = False
        for i in labels:
            if i.text == lag_text:
                is_lag_found = True
                AutoActions().click(i)
                break
        assert is_lag_found is True, f"{lag_text} wasn't found"
        time.sleep(20)

        print(f"Add port {port} to lag group {main_lag_port_string}")
        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_available_port(port=port))
        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lag_add_port_button())
        time.sleep(1)
        selected_port = self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=port)
        assert selected_port is not None, f"Port {port} wasn't added"
        time.sleep(5)
        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_save_port_type_button())
        time.sleep(5)
        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_switch_temp_save_button())
        time.sleep(1)

    def remove_lag(self, main_lag_port, ports):
        """
        This keyword is used to remove ports from LAG
        :param main_lag_port: Master port
        :param ports: other vim ports
        """
        lag_text = main_lag_port + " LAG"
        labels = self.setup_cls_obj.sw_template_web_elements.get_lag_span(lag=main_lag_port)

        is_lag_found = False
        for i in labels:
            if i.text == lag_text:
                is_lag_found = True
                AutoActions().click(i)
                break
        assert is_lag_found is True, f"{lag_text} wasn't found"
        time.sleep(10)
        for port in ports:
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=port))
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lag_remove_port_button())

        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_save_port_type_button())
        time.sleep(5)
        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_switch_temp_save_button())
        time.sleep(1)

    def aggregate_vim_ports(self, nw_policy, sw_template):
        """
            This keyword is used to aggregate the last two ports (VIM ports) of the first device in the stack
            It navigates to Network Policies->[Given Policy]->[Given Switch Template]->Port Configuration Tab

            :param nw_policy: the name of the Network Policy
            :param sw_template: the name of the Switch Template
        """

        self.setup_cls_obj.switch_template.select_sw_template(nw_policy=nw_policy, sw_template=sw_template)
        time.sleep(2)

        if self.setup_cls_obj.sw_template_web_elements.get_sw_template_port_configuration_tab() is None:
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_template_link(template=sw_template))

        time.sleep(2)

        self.setup_cls_obj.switch_template.go_to_port_configuration()
        time.sleep(2)

        AutoActions().click(self.setup_cls_obj.switch_template.sw_template_web_elements.get_aggr_ports_across_stack_button())
        time.sleep(2)

        print("Get all available ports")
        all_ports = self.setup_cls_obj.switch_template.sw_template_web_elements.get_select_ports_available()
        total_number_of_ports = len(all_ports)

        ports = [all_ports[total_number_of_ports - 2].text, all_ports[total_number_of_ports - 1].text]
        AutoActions().click(self.setup_cls_obj.switch_template.sw_template_web_elements.get_cancel_button())
        time.sleep(1)

        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_aggr_ports_across_stack_button())
        time.sleep(1)

        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lacp_toggle_button())
        time.sleep(1)

        for port in ports:
            print(f"Add port {port} to lag")
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_available_port(port=port))
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lag_add_port_button())
            time.sleep(1)
            selected_port = self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=port)
            assert selected_port is not None, f"Port {port} wasn't added"

        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_save_port_type_button())
        time.sleep(2)

        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_sw_template_scli_save_btn())
        time.sleep(4)

        return ports

    def remove_vim_ports_from_lag(self, nw_policy, sw_template):
        """
            This keyword is used to remove the last two ports (VIM ports) of the first device in the stack from an existing LAG
            It navigates to Network Policies->[Given Policy]->[Given Switch Template]->Port Configuration Tab

            :param nw_policy: the name of the Network Policy
            :param sw_template: the name of the Switch Template
        """

        self.setup_cls_obj.switch_template.select_sw_template(nw_policy=nw_policy, sw_template=sw_template)
        time.sleep(2)

        if self.setup_cls_obj.sw_template_web_elements.get_sw_template_port_configuration_tab() is None:
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_template_link(template=sw_template))

        time.sleep(2)

        self.setup_cls_obj.switch_template.go_to_port_configuration()
        time.sleep(2)

        AutoActions().click(self.setup_cls_obj.switch_template.sw_template_web_elements.get_aggr_ports_across_stack_button())
        time.sleep(2)

        print("Get all available ports")
        all_ports = self.setup_cls_obj.switch_template.sw_template_web_elements.get_select_ports_available()
        total_number_of_ports = len(all_ports)

        ports = [all_ports[total_number_of_ports - 2].text, all_ports[total_number_of_ports - 1].text]

        lag_text = str(ports[0]) + " LAG"
        print(f"Remove all ports from {lag_text}")
        labels = self.setup_cls_obj.sw_template_web_elements.get_lag_span(lag=ports[0])
        for i in labels:
            if i.text == lag_text:
                self.setup_cls_obj.auto_actions.click(i)
                break

        time.sleep(5)
        ports.reverse()
        for port in ports:
            print(f"Remove port {port} from lag")
            if port == ports[0]:
                AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=port))
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lag_remove_port_button())
            selected_port = self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=port)
            assert selected_port is None, f"Port {port} wasn't removed"

        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_save_port_type_button())
        time.sleep(2)

        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_sw_template_scli_save_btn())
        time.sleep(4)
        return

    """CLI"""
    def check_lag_cli(self, dut, master_vim_port, last_vim_port):
        """
        Used for checking lacp on the switch matches the reference list:
        lacp_list_ports = ["port1-port2", "port3-port4", ...]
        """
        try:
            self.setup_cls_obj.network_manager.connect_to_network_element_name(dut)
            output = self.setup_cls_obj.devCmd.send_cmd(dut, 'show configuration | i sharing', max_wait=10, interval=2)
            result = output[0].return_text
        finally:
            self.setup_cls_obj.network_manager.close_connection_to_network_element(dut)

        expected_result = f'enable sharing {master_vim_port} grouping {last_vim_port}-{master_vim_port.split(":")[1]}'
        if expected_result not in result:
            pytest.fail(f"Expected result: {expected_result}, actual result: {result}")

    def check_lacp_dut_cli(self, lacp_ports_d360):
        """
        Used for checking lacp on the switch matches the reference expected result:
        """
        dut = self.setup_cls_obj.tb.dut1

        self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

        for attempts in range(3):
            time.sleep(10)
            output = self.setup_cls_obj.devCmd.send_cmd(dut.name, 'show configuration | i sharing',
                                              max_wait=10, interval=2)

            p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
            lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
            print(f"Lacp ports from dut are: {lacp_list_ports_from_dut}")
            return lacp_list_ports_from_dut == lacp_ports_d360

    def check_lacp_dut(self, lacp_list_ports):
        """
        Used for checking lacp on the switch matches the reference list:
        lacp_list_ports = ["port1, "port2", "port3", "port4", ...]
        """
        dut = self.setup_cls_obj.tb.dut1
        if dut.cli_type.upper() != "EXOS":
            return False
        try:
            for attempts in range(3):
                time.sleep(10)
                output = self.setup_cls_obj.devCmd.send_cmd(dut.name, 'show configuration | i sharing',
                                              max_wait=10, interval=2)

                p = re.compile(r'\d:\d+-\d:\d+|\d:\d+,\d:\d+|\d:\d+-\d+', re.M)
                lacp_list_ports_from_dut = re.findall(p, output[0].return_text)

                for i in range(0, len(lacp_list_ports), 2):
                    if lacp_list_ports[i] + '-' + lacp_list_ports[i+1] in lacp_list_ports_from_dut:
                        lacp_list_ports_from_dut.remove(lacp_list_ports[i] + '-' + lacp_list_ports[i+1])
                    elif lacp_list_ports[i] + '-' + lacp_list_ports[i+1].split(":")[1] in lacp_list_ports_from_dut:
                        lacp_list_ports_from_dut.remove(lacp_list_ports[i] + '-' + lacp_list_ports[i+1].split(":")[1])
                    elif lacp_list_ports[i] + ',' + lacp_list_ports[i+1] in lacp_list_ports_from_dut:
                        lacp_list_ports_from_dut.remove(lacp_list_ports[i] + ',' + lacp_list_ports[i+1])
                    else:
                        return False

                if len(lacp_list_ports_from_dut) == 0:
                    return True
            return False
        except Exception as e:
            pytest.fail(e)
            return False

    """Device360"""
    def device360_aggregate_ports(self, ports):
        """
           This keyword is used to aggregate a list of ports
           It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation

           :param ports: list of ports: ex: ["1", "2", "3"]
           :return: True if successful or False on failure
           """
        try:
            for port_name in ports:
                click_checkbox_or_button = self.setup_cls_obj.xiq.xflowsmanageDevice360. \
                    get_device360_port_settings_and_aggregation_interface_exos_standalone(port_name.split(":")[1])
                if click_checkbox_or_button:
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking on port checkbox")
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(click_checkbox_or_button)
                else:
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Checkbox not found")
                    return False

            aggregate_btn = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_configure_port_aggregate_button()
            if aggregate_btn:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking 'Aggregate Selected Ports' button'")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(aggregate_btn)
                time.sleep(5)
            else:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("'Aggregate Selected Ports' button' not found")
                return False
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_toggle())
            time.sleep(5)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_save_button())
            time.sleep(10)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_save_port_config())
            time.sleep(10)
        except Exception as e:
            print(f"Error Exception: {e}")
            return -1
        return 1

    def device360_remove_lag(self, master_port):
        """
        This keyword is used to remove all LAG ports from Device360
        It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation

        :param master_port
        """
        try:
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=master_port))
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_selected_port(port=master_port))
            for i in range(0, 4):
                AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_remove_button())
                time.sleep(2)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_save_button())
            time.sleep(10)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_save_port_config())
            time.sleep(10)
        except Exception as e:
            print(f"Error Exception: {e}")
            return -1
        return 1

    def device360_remove_partial_lag(self, master_port):
        """
        This keyword is used to remove 2 LAG ports from Device360
        It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation

        :param master_port
        """
        try:
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=master_port))
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_selected_port(port=master_port))
            for i in range(0, 2):
                AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_remove_button())
                time.sleep(2)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_save_button())
            time.sleep(10)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_save_port_config())
            time.sleep(10)
        except Exception as e:
            print(f"Error Exception: {e}")
            return -1
        return 1

    def device360_change_slot_view(self, unit):
        """
           This keyword is used to switch between slot port config pages
           It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation

           :param unit: string with slot number
           :return: True if successful or False on failure
           """
        # Get slots dropdown
        slots_dropdown = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_port_config_stack_slots_dropdown()
        if slots_dropdown:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking on slots dropdown")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(slots_dropdown)
            time.sleep(5)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Slots dropdown not found")
            return False

        # Get next slot
        next_slot = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_slot_from_dropdown(unit=unit)
        if next_slot:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking on next slot")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(next_slot)
            time.sleep(5)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Next slot not found in dropdown list")
            return False
        return True

    def navigate_d360_port_settings_and_aggregation(self):
        """
        This keyword is used to navigate to Port Settings and Aggregation
        """
        self.setup_cls_obj.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
        AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_refresh_page_button())
        time.sleep(20)

        button_settings = self.setup_cls_obj.xiq.xflowsmanageDevice360.dev360. \
            get_d360_configure_port_settings_aggregation_tab_button()
        assert button_settings, "Could not find port settings & aggregation button"
        self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(button_settings)
        time.sleep(5)
        return True

    def device360_add_lag_port(self, master_port, port):
        """
        This keyword is used to add a LAG port to an existing LAG
        :param master_port
        :param port
        """
        try:
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=master_port))
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_available_port(port=port))
            time.sleep(1)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_add_button())
            time.sleep(5)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_save_button())
            time.sleep(10)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_save_port_config())
            time.sleep(10)
        except Exception as e:
            print(f"Error Exception: {e}")
            return -1
        return 1

    def device360_aggregate_two_ports_from_different_slots(self, slots_no):
        """
            Keyword used to find two (non vim) ports from different slots to aggregate

            :return: On success: return list of ports ['1:2', '2:3'], on Error return False, on failure return 1
            """
        # Iterate through all the slots

        # contains_port_type = [[port_eth ,port_fiber], ....]
        list_ethernet_ports = []
        list_sfp_ports = []
        for i in range(1, slots_no+1):
            if not self.device360_change_slot_view(i):
                return False

            # Get ethernet ports:
            ethernet_ports = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_get_ports_by_type_slot("ethernet-port", i)
            if ethernet_ports:
                list_ethernet_ports.append(ethernet_ports[0].get_attribute("data-automation-tag").split('-')[2])
            sfp_ports = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_get_ports_by_type_slot("sfp-port", i)
            if sfp_ports:
                list_sfp_ports.append(sfp_ports[0].get_attribute("data-automation-tag").split('-')[2])

        # Try to aggregate two ethernet ports
        for i in range(2, len(list_ethernet_ports)):
            aggregate_rc = self.device360_aggregate_stack_ports_slots([list_ethernet_ports[i-1],
                                                                       list_ethernet_ports[i]],
                                                                      True)
            if aggregate_rc is False:
                return False
            if aggregate_rc is True:
                return [list_ethernet_ports[i-1], list_ethernet_ports[i]]

        # Try to aggregate two sfp ports
        for i in range(2, len(list_sfp_ports)):
            aggregate_rc = self.device360_aggregate_stack_ports_slots([list_sfp_ports[i-1],
                                                                       list_sfp_ports[i]],
                                                                      True)
            if aggregate_rc is False:
                return False
            if aggregate_rc is True:
                return [list_sfp_ports[i-1], list_sfp_ports[i]]

        self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("[WARNING]: Could not find two"
                                                        " ports from different slots to aggregate")
        return 1

    def device360_get_number_of_slots(self):
        """
            Keyword used to get the number of onboarded stack slots from Device360

            :return: On success: number of slots, on Failure False
            """
        slots_rows = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_stack_overview_slot_ports_row()
        if slots_rows:
            return len(slots_rows)
        else:
            return False

    def device360_get_vims(self, slots_no):
        """
            Keyword used to get all the vim ports

            :return: On success: list of all vim ports ex: [1:59, 1:60,..], on Failure False
            """
        ret_vim_ports = []
        for i in range(1, slots_no+1):
            vim_ports = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_stack_slot_vim_ports(i)
            if not vim_ports:
                continue
            for vim_port in vim_ports:
                tag = vim_port.get_attribute("data-automation-tag")
                ret_vim_ports.append(tag.split('-')[2])

        if len(ret_vim_ports) == 0:
            return False

        return ret_vim_ports

    def device360_check_aggregated_ports_number(self, reference_num):
        """
           This keyword is used to check the number of aggregated ports matches the reference
           It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation

           :param reference_num: reference integer
           :return: If match True, else False
           """
        i = 1
        no_of_ports = 0
        while self.device360_change_slot_view(str(i)):
            i = i + 1
            lag_rows = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_configure_aggregated_port_settings_aggregation_rows()
            if lag_rows:
                no_of_ports = no_of_ports + len(lag_rows)

        # Close slots dropdown
        slots_dropdown = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_port_config_stack_slots_dropdown()
        if slots_dropdown:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking on slots dropdown")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(slots_dropdown)
            time.sleep(5)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Slots dropdown not found")
            return False
        return no_of_ports == reference_num

    def device360_update_device(self):
        """
            Performs the update operation from Device360
           It Assumes That Already Navigated to Device360

           :return: True if successful or False on failure
           """
        button_update = self.setup_cls_obj.xiq.xflowsmanageDevice360.dev360.get_device360_device_configuration_update_button()
        if button_update:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking Update device button")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(button_update)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Update device button not found")
            return False

        button_perform_update = self.setup_cls_obj.xiq.xflowsmanageDevice360.dev360.get_device360_perform_update_button()
        if button_perform_update:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking Perform update button")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(button_perform_update)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Perform update button not found")
            return False
        return True

    def device360_aggregate_stack_ports_slots(self, ports, click_lacp):
        """
           This keyword is used to aggregate ports from same/different stack slots
           It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation

           :param click_lacp:  boolean value if needed to click the lacp toggle
           :param ports: port list
           :return: True if successful, False if failed, 1 if couldn't aggregate from other slot
           """

        if not self.device360_change_slot_view(ports[0].split(":")[0]):
            return False

        click_checkbox_or_button = self.setup_cls_obj.xiq.xflowsmanageDevice360. \
            get_device360_port_settings_and_aggregation_interface_exos_standalone(ports[0].split(":")[1])
        if click_checkbox_or_button:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking on port checkbox")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(click_checkbox_or_button)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Checkbox not found")
            return False

        # Aggregate
        aggregate_btn = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_configure_port_aggregate_button()
        if aggregate_btn:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking 'Aggregate Selected Ports' button")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(aggregate_btn)
            time.sleep(5)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("'Aggregate Selected Ports' button not found")
            return False

        # Get cancel button reference
        cancel_button = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_cancel_button()
        if not cancel_button:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Could not find cancel button")
            return False

        # Add other ports to aggregation
        for i in range(1, len(ports)):
            switched_slot = False
            if ports[i - 1].split(":")[0] != ports[i].split(":")[0]:
                # Switching to other slot
                other_slot = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_choose_slot(ports[i].split(":")[0])
                if other_slot:
                    switched_slot = True
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Changing to other slot")
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(other_slot)
                else:
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Failed to change to other slot")
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Exiting LACP Window")
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(cancel_button)
                    return False
            # Choose the next port
            available_port = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_available_port(ports[i])
            if available_port:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Choosing second available port")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(available_port)
            else:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Failed to choose second available port")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Exiting LACP Window")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(cancel_button)
                if switched_slot:
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Deselecting first port")
                    self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(click_checkbox_or_button)
                    return 1
                else:
                    return False

            # Add next port
            add_port_to_lacp = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_add_button()
            if add_port_to_lacp:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking on add port")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(add_port_to_lacp)
            else:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Add port not found")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Exiting LACP Window")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(cancel_button)
                return False

        # Toggle lacp on window
        if click_lacp:
            lacp_switch = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_toggle()
            if lacp_switch:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking LACP toggle")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(lacp_switch)
            else:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("LACP toggle not found")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Exiting LACP Window")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(cancel_button)
                return False

        # Save
        lag_save_button = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_save_button()
        if lag_save_button:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking Save button")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(lag_save_button)
            time.sleep(10)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Save button not found")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Exiting LACP Window")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(cancel_button)
            return False

        # Save port Config
        save_port_config = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_save_port_config()
        if save_port_config:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking Save port config button")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(save_port_config)
            time.sleep(5)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Save port config button not found")
            return False

        # Check lacp formed in Device360
        if self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports[0]):
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("LACP NOT FORMED")
            return True

        return False

    def device360_remove_stack_ports_slots(self, ports):
        """
           This keyword is used to remove port aggregation
           It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation

           :param ports: list of ports: ex: ["1:1", "2:1", "3:2"]
           :return: True if successful or False on failure
           """
        if not self.device360_change_slot_view(ports[0].split(":")[0]):
            return False

        aggregated_ports = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports[0])
        if aggregated_ports:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking on aggregated ports label")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(aggregated_ports)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Failed to find aggregated port")
            return False

        # Get cancel button reference
        cancel_button = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_cancel_button()
        if not cancel_button:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Could not find cancel button")
            return False

        selected_port = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_selected_port(ports[0])
        if selected_port:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Choosing second selected port")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(selected_port)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Failed to choose second selected port")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Exiting lacp window")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(cancel_button)
            return False

        # Remove ports from aggregation
        for i in range(len(ports)):
            # Remove the next port
            remove_port_from_lacp = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_remove_button()
            if remove_port_from_lacp:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking on remove port")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(remove_port_from_lacp)
            else:
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Remove port not found")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Exiting lacp window")
                self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(cancel_button)
                return False

        # Save
        lag_save_button = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_save_button()
        if lag_save_button:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking Save button")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(lag_save_button)
            time.sleep(5)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Save button not found")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Exiting lacp window")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(cancel_button)
            return False

        # Save port Config
        save_port_config = self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_save_port_config()
        if save_port_config:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Clicking Save port config button")
            self.setup_cls_obj.xiq.xflowsmanageDevice360.auto_actions.click(save_port_config)
            time.sleep(5)
        else:
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Save port config button not found")
            return False

        # Check lacp formed in Device360
        if self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports[0]):
            self.setup_cls_obj.xiq.xflowsmanageDevice360.utils.print_info("Aggregation remove failed")
            return False
        return True

    def close_connection_with_error_handling(self, dut):
        try:
            self.setup_cls_obj.network_manager.device_collection.remove_device(dut.name)
            self.setup_cls_obj.network_manager.close_connection_to_network_element(dut.name)
        except Exception as exc:
            print(exc)
        else:
            time.sleep(30)
