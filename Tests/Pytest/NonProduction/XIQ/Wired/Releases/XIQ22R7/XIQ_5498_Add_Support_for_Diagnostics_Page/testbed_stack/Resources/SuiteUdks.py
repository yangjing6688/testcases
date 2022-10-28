import pytest
import re
import time
import selenium

from extauto.common.AutoActions import AutoActions
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from extauto.common.Utils import Utils

class SuiteUdk:

    def __init__(self):
        self.defaultLibrary = DefaultLibrary()
        self.auto_actions = AutoActions()
        self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend
        self.xiq = XiqLibrary()
        self.Utils = Utils()


    def get_virtual_router(self, dut):
        global vrName

        result = self.devCmd.send_cmd(dut.name, 'show vlan', max_wait=10, interval=2)

        output = result[0].cmd_obj.return_text

        pattern = f'(\w+)(\s+)(\d+)(\s+)({dut.ip})(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'

        match = re.search(pattern, output)

        if match:
            print(f"Mgmt Vlan Name : {match.group(1)}")
            print(f"Vlan ID        : {match.group(3)}")
            print(f"Mgmt IPaddress : {match.group(5)}")
            print(f"Active ports   : {match.group(9)}")
            print(f"Total ports    : {match.group(11)}")
            print(f"Virtual router : {match.group(12)}")

            if int(match.group(9)) > 0:
                return match.group(12)
            else:
                print(f"There is no active port in the mgmt vlan {match.group(1)}")
                return -1;
        else:
            print("Pattern not found, unable to get virtual router info!")
            return -1;

    def get_stacking_details_cli(self, dut):
        """
        - This keyword gets stacking details from CLI(Mac add, Slot number and Role -for each unit)
        :return: a list of tuples
        """
        units_list = []

        if dut.cli_type.upper() == "EXOS":
            self.devCmd.send_cmd(dut.name, f'disable cli paging', max_wait=10, interval=2)

            stacking_details_output = self.devCmd.send_cmd(dut.name, f'show stacking', max_wait=10, interval=2)
            p = re.compile(r"((?:[0-9a-fA-F]:?){12})\s+(\d)\s+[^\s]+\s+([^\s]+)", re.M)
            stacking_details = re.findall(p, stacking_details_output[0].return_text)
            units_list.append(stacking_details)

            return units_list

        elif dut.cli_type.upper() == "VOSS":
            pytest.skip("To be done")

    def navigate_to_unit_options_from_xiq_diagnostics_page(self, unit, unit_role):
        """
        - This keyword navigates to unit options from Device360 - Diagnostics Page
        - It is assumed that the Device360 window is open in Monitor-Diagnostics
        :return:
        """
        try:
            ok = 1
            if AutoActions().click(self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_stack_drop_down_unit()) != 1:
                ok = 0
            else:
                print("Clicked on Drop down")
            if ok != 1:
                print("Unable to click on drop down")
                return -1

            ok = 1
            if AutoActions().click(self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_stack_drop_down_unit_options(unit, unit_role)) != 1:
                ok = 0
            else:
                print("Unit was selected")
            if ok != 1:
                print("Unable to select unit")
                return -1
        except Exception as exc:
            print(exc)
            return -1
        return 1


    def select_all_port_diagnostics_page(self):
        """
        - This keyword selects all port in Diagnostics Page
        - It is assumed that the Device360 window is open in Monitor-Diagnostics
        :return:
        """
        try:
            ok = 1
            if AutoActions().click(
                    self.xiq.xflowsmanageDevice360.get_device360_port_diagnostics_select_all_ports_button()) != 1:
                ok = 0
            else:
                print("Clicked on Select All Ports Button")
            if ok != 1:
                print("Unable to click on Select All Ports Button")
                return -1
        except Exception as exc:
            print(exc)
            return -1
        return 1

    def deselect_all_port_diagnostics_page(self):
        """
        - This keyword deselects all port in Diagnostics Page
        - It is assumed that the Device360 window is open in Monitor-Diagnostics
        :return:
        """
        try:
            ok = 1
            if AutoActions().click(
                    self.xiq.xflowsmanageDevice360.get_device360_port_diagnostics_deselect_all_ports_button()) != 1:
                ok = 0
            else:
                print("Clicked on Deselect All Ports Button")
            if ok != 1:
                print("Unable to click on Deselect All Ports Button")
                return -1
        except Exception as exc:
            print(exc)
            return -1
        return 1


    def check_all_the_individual_devices_in_the_stack_monitor_diagnostics(self, dut):
        """
        - This keyword checks the dropdown in Device360 Monitor Diagnostics.
        - It is assumed that the Device360 window is open in Monitor-Diagnostics
        :return:
        """
        stacking_info_cli = self.get_stacking_details_cli(dut)
        print(f"Print a list with mac add, number of slot and role for each stack unit: {stacking_info_cli}")

        mac_add_list_cli = []
        for i in range(0, len(stacking_info_cli[0])):
            unit_i_mac_address = stacking_info_cli[0][i][0]
            unit_i_mac_address_mapped = unit_i_mac_address.replace(':', '')
            unit_i_mac_address_final_mapped = unit_i_mac_address_mapped.upper()
            mac_add_list_cli.append(unit_i_mac_address_final_mapped)
        print(f"Print mac add units: {mac_add_list_cli}")

        print("Navigate to through units and make mac add check")
        for i in range(1, len(stacking_info_cli[0])):
            if stacking_info_cli[0][i][2].upper() == 'STANDBY':
                self.Utils.wait_till(
                    lambda: self.navigate_to_unit_options_from_xiq_diagnostics_page(
                        stacking_info_cli[0][i][1], 'MEMBER'),
                    delay=8, exp_func_resp=True)
            else:
                res = self.navigate_to_unit_options_from_xiq_diagnostics_page(
                    stacking_info_cli[0][i][1], stacking_info_cli[0][i][2].upper())
                if res == -1:
                    print("Unable to navigate to unit options")
                    return -1
            self.Utils.wait_till(delay=5)
            mac_address_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_mac_address_stack_active_unit(
                mac_add_list_cli[i])
            if not mac_address_xiq:
                print(f"Backup/Standby MAC address from the header side is displayed wrong according to the CLI({mac_add_list_cli[i]})")
                return -1

        print("Navigate to master unit and make mac add check")
        res = self.navigate_to_unit_options_from_xiq_diagnostics_page(stacking_info_cli[0][0][1],
                                                                                     stacking_info_cli[0][0][2].upper())
        if res == -1:
            print("Unable to navigate to unit options")
            return -1


        self.Utils.wait_till(delay=5)
        mac_address_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_mac_address_stack_active_unit(
            mac_add_list_cli[0])
        if not mac_address_xiq:
            print(f"Master MAC address from the header side is displayed wrong according to the CLI({mac_add_list_cli[0]})")
            return -1

        return 1

    def device360_get_top_bar_information_stack(self):
        """
        - This keyword gets information from the top bar of the Device360 view.
        - It is assumed that the Device360 window is open.
        - Keyword Usage
         - ``Device360 Get Top Bar Information``
        :return: dictionary of information obtained from the top bar of the Device360 view
        """

        print("Getting Device360 Top Bar Information")
        device360_info = dict()

        cpu_el = self.xiq.xflowsmanageDevice360.get_topbar_cpu()
        mem_el = self.xiq.xflowsmanageDevice360.get_topbar_memory()
        mac_el = self.xiq.xflowsmanageDevice360.get_topbar_mac_usage_diagnostics()
        uptime_el = self.xiq.xflowsmanageDevice360.get_topbar_uptime_diagnostics()
        temp_el = self.xiq.xflowsmanageDevice360.get_topbar_temperature_diagnostics()
        power_el = self.xiq.xflowsmanageDevice360.get_topbar_power_diagnostics()
        fan_el = self.xiq.xflowsmanageDevice360.get_topbar_fan_diagnostics()

        # Workaround - first element moved to isn't being recognized, so move to Memory element first
        if mem_el:
            self.auto_actions.move_to_element(mem_el)

        if cpu_el:
            self.auto_actions.move_to_element(cpu_el)
            time.sleep(2)
            tt_content = self.xiq.xflowsmanageDevice360.get_tooltip_content()
            if tt_content:
                tt_text = tt_content.text
                print(f"Tooltip content for CPU Usage is {tt_text}")
                cpu_values = tt_text.split(":")
                if len(cpu_values) == 2 and cpu_values[0] == "CPU Usage":
                    cpu_value = cpu_values[1].strip()
                    device360_info["cpu_usage"] = cpu_value
                else:
                    print("Unable to parse value for CPU Usage")
                    device360_info["cpu_usage"] = ""
            else:
                print("Could not determine value for CPU Usage")
                device360_info["cpu_usage"] = ""
        else:
            print("Could not find CPU Usage element")
            device360_info["cpu_usage"] = ""

        if mem_el:
            self.auto_actions.move_to_element(mem_el)
            time.sleep(2)
            tt_content = self.xiq.xflowsmanageDevice360.get_tooltip_content()
            if tt_content:
                tt_text = tt_content.text
                print(f"Tooltip content for Memory is {tt_text}")
                mem_values = tt_text.split(":")
                if len(mem_values) == 2 and mem_values[0] == "Memory":
                    mem_value = mem_values[1].strip()
                    device360_info["memory_usage"] = mem_value
                else:
                    print("Unable to parse value for Memory Usage")
                    device360_info["memory_usage"] = ""
            else:
                print("Could not determine value for Memory Usage")
                device360_info["memory_usage"] = ""
        else:
            print("Could not find Memory Usage element")
            device360_info["memory_usage"] = ""

        if mac_el:
            self.auto_actions.move_to_element(mac_el)
            time.sleep(2)
            tt_content = self.xiq.xflowsmanageDevice360.get_tooltip_content()
            if tt_content:
                tt_text = tt_content.text
                print(f"Tooltip content for MAC Table Utilization is {tt_text}")
                mac_values = tt_text.split(":")
                if len(mac_values) == 2 and mac_values[0] == "MAC Table Utilization":
                    mac_value = mac_values[1].strip()
                    device360_info["mac_usage"] = mac_value
                else:
                    print("Unable to parse value for MAC Table Utilization")
                    device360_info["mac_usage"] = ""
            else:
                print("Could not determine value for MAC Table Utilization")
                device360_info["mac_usage"] = ""
        else:
            print("Could not find MAC Table Utilization element")
            device360_info["mac_usage"] = ""

        if uptime_el:
            self.auto_actions.move_to_element(uptime_el)
            time.sleep(2)
            tt_content = self.xiq.xflowsmanageDevice360.get_tooltip_content()
            if tt_content:
                tt_text = tt_content.text
                # This field is currently in the format "Uptime: Last seen: <date>, <time>" so we want to strip
                # off the label ("Uptime: Last seen:"), and remove the comma from the date and time portion.
                # NOTE: This may change when APC-45218 is addressed.
                print(f"Tooltip content for Uptime is {tt_text}")
                tt_text = re.sub('Uptime: Last seen: ', '', tt_text)
                print(f"Stripped tooltip content for Uptime is {tt_text}")
                uptime_values = tt_text.split(",")
                if len(uptime_values) == 2:
                    uptime_date = uptime_values[0].strip()
                    uptime_time = uptime_values[1].strip()
                    device360_info["uptime"] = uptime_date + " " + uptime_time
                else:
                    print("Unable to parse value for Uptime")
                    device360_info["uptime"] = ""
            else:
                print("Could not determine value for Uptime")
                device360_info["uptime"] = ""
        else:
            print("Could not find Uptime element")
            device360_info["uptime"] = ""

        if temp_el:
            self.auto_actions.move_to_element(temp_el)
            time.sleep(2)
            tt_content = self.xiq.xflowsmanageDevice360.get_tooltip_content()
            if tt_content:
                tt_text = tt_content.text
                print(f"Tooltip content for temperature is {tt_text}")
                temp_values = tt_text.split(":")
                if len(temp_values) == 2 and temp_values[0] == "Temperature":
                    temp_value = temp_values[1].strip()
                    device360_info["temp"] = temp_value
                else:
                    print("Unable to parse value for temperature")
                    device360_info["temp"] = ""
            else:
                print("Could not determine value for temperature")
                device360_info["temp"] = ""
        else:
            print("Could not find MAC Table Utilization element")
            device360_info["temp"] = ""

        if power_el:
            self.auto_actions.move_to_element(power_el)
            time.sleep(2)
            tt_content = self.xiq.xflowsmanageDevice360.get_tooltip_content()
            if tt_content:
                power_el_text = tt_content.text
                power_supply_text_2 = power_el_text.split('\n')
                power_supply_list = []
                total_power_available = 0
                total_power_consumed = 0
                threshold_power = 0
                for status in power_supply_text_2:
                    if "Total Power Available" in status:
                        total_power_available = re.sub('[^0-9]+', '', status)
                    elif "Total Power Consumed" in status:
                        total_power_consumed = re.sub('[^0-9]+', '', status)
                    elif "Threshold" in status:
                        threshold_power = re.sub('[^0-9]+', '', status)
                    else:
                        if "Power " in status and "Status" not in status:
                            status = re.sub('Power [0-9]: ', '', status)
                            power_supply_list.append(status)
                print(f"Power supply grepped list in D360 is {power_supply_list}")
                device360_info["power_supply"] = power_supply_list
                device360_info["total_power_available"] = total_power_available
                device360_info["total_power_consumed"] = total_power_consumed
                device360_info["threshold_power"] = threshold_power
            else:
                print("Could not parse the values for Power")
                device360_info["power_supply"] = ""
                device360_info["total_power_available"] = ""
                device360_info["total_power_consumed"] = ""
                device360_info["threshold_power"] = ""
        else:
            print("Could not determine values for Power")
            device360_info["power_supply"] = ""
            device360_info["total_power_available"] = ""
            device360_info["total_power_consumed"] = ""
            device360_info["threshold_power"] = ""

        if fan_el:
            self.auto_actions.move_to_element(fan_el)
            tt_content = self.xiq.xflowsmanageDevice360.get_tooltip_content()
            if tt_content:
                fan_status_text = tt_content.text
                fan_status_text_2 = fan_status_text.split('\n')
                print(f"Fan status output list is {fan_status_text}")
                fan_status_list = []
                for status in fan_status_text_2:
                    if "Operating" in status:
                        status1 = re.sub('Tray [0-9] Fan [0-9]: ', '', status)
                        fan_status_list.append(status1)
                    else:
                        if "failed" in status:
                            fan_status_list.append("Unit has failed")
                print(f"Fan status grepped list is {fan_status_list}")
                device360_info["fan_status"] = fan_status_list
            else:
                print("Could not parse the value for Fan")
                device360_info["fan_status"] = ""
        else:
            print("Could not determine value for Fan status")
            device360_info["fan_status"] = ""

        return device360_info

    def navigate_to_unit_1_n_and_hover_over_top_bar_information_stack(self, dut):
        """
        - This keyword gets information from the top bar of the Device360 view.
        - It is assumed that the Device360 window is open in Diagnostics Page.
        - Keyword Usage
        :return: dictionary of information obtained from the top bar of the Device360 view
        """
        print("Verify the first seven icons from the top bar for each unit")
        stacking_info_cli = self.get_stacking_details_cli(dut)
        for i in range(1, len(stacking_info_cli[0])):
            if stacking_info_cli[0][i][2].upper() == 'STANDBY':
                self.Utils.wait_till(
                    lambda: self.navigate_to_unit_options_from_xiq_diagnostics_page(
                        stacking_info_cli[0][i][1], 'MEMBER'),
                    delay=8, exp_func_resp=True)
            else:
                self.navigate_to_unit_options_from_xiq_diagnostics_page(
                    stacking_info_cli[0][i][1], stacking_info_cli[0][i][2].upper())
            self.Utils.wait_till(delay=5)
            self.device360_get_top_bar_information_stack()

    def get_info_from_stack(self, dut):
        """
        - This keyword gets dut details from CLI(ip, mac address, software version, model, serial, make, iqagent version)
        :return: a list of tuples
        """
        info_list = []

        if dut.cli_type.upper() == "EXOS":
            self.devCmd.send_cmd(dut.name, f'disable cli paging', max_wait=10, interval=2)
            ip_list_cli = []
            ip_list = []
            ip_output = self.devCmd.send_cmd(dut.name, f'show iqagent | include Interface', max_wait=10, interval=2)
            p = re.compile(r"(Source\sInterface)\s+(\d+.\d+.\d+.\d+)", re.M)
            ip_dut_list = re.findall(p, ip_output[0].return_text)
            ip_list.append(ip_dut_list)
            for i in range(0, len(ip_list[0])):
                unit_i_ip = ip_list[0][i][1]
                ip_list_cli.append(unit_i_ip)
            info_list.append(ip_list_cli)

            stacking_info_cli = self.get_stacking_details_cli(dut)
            print(f"Stacking details cli: {stacking_info_cli}")
            stacking_info_cli_list_of_tuples= stacking_info_cli[0]
            sorted_by_second = sorted(stacking_info_cli_list_of_tuples, key=lambda tup: tup[1])
            print(f"Stacking details cli sorted_by_second: {sorted_by_second}")
            mac_add_list_cli = []
            for i in range(0, len(sorted_by_second)):
                unit_i_mac_address = sorted_by_second[i][0]
                unit_i_mac_address_mapped = unit_i_mac_address.replace(':', '')
                unit_i_mac_address_final_mapped = unit_i_mac_address_mapped.upper()
                mac_add_list_cli.append(unit_i_mac_address_final_mapped)
            info_list.append(mac_add_list_cli)

            soft_version_list_cli = []
            soft_version_list = []
            soft_version_output = self.devCmd.send_cmd(dut.name, f'show version', max_wait=10, interval=2)
            p = re.compile(r"(Slot-\d)\s+\W.[^\s]+.[^\s]+.[^\s]+.[^\s]+.[^\s]+.[^\s]+\s+.[^\s]+\W([^\s]+)", re.M)
            soft_version_dut_list = re.findall(p, soft_version_output[0].return_text)
            soft_version_list.append(soft_version_dut_list)
            for i in range(0, len(soft_version_list[0])):
                unit_i_soft_version = soft_version_list[0][i][1]
                soft_version_list_cli.append(unit_i_soft_version)
            info_list.append(soft_version_list_cli)

            type_list_cli = []
            type_list = []
            type_output = self.devCmd.send_cmd(dut.name, f'show slot', max_wait=10, interval=2)
            p = re.compile(r"(Slot-\d)\s{5}([^\s]+)", re.M)
            type_dut_list = re.findall(p, type_output[0].return_text)
            type_list.append(type_dut_list)
            for i in range(0, len(type_list[0])):
                unit_i_type = type_list[0][i][1]
                type_list_cli.append(unit_i_type)
            info_list.append(type_list_cli)

            serial_list_cli = []
            serial_list = []
            serial_output = self.devCmd.send_cmd(dut.name, f'show version', max_wait=10, interval=2)
            p = re.compile(r"(Slot-\d)\s+\W.[^\s]+.([^\s]+)", re.M)
            serial_number_list = re.findall(p, serial_output[0].return_text)
            serial_list.append(serial_number_list)
            for i in range(0, len(serial_list[0])):
                unit_i_serial_number = serial_list[0][i][1]
                serial_list_cli.append(unit_i_serial_number)
            info_list.append(serial_list_cli)

            make_list_cli = []
            make_list = []
            make_output =  self.devCmd.send_cmd(dut.name, f'show version | include Image', max_wait=10, interval=2)
            p = re.compile(r"(Image\s+\W)\s+(.*)\sversion", re.M)
            make_dut_list = re.findall(p, make_output[0].return_text)
            make_list.append(make_dut_list)
            for i in range(0, len(make_list[0])):
                unit_i_make = make_list[0][i][1]
                make_list_cli.append(unit_i_make)
            info_list.append(make_list_cli)

            iqagent_version_cli = []
            iqagent_version_list = []
            iqagent_version_output = self.devCmd.send_cmd(dut.name, f'show iqagent | include Version', max_wait=10,interval=2)
            p = re.compile(r"(Version)\s+([^\s]+)", re.M)
            iqagent_version_dut = re.findall(p, iqagent_version_output[0].return_text)
            iqagent_version_list.append(iqagent_version_dut)
            for i in range(0, len(iqagent_version_list[0])):
                unit_i_iqagent_version = iqagent_version_list[0][i][1]
                iqagent_version_cli.append(unit_i_iqagent_version)
            info_list.append(iqagent_version_cli)

            return info_list

        elif dut.cli_type.upper() == "VOSS":
            pytest.skip("To be done")

    def match_info_stack_cli_with_xiq(self, dut, slot = 1):
        """
        - This keyword Verifies if the device information(ip, mac address, software version, model, serial, make, iqagent version) from the header side is displayed correctly according to the cli
        It is assumed that the Device360 window is open in Diagnostics Page and the dropdown is showing the wanted unit. Default is MASTER.
        If the results
        :return:
        """
        slot = int(slot)
        list = self.get_info_from_stack(dut)
        if not list:
            print("Unable to get info from dut")
            return -1

        print(f"List of info from CLI: {list}")
        ip_address_cli = list[0][0]
        print(f"Ip Add from CLI: {ip_address_cli}")
        ip_address_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_ip_address_stack_active_unit(
            ip_address_cli)
        if not ip_address_xiq:
            print(f"Ip address from the header side is displayed wrong according to the CLI ({ip_address_cli})")
            return -1


        mac_address_cli = list[1][slot-1]
        print(f"MAC Add from CLI: {mac_address_cli}")
        mac_address_cli_mapped = mac_address_cli.replace(':', '')
        mac_address_cli_final_mapped = mac_address_cli_mapped.upper()
        print(f"MAC Add from CLI mapped to match XIQ: {mac_address_cli_final_mapped}")
        mac_address_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_mac_address_stack_active_unit(
            mac_address_cli_final_mapped)
        if not mac_address_xiq:
            print(f"MAC address from the header side is displayed wrong according to the CLI({mac_address_cli})")
            return -1

        soft_version_cli = list[2][slot-1]
        print(f"Soft version from CLI: {soft_version_cli}")
        soft_version_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_soft_version_stack_active_unit(
            soft_version_cli)
        if  not soft_version_xiq:
            print(f"Soft Version from the header side is displayed wrong according to the CLI({soft_version_cli})")
            return -1

        model_cli = list[3][slot-1]
        print(f"Dut Model from CLI: {model_cli}")
        if "EXOS" in model_cli:
            model_cli = model_cli.replace("-EXOS","")
        if list[5][0] == "ExtremeXOS":
            list[5][0] = "Switch Engine"
        if list[5][0] == "Extreme Networks Switch Engine":
            list[5][0] = "Switch Engine"
        # model_cli_mapped = 'Switch Engine ' + model_cli
        model_cli_mapped = list[5][0] + ' ' + model_cli
        print(f"Dut Model from CLI mapped to match XIQ: {model_cli_mapped}")
        model_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_model_stack_active_unit(
            model_cli_mapped)
        if not model_xiq:
            print(f"Model from the header side is displayed wrong according to the CLI({model_cli})")
            return -1

        serial_number_cli = list[4][slot-1]
        print(f"Serial number from CLI: {serial_number_cli}")
        serial_number_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_serial_number_stack_active_unit(
            serial_number_cli)
        if not serial_number_xiq:
            print(f"Serial number from the header side is displayed wrong according to the CLI({serial_number_cli})")
            return -1

        # make_cli = "Switch Engine"
        if list[5][0] == "ExtremeXOS":
            list[5][0] = "Switch Engine"
        else:
            make_cli = list[5][0]
        print(f"Make from CLI: {make_cli}")
        make_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_make_stack_active_unit(
            make_cli)
        if not make_xiq:
            print(f"Make from the header side is displayed wrong according to the CLI({make_cli})")
            return -1

        iqagent_version_cli = list[6][0]
        print(f"Iqagent version from CLI: {iqagent_version_cli}")
        iqagent_version_xiq = self.xiq.xflowsmanageDevice360.dev360.get_device360_monitor_diagnostics_health_item_iqagent_version_stack_active_unit(
            iqagent_version_cli)
        if not make_xiq:
            print(f"Iqagent Version from the header side is displayed wrong according to the CLI({iqagent_version_cli})")
            return -1

        return 1

