import re
from time import sleep

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from extauto.common.AutoActions import AutoActions
from extauto.common.Utils import Utils


def find_between(s, first, last):
    return re.findall(rf'{first}(.*?){last}', s)


class SuiteUdk:

    def __init__(self, setup_cls_obj):
        self.defaultLibrary = DefaultLibrary()
        self.setup_cls_obj = setup_cls_obj
        self.utils = Utils()

    def go_to_switch_template(self, template_name):
        """
            This keyword is used to navigate to a Switch Template -> Port Configuration tab based on ${template_name}.
        """
        xiq = self.setup_cls_obj.xiq
        if xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements. \
                get_sw_template_port_configuration_tab() is None:
            AutoActions().click(xiq.xflowsconfigureSwitchTemplate.sw_template_web_elements.
                                get_template_link(template=template_name))

        self.setup_cls_obj.switch_template.go_to_port_configuration()
        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_port_settings_tab())
        sleep(3)

    def devices_update_config(self, dut):
        """
            This keyword is used to do a config push for a switch ${dut}. 
        """
        xiq = self.setup_cls_obj.xiq
        try:
            xiq.xflowscommonNavigator.navigate_to_devices()
            retry = 0
            while retry < 30:
                sleep(2)
                res = xiq.xflowscommonDevices.get_device_status(dut.serial)
                if res == 'config audit mismatch':
                    break
                retry += 1

            if retry >= 30:
                self.utils.print_info('Error: Audit icon not yellowed: {}')
                return -1

            if xiq.xflowscommonDevices.update_switch_policy_and_configuration(dut.serial) == -1:
                self.utils.print_info("Error: Failed to update switch")
                return -1
            xiq.xflowscommonDevices.refresh_devices_page()
            sleep(2)
            res = xiq.xflowscommonDevices.get_device_status(dut.serial)
            if res != 'green':
                self.utils.print_info('Error: Status not equal to Green: {}')
                return -1
        except Exception as e:
            self.utils.print_info(e)
            return -1
        return 1

    def save_configuration(self):
        """
            This keyword is used to save the existing template configuration.
        """
        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_save_port_type_button())
        sleep(2)
        AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_switch_temp_save_button_v2())
        sleep(1)

    def save_and_upload(self, dut):
        """
            This keyword is used to save the existing template configuration and to do a config push for 
            a switch ${dut}.
        """
        try:
            self.save_configuration()
            return self.devices_update_config(dut)
        except Exception as e:
            print(e)
            return -1

    def remove_lag_ports(self, network_policy, template_stack, main_lag_port, no_of_ports):
        self.setup_cls_obj.switch_template.select_sw_template(network_policy, template_stack)
        self.setup_cls_obj.switch_template.go_to_port_configuration()
        sleep(3)
        lag_text = str(main_lag_port) + " LAG"
        labels = self.setup_cls_obj.sw_template_web_elements.get_lag_span(lag=main_lag_port)
        if labels is None:
            self.utils.print_info('Warning: main lag port not found, nothing to remove')
            return
        is_lag_found = False
        for i in labels:
            if i.text == lag_text:
                is_lag_found = True
                AutoActions().click(i)
                break
        if is_lag_found:
            selected_port = self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=main_lag_port)
            if selected_port:
                AutoActions().click(selected_port)
                sleep(1)
                for i in range(0, no_of_ports):
                    AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lag_remove_port_button())
                    sleep(1)

    def add_ports_to_lag(self, dut, main_lag_port, ports, is_lag_created):
        """
            This keyword is used for:
             - creating a lag based on a ${main_lag_port} (ex: 57) and the ${ports} (ex: [57, 58]) if 
               ${is_lag_created} = False
             - adding ${ports} (ex: [58, 60]) to an existing lag defined by a ${main_lag_port} (ex: 57) if 
               ${is_lag_created} = True
        """
        main_lag_port_string = str(main_lag_port)
        if is_lag_created is False:
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_aggr_ports_standalone_button())
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lacp_toggle_button())
        else:
            lag_text = main_lag_port_string + " LAG"
            labels = self.setup_cls_obj.sw_template_web_elements.get_lag_span(lag=main_lag_port_string)
            is_lag_found = False
            for i in labels:
                if i.text == lag_text:
                    is_lag_found = True
                    AutoActions().click(i)
                    break
            assert is_lag_found is True, f"{lag_text} wasn't found"
        sleep(2)

        for port in ports:
            print(f"Add port {port} to lag group {main_lag_port_string}")
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_available_port(port=port))
            AutoActions().click(self.setup_cls_obj.sw_template_web_elements.get_lag_add_port_button())
            sleep(1)
            selected_port = self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=port)
            assert selected_port is not None, f"Port {port} wasn't added"

        self.save_and_upload(dut)

        print("Verify in CLI")
        lacp_config = self.get_lacp_configuration_from_device(dut)
        assert main_lag_port_string in lacp_config, f"Device doesn't have a lag group {main_lag_port}"
        lacp_ports = lacp_config.get(main_lag_port_string)
        if lacp_ports is not None:
            for vim in ports:
                assert vim in lacp_ports, f"Port {vim} is not in lag group {main_lag_port}"

    def aggregate_vim_ports(self, nw_policy, sw_template):
        """
            This keyword is used to aggregate the last two ports (VIM ports) of the device
            It navigates to Network Policies->[Given Policy]->[Given Switch Template]->Port Configuration Tab

            :param nw_policy: the name of the Network Policy
            :param sw_template: the name of the Switch Template
        """

        self.setup_cls_obj.switch_template.select_sw_template(nw_policy=nw_policy, sw_template=sw_template)
        sleep(2)
        self.setup_cls_obj.switch_template.go_to_port_configuration()
        sleep(2)
        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.switch_template.sw_template_web_elements.
                                              get_aggr_ports_standalone_button())
        sleep(2)

        print("Get all available ports")
        all_ports = self.setup_cls_obj.switch_template.sw_template_web_elements.get_select_ports_available()
        total_number_of_ports = len(all_ports)

        ports = [int(all_ports[total_number_of_ports - 2].text), int(all_ports[total_number_of_ports - 1].text)]
        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.switch_template.sw_template_web_elements.
                                              get_cancel_button())
        sleep(1)

        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.
                                              get_aggr_ports_standalone_button())
        sleep(1)

        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.get_lacp_toggle_button())
        sleep(1)

        for port in ports:
            print(f"Add port {port} to lag")
            self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.
                                                  get_available_port(port=port))
            self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.get_lag_add_port_button())
            sleep(1)
            selected_port = self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=port)
            assert selected_port is not None, f"Port {port} wasn't added"

        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.get_save_port_type_button())
        sleep(2)

        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.
                                              get_switch_temp_save_button_v2())
        sleep(2)

        return ports

    def remove_vim_ports_from_lag(self, nw_policy, sw_template):
        """
            This keyword is used to remove the last two ports (VIM ports) of the device from an existing LAG
            It navigates to Network Policies->[Given Policy]->[Given Switch Template]->Port Configuration Tab

            :param nw_policy: the name of the Network Policy
            :param sw_template: the name of the Switch Template
        """

        self.setup_cls_obj.switch_template.select_sw_template(nw_policy=nw_policy, sw_template=sw_template)
        sleep(2)
        self.setup_cls_obj.switch_template.go_to_port_configuration()
        sleep(2)
        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.switch_template.sw_template_web_elements.
                                              get_aggr_ports_standalone_button())
        sleep(2)

        print("Get all available ports")
        all_ports = self.setup_cls_obj.switch_template.sw_template_web_elements.get_select_ports_available()
        total_number_of_ports = len(all_ports)

        ports = [int(all_ports[total_number_of_ports - 2].text), int(all_ports[total_number_of_ports - 1].text)]

        lag_text = str(ports[0]) + " LAG"
        print(f"Remove all ports from {lag_text}")
        labels = self.setup_cls_obj.sw_template_web_elements.get_lag_span(lag=ports[0])
        for i in labels:
            if i.text == lag_text:
                self.setup_cls_obj.auto_actions.click(i)
                break

        sleep(5)
        ports.reverse()
        for port in ports:
            print(f"Remove port {port} from lag")
            if port == ports[0]:
                self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.
                                                      get_selected_port(port=port))
            self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.
                                                  get_lag_remove_port_button())
            selected_port = self.setup_cls_obj.sw_template_web_elements.get_selected_port(port=port)
            assert selected_port is None, f"Port {port} wasn't removed"

        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.get_save_port_type_button())
        sleep(2)

        self.setup_cls_obj.auto_actions.click(self.setup_cls_obj.sw_template_web_elements.
                                              get_switch_temp_save_button_v2())
        sleep(2)

        return

    def get_lacp_configuration_from_device(self, dut):
        """
            This Keyword is used to return the lacp configuration from a switch ${dut}.
        """
        self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)
        result = self.setup_cls_obj.devCmd.send_cmd(dut.name, 'show configuration | i sharing', max_wait=10, interval=2)
        res = ""
        if result:
            result_text = result[0].return_text
            main_lag_ports = find_between(result_text, "sharing ", " grouping")
            ports = find_between(result_text, "grouping ", " algorithm")
            if ports:
                for i in range(len(ports)):
                    p = ports[i].split(',')
                    ports_list = []
                    for p1 in p:
                        if '-' in p1:
                            ports_range = p1.split('-')
                            for j in range(int(ports_range[0]), int(ports_range[1]) + 1):
                                ports_list.append(j)
                        else:
                            ports_list.append(int(p1))
                    ports[i] = ports_list
                    print(ports_list)
            res = dict(zip(main_lag_ports, ports))
            self.close_connection_with_error_handling(dut)
        return res

    def check_lacp_dut(self, dut, lacp_list_ports):
        """
        Used for checking lacp on the switch matches the reference list:
        lacp_list_ports = ["port1-port2", "port3-port4", ...]
        """
        if dut.cli_type.upper() != "EXOS":
            return False

        self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

        output = self.setup_cls_obj.devCmd.send_cmd(dut.name, 'show configuration | i sharing',
                                                    max_wait=10, interval=2)

        p = re.compile(r' \d+-\d+ ', re.M)
        lacp_list_ports_from_dut = re.findall(p, output[0].return_text)
        lacp_list_ports_from_dut_stripped = [s.strip() for s in lacp_list_ports_from_dut]
        self.close_connection_with_error_handling(dut)

        if len(lacp_list_ports_from_dut_stripped) != len(lacp_list_ports):
            return False
        return sorted(lacp_list_ports_from_dut_stripped) == sorted(lacp_list_ports)

    def cleanup_lacp_on_dut(self, dut, main_lag_port):
        """
            This keyword is used to delete the lacp configuration defined by ${main_lag_port} from a switch ${dut}. 
        """
        self.close_connection_with_error_handling(dut)
        self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)
        self.setup_cls_obj.devCmd.send_cmd(dut.name, f'disable sharing {main_lag_port}', max_wait=10, interval=2)

    def close_connection_with_error_handling(self, dut):
        try:
            self.setup_cls_obj.network_manager.device_collection.remove_device(dut.name)
            self.setup_cls_obj.network_manager.close_connection_to_network_element(dut.name)
        except Exception as exc:
            print(exc)
        else:
            sleep(2)

    """Device 360"""
    def device360_check_aggregated_ports_number(self, reference_num):
        """
           This keyword is used to check the number of aggregated ports matches the reference
           It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation
           :param reference_num: reference integer
           :return: If match True, else False
           """
        xiq = self.setup_cls_obj.xiq
        lag_rows = xiq.xflowsmanageDevice360.get_device360_configure_aggregated_port_settings_aggregation_rows()
        if lag_rows:
            return len(lag_rows) == reference_num
        else:
            return reference_num == 0

    def device360_aggregate_ports(self, ports, click_lacp):
        """
           This keyword is used to aggregate a list of ports
           It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation
           :param ports: list of ports: ex: ["1", "2", "3"]
           :param click_lacp:  boolean value if needed to click the lacp toggle
           :return: True if successful or False on failure
           """
        xiq = self.setup_cls_obj.xiq
        for port_name in ports:
            click_checkbox_or_button = xiq.xflowsmanageDevice360. \
                get_device360_port_settings_and_aggregation_interface_exos_standalone(port_name)
            if click_checkbox_or_button:
                xiq.xflowsmanageDevice360.utils.print_info("Clicking on port checkbox")
                xiq.xflowsmanageDevice360.auto_actions.click(click_checkbox_or_button)
            else:
                xiq.xflowsmanageDevice360.utils.print_info("Checkbox not found")
                return False

        # Aggregate
        aggregate_btn = xiq.xflowsmanageDevice360.get_device360_configure_port_aggregate_button()
        if aggregate_btn:
            xiq.xflowsmanageDevice360.utils.print_info("Clicking 'Aggregate Selected Ports' button'")
            xiq.xflowsmanageDevice360.auto_actions.click(aggregate_btn)
            sleep(5)
        else:
            xiq.xflowsmanageDevice360.utils.print_info("'Aggregate Selected Ports' button' not found")
            return False

        # Toggle lacp on window
        if click_lacp:
            lacp_switch = xiq.xflowsmanageDevice360.get_device360_lacp_toggle()
            if lacp_switch:
                xiq.xflowsmanageDevice360.utils.print_info("Clicking LACP toggle")
                xiq.xflowsmanageDevice360.auto_actions.click(lacp_switch)
            else:
                xiq.xflowsmanageDevice360.utils.print_info("LACP toggle not found")
                return False

        # Save
        lag_save_button = xiq.xflowsmanageDevice360.get_device360_lag_save_button()
        if lag_save_button:
            xiq.xflowsmanageDevice360.utils.print_info("Clicking Save button")
            xiq.xflowsmanageDevice360.auto_actions.click(lag_save_button)
            sleep(5)
        else:
            xiq.xflowsmanageDevice360.utils.print_info("Save button not found")
            return False

        # Save port Config
        save_port_config = xiq.xflowsmanageDevice360.get_device360_save_port_config()
        if save_port_config:
            xiq.xflowsmanageDevice360.utils.print_info("Clicking Save port config button")
            xiq.xflowsmanageDevice360.auto_actions.click(save_port_config)
            sleep(5)
        else:
            xiq.xflowsmanageDevice360.utils.print_info("Save port config button not found")
            return False

        # Check lacp formed in Device360
        if xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports[0]):
            return True

        return False

    def device360_remove_port_aggregation(self, ports, click_lacp):
        """
           This keyword is used to remove port aggregation
           It Assumes That Already Navigated to Device360->Port Configuration->Port Settings & Aggregation
           :param ports: list of ports: ex: ["1", "2", "3"]
           :param click_lacp:  boolean value if needed to click the lacp toggle
           :return: True if successful or False on failure
           """
        xiq = self.setup_cls_obj.xiq
        port_label = xiq.xflowsmanageDevice360.get_device360_lacp_label(ports[0])
        if port_label:
            xiq.xflowsmanageDevice360.utils.print_info("Clicking on port label")
            xiq.xflowsmanageDevice360.auto_actions.click(port_label)
        else:
            xiq.xflowsmanageDevice360.utils.print_info("The port label was not found")
            return False

        port_from_list = xiq.xflowsmanageDevice360.get_device360_port_from_aggregation_list(ports[0])
        if port_from_list:
            xiq.xflowsmanageDevice360.utils.print_info("Clicking on port from aggregation list")
            xiq.xflowsmanageDevice360.auto_actions.click(port_from_list)
        else:
            xiq.xflowsmanageDevice360.utils.print_info("Port not found in aggregation list")
            return False

        # Toggle lacp on window
        if click_lacp:
            lacp_switch = xiq.xflowsmanageDevice360.get_device360_lacp_toggle()
            if lacp_switch:
                xiq.xflowsmanageDevice360.utils.print_info("Clicking LACP toggle'")
                xiq.xflowsmanageDevice360.auto_actions.click(lacp_switch)
            else:
                xiq.xflowsmanageDevice360.utils.print_info("LACP toggle not found")
                return False

        remove_from_aggregation_button = xiq.xflowsmanageDevice360.get_device360_aggregate_remove_button()
        if remove_from_aggregation_button:
            for port_name in ports:
                xiq.xflowsmanageDevice360.utils.print_info("Clicking on 'Remove from aggregation' button")
                xiq.xflowsmanageDevice360.auto_actions.click(remove_from_aggregation_button)
        else:
            xiq.xflowsmanageDevice360.utils.print_info("'Remove from aggregation button' not found")
            return False

        # Get save button
        lag_save_button = xiq.xflowsmanageDevice360.get_device360_lag_save_button()
        if lag_save_button:
            xiq.xflowsmanageDevice360.utils.print_info("Clicking Save button")
            xiq.xflowsmanageDevice360.auto_actions.click(lag_save_button)
            sleep(5)
        else:
            xiq.xflowsmanageDevice360.utils.print_info("Save button not found")
            return False

        # Save port Config
        save_port_config = xiq.xflowsmanageDevice360.get_device360_save_port_config()
        if save_port_config:
            xiq.xflowsmanageDevice360.utils.print_info("Clicking Save port config button'")
            xiq.xflowsmanageDevice360.auto_actions.click(save_port_config)
            sleep(5)
        else:
            xiq.xflowsmanageDevice360.utils.print_info("Save port config button not found")
            return False

        # Check lacp not formed in Device360
        if xiq.xflowsmanageDevice360.get_device360_lacp_label(port=ports[0]):
            return False
        return True

    def device360_add_lag_port(self, master_port, port):
        try:
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=master_port))
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.
                                get_device360_aggregate_available_port(port=port))
            sleep(1)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_aggregate_add_button())
            sleep(5)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_save_button())
            sleep(5)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_save_port_config())
            sleep(5)
        except Exception as exc:
            print(exc)
            return -1
        return 1

    def device360_remove_lag(self, master_port):
        try:
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lacp_label(port=master_port))
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.
                                get_device360_aggregate_selected_port(port=master_port))
            for i in range(0, 4):
                AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.
                                    get_device360_aggregate_remove_button())
                sleep(2)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_lag_save_button())
            sleep(5)
            AutoActions().click(self.setup_cls_obj.xiq.xflowsmanageDevice360.get_device360_save_port_config())
            sleep(5)
        except Exception as exc:
            print(exc)
            return -1
        return 1
