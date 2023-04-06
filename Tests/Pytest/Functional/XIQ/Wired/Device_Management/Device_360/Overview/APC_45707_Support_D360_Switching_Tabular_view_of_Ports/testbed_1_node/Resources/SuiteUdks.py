import re
import time
import selenium
import random

from pytest_testconfig import config
from selenium.webdriver.common.keys import Keys

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import NetworkElementConnectionManager
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from extauto.common.Screen import Screen
from extauto.xiq.flows.common.Navigator import Navigator
from extauto.xiq.elements.SwitchTemplateWebElements import SwitchTemplateWebElements
from extauto.xiq.elements.CommonObjectsWebElements import CommonObjectsWebElements
from extauto.xiq.flows.configure.NetworkPolicy import NetworkPolicy
from extauto.xiq.flows.configure.SwitchTemplate import SwitchTemplate
from extauto.common.AutoActions import AutoActions
from extauto.common.Utils import Utils
from extauto.xiq.elements.DeviceTemplateWebElements import DeviceTemplateWebElements
from extauto.xiq.elements.NetworkPolicyWebElements import NetworkPolicyWebElements
from extauto.xiq.elements.SwTemplateLegacyPortTypeWebElements import SwTemplateLegacyPortTypeWebElements
from extauto.xiq.flows.configure.CommonObjects import CommonObjects
from extauto.xiq.elements.Device360WebElements import Device360WebElements
from extauto.xiq.elements.AlarmsWebElements import AlarmsWebElements


DEFAULT_VLAN_ID = "1"


class SuiteUdk:
    
    def __init__(self, setup_cls_obj):
        self.defaultLibrary = DefaultLibrary()
        self.udks = self.defaultLibrary.apiUdks
        self.setup_cls_obj = setup_cls_obj
        self.xiq = setup_cls_obj.xiq
        self.devCmd = self.setup_cls_obj.devCmd
        self.tb = PytestConfigHelper(config)
        self.cfg = config
        self.network_manager = NetworkElementConnectionManager()
        self.utils = Utils()
        self.auto_actions = AutoActions()
        self.navigator = Navigator()
        self.device_template_web_elements = DeviceTemplateWebElements()
        self.sw_template_web_elements = SwitchTemplateWebElements()
        self.np_web_elements = NetworkPolicyWebElements()
        self.nw_policy = NetworkPolicy()
        self.legacy_port_type_editor = SwTemplateLegacyPortTypeWebElements();
        self.dev360 = Device360WebElements()
        self.alarm = AlarmsWebElements()
        self.screen = Screen()
        self.switch_template = SwitchTemplate()
        self.cobj_web_elements = CommonObjectsWebElements()
        self.xflowsconfigureCommonObjects = CommonObjects()
        self.devices = setup_cls_obj.xiq.xflowscommonDevices
        self.dev360 = setup_cls_obj.xiq.xflowsmanageDevice360

    def get_ports_from_dut(self, dut):
    
        try:
            self.close_connection_with_error_handling(dut)
            self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

            if dut.cli_type.upper() == "EXOS":
                self.setup_cls_obj.devCmd.send_cmd(dut.name, f'disable cli paging', max_wait=10, interval=2)
                output = self.setup_cls_obj.devCmd.send_cmd(dut.name, f'show ports info', max_wait=10, interval=2)[
                    0].return_text
                output = re.findall(r"\r\n(\d+)\s+", output)
                
            elif dut.cli_type.upper() == "VOSS":
                output = \
                self.setup_cls_obj.devCmd.send_cmd(dut.name, "show int gig int | no-more", max_wait=10, interval=2)[
                    0].return_text
                output = re.findall(r"\r\n(\d+/\d+)\s+", output)
        finally:
            self.close_connection_with_error_handling(dut)
        return output

    def close_connection_with_error_handling(self, dut):
        try:
            
            try:
                if dut.cli_type.upper() == "VOSS":
                    for session_id in range(7):
                        self.setup_cls_obj.devCmd.send_cmd(dut.name, f"clear ssh {session_id}")
                elif dut.cli_type.upper() == "EXOS":
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, "clear session all")
            except Exception as err:
                print(err)
                
            self.setup_cls_obj.network_manager.device_collection.remove_device(dut.name)
            self.setup_cls_obj.network_manager.close_connection_to_network_element(dut.name)
            
        except Exception as exc:
            print(exc)
        else:
            time.sleep(30)

    def do_onboarding(self, dut, location='Salem,Northeastern,Groundfloor',
                      delete_if_already_onboarded=True, configure_iqagent=False, wait_for_green_status=False):

        try:
            xiq_ip_address = self.setup_cls_obj.cfg['sw_connection_host']
            self.close_connection_with_error_handling(dut)
            self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

            if delete_if_already_onboarded:
                self.setup_cls_obj.xiq.xflowscommonDevices._goto_devices()
                self.setup_cls_obj.xiq.xflowscommonDevices.delete_device(device_serial=dut.serial)

            assert self.setup_cls_obj.xiq.xflowscommonDevices.onboard_device_quick(dut) == 1

            if configure_iqagent:

                if dut.cli_type.upper() == "EXOS":

                    self.setup_cls_obj.devCmd.send_cmd_verify_output(
                        dut.name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                        confirmation_phrases='Do you want to continue?', confirmation_args='y')
                    self.setup_cls_obj.devCmd.send_cmd(
                        dut.name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure iqagent server ipaddress ' + xiq_ip_address,
                                        max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)

                elif dut.cli_type.upper() == "VOSS":

                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'iqagent server ' + xiq_ip_address,
                                        max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd_verify_output(
                        dut.name, 'show application iqagent', 'true', max_wait=30, interval=10)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'exit', max_wait=10, interval=2)

                time.sleep(10)

            if wait_for_green_status:
                self.setup_cls_obj.xiq.xflowscommonDevices.wait_until_device_online(dut.serial)
                res = self.setup_cls_obj.xiq.xflowscommonDevices.get_device_status(device_serial=dut.serial)
                assert res == 'green', f"The EXOS device did not come up successfully in the XIQ; Device: {dut}"

        finally:
            self.close_connection_with_error_handling(dut)

    def set_lldp(self, dut, ports, action="enable"):
        
        try:
            
            self.close_connection_with_error_handling(dut)
            self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

            if dut.cli_type.upper() == "EXOS":
                if action == "enable":
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable cdp ports all', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable edp ports all', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable lldp ports all', max_wait=10, interval=2)
                elif action == "disable":
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'disable cdp ports all', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'disable edp ports all', max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, 'disable lldp ports all', max_wait=10, interval=2)

            elif dut.cli_type.upper() == "VOSS":
                self.setup_cls_obj.devCmd.send_cmd(dut.name, "enable", max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, "configure terminal", max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(
                    dut.name, f"interface gigabitEthernet {ports[0]}-{ports[-1]}", max_wait=10, interval=2)
                cmd_action = f"lldp port {ports[0]}-{ports[-1]} cdp enable"
                if action == "enable":
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, "no auto-sense enable", max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, "no fa enable", max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, cmd_action, max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, "fa enable", max_wait=10, interval=2)
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, "auto-sense enable", max_wait=10, interval=2)
                elif action == "disable":
                    self.setup_cls_obj.devCmd.send_cmd(dut.name, "no " + cmd_action, max_wait=10, interval=2)

        finally:
            self.close_connection_with_error_handling(dut)

    def bounce_IQAgent(self, dut, xiq_ip_address=None, connect_to_dut=True, disconnect_from_dut=True, wait=True):
        
        try:
            
            if connect_to_dut:
                self.close_connection_with_error_handling(dut)
                self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)

            if dut.cli_type.upper() == "EXOS":
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'disable iqagent', max_wait=10, interval=2,
                                                   confirmation_phrases='Do you want to continue?',
                                                   confirmation_args='Yes')
                if xiq_ip_address:
                    self.setup_cls_obj.devCmd.send_cmd(
                        dut.name, "configure iqagent server ipaddress {xiq_ip_address}", max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable iqagent', max_wait=10, interval=2)
            
            elif dut.cli_type.upper() == "VOSS":
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'configure terminal', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'application', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'no iqagent enable', max_wait=10, interval=2)
                if xiq_ip_address:
                    self.setup_cls_obj.devCmd.send_cmd(
                        dut.name, f'iqagent server {xiq_ip_address}', max_wait=10, interval=2)
                self.setup_cls_obj.devCmd.send_cmd(dut.name, 'iqagent enable', max_wait=10, interval=2)
        finally:
            if disconnect_from_dut:
                self.close_connection_with_error_handling(dut)
        if wait:
            self.setup_cls_obj.xiq.xflowscommonDevices.wait_until_device_online(dut.serial)

    def get_the_number_of_ports_from_cli(self, dut):
        
        try:
            self.close_connection_with_error_handling(dut)
            self.setup_cls_obj.network_manager.connect_to_network_element_name(dut.name)
            
            if dut.cli_type.upper() == "VOSS":

                self.devCmd.send_cmd(dut.name, 'enable',
                                    max_wait=10, interval=2)
                output = self.devCmd.send_cmd(dut.name, 'show int gig int | no-more',
                                            max_wait=10, interval=2)
                p = re.compile(r'^\d+\/\d+\/?\d*', re.M)
                match_port = re.findall(p, output[0].return_text)
                print(f"{match_port}")
                no_ports = len(match_port)
                no_ports = int(no_ports)

            elif self.tb.dut1.cli_type.upper() == "EXOS":
                self.devCmd.send_cmd(self.tb.dut1.name, f'disable cli paging',
                                    max_wait=10)
                output = self.devCmd.send_cmd(dut.name, f'show ports vlan',
                                            max_wait=10)
                output = output[0].return_text
                match_port = re.findall(r'(\d+)\s+\w+', output)
                no_ports = len(match_port)
                no_ports = int(no_ports)

            print(f'Number of ports for this switch is {no_ports}')
            return no_ports
        
        finally:
            self.close_connection_with_error_handling(dut)
      
    def device360_monitor_overview_pagination_next_page_by_number(self):
        """
         - This keyword will navigate to the next page of the Monitoring Overview Ports Table, using the
         page number button
         - Flow: Click next page number
         It Assumes That Already Navigated to Device360 Page
         - Keyword Usage:
         - ``Device360 Monitor Overview Pagination Next Page By Number``
        :return: 1 if successfully changed to next page
        :return: 2 if already on the last page
        :return: -1 if error
        """
        try:
            current_page = int(
                self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagin_number().text)
            other_pages = self.xiq.xflowsmanageDevice360.dev360.get_device360_pagination_page_buttons()
            for page in other_pages:
                if int(page.text) == current_page + 1:
                    self.xiq.xflowsmanageDevice360.utils.print_info(f"Going to page " + str(current_page + 1))
                    self.xiq.xflowsmanageDevice360.auto_actions.click(page)
                    time.sleep(5)
                    return 1
            return 2
        except Exception as e:
            return -1

    def device360_confirm_current_page_number(self, page_num_ref):
        """
         - This keyword will check if the page with page_num_ref number is currently displayed
         It Assumes That Already Navigated to Device360 Page (Monitoring->Overview)
         - Keyword Usage:
         - ``Device360 Monitor Overview Pagination Next Page By Number``
        :return: True if page number matches
        :return: False if page number doesn't match or on error
        """
        try:
            current_page = int(
                self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_current_pagin_number().text)
            if current_page == page_num_ref:
                return True
            return False
        except Exception as e:
            return False

    def list_port_element(self, xiq, port_no):
        rows = xiq.xflowscommonDevices.devices_web_elements.get_port_details_info()
        matchers = ['Type', 'LACP Status', 'Port Mode', 'Port Status',
                    'Transmission Mode', 'Access VLAN', 'Tagged VLAN(s)', 'LLDP Neighbor', 'Traffic Received',
                    'Traffic Sent', 'Port Errors', 'STP Port State', 'Port Speed']
        if rows:
            xiq.xflowscommonDevices.utils.print_debug(f"Searching {len(rows)} rows")
            for row in rows:
                xiq.xflowscommonDevices.utils.print_info(f"Port {port_no} details: ",
                                                         xiq.xflowscommonDevices.format_row(row.text))
                for i in matchers:
                    test = any(i in string for string in xiq.xflowscommonDevices.format_row(row.text))
                    if test == False:
                        return -1
            return 1
        else:
            return -1

    def device360_switch_get_current_page_port_name_list(self):
        """
         - This keyword will get a list with all the port names from the current page (Monitoring->Overview)
         - Flow: Click next page number
         It Assumes That Already Navigated to Device360 Page (Monitoring->Overview)
         - Keyword Usage:
         - ``Device360 Monitor Overview Pagination Next Page By Number``
        :return: port_name_list if successfully extracted the port names
        :return: -1 if error
        """
        try:
            port_name_list = []
            rows = self.get_device360_port_table_rows()
            for row in rows:
                port_name_list.append(
                    self.xiq.xflowsmanageDevice360.get_d360_switch_ports_table_interface_port_name_cell(row).text)
            if 'PORT NAME' in port_name_list:
                port_name_list.remove('PORT NAME')
            pattern_voss_three_nums = re.compile(r'\d+\/\d+\/\d+', re.M)
            filtered = [i for i in port_name_list if not pattern_voss_three_nums.match(i)]
            pattern_mgmt = re.compile(r'.*mgmt.*', re.M)
            filtered = [i for i in filtered if not pattern_mgmt.match(i)]
            return filtered
        except Exception as e:
            return -1

    def get_port_list_from_dut(self, dut):
        
        if dut.cli_type.upper() == "VOSS":
            
            time.sleep(10)
            self.devCmd.send_cmd(dut.name, 'enable',
                                max_wait=10, interval=2)
            output = self.devCmd.send_cmd(dut.name, 'show int gig int | no-more',
                                max_wait=10, interval=2)
            
            p = re.compile(r'^\d+\/\d+', re.M)
            match_port = re.findall(p, output[0].return_text)
            print(f"{match_port}")

            #remove elements with two /
            p2 = re.compile(r'\d+\/\d+\/\d+', re.M)
            filtered = [port for port in match_port if not p2.match(port)]
            return filtered
        
        elif dut.cli_type.upper() == "EXOS":
            
            time.sleep(10)
            self.devCmd.send_cmd(dut.name, 'disable cli paging',
                                max_wait=10, interval=2)
            output = self.devCmd.send_cmd(dut.name, 'show ports info',
                                max_wait=20, interval=5)
            p = re.compile(r'^\d+:\d+', re.M)
            match_port = re.findall(p, output[0].return_text)
            is_stack = True
            if len(match_port) == 0:
                is_stack = False
                p = re.compile(r'^\d+', re.M)
                match_port = re.findall(p, output[0].return_text)

            # Remove "not present" ports
            if is_stack:
                p_notPresent = re.compile(r'^\d+:\d+.*NotPresent.*$', re.M)
            else:
                p_notPresent = re.compile(r'^\d+.*NotPresent.*$', re.M)
            parsed_info = re.findall(p_notPresent, output[0].return_text)

            for port in parsed_info:
                port_num = re.findall(p, port)
                match_port.remove(port_num[0])

            return match_port

    def check_port_type(self, dut):
        
        if dut.cli_type.upper() == "VOSS":
            
            time.sleep(10)
            self.devCmd.send_cmd(dut.name, 'enable',
                                    max_wait=10, interval=2)
            output = self.devCmd.send_cmd(dut.name, 'show int gig l1-config | no-more',
                                            max_wait=10, interval=2)
            p = re.compile(r'(^\d+\/\d+)\s+(false|true)\s+(false|true)', re.M)
            match_port = re.findall(p, output[0].return_text)
            print(f"{match_port}")
            
            x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            x.pop(0)
            cnt_values_port_type = 0
            j = 0
            
            for it in x:
            
                port_type = it["TYPE"]
                port_name = it["PORT NAME"]
                print(f"port name:{port_name} and port type:{port_type}")
                
                print(f"Verify that each entry has a value set for the 'port type' column('RJ45,'SFP+','SFP-DD')")
                assert port_type in ['RJ45', 'SFP', 'SFP+', "QSFP28", 'SFP-DD', "SFP28"], \
                    "Port type column has an entry with a value different from ('RJ45','SFP+','SFP-DD')"
                
                cnt_values_port_type = cnt_values_port_type + 1
                
                if port_type == 'RJ45':
                
                    port_type_match_cli = 'true'
                    print("check if the port type 'RJ45' from XIQ is the same as the one from CLI")
                    assert (match_port[j][0] == port_name) and (match_port[j][
                                                                    2] == port_type_match_cli), \
                        "Did not found the expected port type value for expected port name value"
                    j = j + 1
                
                else:
                
                    print(f"{port_name},{port_type}")
                    assert port_type in ['RJ45', 'SFP', 'SFP+', "QSFP28", 'SFP-DD', "SFP28"], \
                        "Did not found the expected value. Port type column has an entry with " \
                        "a value different from ('SFP+','SFP-DD')"
            
            print(f"Verify that the 'port type' column has no empty entry")
            assert len(
                x) == cnt_values_port_type, "Expecting to find a value for the 'port type' field of each table entry"

        elif dut.cli_type.upper() == "EXOS":
            
            time.sleep(10)
            self.devCmd.send_cmd(self.tb.dut1.name, 'disable cli paging',
                                    max_wait=10, interval=2)
            output = self.devCmd.send_cmd(self.tb.dut1.name, 'show ports transceiver information',
                                            max_wait=10, interval=2)
            p = re.compile(r'(^\d+)\s+(DDMI\sis\snot\ssupported\son\sthis\sport)', re.M)
            match_port = re.findall(p, output[0].return_text)
            print(f"{match_port}")

            x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
            x.pop(0)
            cnt_values_port_type = 0
            j = 0
            
            for it in x:
                
                port_type = it["TYPE"]
                port_name = it["PORT NAME"]
                print(f"port name:{port_name} and port type:{port_type}")
                
                print(f"Verify that each entry has a value set for the 'port type' column('RJ45,'SFP+','SFP-DD')")
                assert port_type in ['RJ45', 'SFP', 'SFP+', "QSFP28", 'SFP-DD', "SFP28"], \
                    "Port type column has an entry with a value different from ('RJ45','SFP+','SFP-DD')"
                
                cnt_values_port_type = cnt_values_port_type + 1
                
                if port_type == 'RJ45':
                    port_type_match_cli = 'DDMI is not supported on this port'
                    print("check if the port type 'RJ45' from XIQ is the same as the one from CLI")
                    assert (match_port[j][0] == port_name) and (match_port[j][
                                                                    1] == port_type_match_cli), \
                        "Did not found the expected port type value RJ45 for expected port name"
                    j = j + 1
                
                else:
                    print(f"{port_name},{port_type}")
                    assert port_type in ['RJ45', 'SFP', 'SFP+', "QSFP28", 'SFP-DD', "SFP28"], \
                        "Did not found the expected value. Port type column has an entry with a " \
                        "value different from ('SFP+','SFP-DD')"
            
            print(f"Verify that the 'port type' column has no empty entry")
            assert len(x) == cnt_values_port_type, \
                "Expecting to find a value for the 'port type' field of each table entry"

    def get_device_port_status(self, devCmd=None, dut=None):
        if devCmd is None or dut is None:
            return

        # get the required information from the device CLI
        if dut.cli_type.upper() == 'VOSS':
            time.sleep(10)
            output = devCmd.send_cmd(
                dut.name, 'show interfaces gigabitEthernet name | no-more', max_wait=10, interval=2)
            # get a list of all the ports from the device
            p = re.compile(r'^\d+\/\d+', re.M)
            match_port = re.findall(p, output[0].return_text)
            # search the port status values in the command output
            p = re.compile(r'(?:up|down)', re.M)
            match_cli_port_status = re.findall(p, output[0].return_text)

            # get a dictionary with ports as the keys and their corresponding speeds as the values
            cli_ports_status = dict(zip(match_port, match_cli_port_status))
        elif dut.cli_type.upper() == 'EXOS':
            time.sleep(10)
            devCmd.send_cmd(dut.name, 'disable cli refresh', max_wait=10, interval=2)
            devCmd.send_cmd(dut.name, 'disable cli paging', max_wait=10, interval=2)
            output = devCmd.send_cmd(dut.name, 'show ports', max_wait=10, interval=2)
            # get a list of all the ports from the device
            match_port = re.findall(r"\r\n(\d+)\s+", output[0].return_text)
            cli_ports_status={}
            for port in match_port:
                row_text = re.search(fr"\r\n{port}\s.*\r\n", output[0].return_text).group(0)
                cli_ports_status[port] = "up" if re.search(r"\s+A\s+", row_text) else "down"

        print("****************** Device ports status dictionary: ******************")
        print(cli_ports_status)

        return cli_ports_status

    def setup_vlans(self, udks, dut, vlan, port_list):
        try:
            udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(dut.name, vlan)
        except Exception as exc:
            print(repr(exc))
        
        try:
            udks.vlanUdks.Create_VLAN_and_Add_Ports_Untagged_then_Verify(self.tb.dut1_name, vlan, port_list)
        except Exception as exc:
            print(repr(exc))

    def get_device_ports_speed(self, devCmd=None, dut=None):
        if devCmd is None or dut is None:
            return

        match_port = None
        device_ports_speed = None

        # get the required information from the device CLI
        if dut.cli_type.upper() == 'VOSS':
            output = devCmd.send_cmd(dut.name, 'show interfaces gigabitEthernet name | no-more', max_wait=10, interval=2)

            # get a list of all the ports from the device
            p = re.compile(r'^\d+\/\d+', re.M)
            match_port = re.findall(p, output[0].return_text)

            # search the speed values in the command output
            p = re.compile(r'(?:half|full)\s+(\d+)', re.M)
            match_device_ports_speed = re.findall(p, output[0].return_text)

            # get a dictionary with ports as the keys and their corresponding speeds as the values
            device_ports_speed = dict(zip(match_port, match_device_ports_speed))
        elif dut.cli_type.upper() == 'EXOS':
            devCmd.send_cmd(dut.name, 'disable cli refresh', max_wait=10, interval=2)
            devCmd.send_cmd(dut.name, 'disable cli paging', max_wait=10, interval=2)
            output = devCmd.send_cmd(dut.name, 'show ports', max_wait=10, interval=2)

            # get a list of all the ports from the device
            p = re.compile(r'^\d+', re.M)
            match_port = re.findall(p, output[0].return_text)

            # search the speed values in the command output (the link state is needed in the result
            # because the speed is not shown if the port is down)
            p = re.compile(r'([ARNPLDdB]+\s\s\s\s\s\s(?:\d+G?)?)', re.M)
            match_port_link_state_speed = re.findall(p, output[0].return_text)

            # refine the values from the list
            for i in range(len(match_port_link_state_speed)):
                speed = re.search(r'\d+', match_port_link_state_speed[i])
                unit = re.search(r'G', match_port_link_state_speed[i])

                # if the speed value is not present set it as "0"
                if speed is None:
                    speed = "0"
                else:
                    # if a 'G' is found next to the speed value, transform it to Mbps
                    if unit is not None:
                        speed = str(int(speed.group(0)) * 1000)
                    else:
                        speed = speed.group(0)

                # replace the current value in the list with the speed value
                match_port_link_state_speed[i] = speed

            match_device_ports_speed = match_port_link_state_speed

            # get a dictionary with ports as the keys and their corresponding speeds as the values
            device_ports_speed = dict(zip(match_port, match_device_ports_speed))

        print("****************** Device port list: ******************")
        print(match_port)

        print("****************** Device ports speed dictionary: ******************")
        print(device_ports_speed)

        return device_ports_speed

    def Transmit_Traffic_Bidirectionally_and_Verify_it_was_Received_tcxm_9568(
        self, port_a, port_b, tx_packet_name_a,tx_packet_name_b, rx_packet_name_a,
        rx_packet_name_b,tx_count=100, tx_rate=100, **kwargs):

        self.udks.trafficGenerationUdks.Configure_Packet_on_Port_Single_Burst(
            port_a, tx_packet_name_a, count=tx_count,rate=tx_rate, **kwargs)
        self.udks.trafficGenerationUdks.Configure_Packet_on_Port_Single_Burst(
            port_b, tx_packet_name_b, count=tx_count,rate=tx_rate, **kwargs)
        rx_packet_a = self.udks.trafficGenerationUdks.trafficPacketCreationKeywords.get_packet(
            rx_packet_name_a)
        rx_packet_b = self.udks.trafficGenerationUdks.trafficPacketCreationKeywords.get_packet(
            rx_packet_name_b)

        assert rx_packet_a and rx_packet_b, "You must define the packets to use this keyword"

        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(
            port_a, rx_packet_a.get_destination_mac(), rx_packet_a.get_source_mac(),
            rx_packet_a.get_destination_mac_mask(), rx_packet_a.get_source_mac_mask())
        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(
            port_b, rx_packet_b.get_destination_mac(), rx_packet_b.get_source_mac(),
            rx_packet_b.get_destination_mac_mask(), rx_packet_b.get_source_mac_mask())

        self.udks.trafficGenerationUdks.trafficTransmitKeywords.start_transmit_on_port(
            port_a, **kwargs)
        self.udks.trafficGenerationUdks.trafficTransmitKeywords.start_transmit_on_port_and_wait(
            port_b, **kwargs)

    def device360_display_traffic_transmitted_from_xiq_and_return_traffic_list(
        self, dut, first_port, second_port):
        """
         - This keyword will display the transmitted traffic from ports 1/1 and 1/24 visible in XIQ and returns a list with them
        :return: -1 if error
        """
        try:
            paginations = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
            assert paginations, "Failed to find the paginations for Device 360 tabular ports view"

            [pagination] = [pg for pg in paginations if pg.text == '10']
            time.sleep(5)
            AutoActions().click(pagination)
            time.sleep(3)

            if dut.cli_type.upper() == "VOSS":
                x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
                print("Displaying the traffic transmitted value for the first 10 entries in the table")
                for i in x:
                    traffic_received = i["TRAFFIC TRANSMITTED (TX)"]
                    port_name = i["PORT NAME"]
                    if port_name == first_port or port_name == second_port:
                        print(f"Found TRAFFIC TRANSMITTED (TX): {traffic_received} for port: {port_name}")
                time.sleep(5)

                [pagination] = [pg for pg in paginations if pg.text == '100']
                time.sleep(5)
                AutoActions().click(pagination)
                time.sleep(3)

                x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

                traffic_list_xiq = []

                print(" Displaying the traffic transmitted value for pagination 100")
                for i in x:
                    traffic_received = i["TRAFFIC TRANSMITTED (TX)"]
                    port_name = i["PORT NAME"]
                    if port_name == first_port or port_name == second_port:
                        print(f"TRAFFIC TRANSMITTED (TX): {traffic_received} for port: {port_name}")
                        traffic_list_xiq.append(traffic_received)
                time.sleep(5)

                return traffic_list_xiq

            elif dut.cli_type.upper() == "EXOS":
                x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

                print("Displaying the traffic transmitted value for the first 10 entries in the table")
                for i in x:
                    traffic_received = i["TRAFFIC TRANSMITTED (TX)"]
                    port_name = i["PORT NAME"]
                    if port_name == first_port or port_name == second_port:
                        print(f"Found TRAFFIC TRANSMITTED (TX): {traffic_received} for port: {port_name}")
                time.sleep(5)

                [pagination] = [pg for pg in paginations if pg.text == '100']
                time.sleep(5)
                AutoActions().click(pagination)
                time.sleep(3)

                x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

                traffic_list_xiq = []

                print(" Displaying the traffic transmitted value for pagination 100")
                for i in x:
                    traffic_received = i["TRAFFIC TRANSMITTED (TX)"]
                    port_name = i["PORT NAME"]
                    if port_name == first_port or port_name == second_port:
                        print(f"Found TRAFFIC TRANSMITTED (TX): {traffic_received} for port: {port_name}")
                        traffic_list_xiq.append(traffic_received)
                time.sleep(5)

                return traffic_list_xiq
        except Exception as e:
            return -1

    def get_transmitted_traffic_list_from_dut(
        self, dut, first_port, second_port):
        
        if dut.cli_type.upper() == "VOSS":
            time.sleep(10)

            self.devCmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
            output = self.devCmd.send_cmd(
                dut.name, f'show interfaces gigabitEthernet statistics {first_port},{second_port}', max_wait=10,
                interval=2)

            time.sleep(2)
            print(output[0].return_text)
            p = re.compile(r'(^\d+\/\d+)\s+(\d+)\s+(\d+)', re.M)
            match_port = re.findall(p, output[0].return_text)
            print(f"{match_port}")

            transmitted_traffic_list = []
            transmitted_traffic_list.append(match_port[0][2])
            transmitted_traffic_list.append(match_port[1][2])

            print(f"transmitted traffic for port {first_port} is {match_port[0][2]} octets")
            print(f"transmitted traffic for port {second_port} is {match_port[1][2]} octets")

            print("list from dut is ", transmitted_traffic_list)

        elif dut.cli_type.upper() == "EXOS":
            time.sleep(10)
            self.devCmd.send_cmd(dut.name, 'disable cli paging',
                                max_wait=10, interval=2)
            output = self.devCmd.send_cmd(dut.name, f'show port {first_port},{second_port} statistics no-refresh',
                                        max_wait=10, interval=2)
            print(output[0].return_text)
            p = re.compile(r'(^\d+)\s+(\D+)\s+(\d+)\s+(\d+)', re.M)
            match_port = re.findall(p, output[0].return_text)
            print(f"{match_port}")

            transmitted_traffic_list = []
            transmitted_traffic_list.append(match_port[0][3])
            transmitted_traffic_list.append(match_port[1][3])

            print(f"transmitted_traffic_list for port {first_port} is {match_port[0][3]} octets")
            print(f"transmitted_traffic_list for port {second_port} is {match_port[1][3]} octets")

        return transmitted_traffic_list

    def Transmit_Traffic_Bidirectionally_and_Verify_it_was_Received_tcxm_9567(
        self, port_a, port_b, tx_packet_name_a,tx_packet_name_b, rx_packet_name_a,
        rx_packet_name_b,tx_count=100, tx_rate=100, **kwargs):

        self.udks.trafficGenerationUdks.Configure_Packet_on_Port_Single_Burst(
            port_a, tx_packet_name_a, count=tx_count,rate=tx_rate, **kwargs)
        self.udks.trafficGenerationUdks.Configure_Packet_on_Port_Single_Burst(
            port_b, tx_packet_name_b, count=tx_count,rate=tx_rate, **kwargs)
        rx_packet_a = self.udks.trafficGenerationUdks.trafficPacketCreationKeywords.get_packet(
            rx_packet_name_a)
        rx_packet_b = self.udks.trafficGenerationUdks.trafficPacketCreationKeywords.get_packet(
            rx_packet_name_b)

        assert rx_packet_a and rx_packet_b, "You must define the packets to use this keyword"

        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(
            port_a, rx_packet_a.get_destination_mac(), rx_packet_a.get_source_mac(),
            rx_packet_a.get_destination_mac_mask(), rx_packet_a.get_source_mac_mask())
        
        self.udks.trafficGenerationUdks.Start_Capture_with_DMAC_and_SMAC_Filter(
            port_b, rx_packet_b.get_destination_mac(), rx_packet_b.get_source_mac(),
            rx_packet_b.get_destination_mac_mask(), rx_packet_b.get_source_mac_mask())

        self.udks.trafficGenerationUdks.trafficTransmitKeywords.start_transmit_on_port(
            port_a, **kwargs)
        self.udks.trafficGenerationUdks.trafficTransmitKeywords.start_transmit_on_port_and_wait(
            port_b, **kwargs)

    def device360_display_traffic_received_from_xiq_and_return_traffic_list(self, dut, first_port, second_port):
        """
         - This keyword will display the received traffic from ports 1/1 and 1/24 visible in XIQ and returns a list with them
        :return: -1 if error
        """
        try:
            paginations = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
            assert paginations, "Failed to find the paginations for Device 360 tabular ports view"

            [pagination] = [pg for pg in paginations if pg.text == '10']
            time.sleep(5)
            AutoActions().click(pagination)
            time.sleep(3)

            if dut.cli_type.upper() == "VOSS":
                x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()
                print("Displaying the traffic received value for the first 10 entries in the table")
                for i in x:
                    traffic_received = i["TRAFFIC RECEIVED (RX)"]
                    port_name = i["PORT NAME"]
                    if port_name == first_port or port_name == second_port:
                        print(f"Found TRAFFIC RECEIVED: {traffic_received} for port: {port_name}")
                time.sleep(5)

                [pagination] = [pg for pg in paginations if pg.text == '100']
                time.sleep(5)
                AutoActions().click(pagination)
                time.sleep(3)

                x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

                traffic_list_xiq = []

                print(" Displaying the traffic received value for pagination 100")
                for i in x:
                    traffic_received = i["TRAFFIC RECEIVED (RX)"]
                    port_name = i["PORT NAME"]
                    if port_name == first_port or port_name == second_port:
                        print(f"Found TRAFFIC RECEIVED: {traffic_received} for port: {port_name}")
                        traffic_list_xiq.append(traffic_received)
                time.sleep(5)

                return traffic_list_xiq
            elif dut.cli_type.upper() == "EXOS":
                x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

                print("x pentru exos 67 este: ", x)
                print("Displaying the traffic received value for the first 10 entries in the table")
                for i in x:
                    traffic_received = i["TRAFFIC RECEIVED (RX)"]
                    port_name = i["PORT NAME"]
                    if port_name == first_port or port_name == second_port:
                        print(f"Found TRAFFIC RECEIVED: {traffic_received} for port: {port_name}")
                time.sleep(5)

                [pagination] = [pg for pg in paginations if pg.text == '100']
                time.sleep(5)
                AutoActions().click(pagination)
                time.sleep(3)

                x = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table()

                traffic_list_xiq = []

                print(" Displaying the traffic received value for pagination 100")
                for i in x:
                    traffic_received = i["TRAFFIC RECEIVED (RX)"]
                    port_name = i["PORT NAME"]
                    if port_name == first_port or port_name == second_port:
                        print(f"Found TRAFFIC RECEIVED: {traffic_received} for port: {port_name}")
                        traffic_list_xiq.append(traffic_received)
                time.sleep(5)

                return traffic_list_xiq

        except Exception as e:
            return -1

    def get_received_traffic_list_from_dut(self, dut, first_port, second_port):

        if dut.cli_type.upper() == "VOSS":
            time.sleep(10)

            self.devCmd.send_cmd(dut.name, 'enable', max_wait=10, interval=2)
            output = self.devCmd.send_cmd(
                dut.name, f'show interfaces gigabitEthernet statistics {first_port},{second_port}', max_wait=10,
                interval=2)

            time.sleep(2)
            print(output[0].return_text)
            p = re.compile(r'(^\d+\/\d+)\s+(\d+)', re.M)
            match_port = re.findall(p, output[0].return_text)
            print(f"{match_port}")

            received_traffic_list = []
            received_traffic_list.append(match_port[0][1])
            received_traffic_list.append(match_port[1][1])

            print(f"received_traffic for port {first_port} is {match_port[0][1]} octets")
            print(f"received_traffic for port {second_port} is {match_port[1][1]} octets")

        elif dut.cli_type.upper() == "EXOS":
            time.sleep(10)
            self.devCmd.send_cmd(dut.name, 'disable cli paging',
                                max_wait=10, interval=2)
            output = self.devCmd.send_cmd(dut.name, f'show port {first_port},{second_port} statistics no-refresh',
                                            max_wait=10,
                                            interval=2)
            print(output[0].return_text)
            p = re.compile(r'(^\d+)\s+(\D+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)', re.M)
            match_port = re.findall(p, output[0].return_text)
            print(f"{match_port}")

            received_traffic_list = []
            received_traffic_list.append(match_port[0][5])
            received_traffic_list.append(match_port[1][5])

            print(f"received_traffic for port {first_port} is {match_port[0][5]} octets")
            print(f"received_traffic for port {second_port} is {match_port[1][5]} octets")

        return received_traffic_list

    def generate_port_type_name(self):
        return f"port_type_{str(time.time())[::-1][:5]}"

    def generate_policy_name(self):
        return f"test_policy_{str(time.time())[::-1][:5]}"

    def generate_template_name(self):
        return f"template_{str(time.time())[::-1][:5]}"

    def assign_policy(self, policy_name, dut):
    
        time.sleep(10)
        self.setup_cls_obj.xiq.xflowscommonDevices._goto_devices()
        time.sleep(10)

        self.utils.print_info(f"Select switch row with serial {dut.mac}")
        if not self.devices.select_device(device_mac=dut.mac):
            self.utils.print_info(f"Switch {dut.mac} is not present in the grid")
            return -1
        time.sleep(2)

        self.utils.print_info("Click on actions button")
        self.auto_actions.click(self.devices.devices_web_elements.get_manage_device_actions_button())
        time.sleep(3)

        self.utils.print_info("Click on Assign Network policy action for selected switch")
        self.auto_actions.click(self.devices.devices_web_elements.get_actions_assign_network_policy_combo_switch())
        time.sleep(4)

        self.utils.print_info("Click on network policy drop down")
        try:
            drop_down_button = self.devices.devices_web_elements.get_actions_assign_network_policy_drop_down()
            drop_down_button.click()
        except selenium.common.exceptions.ElementNotInteractableException as exc:
            self.utils.print_warning(repr(exc))
            [drop_down_button] = [btn for btn in self.devices.devices_web_elements.weh.get_elements(
                {"XPATH": '//tbody[@role="presentation"]'}) if btn.text == '--Select--']

            self.auto_actions.click(drop_down_button)
            time.sleep(5)

        network_policy_items = self.devices.devices_web_elements.get_actions_network_policy_drop_down_items()
        time.sleep(2)

        if self.auto_actions.select_drop_down_options(network_policy_items, policy_name):
            self.utils.print_info(f"Selected Network policy from drop down:{policy_name}")
        else:
            self.utils.print_info("Network policy is not present in drop down")
            return False

        time.sleep(5)

        self.utils.print_info("Click on network policy assign button")
        self.auto_actions.click(self.devices.devices_web_elements.get_actions_network_policy_assign_button())
        time.sleep(10)
        return True

    def update_and_wait_switch(self, policy_name, dut):
    
        time.sleep(10)
        self.setup_cls_obj.xiq.xflowscommonDevices._goto_devices()
        time.sleep(10)
        
        self.utils.print_info(f"Select switch row with serial {dut.mac}")
        if not self.devices.select_device(device_mac=dut.mac):
            self.utils.print_info(f"Switch {dut.mac} is not present in the grid")
            return -1
        time.sleep(2)
        self.devices._update_switch(update_method="PolicyAndConfig")
        return self.devices._check_update_network_policy_status(policy_name, dut.serial)

    def get_connected_ports(self, dut):
    
        try:
            time.sleep(8)
            self.dev360.navigator.navigate_to_device360_page_with_mac(dut.mac)
            time.sleep(8)

            self.auto_actions.click(self.dev360.get_d360_switch_port_view_all_pages_button())
            time.sleep(4)

            rows = self.dev360.get_d360_switch_ports_table_grid_rows()[1:]
            connected_ports = []

            for row in rows:
                try:
                    port_name = row.text.split(" ")[0]
                    if (not "Disconnected" in row.text) and port_name != "mgmt":
                        connected_ports.append(port_name)
                except:
                    pass
            return connected_ports
        finally:
            self.dev360.exit_d360_Page()

    def go_to_device360(self, dut):
        time.sleep(5)
        self.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
        time.sleep(5)

    def create_network_policy(self, policy_name):
        assert self.setup_cls_obj.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(
            policy_name=policy_name) == 1, f"Failed to create this network policy: {policy_name}"
        time.sleep(5)

    def revert_port_configuration(self, port, port_type_name="", retries=5):
    
        for _ in range(retries):
            try:
                rows = self.dev360.get_device360_configure_port_rows()
                for row in rows:
                    if re.search(rf"{port}\n{port_type_name}", row.text):
                        port_row = row
                        break
                else:
                    raise AssertionError("Failed to get the port row")

                port_row.location_once_scrolled_into_view
                self.utils.print_info("Found row for port: ", port_row.text)
                time.sleep(3)
                port_override_revert = self.dev360.get_d360_configure_port_row_override_revert(port_row)
                time.sleep(3)

                if port_override_revert:
                    self.utils.print_info("move on 'override' button ")
                    try:
                        self.auto_actions.move_to_element(port_override_revert)
                    except Exception as exc:
                        self.utils.print_debug(repr(exc))
                        port_override_revert = self.dev360.dev360.weh.get_elements(
                            {"XPATH": "//div[@class='override-revert-container']//span[@class='override-revert']"},
                            parent=port_row)[0]
                        self.auto_actions.move_to_element(port_override_revert)
                    time.sleep(5)

                    port_revert = self.dev360.get_d360_configure_port_row_revert_button(port_row)
                    if not port_revert:
                        port_revert = self.dev360.dev360.weh.get_element(
                            {"XPATH": "//button[@data-dojo-attach-point='revertButton']"})

                    if port_revert:
                        self.utils.print_info("Clicking 'Revert' button")
                        self.auto_actions.click(port_revert)
                        time.sleep(5)
                        break
                    else:
                        raise AssertionError("Could not click Revert button")
                else:
                    raise AssertionError("The override revert button was not found")
            except Exception as exc:
                self.utils.print_info(repr(exc))
                time.sleep(30)
        else:
            raise AssertionError("Failed to revert to default port config")

    def change_device_management_settings(self, option, retries=5, step=20):
    
        for _ in range(retries):
            try:
                self.setup_cls_obj.xiq.xflowsglobalsettingsGlobalSetting.change_device_management_settings(option=option)
            except Exception as exc:
                self.utils.print_info(repr(exc))
                time.sleep(step)
            else:
                break
        else:
            assert False, "Failed to change device management settings"

    def generate_template_for_given_model(self, platform, model, slots=""):
    
        if (platform.lower() == 'stack'):
            if not slots:
                self.utils.print_error("Provide information of Slots..")
                return -1

            model_list = []
            sw_model = ""
            model_units=None

            for eachslot in slots:
                if "SwitchEngine" in eachslot:
                    mat = re.match('(.*)(Engine)(.*)', eachslot)
                    model_md = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_', '-')
                    switch_type=re.match('(\d+).*',mat.group(3).split('_')[0]).group(1)
                    sw_model = 'Switch Engine ' + switch_type + '-Series-Stack'

                else:
                    model_act = eachslot.replace('10_G4', '10G4')
                    m = re.match(r'(X\d+)(G2)(.*)', model_act)
                    model_md = m.group(1) + '-' + m.group(2) + m.group(3).replace('_', '-')
                    sw_model = m.group(1) + '-' + m.group(2) + '-Series-Stack'
                model_list.append(model_md)

            model_units = ','.join(model_list)
            return sw_model,model_units

        elif "Engine" in model:
            mat = re.match('(.*)(Engine)(.*)', model)
            sw_model = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_', '-')

        elif "G2" in model:
            model_act = model.replace('10_G4', '10G4')
            m = re.match(r'(X\d+)(G2)(.*)', model_act)
            sw_model = m.group(1) + '-' + m.group(2) + m.group(3).replace('_', '-')

        else:
            sw_model = model.replace('_', '-')
        return sw_model

    def go_to_device_360_port_config(self, dut):
    
        time.sleep(10)
        self.setup_cls_obj.xiq.xflowscommonDevices._goto_devices()
        time.sleep(10)

        time.sleep(15)
        self.setup_cls_obj.xiq.xflowscommonDeviceCommon.go_to_device360_window(device_mac=dut.mac)
        time.sleep(5)
        self.setup_cls_obj.xiq.xflowscommonNavigator.navigate_to_port_configuration_d360()

    def get_no_of_ports(self, onboarded_switch):
        try:
            self.close_connection_with_error_handling(onboarded_switch)
            self.network_manager.connect_to_network_element_name(onboarded_switch.name)
            
            _port = 0
            
            if onboarded_switch.cli_type.upper() == "VOSS":
                self.devCmd.send_cmd(onboarded_switch.name, f'enable',
                                    max_wait=10)
                output = self.devCmd.send_cmd(onboarded_switch.name, f'show sys-info | include NumPorts',
                                    max_wait=10)
                output = output[0].return_text
                match_port = re.search(r"(NumPorts +): (\d+)", output)
                _port = match_port.group(2)
                _port = int(_port)
                
            elif onboarded_switch.cli_type.upper() == "EXOS":
                
                self.devCmd.send_cmd(onboarded_switch.name, f'disable cli paging',
                                    max_wait=10)
                output = self.devCmd.send_cmd(onboarded_switch.name, f'show ports vlan',
                                    max_wait=10)
                output = output[0].return_text
                match_port = re.findall(r"(\d+)\s+\w+",output)
                _port = len(match_port)
                _port = int(_port)
                
            return _port
        finally:
            self.close_connection_with_error_handling(onboarded_switch)

    def enter_port_type_and_vlan_id(
            self, port, port_type=None, access_vlan_id=None, native_vlan=None, allowed_vlans=None):
        time.sleep(8)
        port_row = self.dev360.device360_get_port_row(port)
        if port_row:
            self.utils.print_debug("Found row for port: ", port_row.text)

            if port_type:
                self.utils.print_info("click Port Usage drop down")
                self.auto_actions.click(self.dev360.get_device360_configure_port_usage_drop_down_button(port_row))
                time.sleep(2)

                self.utils.print_info("Selecting Port Usage")
                dropdown_options = self.dev360.get_device360_configure_port_usage_drop_down_options(port_row)
                if not dropdown_options:
                    dropdown_options = self.dev360.weh.get_elements(
                        {"XPATH": f"//li[contains(@data-automation-tag, 'automation-port-details-port-dropdown-{port}-chzn-option')]"})

                self.auto_actions.select_drop_down_options(dropdown_options, port_type)
                time.sleep(2)

            if access_vlan_id:
                self.utils.print_info("Deleting the selected values in port..")
                input_field_access_vlan_id = self.dev360.get_device360_configure_port_access_vlan_textfield(port_row)
                if not input_field_access_vlan_id:
                    input_field_access_vlan_id = self.dev360.weh.get_element(
                        {"XPATH": f".//input[contains(@data-automation-tag, 'automation-port-details-port-access-vlan')]"}, parent=port_row)

                self.auto_actions.send_keys(input_field_access_vlan_id, Keys.BACK_SPACE * 10 + access_vlan_id + Keys.ENTER)
                time.sleep(2)

            if native_vlan:

                self.utils.print_info("Deleting the selected values in port..")
                input_field_trunk_native = self.dev360.get_device360_configure_port_trunk_native_vlan_textfield(port_row)
                if not input_field_trunk_native:
                    input_field_trunk_native = self.dev360.weh.get_element(
                        {"XPATH": f".//input[contains(@data-automation-tag, 'automation-port-details-port-trunk-native-vlan')]"}, parent=port_row)

                self.auto_actions.send_keys(input_field_trunk_native, Keys.BACK_SPACE * 10 + native_vlan + Keys.ENTER)
                time.sleep(2)

            if allowed_vlans:
                input_field_allowed_vlans = self.dev360.get_device360_configure_port_trunk_vlan_textfield(port_row)
                if not input_field_allowed_vlans:
                    input_field_allowed_vlans = self.dev360.weh.get_element(
                        {"XPATH": f".//input[contains(@data-automation-tag, 'automation-port-details-port-trunk-allowed-vlan')]"}, parent=port_row)

                self.auto_actions.send_keys(input_field_allowed_vlans, Keys.BACK_SPACE * 10 + allowed_vlans + Keys.ENTER)

            time.sleep(8)

    def save_device_360_port_config(self):
        time.sleep(5)
        save_btn = self.dev360.get_device360_configure_port_save_button()
        if not save_btn:
            save_btn = self.dev360.weh.get_element(
                {"XPATH": "//button[@data-automation-tag='automation-port-config-save']"})
        assert save_btn, "Failed to get the save button of device 360"
        self.auto_actions.click(save_btn)
        time.sleep(20)

    def generate_vlan_id(self, rng=range(1024, 4096)):
        return str(random.choice(rng))

    def enter_port_transmission_mode(self, port, transmission_mode):

        time.sleep(10)
        configure_port_btn = self.dev360.get_d360_configure_port_settings_aggregation_tab_button()
        if not configure_port_btn:
            configure_port_btn = self.dev360.weh.get_element({"XPATH": '//div[@data-automation-tag="automation-port-configuration-port-settings"]'})
        assert configure_port_btn, "Could not find element port configuration button"
        self.utils.print_info("Click Port Settings Tab")
        self.auto_actions.click(configure_port_btn)
        time.sleep(3)

        rows = self.dev360.get_device360_configure_port_settings_aggregation_rows()
        if not rows:
            rows = self.dev360.weh.get_elements({"XPATH": '//div[@class="port-details-entry line clearfix"]'})
        assert rows, "Could not get the port settings aggregation rows"

        for port_row in rows:
            if re.search(f"{port}\n", port_row.text):
                self.utils.print_debug("Found row for port: ", port_row.text)
                break
        else:
            assert False, f"Failed to find the row for port {port}"

        self.utils.print_info("clicking Transmission Mode drop down Button")
        drop_down_button = self.dev360.get_device360_port_settings_transmission_mode_drop_down_button(port_row)
        if self.auto_actions.click(drop_down_button) in [None, -1]:
            drop_down_button = self.dev360.weh.get_element({
                "XPATH": ".//div[@data-automation-tag='automation-automation-port-settings-port-transmission-type-chzn-container-ctn']"
            }, parent=port_row)
            assert self.auto_actions.click(drop_down_button) == 1, f"Failed to open transmission type drop down"

        time.sleep(2)

        drop_down_options = self.dev360.get_device360_port_settings_transmission_mode_drop_down_options(port_row)
        if not drop_down_options:
            drop_down_options = self.dev360.weh.get_elements({
                "XPATH": './/li[contains(@data-automation-tag, "automation-automation-port-settings-port-transmission-type-chzn-option")]'
            })
        assert drop_down_options
        drop_down_options = [opt for opt in drop_down_options if opt.text]
        self.utils.print_info(f"Selecting Transmission Mode Option : {transmission_mode}")
        self.auto_actions.select_drop_down_options(drop_down_options, transmission_mode)
        time.sleep(2)

    def check_power_values(self, ports_power_xiq, ports_power_cli):
        results = []
        for port_xiq, port_cli in zip(ports_power_xiq, ports_power_cli):
            if port_xiq[0] == port_cli[0]:
                if port_xiq[1] == "N/A":
                    if port_xiq[1] == port_cli[1]:
                        results.append(["Port: " + port_xiq[0], "PASSED"])
                    else:
                        results.append(["Port: " + port_xiq[0], "FAILED"])
                else:
                    if float(port_xiq[1]) == (float(port_cli[1])*1000):
                        results.append(["Port: " + port_xiq[0], "PASSED"])
                    else:
                        results.append(["Port: " + port_xiq[0], "FAILED"])
            else:
                return -1
        return results

    def no_channel_enable_on_all_ports(self, onboarded_switch):
        output = self.devCmd.send_cmd(onboarded_switch.name, f'show interface GigabitEthernet channelize',
                                      max_wait=10,
                                      interval=2)[0].return_text
        match_port = re.findall(r"(\d+)\/(\d+)\s+(false|true)\s+[a-zA-Z0-9]+", output)

        for port in match_port:
            if port[2] == "true":
                command = "interface GigabitEthernet " + port[0] + "/" + port[1] + "/1"
                self.devCmd.send_cmd(onboarded_switch.name, command)
                self.devCmd.send_cmd(onboarded_switch.name, 'no channelize enable',
                                     confirmation_phrases='Do you wish to continue (y/n) ?',
                                     confirmation_args='y')

    def get_device360_port_table_rows(self):
        table_rows = self.xiq.xflowsmanageDevice360.dev360.get_device360_port_table_rows()
        assert table_rows, "Did not find the rows of the ports table"
        table_rows[0].location_once_scrolled_into_view
        return [
            row for row in table_rows if not 
            any(field in row.text for field in ["PORT NAME", "LLDP NEIGHBOR", "PORT STATUS"])
        ]

    def select_max_pagination_size(self):
        try:
            time.sleep(2)
            pagination_size = max(self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes(),
                                key=lambda x: int(x.text))
            pagination_size.location_once_scrolled_into_view
            self.auto_actions.click(pagination_size)
            print(f"Selected the max pagination size: {pagination_size.text}")
            time.sleep(5)
            return 1
        except Exception as exc:
            print(repr(exc))
            return -1

    def select_pagination_size(self, int_size):
        try:
            time.sleep(2)
            paginations = self.xiq.xflowsmanageDevice360.dev360.get_device360_ports_table_pagination_sizes()
            [pg_size] = [pg for pg in paginations if pg.text == int_size]
            self.auto_actions.click(pg_size)
            time.sleep(5)
            return 1
        except Exception as exc:
            print(repr(exc))
            return -1

    def verify_vlan_config_on_switch(self, onboarded_switch, port_vlan_mapping, logger):
        try:
            self.close_connection_with_error_handling(onboarded_switch)
            self.network_manager.connect_to_network_element_name(onboarded_switch.name)

            logger.info("Wait 120 seconds for the configuration of the ports to update on the dut")
            start_time = time.time()
            while time.time() - start_time < 120:
                
                if onboarded_switch.cli_type.upper() == "EXOS":
                    try:
                        for port, vlan in port_vlan_mapping.items():
                            output = self.devCmd.send_cmd(onboarded_switch.name, f'show vlan ports {port}',
                                                            max_wait=10, interval=2)[0].return_text
                            assert re.search(fr"\r\nVLAN_{str(vlan).zfill(4)}\s+{vlan}\s+", output)
                    except Exception as exc:
                        logger.info(f"Sleep 10s...\n{repr(exc)}")
                        time.sleep(10)
                    else:
                        logger.info("Configuration successfully updated on the dut")
                        break
                    
                elif onboarded_switch.cli_type.upper() == "VOSS":
                    try:
                        output = self.devCmd.send_cmd(onboarded_switch.name, 'show vlan members',
                                                        max_wait=10, interval=2)[0].return_text

                        for port, vlan in port_vlan_mapping.items():
                            assert re.search(fr"\r\n{vlan}\s+{port}\s+", output)

                    except Exception as exc:
                        logger.info(f"Sleep 10s...\n{repr(exc)}")
                        time.sleep(10)
                    else:
                        logger.info("Configuration successfully updated on the dut")
                        break
            else:
                raise AssertionError("The configuration did not update on the dut after 120 seconds")
        finally:
            self.close_connection_with_error_handling(onboarded_switch)

    def clear_counters(self, dut, first_port=None, second_port=None):
        if dut.cli_type.upper() == "EXOS":
            self.devCmd.send_cmd(
                self.tb.dut1.name, "clear counters ports all", max_wait=10, interval=2)
        elif dut.cli_type.upper() == "VOSS":
            self.devCmd.send_cmd(
                self.tb.dut1.name, f"clear-stats port {first_port},{second_port}", max_wait=10, interval=2)
