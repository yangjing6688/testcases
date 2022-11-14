# Author        : Aldea Bogdan, Scaunasu Arina
# Description   : These tests were created for XIQ-921- Support Honeycomb Port Editor for EXOS(Single/Stack)/VOSS.
# Testcases     : TCXM-18417, TCXM-18419, TCXM-18420, TCXM-18422, TCXM-18423, TCXM-18425, TCXM-18426, TCXM-18428,
#                 TCXM-18429, TCXM-18431, TCXM-18432, TCXM-18434, TCXM-18440, TCXM-18473, TCXM-18475, TCXM-18476,
#                 TCXM-18478, TCXM-18479, TCXM-18481, TCXM-18482, TCXM-18484, TCXM-18485, TCXM-18487, TCXM-18488,
#                 TCXM-18490, TCXM-18561, TCXM-18493, TCXM-18494, TCXM-18496, TCXM-18497, TCXM-18499, TCXM-18500,
#                 TCXM-18502, TCXM-18503, TCXM-18505, TCXM-18506, TCXM-18508
# Comments      : These tests are applicable for FabricEngine, SwitchEngine and Stack.

from pytest_testconfig import config, load_yaml
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords import NetworkElementConnectionManager
from ExtremeAutomation.Keywords.NetworkElementKeywords.Utils import NetworkElementCliSend

from pytest import mark
from pytest import fixture
import pytest
import os
import os.path
import re
import sys
import time
import random
from pprint import pprint
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.XiqLibraryHelper import XiqLibraryHelper
import string


def random_word(x=12):
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(x))
    return randword


location = "Location_" + random_word()
building = "Building_" + random_word()
floor = "Floor_" + random_word()
sw_template_name_original = "Template_" + random_word()
network_policy_name = 'Policy_' + random_word()
stack_template_name_original = sw_template_name_original

# Fail Flags
setup_onboard_fail_flag = 0
setup_stack_fail_come_online = 0
setup_xiq_connect_fail = 0

@mark.testbed_1_node
class xiqTests():

    def get_virtual_router(self, dut_name):
        global vr_name, slot, port, dut_vlan_name
        if self.tb.dut1_make.upper() == "EXOS":
            cmd = 'show vlan | grep ' + self.tb.dut1.ip
            output = self.devCmd.send_cmd(dut_name, cmd, max_wait=10, interval=2)
            output_text = output[0].cmd_obj.return_text
            out_txt = output_text.strip()
            out_lst = out_txt.split()
            dut_vlan_name = out_lst[0]
            vr_name = out_lst[8]
            if vr_name == "VR-Default":
                cmd = 'show vlan ' + dut_vlan_name
                output = self.devCmd.send_cmd(dut_name, cmd, max_wait=10, interval=2)
                output_text = output[0].cmd_obj.return_text
                out_lst = output_text.split('\r\n')
                out_str = ''.join(out_lst)
                if self.tb.dut1_platform.lower() == 'stack':
                    slot = re.match(r'.*Untag:\s+\*(\d):(\d+)', out_str).group(1)
                    port = re.match(r'.*Untag:\s+\*(\d):(\d+)', out_str).group(2)
                else:
                    port = re.match(r'.*Untag:\s+\*(\d)', out_str).group(1)
        else:
            vr_name = 'None'

    def create_network_policy_local(self, network_policy_name):

        def _check_nw_policy_creation():
            try:
                self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(network_policy_name)
                return True
            except Exception as e:
                print(f"Got the error: {e} ; Retrying...")
                return False

        self.xiq.Utils.wait_till(_check_nw_policy_creation, timeout=30, delay=10)

        def _check_nw_policy_assignation():
            try:
                self.xiq.xflowscommonNavigator.navigate_to_devices()
                self.xiq.xflowsmanageDevices.assign_network_policy_to_switch_mac(network_policy_name, self.tb.dut1.mac)
                return True
            except Exception as e:
                print(f"Got the error: {e} ; Retrying...")
                return False

        self.xiq.Utils.wait_till(_check_nw_policy_assignation, timeout=30, delay=10)

    def init_xiq_libaries_and_login(self, username, password, url="default"):
        self.xiq = XiqLibrary()
        res = self.xiq.login.login_user(username, password, url=url)
        if res != 1:
            pytest.fail('Could not Login')

    def deactivate_xiq_libaries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None

    def delete_create_location_organization(self):
        self.xiq.xflowsmanageLocation.create_first_organization("Extreme", "broadway", "newyork", "Romania")
        self.xiq.xflowsmanageLocation.delete_location_building_floor(location, building, floor)
        self.xiq.xflowsmanageLocation.create_location_building_floor(location, building, floor)

    def delete_device_local(self, mac):
        # Check if device is onboarded and delete it.
        nav = self.xiq.xflowscommonNavigator.navigate_to_devices()
        # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
        time.sleep(10)
        if nav == -1:
            pytest.fail("Could not navigate to devices.")
        check_delete = self.xiq.xflowscommonDevices.delete_device(device_mac=mac)

        if check_delete != 1:
            pytest.fail("Could not delete the device.")

    def verify_poe_supported(self, dut_name, os):
        check_poe = False
        if os.lower() == "voss":
            self.devCmd.send_cmd(dut_name, 'enable', max_wait=30, interval=10)
            self.devCmd.send_cmd(dut_name, 'configure terminal', max_wait=30, interval=10)
            print("Trying to see if device supoorts POE")
            result = self.devCmd.send_cmd(dut_name, 'show poe-main-status', max_wait=30, interval=10)[0].cmd_obj._return_text
            print(f"Result was: {result}")
            if "PoE Main Status" in result:
                check_poe = True
            elif "Device is not a POE device" in result:
                pytest.skip("Device does not support POE!")
        elif os.lower() == 'exos' and self.tb.dut1.platform.lower() == 'stack':
            self.devCmd.send_cmd(self.tb.dut1.name, 'enable telnet')
            self.devCmd.send_cmd(self.tb.dut1.name, 'disable cli paging')
            print("Trying to see if device supoorts POE")
            try:
                result = self.devCmd.send_cmd(dut_name, 'show inline-power | begin Slot', max_wait=30, interval=10)[0].cmd_obj._return_text
            except Exception:
                pytest.skip("Device does not support PoE!")
            print(f"Result was: {result}")
            if 'Operational' in result:
                print("EXOS stack device supports PoE")
                check_poe = True
            else:
                pytest.skip("Stack does not support PoE!")
        elif os.lower() == "exos":
            self.devCmd.send_cmd(self.tb.dut1.name, 'enable telnet')
            self.devCmd.send_cmd(self.tb.dut1.name, 'disable cli paging')
            print("Trying to see if device supoorts POE")
            try:
                result = self.devCmd.send_cmd(dut_name, 'show inline-power', max_wait=30, interval=10)[0].cmd_obj._return_text
            except Exception:
                pytest.skip("Device does not support PoE!")
            print(f"Result was: {result}")
            if 'Inline Power System Information' in result:
                print("EXOS device supports PoE")
                check_poe = True
            else:
                pytest.skip("Device does not support PoE!")
        else:
            pytest.skip("Device is neither VOSS, nor EXOS!")
        return check_poe

    def get_random_name(self, base_string):
        random_value = base_string + "_" + random_word(x=6)
        return random_value

    def get_delete_port_type(self, port_type_name):
        self.xiq.xflowsconfigureCommonObjects.delete_port_type_profile(port_type_name)

    def check_ports_existence(self, check_port_voss, check_port_exos, os):
        if os == "voss":
            system_type_regex = "(\\d+/\\d+)\\s+\\w+"
            output = self.devCmd.send_cmd(self.tb.dut1.name, 'show ports vlan')[0].cmd_obj._return_text
            all_ports = self.xiq.Utils.get_regexp_matches(output, system_type_regex, 1)
            print("Found the ports: ", all_ports)
            for elem in all_ports:
                if check_port_voss == elem:
                    return elem
            if len(all_ports) > 3:
                return all_ports[1]
            else:
                return '1/2'
        if os == "exos":
            system_type_regex = "(\\d+)\\s+\\w+"
            output = self.devCmd.send_cmd(self.tb.dut1.name, 'show ports vlan')[0].cmd_obj._return_text
            all_ports = self.xiq.Utils.get_regexp_matches(output, system_type_regex, 1)
            print("Found the ports: ", all_ports)
            for elem in all_ports:
                if check_port_exos == elem:
                    flag_port_found = True
                    if self.tb.dut1.platform.lower() == 'stack':
                        return '1:' + elem
                    return elem
            if len(all_ports) > 3:
                return all_ports[1]
            else:
                if self.tb.dut1.platform.lower() == 'stack':
                    return '1:2'
                return '2'

    def get_sw_model(self):
        self.xiq.xflowscommonDevices.column_picker_select('Model')
        sw_model = self.xiq.xflowsmanageDevices.get_device_model(self.tb.dut1.mac)
        if not sw_model:
            pytest.fail("Fail on getting the device's model")
        return sw_model

    def create_device_template(self, policy_name, sw_template_model, sw_template_name):
        check_nav = self.xiq.xflowscommonNavigator.navigate_to_network_policies_list_view_page()
        if check_nav:
            check_config = self.xiq.xflowsconfigureSwitchTemplate.add_sw_template(policy_name,
                                                                                  sw_template_model,
                                                                                  sw_template_name)
            if check_config != 1:
                pytest.fail("Could not create device model in policy.")
        else:
            pytest.fail("Could not navigate to network Policy tab.")

    def create_stack_template(self, mac, generic_name):
        print("creating the model for stack.")
        time.sleep(10)
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        time.sleep(10)
        check_stack_template = self.xiq.xflowscommonDevices.create_stack_auto_template(device_mac=mac,
                                                                                       name_stack_template=generic_name)
        time.sleep(10)
        self.xiq.xflowsconfigureSwitchTemplate.save_stack_template(generic_name)

    def delete_port_type_local(self, delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name):
        self.xiq.xflowsmanageDevice360.close_device360_window()
        if self.tb.dut1.cli_type.lower() == 'voss' and delete_port_type:
            self.get_delete_port_type(port_type_voss_auto_sense_off_name)
        elif self.tb.dut1.cli_type.lower() == 'exos' and delete_port_type:
            self.get_delete_port_type(port_type_exos_name)

    def configure_access_port_local(self, voss_port, exos_port, vlan_id=1):
        if self.tb.dut1.cli_type.lower() == 'voss':
            if not self.xiq.xflowsmanageDevice360.device360_configure_port_access_vlan(
                    device_mac=self.tb.dut1.mac, port_number=voss_port, access_vlan_id=vlan_id) == 1:
                pytest.fail("port access was not configured")
        if self.tb.dut1.cli_type.lower() == 'exos':
            if not self.xiq.xflowsmanageDevice360.device360_configure_port_access_vlan(
                    device_mac=self.tb.dut1.mac, port_number=exos_port, access_vlan_id=vlan_id) == 1:
                pytest.fail("port access was not configured")

    def save_port_conf_local(self):
        if not self.xiq.xflowsmanageDevice360.d360_save_port_configuration() == 1:
            pytest.fail("Fail on navigating to Port Config")
        if not self.xiq.xflowsmanageDevice360.d360_cancel_port_configuration() == 1:
            pytest.fail("Fail on navigating to Port Config")

    def configure_port_type_local(self, template_voss_auto_sense_off, template_exos, voss_port, exos_port,
                                  policy_name=None, device_name=None, d360=True):
        delete_port_type = False
        create_new_port_type_and_check_summary = -1
        time.sleep(10)
        if d360:
            if not self.xiq.xflowscommonNavigator.navigate_to_devices() == 1:
                pytest.fail("Fail on navigating to devices")

            self.xiq.xflowsmanageDevices.refresh_devices_page()
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)

            if not self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(self.tb.dut1.mac) == 1:
                pytest.fail("Fail on navigating to D360 view with MAC")
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            if not self.xiq.xflowscommonNavigator.navigate_to_port_configuration_d360() == 1:
                pytest.fail("Fail on navigating to Port Config")
            time.sleep(10)
            if self.tb.dut1.cli_type.lower() == 'voss':
                create_new_port_type_and_check_summary = self.xiq.xflowsmanageDevice360.create_new_port_type(
                    template_voss_auto_sense_off, voss_port, d360=d360)

            elif self.tb.dut1.cli_type.lower() == 'exos':
                if self.tb.dut1.platform.lower() == 'stack':
                    self.xiq.xflowsmanageDevice360.select_stack_unit(1)
                time.sleep(10)
                create_new_port_type_and_check_summary = self.xiq.xflowsmanageDevice360.create_new_port_type(
                    template_exos, exos_port, d360=d360)

            if not create_new_port_type_and_check_summary == 1:
                print("Result is: ", create_new_port_type_and_check_summary)
                pytest.fail("Fail on Creating Port Type template")
            else:
                print("Result is: ", create_new_port_type_and_check_summary)
                print("Port Type template was created on device.")
                delete_port_type = True

        else:
            print("***Selecting SW template ", device_name)
            time.sleep(10)
            select_template = self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(policy_name, device_name)
            if select_template != 1:
                pytest.fail("Could not select switch template ", device_name)

            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            time.sleep(10)
            if self.tb.dut1.cli_type.lower() == 'voss':
                create_new_port_type_and_check_summary = self.xiq.xflowsmanageDevice360.create_new_port_type(
                    template_voss_auto_sense_off, voss_port.split('/')[1], d360=d360)
            elif self.tb.dut1.cli_type.lower() == 'exos':
                create_new_port_type_and_check_summary = self.xiq.xflowsmanageDevice360.create_new_port_type(
                    template_exos, exos_port, d360=d360)

            if not create_new_port_type_and_check_summary == 1:
                print("Result is: ", create_new_port_type_and_check_summary)
                pytest.fail("Fail on Creating Port Type template")
            else:
                print("Result is: ", create_new_port_type_and_check_summary)
                print("Port Type template was created on device.")
                delete_port_type = True

        return delete_port_type

    def edit_port_type_local(self, policy_name, device_name, template_voss, template_exos, voss_port, exos_port):
        delete_port_type = False
        create_new_port_type_and_check_summary = -1
        # Edit Port Type and check summary
        time.sleep(10)
        if self.tb.dut1.cli_type.lower() == 'voss':
            create_new_port_type_and_check_summary = self.xiq.xflowsmanageDevice360.edit_port_type(template_voss,
                                                                                                   voss_port)
        elif self.tb.dut1.cli_type.lower() == 'exos':
            create_new_port_type_and_check_summary = self.xiq.xflowsmanageDevice360.edit_port_type(template_exos,
                                                                                                   exos_port)
        time.sleep(10)
        if not create_new_port_type_and_check_summary == 1:
            print("Result is: ", create_new_port_type_and_check_summary)
            pytest.fail("Fail on Editing Port Type template")
        else:
            print("Result is: ", create_new_port_type_and_check_summary)
            print("Port Type template was created on device.")
            delete_port_type = True
        return delete_port_type

    def onboard_local(self, mac, os, ip, port, username, password):
        # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
        time.sleep(10)
        self.delete_device_local(self, mac=mac)
        dut_location = f'{location},{building},{floor}'

        ##Onboard device on cloud
        self.get_virtual_router(self, self.tb.dut1.name)

        if 'exos' in self.tb.dut1.cli_type.lower():
            self.devCmd.send_cmd(self.tb.dut1.name, 'configure iq server ipaddress none')
            self.devCmd.send_cmd(self.tb.dut1.name, 'enable iqagent')
        elif 'voss' in self.tb.dut1.cli_type.lower():
            self.devCmd.send_cmd(self.tb.dut1.name, 'enable')
            self.devCmd.send_cmd(self.tb.dut1.name, 'configure terminal')
            self.devCmd.send_cmd(self.tb.dut1.name, 'application')
            self.devCmd.send_cmd(self.tb.dut1.name, 'no iq enable')
            self.devCmd.send_cmd(self.tb.dut1.name, 'iq server none')
            self.devCmd.send_cmd(self.tb.dut1.name, 'iq en')

        if self.xiq.xflowscommonDevices.onboard_device_quick(self.tb.dut1) != 1:
            setup_onboard_fail_flag = 1
            pytest.fail("Failed to onboard the device. Cleaning up...")
        self.xiq.xflowscommonDevices.check_100_rows_per_page_button()
        # spawn_connection = cls.xiq.Cli.open_spawn(cls.tb.dut1.ip, cls.tb.dut1.port, cls.tb.dut1.username,
        #                                           cls.tb.dut1.password, cls.tb.dut1.cli_type)
        # cls.xiq.Cli.configure_device_to_connect_to_cloud(cls.tb.dut1.cli_type, cls.cfg['sw_connection_host'],
        #                                                  spawn_connection, vr='VR-Default', retry_count=30)
        # cls.xiq.Cli.close_spawn(spawn_connection)
        spawn_connection = self.xiq.Cli.open_spawn(ip, port, username, password, os)
        if self.xiq.Cli.configure_device_to_connect_to_cloud(os, self.cfg['sw_connection_host'], spawn_connection,
                                                             vr=vr_name, retry_count=30) != 1:
            setup_xiq_connect_fail = 1
            pytest.fail("Device failed to connect to cloud")
        self.xiq.Cli.close_spawn(spawn_connection)

        if self.xiq.xflowscommonDevices.wait_until_device_online(device_mac=mac) != 1:
            setup_xiq_connect_fail = 1
            pytest.fail("Device didn't come online.")

        if self.tb.dut1.platform == "Stack":
            # Temporary sleep until XIQ-8621 is fixed
            time.sleep(60)
            if self.xiq.xflowsmanageDevices.get_device_stack_status(device_mac=self.tb.dut1.mac) != 'blue':
                pytest.fail("Stack status is disconnected.")

    @classmethod
    def setup_class(cls):
        try:
            cls.executionHelper = PytestExecutionHelper(defaultAction="fail")
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config
            print("TestBed ################%s", cls.tb)
            print("Config #################%s", cls.cfg)
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'

            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()
            cls.udks = cls.defaultLibrary.apiUdks
            cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend
            cls.devCmdManager = cls.defaultLibrary.deviceNetworkElement.networkElementConnectionManager
            cls.devCmdManager.connect_to_all_network_elements()

            # Login
            cls.init_xiq_libaries_and_login(cls, cls.cfg['tenant_username'], cls.cfg['tenant_password'],
                                            url=cls.cfg['test_url'])
            cls.xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings("disable", "EXOS")
            # delete and create location
            cls.delete_create_location_organization(cls)
            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            # Onboard device
            cls.onboard_local(cls, cls.tb.dut1.mac, cls.tb.dut1.cli_type, cls.tb.dut1.ip,
                              cls.tb.dut1.port, cls.tb.dut1.username, cls.tb.dut1.password)
            global sw_template_model
            sw_template_model = cls.get_sw_model(cls)
            print("SW Model: ", sw_template_model)
            cls.create_network_policy_local(cls, network_policy_name)
            # Create device/stack model
            if cls.tb.dut1.platform.lower() == "stack":
                cls.xiq.xflowscommonDevices.column_picker_select('Template')
                cls.create_stack_template(cls, cls.tb.dut1.mac, stack_template_name_original)
                # print("Network policy name:", network_policy_name)

            elif cls.tb.dut1.cli_type.lower() == "exos" or cls.tb.dut1.cli_type == "voss":
                print("Network policy name:", network_policy_name)
                # create device model
                print("Creating device model...")
                cls.create_device_template(cls, network_policy_name, sw_template_model, sw_template_name_original)
            else:
                pytest.fail("The selected device is neither exos, nor voss.")
            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            # Disable_update_setings for exos
            if cls.tb.dut1.cli_type == 'exos':
                cls.xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings('disable', 'exos')

            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            if cls.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name,
                                                                              option="disable",
                                                                              device_mac=cls.tb.dut1.mac) != 1:
                pytest.fail("device was not updated ")
            if cls.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(cls.tb.dut1.mac) != 1:
                pytest.fail("Failed to update the device")

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        cls.cfg['${TEST_NAME}'] = 'Teardown'

        if setup_onboard_fail_flag:
            cls.xiq.login.quit_browser()
            pytest.exit("Failed to onboard the device. Exiting...")

        if setup_xiq_connect_fail:
            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            # TEMPORARY SLEEP UNTIL XIQ 9267 BUG IS FIXED
            time.sleep(10)
            for slot_serial in cls.tb.dut1.serial.split(','):
                cls.xiq.xflowscommonDevices.delete_device(device_serial=slot_serial)
            cls.xiq.xflowsmanageLocation.delete_location_building_floor(location, building, floor)
            cls.deactivate_xiq_libaries_and_logout(cls)
            pytest.exit("Device failed to connect to cloud. Exiting...")

        # Delete device
        cls.delete_device_local(cls, mac=cls.tb.dut1.mac)
        cls.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
        if cls.tb.dut1.platform == 'Stack':
            for slot in range(1, len(cls.tb.dut1.serial.split(',')) + 1):
                cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(stack_template_name_original +
                                                                            '-' + str(slot))
        else:
            cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(sw_template_name_original)
        cls.xiq.xflowsmanageLocation.delete_location_building_floor(location, building, floor)
        # Logout
        cls.deactivate_xiq_libaries_and_logout(cls)

    @mark.tcxm_18417
    @mark.tcxm_18419
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18417_tcxm_18419_add_port_name_and_usage_in_d360(self):
        """	 TCXM-18417 - D360 View - Add Port Name&Usage Configuration in Create Port Type tab for U100 device and check
         config Summary tab.
            TCXM-18419 - D360 View - Add Port Name&Usage Configuration in Create Port Type tab for U100 stack and check
         config Summary tab."""
        self.cfg['${TEST_NAME}'] = 'Add Port Name&Usage Configuration in Create Port Type tab for U100 devices'
        self.executionHelper.testSkipCheck()
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': ['click', None],
            'port usage': ['trunk port', 'trunk'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
        }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': ["port_type_description", "port_type_description"],
                         'status': [None, 'on'],
                         'port usage': ['trunk port', 'trunk'],

                         'page2 trunkVlanPage': ["next_page", None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18420
    @mark.tcxm_18422
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18420_tcxm_18422_add_vlan_in_vlan_tab_in_d360(self):
        """	 TCXM-18420 - D360 View - Add Vlan in VLAN tab for U100 device and check config Summary tab.
            TCXM-18422 - D360 View - Add Vlan in VLAN tab for U100 stack and check config Summary tab."""
        self.cfg['${TEST_NAME}'] = 'D360 View - Add Vlan in VLAN tab for U100 device'
        self.executionHelper.testSkipCheck()
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],
            'vlan': ['50', '50'],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ["next_page", None],
                         'vlan': ['30', '30'],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18423
    @mark.tcxm_18425
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18423_tcxm_18425_add_transmission_settings_in_d360(self):
        """	 TCXM-18423 - D360 View - Add Transmission Settings in Create Port Type tab for U100 device and check
        config Summary tab.
        TCXM-18425 - D360 View - Add Transmission Settings in Create Port Type tab for U100 stack and check
        config Summary tab."""
        self.cfg['${TEST_NAME}'] = 'D360 View - Add Transmission Settings in Create Port Type tab for U100 devices'
        self.executionHelper.testSkipCheck()
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],
            'transmission type': ['Full-Duplex', 'Full-Duplex'],
            'transmission speed': ['100 Mbps', '100'],
            'cdp receive': [None, 'off'],
            'lldp transmit': ['click', 'off'],
            'lldp receive': [None, 'off'],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'Access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],
                         'transmission type': ['Full-Duplex', 'Full-Duplex'],
                         'transmission speed': ['100 Mbps', '100'],
                         'cdp receive': ['click', 'on'],
                         'lldp transmit': ['click', 'off'],
                         'lldp receive': ['click', 'off'],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18426
    @mark.tcxm_18428
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18426_tcxm_18428_add_stp_settings_in_d360(self):
        """	 TCXM-18426 - D360 View - Add STP Settings in Create Port Type tab for U100 device and check config Summary tab.
            TCXM-18428 - D360 View - Add STP Settings in Create Port Type tab for U100 stack and check config Summary tab.
        """
        self.cfg['${TEST_NAME}'] = 'D360 View - Add STP Settings in Create Port Type tab for U100 devices'
        self.executionHelper.testSkipCheck()
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],
            'stp enable': [None, None],
            'edge port': ['click', 'enabled'],
            'bpdu protection': [None, None],
            'priority': ['32', '32'],
            'path cost': ['50', '50'],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'Access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],
                         'stp enable': [None, None],
                         'edge port': ['click', 'enabled'],
                         'bpdu protection': [None, None],
                         'priority': ['48', '48'],
                         'path cost': ['90000', '90000'],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18429
    @mark.tcxm_18431
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18429_tcxm_18431_add_storm_control_settings_in_d360(self):
        """	 TCXM-18429 - D360 View - Add Storm Control Settings in Create Port Type tab for U100 device and
        check config Summary tab.
            TCXM-18431 - D360 View - Add Storm Control Settings in Create Port Type tab for U100 stack and
        check config Summary tab."""
        self.cfg['${TEST_NAME}'] = 'D360 View - Add Storm Control Settings in Create Port Type tab for U100 devices'
        self.executionHelper.testSkipCheck()
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],
            'broadcast': ['click', 'enabled'],
            'unknown unicast': [None, 'disabled'],
            'multicast': ['click', 'enabled'],
            'rate limit type': [None, 'pps'],
            'rate limit value': ['65521', '65521'],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],
                         'broadcast': ['click', 'enabled'],
                         'unknown unicast': ['click', 'enabled'],
                         'multicast': ['click', 'enabled'],
                         'rate limit type': [None, 'pps'],
                         'rate limit value': ['262100', '262100'],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18432
    @mark.tcxm_18434
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18432_tcxm_18434_add_pse_settings_in_d360(self):
        """	 TCXM-18432 - D360 View - Add PSE Settings in Create Port Type tab for U100 device and check config Summary tab.
             TCXM-18434 - D360 View - Add PSE Settings in Create Port Type tab for U100 stack and check config Summary tab.
        """
        self.cfg['${TEST_NAME}'] = 'D360 View - Add PSE Settings in Create Port Type tab for U100 devices'
        self.executionHelper.testSkipCheck()
        # This test should skip if device does not support POE.
        self.verify_poe_supported(self.tb.dut1.name, self.tb.dut1.cli_type)

        # refresh page
        self.xiq.CloudDriver.refresh_page()

        def _check_page_after_refresh():
            try:
                self.xiq.xflowscommonNavigator.navigate_to_devices()
                return True
            except Exception as e:
                print("Exception: ", e)
                return False

        self.xiq.Utils.wait_till(_check_page_after_refresh, timeout=30, is_logging_enabled=True)

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")
        pse_profile_name = "PSE_" + random_word(x=6)

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],
            'pse profile': [{'pse_profile_name': pse_profile_name,
                             'pse_profile_power_mode': '802.3at',
                             'pse_profile_power_limit': '20000',
                             'pse_profile_priority': 'high',
                             'pse_profile_description': 'Testing PSE'
                             }, pse_profile_name],

            'POE status': ['off', 'off'],

            'page7 summary': ["next_page", None]
        }
        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],
                         'pse profile': [{'pse_profile_name': pse_profile_name,
                                          'pse_profile_power_mode': '802.3at',
                                          'pse_profile_power_limit': '20000',
                                          'pse_profile_priority': 'high',
                                          'pse_profile_description': 'Testing PSE'
                                          }, pse_profile_name],
                         'poe status': ['off', 'off'],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18440
    @mark.p2
    @mark.testbed_1_node
    def test_tcxm_18440_create_port_type_and_toggle_auto_sense_button_in_d360(self):
        """	 TCXM-18440 - D360 View - Created a Port Type Template on U100 VOSS device and toggle Auto-Sense button."""
        self.executionHelper.testSkipCheck()

        self.cfg['${TEST_NAME}'] = 'D360 View - Created a Port Type Template on U100 VOSS device and toggle Auto-Sense button.'
        # This test should skip if device is not VOSS
        if self.tb.dut1.cli_type.lower() != "voss":
            pytest.skip("This test can run only on VOSS.")

        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_on_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_on = {
            'name': [port_type_voss_auto_sense_on_name, port_type_voss_auto_sense_on_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': [None, None],
            'port usage': [None, 'auto_sense'],

            'page3 transmissionSettings': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 pseSettings': ["next_page", None],

            'page7 summary': ["next_page", None]
        }
        template_exos = None

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_on, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, d360=True)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_on_name, port_type_exos_name)

    @mark.tcxm_18473
    @mark.tcxm_18475
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18473_tcxm_18475_add_port_name_and_usage_configuration_in_policy_template(self):
        """	 TCXM-18473 - Policy Template - Add Port Name&Usage Configuration in Create Port Type tab for U100 device
        and check config Summary tab.
            TCXM-18473 - Policy Template - Add Port Name&Usage Configuration in Create Port Type tab for U100 stack
        and check config Summary tab."""
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Add Port Name&Usage Configurationin Create Port Type tab for U100 devices'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': ['click', None],
            'port usage': ['trunk port', 'trunk'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': ["port_type_description", "port_type_description"],
                         'status': [None, 'on'],
                         'port usage': ['trunk port', 'trunk'],

                         'page2 trunkVlanPage': ["next_page", None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port,
                                                          network_policy_name, sw_template_name_original, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18476
    @mark.tcxm_18478
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18476_tcxm_18478_add_vlan_in_vlan_tab_in_policy_template(self):
        """	 TCXM-18476 - Policy Template - Add Vlan in VLAN tab for U100 device and check config Summary tab.
             TCXM-18478 - Policy Template - Add Vlan in VLAN tab for U100 stack and check config Summary tab."""
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Add Vlan in VLAN tab for U100 devices and check config Summary tab'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],
            'vlan': ['50', '50'],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': [None, None],
            'status': [None, 'on'],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],
            'vlan': ['30', '30'],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port,
                                                          network_policy_name, sw_template_name_original, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18479
    @mark.tcxm_18481
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18479_tcxm_18481_add_transmission_settings_in_policy_template(self):
        """	 TCXM-18479 - Policy Template - Add Transmission Settings in Create Port Type tab for U100 device
        and check config Summary tab.
             TCXM-18481 - Policy Template - Add Transmission Settings in Create Port Type tab for U100 stack
        and check config Summary tab."""
        self.executionHelper.testSkipCheck()
        self.cfg[
            '${TEST_NAME}'] = 'Policy Template - Add Transmission Settings in Create Port Type tab for U100 device ' \
                              'and check config Summary tab'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],
            'transmission type': ['Full-Duplex', 'Full-Duplex'],
            'transmission speed': ['100 Mbps', '100'],
            'cdp receive': [None, 'off'],
            'lldp transmit': ['click', 'off'],
            'lldp receive': [None, 'off'],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': [None, None],
            'status': [None, 'on'],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ['next_page', None],

            'page3 transmissionSettings': ["next_page", None],
            'transmission type': ['Full-Duplex', 'Full-Duplex'],
            'transmission speed': ['100 Mbps', '100'],
            'cdp receive': ['click', 'on'],
            'lldp transmit': ['click', 'off'],
            'lldp receive': ['click', 'off'],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18482
    @mark.tcxm_18484
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18482_tcxm_18484_add_stp_settings_in_policy_template(self):
        """	 TCXM-18482 - Policy Template - Add STP Settings in Create Port Type tab for U100 device and check config
            in Summary tab.
            TCXM-18484 - Policy Template - Add STP Settings in Create Port Type tab for U100 stack and check config
            in Summary tab.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Add STP Settings in Create Port Type tab for U100 devices and ' \
                                   'check config in Summary tab'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],
            'stp enable': [None, None],
            'edge port': ['click', 'enabled'],
            'bpdu protection': [None, None],
            'priority': ['32', '32'],
            'path cost': ['50', '50'],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': [None, None],
            'status': [None, 'on'],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ['next_page', None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],
            'stp enable': [None, None],
            'edge port': ['click', 'enabled'],
            'bpdu protection': [None, None],
            'priority': ['48', '48'],
            'path cost': ['90000', '90000'],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18485
    @mark.tcxm_18487
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18485_tcxm_18487_add_storm_control_settings_in_policy_template(self):
        """	 TCXM-18485 - Policy Template - Add Storm Control Settings in Create Port Type tab for U100 device
        and check config Summary tab.
            TCXM-18487 - Policy Template - Add Storm Control Settings in Create Port Type tab for U100 stack
        and check config Summary tab."""
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Add Storm Control Settings in Create Port Type tab for U100 ' \
                                   'devices and check config Summary tab.'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],
            'broadcast': ['click', 'enabled'],
            'unknown unicast': [None, 'disabled'],
            'multicast': ['click', 'enabled'],
            'rate limit type': [None, 'pps'],
            'rate limit value': ['65521', '65521'],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': [None, None],
            'status': [None, 'on'],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ['next_page', None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],
            'broadcast': ['click', 'enabled'],
            'unknown unicast': ['click', 'enabled'],
            'multicast': ['click', 'enabled'],
            'rate limit type': [None, 'pps'],
            'rate limit value': ['262100', '262100'],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18488
    @mark.tcxm_18490
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18488_tcxm_18490_add_pse_settings_in_policy_template(self):
        """	 TCXM-18488 - Policy Template - Add PSE Settings in Create Port Type tab for U100 device and check
            config in Summary tab.
            TCXM-18490 - Policy Template - Add PSE Settings in Create Port Type tab for U100 stack and check
            config in Summary tab.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Add PSE Settings in Create Port Type tab for U100 devices and ' \
                                   'check config in Summary tab.'
        # This test should skip if device does not support POE.
        self.verify_poe_supported(self.tb.dut1.name, self.tb.dut1.cli_type)

        # refresh page
        self.xiq.CloudDriver.refresh_page()

        def _check_page_after_refresh():
            try:
                self.xiq.xflowscommonNavigator.navigate_to_devices()
                return True
            except Exception as e:
                print("Exception: ", e)
                return False

        self.xiq.Utils.wait_till(_check_page_after_refresh, timeout=30, is_logging_enabled=True)

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")
        pse_profile_name = "PSE_" + random_word(x=6)

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page7 pseSettings': ["next_page", None],
            'pse profile': [{'pse_profile_name': pse_profile_name,
                             'pse_profile_power_mode': '802.3at',
                             'pse_profile_power_limit': '20000',
                             'pse_profile_priority': 'high',
                             'pse_profile_description': 'Testing PSE'
                             }, pse_profile_name],
            'POE status': ['off', 'off'],

            'page9 summary': ["next_page", None]
            }
        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],
                         'pse profile': [{'pse_profile_name': pse_profile_name,
                                          'pse_profile_power_mode': '802.3at',
                                          'pse_profile_power_limit': '20000',
                                          'pse_profile_priority': 'high',
                                          'pse_profile_description': 'Testing PSE'
                                          }, pse_profile_name],
                         # 'pse profile': [(pse_profile_name, '802.3at', '20000', 'high', 'Testing PSE', False),
                         #                 pse_profile_name],
                         'poe status': ['off', 'off'],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original, d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18561
    @mark.p2
    @mark.testbed_1_node
    def test_tcxm_18561_create_port_type_and_toggle_auto_sense_button_in_policy_template(self):
        """	 TCXM-18561 - Policy Template - Created a Port Type Template on U100 VOSS device and toggle Auto-Sense button.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Created a Port Type Template on U100 VOSS device and ' \
                                   'toggle Auto-Sense button.'
        # This test should skip if device is not VOSS
        if self.tb.dut1.cli_type.lower() != "voss":
            pytest.skip("This test cand run only on VOSS.")

        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_on_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_on = {
            'name': [port_type_voss_auto_sense_on_name, port_type_voss_auto_sense_on_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': [None, None],
            'port usage': [None, 'auto_sense'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = None

        # Configure port type
        print("Configuring Port Type")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_on, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original, d360=False)

        if delete_port_type != 1:
            pytest.fail('Failed to configure port type.')

        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_on_name, port_type_exos_name)

    @mark.tcxm_18493
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18493_edit_port_name_and_usage_in_policy_template(self):
        """	 TCXM-18493 - Policy Template - Edit Port Name&Usage in Create Port Type tab for U100 stack and check
            config in Summary tab."""

        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Edit Port Name&Usage in Create Port Type tab for U100 devices ' \
                                   'and check config in Summary tab.'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'auto-sense': ['click', None],
            'port usage': ['trunk port', 'trunk'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {
            'name': [port_type_exos_name, port_type_exos_name],
            'description': ["port_type_description", "port_type_description"],
            'status': ['click', 'off'],
            'port usage': ['trunk port', 'trunk'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 ELRP': ["next_page", None],

            'page8 pseSettings': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        # Configure port type
        print(f"Configuring Port Type in network policy {network_policy_name} and sw "
              f"template {sw_template_name_original}")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port, voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original, d360=False)
        if delete_port_type != 1:
            pytest.fail("Failed to create new port type.")
        template_voss_auto_sense_off_edit = {'page1 usagePage': ["usagePage", None],
                                             'name': [port_type_voss_auto_sense_off_name,
                                                      port_type_voss_auto_sense_off_name],
                                             'description': ["port_type_description1", "port_type_description1"],
                                             'status': ['click', 'on'],
                                             'auto-sense': [None, None],
                                             'port usage': ['trunk port', 'trunk'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {
            'page1 usagePage': ["usagePage", None],
            'name': [port_type_exos_name, port_type_exos_name],
            'description': ["port_type_description1", "port_type_description1"],
            'status': ['click', 'on'],
            'port usage': ['trunk port', 'trunk'],
            'page7 summaryPage': ["summaryPage", None]
        }

        # Create port type
        print("EDITING Port Type")
        if self.tb.dut1.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(network_policy_name, stack_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(network_policy_name, sw_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail("Failed to edit the port type.")
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18494
    @mark.tcxm_18496
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18494_tcxm_18496_edit_vlan_in_vlan_tab_in_policy_template(self):
        """	 TCXM-18494 - Policy Template - Edit Vlan in VLAN tab for U100 device and check config Summary tab.
             TCXM-18496 - Policy Template - Edit Vlan in VLAN tab for U100 stack and check config Summary tab."""
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Edit Vlan in VLAN tab for U100 devices and check config ' \
                                   'Summary tab'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],
            'vlan': ['50', '50'],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ["next_page", None],
                         'vlan': ['30', '30'],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {network_policy_name} and sw template {sw_template_name_original}")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to create a new port type.')
        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page2 accessVlanPage': ["tab_vlan", None],
                                             'vlan': ['30', '30'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page2 accessVlanPage': ["tab_vlan", None],
                              'vlan': ['30', '30'],
                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if self.tb.dut1.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(network_policy_name, stack_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(network_policy_name, sw_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail('Failed to edit port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18497
    @mark.tcxm_18499
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18497_tcxm_18499_edit_transmission_settings_in_policy_template(self):
        """	 TCXM-18497 - Policy Template - Edit Transmission Settings in Create Port Type tab for U100 device and
            check config in Summary tab.
            TCXM-18499 - Policy Template - Edit Transmission Settings in Create Port Type tab for U100 stack and
            check config in Summary tab."""
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Edit Transmission Settings in Create Port Type tab for U100 ' \
                                   'devices and check config in Summary tab'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],
            'transmission type': ['Full-Duplex', 'Full-Duplex'],
            'transmission speed': ['100 Mbps', '100'],
            'cdp receive': [None, 'off'],
            'lldp transmit': ['click', 'off'],
            'lldp receive': [None, 'off'],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],
                         'transmission type': ['Full-Duplex', 'Full-Duplex'],
                         'transmission speed': ['100 Mbps', '100'],
                         'cdp receive': ['click', 'on'],
                         'lldp transmit': ['click', 'off'],
                         'lldp receive': ['click', 'off'],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {network_policy_name} and sw template {sw_template_name_original}")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to create port type.')
        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page3 transmissionSettingsPage': ["transmissionSettingsPage", None],
                                             'transmission type': ['auto', 'auto'],
                                             'transmission speed': ['auto', 'auto'],
                                             'cdp receive': [None, 'off'],
                                             'lldp transmit': ['click', 'on'],
                                             'lldp receive': [None, 'on'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page3 transmissionSettingsPage': ["transmissionSettingsPage", None],
                              'transmission type': ['auto', 'auto'],
                              'transmission speed': ['auto', 'auto'],
                              'cdp receive': ['click', 'off'],
                              'lldp transmit': ['click', 'on'],
                              'lldp receive': ['click', 'on'],
                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if self.tb.dut1.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(network_policy_name, stack_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(network_policy_name, sw_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail('Failed to edit port type.')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18500
    @mark.tcxm_18502
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18500_tcxm_18502_edit_stp_settings_in_policy_template(self):
        """	 TCXM-18500 - Policy Template - Edit STP Settings in Create Port Type tab for U100 device and check
            config in Summary tab.
            TCXM-18502 - Policy Template - Edit STP Settings in Create Port Type tab for U100 stack and check
            config in Summary tab.
        """

        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Edit STP Settings in Create Port Type tab for U100 devices and ' \
                                   'check config in Summary tab.'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 trunkVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],
            'stp enable': [None, None],
            'edge port': [None, None],
            'bpdu protection': [None, None],
            'priority': ['32', '32'],
            'path cost': ['50', '50'],

            'page5 stormControlSettings': ["next_page", None],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
            }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 trunkVlanPage': ["next_page", None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],
                         'stp enable': [None, None],
                         'edge port': [None, None],
                         'bpdu protection': [None, None],
                         'priority': ['48', '48'],
                         'path cost': ['90000', '90000'],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {network_policy_name} and sw template {sw_template_name_original}")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail("Failed to create new port type")
        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page4 stpPage': ["stpPage", None],
                                             'stp enable': [None, None],
                                             'edge port': [None, None],
                                             'bpdu protection': [None, None],
                                             'priority': ['16', '16'],
                                             'path cost': ['2435', '2435'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page4 stpPage': ["stpPage", None],
                              'stp enable': [None, None],
                              'edge port': [None, None],
                              'bpdu protection': [None, None],
                              'priority': ['16', '16'],
                              'path cost': ['2435', '2435'],
                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if self.tb.dut1.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(network_policy_name, stack_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(network_policy_name, sw_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail("Failed to edit port type.")
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18503
    @mark.tcxm_18505
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18503_tcxm_18505_edit_storm_control_settings_in_policy_template(self):
        """	 TCXM-18503 - Policy Template - Edit Storm Control Settings in Create Port Type tab for U100 device and
            check config in Summary tab.
            TCXM-18505 - Policy Template - Edit Storm Control Settings in Create Port Type tab for U100 stack and
            check config in Summary tab."""

        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Edit Storm Control Settings in Create Port Type tab for U100 ' \
                                   'devices and check config in Summary tab.'
        # refresh page
        # self.xiq.CloudDriver.refresh_page()

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:6'
        else:
            exos_port_check = "6"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],
            'broadcast': ['click', 'enabled'],
            'unknown unicast': [None, 'disabled'],
            'multicast': ['click', 'enabled'],
            'rate limit type': [None, 'pps'],
            'rate limit value': ['65521', '65521'],

            'page6 MACLocking': ["next_page", None],

            'page7 pseSettings': ["next_page", None],

            'page8 ELRP': ["next_page", None],

            'page9 summary': ["next_page", None]
        }

        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 trunkVlanPage': ["next_page", None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],
                         'page5 stormControlSettings': ["next_page", None],
                         'broadcast': ['click', 'enabled'],
                         'unknown unicast': ['click', 'enabled'],
                         'multicast': ['click', 'enabled'],
                         'rate limit type': [None, 'pps'],
                         'rate limit value': ['262100', '262100'],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {network_policy_name} and sw template {sw_template_name_original}")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to create new port type.')
        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page5 stormControlSettingsPage': ["stormControlSettingsPage", None],
                                             'broadcast': ['click', 'disabled'],
                                             'unknown unicast': [None, 'disabled'],
                                             'multicast': ['click', 'disabled'],
                                             'rate limit type': [None, 'pps'],
                                             'rate limit value': ['65522', '65522'],
                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page5 stormControlSettingsPage': ["stormControlSettingsPage", None],
                              'broadcast': ['click', 'disabled'],
                              'unknown unicast': ['click', 'disabled'],
                              'multicast': ['click', 'disabled'],
                              'rate limit type': [None, 'pps'],
                              'rate limit value': ['265', '265'],
                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if self.tb.dut1.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(network_policy_name, stack_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(network_policy_name, sw_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail("Failed to edit port type.")
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)

    @mark.tcxm_18506
    @mark.tcxm_18508
    @mark.p1
    @mark.testbed_1_node
    def test_tcxm_18506_tcxm_18508_edit_pse_settings_in_policy_template(self):
        """	 TCXM-18506 - Policy Template - Edit PSE Settings in Create Port Type tab for U100 device and check
            config in Summary tab.
            TCXM-18508 - Policy Template - Edit PSE Settings in Create Port Type tab for U100 device and check
            config in Summary tab.
        """
        self.executionHelper.testSkipCheck()
        self.cfg['${TEST_NAME}'] = 'Policy Template - Edit PSE Settings in Create Port Type tab for U100 devices ' \
                                   'and check config in Summary tab'
        # This test should skip if device does not support PSE
        self.verify_poe_supported(self.tb.dut1.name, self.tb.dut1.cli_type)

        self.xiq.CloudDriver.refresh_page()
        
        def _check_page_after_refresh():
            try:
                self.xiq.xflowscommonNavigator.navigate_to_devices()
                return True
            except Exception as e:
                print("Exception: ", e)
                return False

        self.xiq.Utils.wait_till(_check_page_after_refresh, timeout=30, is_logging_enabled=True)

        voss_port_check = "1/2"
        if self.tb.dut1.platform.lower == 'stack':
            print("EXOS STACK")
            exos_port_check = '1:7'
        else:
            exos_port_check = "7"
        voss_or_exos_port = self.check_ports_existence(voss_port_check, exos_port_check, self.tb.dut1.cli_type)

        # randomize port template name:
        port_type_voss_auto_sense_off_name = self.get_random_name("ALTA_voss")
        port_type_exos_name = self.get_random_name("ALTA_exos")
        pse_profile_name = "PSE_" + random_word(x=6)

        template_voss_auto_sense_off = {
            'name': [port_type_voss_auto_sense_off_name, port_type_voss_auto_sense_off_name],
            'description': [None, None],
            'status': [None, 'on'],
            'auto-sense': ['click', None],
            'port usage': [None, 'access'],

            'page2 accessVlanPage': ["next_page", None],

            'page3 transmissionSettings': ["next_page", None],

            'page4 stp': ["next_page", None],

            'page5 stormControlSettings': ["next_page", None],

            'page7 pseSettings': ["next_page", None],
            'pse profile': [{'pse_profile_name': pse_profile_name,
                             'pse_profile_power_mode': '802.3at',
                             'pse_profile_power_limit': '20000',
                             'pse_profile_priority': 'high',
                             'pse_profile_description': 'Testing PSE'
                             }, pse_profile_name],
            'poe status': ['off', 'off'],

            'page9 summary': ["next_page", None]
        }
        template_exos = {'name': [port_type_exos_name, port_type_exos_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': [None, 'access'],

                         'page2 accessVlanPage': ['next_page', None],

                         'page3 transmissionSettings': ["next_page", None],

                         'page4 stp': ["next_page", None],

                         'page5 stormControlSettings': ["next_page", None],

                         'page6 MACLocking': ["next_page", None],

                         'page7 ELRP': ["next_page", None],

                         'page8 pseSettings': ["next_page", None],
                         'pse profile': [{'pse_profile_name': pse_profile_name,
                                          'pse_profile_power_mode': '802.3at',
                                          'pse_profile_power_limit': '20000',
                                          'pse_profile_priority': 'high',
                                          'pse_profile_description': 'Testing PSE'
                                          }, pse_profile_name],
                         'poe status': ['off', 'off'],

                         'page9 summary': ["next_page", None]
                         }

        # Configure port type
        print(
            f"Configuring Port Type in network policy {network_policy_name} and sw template {sw_template_name_original}")
        delete_port_type = self.configure_port_type_local(template_voss_auto_sense_off, template_exos,
                                                          voss_or_exos_port,
                                                          voss_or_exos_port, network_policy_name,
                                                          sw_template_name_original,
                                                          d360=False)
        if delete_port_type != 1:
            pytest.fail('Failed to create new port type')

        print("Saving template")

        def _check_template_save():
            if self.xiq.xflowsconfigureSwitchTemplate.save_template() == 1:
                return True
            else:
                return False

        self.xiq.Utils.wait_till(_check_template_save, delay=5, timeout=30)

        # refresh page
        self.xiq.CloudDriver.refresh_page()

        def _check_page_after_refresh():
            try:
                self.xiq.xflowscommonNavigator.navigate_to_devices()
                return True
            except Exception as e:
                print("Exception: ", e)
                return False

        self.xiq.Utils.wait_till(_check_page_after_refresh, timeout=30, is_logging_enabled=True)
        time.sleep(10)
        select_template = self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                    sw_template_name_original)
        if select_template != 1:
            pytest.fail("Could not select switch template ", sw_template_name_original)

        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        # Create new templates for editing port type - the name of the template should remain the same
        template_voss_auto_sense_off_edit = {'page6 pseSettingsPage': ["pseSettingsPage", None],
                                             'pse profile': [{'pse_profile_name': pse_profile_name,
                                                              'pse_profile_power_mode': '802.3bt',
                                                              'pse_profile_power_limit': '30000',
                                                              'pse_profile_priority': 'critical',
                                                              'pse_profile_description': 'Testing PSE EDIT',
                                                              'pse_profile_edit_flag': True
                                                              }, pse_profile_name],
                                             'poe status': ['on', 'on'],

                                             'page7 summaryPage': ["summaryPage", None]
                                             }

        template_exos_edit = {'page6 pseSettingsPage': ["pseSettingsPage", None],
                              'pse profile': [{'pse_profile_name': pse_profile_name,
                                               'pse_profile_power_mode': '802.3bt',
                                               'pse_profile_power_limit': '30000',
                                               'pse_profile_priority': 'critical',
                                               'pse_profile_description': 'Testing PSE EDIT',
                                               'pse_profile_edit_flag': True
                                               }, pse_profile_name],
                              'poe status': ['on', 'on'],

                              'page7 summaryPage': ["summaryPage", None]
                              }

        # Create port type
        print("EDITING Port Type")
        if self.tb.dut1.platform.lower() == "stack":
            delete_port_type = self.edit_port_type_local(network_policy_name, stack_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        else:
            delete_port_type = self.edit_port_type_local(network_policy_name, sw_template_name_original,
                                                         template_voss_auto_sense_off_edit, template_exos_edit,
                                                         voss_or_exos_port, voss_or_exos_port)
        if delete_port_type != 1:
            pytest.fail('Failed to edit port type')
        if self.tb.dut1.make == 'voss':
            voss_or_exos_port = voss_or_exos_port.split('/')[1]
            self.xiq.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(voss_or_exos_port,
                                                                                                  'Auto-sense Port')
        else:
            if self.tb.dut1.platform.lower() == 'stack':
                voss_or_exos_port = voss_or_exos_port.split(':')[1]
            self.xiq.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(voss_or_exos_port,
                                                                                                  'Access Port')
        # Delete port type
        self.delete_port_type_local(delete_port_type, port_type_voss_auto_sense_off_name, port_type_exos_name)
