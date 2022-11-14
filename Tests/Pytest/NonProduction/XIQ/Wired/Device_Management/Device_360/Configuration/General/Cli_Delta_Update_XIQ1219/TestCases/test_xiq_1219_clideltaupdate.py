# Author        : Dragos Sofiea, Devi Ranganathan, Raluca Cionca
# Description   : This script run the below tests for CLI Delta Update feature according with XIQ-1219 story
# Testcases     : TCXM16515, TCXM16916, TCXM16915, TCXM16917
# Comments      : This test is applicable for exos-voss, exos_Stack

from pytest_testconfig import config, load_yaml
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from pytest import mark
from pytest import fixture
import pytest
import os
import os.path
import re
import sys
import time
from pprint import pprint
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.XiqLibraryHelper import XiqLibraryHelper


@pytest.fixture()
def xiq_cli_spans_minutes_teardown(request):

    request.instance.executionHelper.testSkipCheck()

    def teardown():
        request.instance.cfg['${TEST_NAME}'] = 'Teardown - CLI command which spans many minutes'
        if request.instance.tb.dut1.cli_type.lower() == "exos":
            request.instance.get_supplemental_cli_vlan(mac=request.instance.tb.dut1.mac, os="exos", profile_scli="delete_vlan_exos", option="delete",
                                                       vlan_min=2, vlan_max=4000)
        elif request.instance.tb.dut1.cli_type.lower() == "voss":
            request.instance.get_supplemental_cli_vlan(mac=request.instance.tb.dut1.mac, os="voss", profile_scli="delete_vlan_voss", option="delete",
                                                       vlan_min=2, vlan_max=200)
        request.instance.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + request.instance.tb.dut1.mac[:-2],
                                                                                    option="disable", device_mac=request.instance.tb.dut1.mac)
        request.instance.xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=request.instance.tb.dut1.mac)

    request.addfinalizer(teardown)


@pytest.fixture()
def xiq_teardown_long_config(request):

    request.instance.executionHelper.testSkipCheck()

    def teardown():
        request.instance.cfg['${TEST_NAME}'] = 'Teardown - Configure a long config update and check the config update messages'
        if request.instance.tb.dut1.cli_type.lower() == "exos":
            request.instance.get_supplemental_cli_vlan(mac=request.instance.tb.dut1.mac, os="exos",
                                                       profile_scli="delete_vlan_exos", option="delete",
                                                       vlan_min=2, vlan_max=2000)
            request.instance.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + request.instance.tb.dut1.mac[:-2], option="disable", device_mac=request.instance.tb.dut1.mac)
            request.instance.xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=request.instance.tb.dut1.mac)
        elif request.instance.tb.dut1.cli_type.lower() == "voss":
            request.instance.get_supplemental_cli_vlan(mac=request.instance.tb.dut1.mac, os="voss",
                                                       profile_scli="delete_vlan_voss", option="delete", vlan_min=2,
                                                       vlan_max=200)
            request.instance.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + request.instance.tb.dut1.mac[:-2], option="disable",
                                                                                        device_mac=request.instance.tb.dut1.mac)
            request.instance.xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=request.instance.tb.dut1.mac)

        request.instance.xiq.xflowscommonDevices.delete_device(device_mac=request.instance.tb.dut1.mac)
        time.sleep(10)
        request.instance.xiq.xflowscommonDevices.onboard_device_quick(request.instance.tb.dut1)
        time.sleep(60)
        request.instance.xiq.xflowscommonDevices.wait_until_device_online(device_mac=request.instance.tb.dut1.mac)
    request.addfinalizer(teardown)

@pytest.fixture()
def xiq_teardown_small_config(request):

    request.instance.executionHelper.testSkipCheck()

    def teardown():
        request.instance.cfg['${TEST_NAME}'] = 'Teardown - Configure a small config update and check the config update messages'
        if request.instance.tb.dut1.cli_type.lower() == "exos":
            request.instance.get_supplemental_cli_vlan(mac=request.instance.tb.dut1.mac, os="exos",
                                                       profile_scli="delete_vlan_exos", option="delete",
                                                       vlan_min=2, vlan_max=200)
            request.instance.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + request.instance.tb.dut1.mac[:-2], option="disable", device_mac=request.instance.tb.dut1.mac)
            request.instance.xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=request.instance.tb.dut1.mac)
        elif request.instance.tb.dut1.cli_type.lower() == "voss":
            request.instance.get_supplemental_cli_vlan(mac=request.instance.tb.dut1.mac, os="voss",
                                                       profile_scli="delete_vlan_voss", option="delete", vlan_min=2,
                                                       vlan_max=50)
            request.instance.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" +
                                                                                                    request.instance.tb.dut1.mac[:-2], option="disable",
                                                                                        device_mac=request.instance.tb.dut1.mac)
            request.instance.xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=request.instance.tb.dut1.mac)

        request.instance.xiq.xflowscommonDevices.delete_device(device_mac=request.instance.tb.dut1.mac)
        time.sleep(10)
        request.instance.xiq.xflowscommonDevices.onboard_device_quick(request.instance.tb.dut1)
        time.sleep(60)
        request.instance.xiq.xflowscommonDevices.wait_until_device_online(device_mac=request.instance.tb.dut1.mac)
    request.addfinalizer(teardown)


@mark.testbed_1_node
class xiqTests():

    def init_xiq_libaries_and_login(self, username, password, capture_version=False, code="default", url="default",
                                    incognito_mode="False"):
        self.xiq = XiqLibrary()
        time.sleep(5)
        res = self.xiq.init_xiq_libaries_and_login(username, password, capture_version=capture_version, code=code,
                                                   url=url, incognito_mode=incognito_mode)
        if res != 1:
            pytest.fail('Could not Login')

    def deactivate_xiq_libaries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None

    def create_policy(self, policy_name):

        res = self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(policy_name=policy_name)
        if res != 1:
            pytest.fail(f"No policy was created'{policy_name}'")
        else:
            print("Policy was created")

    def assign_policy_device(self, mac, policy_name):

        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        # TEMPORARY SLEEP UNTIL XIQ BUG IS FIXED
        time.sleep(10)
        res = self.xiq.xflowscommonDevices.assign_network_policy_to_switch_mac(policy_name=policy_name, mac=mac)
        if res != 1:
            pytest.fail(f"No policy was assigned'{policy_name}'")
        else:
            print("Policy was assigned")

    def iqagent(self, os, dut_name):

        if os.lower() == "exos":
            self.devCmd.send_cmd_verify_output(dut_name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
            self.devCmd.send_cmd(dut_name, 'disable iqagent', max_wait=10, interval=2,
                                 confirmation_phrases='Do you want to continue?', confirmation_args='y')
            self.devCmd.send_cmd(dut_name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'configure iqagent server ipaddress ' + self.cfg['sw_connection_host'],
                                 max_wait=10, interval=2)
            if '5320' in self.tb.dut1.model:
                self.devCmd.send_cmd(dut_name, 'configure iqagent server vr VR-Default',
                                     max_wait=10, interval=2)
            else:
                self.devCmd.send_cmd(dut_name, 'configure iqagent server vr VR-Mgmt',
                                     max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'enable iqagent', max_wait=10, interval=2)
            time.sleep(10)
        elif os.lower() == "voss":
            self.devCmd.send_cmd(dut_name, 'configure terminal', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'application', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'no iqagent enable', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'iqagent server ' + self.cfg['sw_connection_host'],
                                 max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'iqagent enable', max_wait=10, interval=2)
            self.devCmd.send_cmd_verify_output(dut_name, 'show application iqagent', 'true', max_wait=30,
                                               interval=10)
            self.devCmd.send_cmd(dut_name, 'exit', max_wait=10, interval=2)
            time.sleep(10)
        else:
            pytest.fail("No device os found")
        time.sleep(2)

    def save_initial_configuration(self):

        os = self.tb.dut1.cli_type
        dut_name = self.tb.dut1.name
        if os.lower() == "voss":
            self.devCmd.send_cmd(dut_name, 'configure terminal', max_wait=10, interval=1)
            self.devCmd.send_cmd(dut_name, 'save config')
        elif os.lower() == "exos":
            self.devCmd.send_cmd(dut_name, 'disable cli prompting', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'save configuration primary', max_wait=30, interval=10)
        else:
            pytest.fail("No device os found")

    def save_config(self, os, dut_name, config_file_name=""):
        if os.lower() == "voss":
            self.devCmd.send_cmd(dut_name, 'configure terminal', max_wait=10, interval=1)
            # output = self.devCmd.send_cmd(dut_name, f'save config file {config_file_name}.cfg', max_wait=10, interval=2)
            # print(output)
            self.devCmd.send_cmd(dut_name, 'save config file ' + config_file_name,
                                 confirmation_phrases='overwrite(y / n) ?', confirmation_args='yes')
        elif os.lower() == "exos":
            self.devCmd.send_cmd(dut_name, 'disable cli prompting', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, f'save configuration {config_file_name}', max_wait=30, interval=10)
        else:
            pytest.fail("No device os found")

    def delete_config(self, os, config_file_name=""):
        if os.lower() == "voss":
            spawn_ssh = self.xiq.Cli.open_spawn(self.tb.dut1.ip, self.tb.dut1.port, self.tb.dut1.username,
                                                self.tb.dut1.password, self.tb.dut1.cli_type)
            self.xiq.Cli.send(spawn_ssh, f"configure terminal")
            self.xiq.Cli.send(spawn_ssh, f"delete {config_file_name} -y")
            self.xiq.Cli.send(spawn_ssh, f"reset -y", ignore_error=True, ignore_cli_feedback=True)
        elif os.lower() == "exos":
            spawn_ssh = self.xiq.Cli.open_spawn(self.tb.dut1.ip, self.tb.dut1.port, self.tb.dut1.username,
                                                self.tb.dut1.password, self.tb.dut1.cli_type)
            self.xiq.Cli.send(spawn_ssh, f"disable cli prompting")
            self.xiq.Cli.send(spawn_ssh, f"use configuration primary")
            self.xiq.Cli.send(spawn_ssh, f"reboot", ignore_error=True, ignore_cli_feedback=True)
        else:
            pytest.fail("No device os found")

    def get_supplemental_cli_vlan(self, mac, os, vlan_min, vlan_max, option="", profile_scli=""):

        vlan_list = []
        self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(device_mac=mac)
        if os.lower() == "voss":
            vlan_list.append("configure terminal")
            if option == "create":
                print(f"Creating {vlan_min}-{vlan_max} vlans")
                for vlan in range(vlan_min, vlan_max + 1):
                    vlan_commands = f"vlan create {vlan} type port-mstprstp 0"
                    vlan_list.append(vlan_commands)
                i = 10
                for show in range(10):
                    show = "show running-config | no-more"
                    vlan_list.insert(i, show)
                    i += 10
                vlan_list_one_string = ",".join(vlan_list)
                self.xiq.xflowsmanageDevice360.get_supplemental_cli(profile_scli, vlan_list_one_string)
            elif option == "delete":
                print(f"Deleting {vlan_min}-{vlan_max} vlans")
                for vlan in range(vlan_min, vlan_max + 1):
                    vlan_commands = f"vlan delete {vlan}"
                    vlan_list.append(vlan_commands)
                vlan_list_one_string = ",".join(vlan_list)
                self.xiq.xflowsmanageDevice360.get_supplemental_cli(profile_scli, vlan_list_one_string)
            else:
                print("No option available")
        elif os.lower() == "exos":
            if option.lower() == "create":
                print(f"Creating {vlan_min}-{vlan_max} vlans")
                vlan_commands_1 = f"create vlan {vlan_min}-{int(vlan_max / 4)}"
                vlan_commands_2 = f"create vlan {int(vlan_max / 4 + 1)}-{int(vlan_max / 2)}"
                vlan_commands_3 = f"create vlan {int(vlan_max / 2 + 1)}-{vlan_max}"
                vlan_list.append(vlan_commands_1)
                vlan_list.append(vlan_commands_2)
                vlan_list.append(vlan_commands_3)
                vlan_list_one_string = ",".join(vlan_list)
                self.xiq.xflowsmanageDevice360.get_supplemental_cli(profile_scli, vlan_list_one_string)
            elif option.lower() == "delete":
                print(f"Deleting {vlan_min}-{vlan_max} vlans")
                vlan_commands_1 = f"delete vlan {vlan_min}-{int(vlan_max / 4)}"
                vlan_commands_2 = f"delete vlan {int(vlan_max / 4 + 1)}-{int(vlan_max / 2)}"
                vlan_commands_3 = f"delete vlan {int(vlan_max / 2 + 1)}-{vlan_max}"
                vlan_list.append(vlan_commands_1)
                vlan_list.append(vlan_commands_2)
                vlan_list.append(vlan_commands_3)
                vlan_list_one_string = ",".join(vlan_list)
                self.xiq.xflowsmanageDevice360.get_supplemental_cli(profile_scli, vlan_list_one_string)
            else:
                pytest.fail("No option available")
        else:
            pytest.fail("No device os available")

    def check_logs(self, os, spawn, mac):

        percentage_list = []
        percentage_list.append(21)
        retry = 0
        while retry <= 900:
            output = self.xiq.Cli.send_line_and_wait(spawn, "", 15)
            print(output)
            if output:
                if os.lower() == "voss":
                    if 'Send 30 second in-progress report for cli command processing' in output:
                        output_commands = re.search(r'Send 30 second in-progress report for cli command processing. Processing \d+ out of \d+ commands', output)
                        output_commands_new = output_commands.group(0)
                        digit = [int(d) for d in output_commands_new.split() if d.isdigit()]
                        print(" ", digit)
                        percentage = self.xiq.xflowscommonDevices.get_device_updated_status_percentage(device_mac=mac)
                        percentage_list.append(percentage)
                        if "Device Update Failed" in percentage_list:
                            pytest.fail("Device Update Failed")
                            break
                        elif (int(percentage_list[-1]) > 21 and int(percentage_list[-1]) < 100) and (
                                int(percentage_list[-1]) > int(percentage_list[-2])):
                            print(f"Update status is increasing from {percentage_list[-2]}% to {percentage_list[-1]}%")
                        elif int(percentage_list[-1]) == 100:
                            print("Update configuration is done")
                            break
                        elif int(percentage_list[-1]) == int(percentage_list[-2]):
                            print(f"Still updating {percentage_list[-1]}%. No update status increasing")
                        else:
                            pytest.fail("No update configuration info")
                    elif 'SNMP INFO Save config successful' in output:
                        percentage = self.xiq.xflowscommonDevices.get_device_updated_status_percentage(device_mac=mac)
                        percentage_list.append(percentage)
                        if int(percentage_list[-1]) == 100:
                            print("Update configuration is done")
                            break
                        else:
                            pytest.fail("No Update configuration is done")
                    elif retry == 500:
                        percentage = self.xiq.xflowscommonDevices.get_device_updated_status_percentage(device_mac=mac)
                        percentage_list.append(percentage)
                        if "Device Update Failed" in percentage_list:
                            pytest.fail("Device Update Failed")
                            break
                        elif (int(percentage_list[-1]) > 21 and int(percentage_list[-1]) < 100) and (
                                int(percentage_list[-1]) > int(percentage_list[-2])):
                            print(f"Update status is increasing from {percentage_list[-2]}% to {percentage_list[-1]}%")
                        elif int(percentage_list[-1]) == 100:
                            print("Update configuration is done")
                            break
                        elif int(percentage_list[-1]) == int(percentage_list[-2]):
                            print(f"Still updating {percentage_list[-1]}%. No update status increasing")
                        else:
                            pytest.fail("No update configuration info")
                    else:
                        print("No 'Send 30 second in-progress report'")
                        retry += 10
                        pass
                elif os.lower() == "exos":
                    if '"commandsExec"' in output:
                        output_commands_exec = re.search(r'"commandsExec":\s\d+', output)
                        print(output_commands_exec)
                        output_commands_exec_new = output_commands_exec.group(0)
                        digit_exec = [int(d) for d in output_commands_exec_new.split() if d.isdigit()]
                        print(" ", digit_exec)
                        percentage = self.xiq.xflowscommonDevices.get_device_updated_status_percentage(device_mac=mac)
                        percentage_list.append(percentage)
                        if "Device Update Failed" in percentage_list:
                            pytest.fail("Device update failed")
                        elif (int(percentage_list[-1]) > 21 and int(percentage_list[-1]) < 100) and (
                                int(percentage_list[-1]) > int(percentage_list[-2])):
                            print(f"Update status is increasing from {percentage_list[-2]}% to {percentage_list[-1]}%")
                        elif int(percentage_list[-1]) == 100:
                            print("Update configuration is done")
                            break
                        elif int(percentage_list[-1]) == int(percentage_list[-2]):
                            print(f"Still updating {percentage_list[-1]}%. No update status increasing")
                        else:
                            pytest.fail("No update configuration info")
                    elif retry == 500:
                        percentage = self.xiq.xflowscommonDevices.get_device_updated_status_percentage(device_mac=mac)
                        percentage_list.append(percentage)
                        if "Device Update Failed" in percentage_list:
                            pytest.fail("Device Update Failed")
                            break
                        elif (int(percentage_list[-1]) > 21 and int(percentage_list[-1]) < 100) and (
                                int(percentage_list[-1]) > int(percentage_list[-2])):
                            print(f"Update status is increasing from {percentage_list[-2]}% to {percentage_list[-1]}%")
                        elif int(percentage_list[-1]) == 100:
                            print("Update configuration is done")
                            break
                        elif int(percentage_list[-1]) == int(percentage_list[-2]):
                            print(f"Still updating {percentage_list[-1]}%. No update status increasing")
                        else:
                            pytest.fail("No update configuration info")
                    elif 'running config saved as startup config' in output:
                        percentage = self.xiq.xflowscommonDevices.get_device_updated_status_percentage(device_mac=mac)
                        percentage_list.append(percentage)
                        if int(percentage_list[-1]) == 100:
                            print("Update configuration is done")
                            break
                        else:
                            pytest.fail("No Update configuration is done")
                    else:
                        print("No 'Send 30 second in-progress report'")
                        retry += 10
                        pass
                else:
                    pytest.fail("No os device found")
            elif retry == 900:
                pytest.fail("Timeout exceeded")
            else:
                print("No 'Send 30 second in-progress report' ")

    def check_event(self, event, mac):

        self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(device_mac=mac)
        self.xiq.xflowsmanageDevice360.device360_select_events_view()
        try:
            def _check_event():
                self.xiq.xflowsmanageDevice360.device360_refresh_page()
                return self.xiq.xflowsmanageDevice360.device360_search_event_and_confirm_event_description_contains(event_str=event)
            self.xiq.Utils.wait_till(_check_event, timeout=30, delay=1)
            print(f"'{event}' found in Events Tab")
            close_dialog = self.xiq.xflowsmanageDevice360.get_close_dialog()
            self.xiq.xflowscommonAutoActions.click(close_dialog)
        except Exception as e:
            pytest.fail(f"No '{event}' found in Events Tab")
            close_dialog = self.xiq.xflowsmanageDevice360.get_close_dialog()
            self.xiq.xflowscommonAutoActions.click(close_dialog)

    def get_stack_slots(self):
        spawn_ssh = self.xiq.Cli.open_spawn(self.tb.dut1.ip, self.tb.dut1.port, self.tb.dut1.username,
                                            self.tb.dut1.password,
                                            self.tb.dut1.cli_type)
        show_slots = self.xiq.Cli.send(spawn_ssh, f"show slot | include Operational | count")
        print(show_slots)
        get_slots = self.xiq.Utils.get_regexp_matches(show_slots, "Total\s+lines:\s+(\d+)", 1)
        if get_slots:
            return int(get_slots[0])
        else:
            pytest.fail("Can't find any slots")

    @classmethod
    def setup_class(cls):
        try:
            cls.executionHelper = PytestExecutionHelper()
            # Create an instance of the helper class that will read in the test bed yaml file and
            # provide basic methods and variable access.
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
            cls.udks.setupTeardownUdks.Base_Test_Suite_Setup()

            cls.init_xiq_libaries_and_login(cls,
                                            cls.cfg['tenant_username'],
                                            cls.cfg['tenant_password'],
                                            url=cls.cfg['test_url'])
            cls.save_initial_configuration(cls)
            cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
            cls.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(policy="policy_test_" + cls.tb.dut1.mac[:-2])
            if cls.tb.dut1.platform.lower() == "stack":
                slots = cls.get_stack_slots(cls)
                for slot in range(1, slots + 1):
                    if cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(template_name="Template_" + cls.tb.dut1.mac[:-2]+f"-{slot}") != 1:
                        pytest.fail("Cannot delete the template in Common Objects")
            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            if cls.tb.dut1_platform.lower() == "stack":
                solo_serial = cls.tb.dut1.serial.split(',')
                for eachdevice in solo_serial:
                    cls.xiq.xflowscommonDevices.delete_device(device_serial=eachdevice)

            cls.iqagent(cls, os=cls.tb.dut1.cli_type, dut_name=cls.tb.dut1_name)

            res = -1
            if cls.tb.dut1.cli_type.lower() == "exos":
                res = cls.xiq.xflowscommonDevices.onboard_device_quick(cls.tb.dut1)
            elif cls.tb.dut1.cli_type.lower() == "voss":
                res = cls.xiq.xflowscommonDevices.onboard_device_quick(cls.tb.dut1)
            if res != 1 and cls.tb.dut1.platform.lower() != "stack":
                pytest.fail("There is a problem while onboarding device.. Initiating Cleanup...")
            online = cls.xiq.xflowscommonDevices.wait_until_device_online(device_mac=cls.tb.dut1.mac)
            if online != 1:
                pytest.fail("Device didn't come online")

            if cls.tb.dut1.platform.lower() == "stack":
                try:
                    def _check_stack_status():
                        return cls.xiq.xflowsmanageDevices.get_device_stack_status(device_mac=cls.tb.dut1.mac)
                    cls.xiq.Utils.wait_till(_check_stack_status, timeout=300, delay=5, custom_response=['blue'])
                except Exception as e:
                    pytest.fail("Failed to onboard the stack")

            cls.create_policy(cls, policy_name="policy_test_" + cls.tb.dut1.mac[:-2])
            cls.assign_policy_device(cls, mac=cls.tb.dut1.mac, policy_name="policy_test_" + cls.tb.dut1.mac[:-2])

            if cls.tb.dut1.cli_type.lower() == "exos" and cls.tb.dut1_platform.lower() == "stack":
                cls.xiq.xflowscommonDevices.column_picker_select('Template')
                if cls.xiq.xflowsmanageDevices.create_stack_auto_template(device_mac=cls.tb.dut1.mac,
                                                                          name_stack_template="Template_" + cls.tb.dut1.mac[:-2]) == 1:
                    time.sleep(5)
                    stack_template_name = "Template_" + cls.tb.dut1.mac[:-2]
                    cls.xiq.xflowsconfigureSwitchTemplate.save_stack_template(stack_template_name)
                else:
                    pytest.fail("Failed to create template for the stack!")
                time.sleep(20)

            cls.xiq.xflowsglobalsettingsGlobalSetting.get_supplemental_cli_option("enable")
            if cls.tb.dut1.cli_type.lower() == "exos":
                cls.xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings(option="disable", platform=cls.tb.dut1.cli_type)
            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            cls.save_config(cls, os=cls.tb.dut1.cli_type, dut_name=cls.tb.dut1_name, config_file_name="start")

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        time.sleep(5)
        cls.cfg['${TEST_NAME}'] = 'Teardown'
        time.sleep(5)
        cls.xiq.xflowscommonNavigator.navigate_to_devices()
        cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
        if cls.tb.dut1.platform.lower() == "stack":
            solo_serial = cls.tb.dut1.serial.split(',')
            for eachdevice in solo_serial:
                cls.xiq.xflowscommonDevices.delete_device(device_serial=eachdevice)
            if cls.xiq.xflowsconfigureSwitchTemplate.delete_stack_switch_template(nw_policy="policy_test_" + cls.tb.dut1.mac[:-2],
                                                                                  sw_template_name="Template_" + cls.tb.dut1.mac[:-2]) != 1:
                pytest.fail("Cannot delete the template")
        cls.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(policy="policy_test_" + cls.tb.dut1.mac[:-2])
        if cls.tb.dut1.platform.lower() == "stack":
            slots = cls.get_stack_slots(cls)
            for slot in range(1, slots + 1):
                if cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(template_name="Template_" + cls.tb.dut1.mac[:-2] + f"-{slot}") != 1:
                    pytest.fail("Cannot delete the template in Common Objects")
        cls.delete_config(cls, os=cls.tb.dut1.cli_type, config_file_name="start")
        time.sleep(5)
        cls.deactivate_xiq_libaries_and_logout(cls)

    @mark.p1
    @mark.development
    @mark.xim_txcm_TCXM16515_TCXM16916
    @mark.testbed_1_node

    def test_TCXM16515_TCXM16916_long_config_update(self, xiq_teardown_long_config):
        """TCXM16515 - Configure a long  config update and check the config update messages"""
        """TCXM16916 - Long list of CLI commands"""

        self.cfg['${TEST_NAME}'] = 'Configure a long  config update and check the config update messages'
        if self.tb.dut1.cli_type.lower() == "exos":
            self.get_supplemental_cli_vlan(mac=self.tb.dut1.mac, os="exos", profile_scli="create_vlan_exos",
                                           option="create",
                                           vlan_min=2, vlan_max=2000)
        elif self.tb.dut1.cli_type.lower() == "voss":
            self.get_supplemental_cli_vlan(mac=self.tb.dut1.mac, os="voss", profile_scli="create_vlan_voss",
                                           option="create",
                                           vlan_min=2, vlan_max=200)
        else:
            pytest.fail("No os found")
        spawn_debug = self.xiq.Cli.enable_debug_mode_iqagent(self.tb.dut1.ip, self.tb.dut1.username, self.tb.dut1.password, self.tb.dut1.cli_type)
        self.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + self.tb.dut1.mac[:-2], option="disable", device_mac=self.tb.dut1.mac)
        self.check_logs(os=self.tb.dut1.cli_type, spawn=spawn_debug, mac=self.tb.dut1.mac)
        time.sleep(15)
        self.check_event(event="Download Config", mac=self.tb.dut1.mac)

    @mark.p2
    @mark.development
    @mark.xim_txcm_16915
    @mark.testbed_1_node
    def test_TCXM16915_small_config_update(self, xiq_teardown_small_config):
        """TCXM16915 - Configure a small config update and check the config update messages"""

        self.cfg['${TEST_NAME}'] = 'Configure a small config update and check the config update messages'
        self.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + self.tb.dut1.mac[:-2], option="disable", device_mac=self.tb.dut1.mac)
        self.xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=self.tb.dut1.mac)
        if self.tb.dut1.cli_type.lower() == "exos":
            self.get_supplemental_cli_vlan(mac=self.tb.dut1.mac, os="exos", profile_scli="create_vlan_exos", option="create",
                                           vlan_min=2, vlan_max=200)
        elif self.tb.dut1.cli_type.lower() == "voss":
            self.get_supplemental_cli_vlan(mac=self.tb.dut1.mac, os="voss", profile_scli="create_vlan_voss", option="create",
                                           vlan_min=2, vlan_max=50)
        else:
            pytest.fail("No os found")
        spawn_debug = self.xiq.Cli.enable_debug_mode_iqagent(self.tb.dut1.ip, self.tb.dut1.username,
                                                             self.tb.dut1.password, self.tb.dut1.cli_type)
        self.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + self.tb.dut1.mac[:-2], option="disable", device_mac=self.tb.dut1.mac)
        self.check_logs(os=self.tb.dut1.cli_type, spawn=spawn_debug, mac=self.tb.dut1.mac)
        time.sleep(15)
        self.check_event(event="Download Config", mac=self.tb.dut1.mac)

    @mark.p2
    @mark.development
    @mark.xim_txcm_16917
    @mark.testbed_1_node

    def test_TCXM16917_cli_spans_many_minutes(self, xiq_cli_spans_minutes_teardown):
        """TXCM16917 - CLI command which spans many minutes"""

        self.cfg['${TEST_NAME}'] = 'CLI command which spans many minutes'
        self.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + self.tb.dut1.mac[:-2], option="disable", device_mac=self.tb.dut1.mac)
        self.xiq.xflowscommonDevices.check_device_update_status_by_using_mac(device_mac=self.tb.dut1.mac)
        if self.tb.dut1.cli_type.lower() == "exos":
            self.get_supplemental_cli_vlan(mac=self.tb.dut1.mac, os="exos", profile_scli="create_vlan_exos", option="create",
                                           vlan_min=2, vlan_max=4000)
        elif self.tb.dut1.cli_type.lower() == "voss":
            self.get_supplemental_cli_vlan(mac=self.tb.dut1.mac, os="voss", profile_scli="create_vlan_voss", option="create",
                                           vlan_min=2, vlan_max=200)
        else:
            pytest.fail("No os found")
        spawn_debug = self.xiq.Cli.enable_debug_mode_iqagent(self.tb.dut1.ip, self.tb.dut1.username, self.tb.dut1.password, self.tb.dut1.cli_type)
        self.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name="policy_test_" + self.tb.dut1.mac[:-2], option="disable", device_mac=self.tb.dut1.mac)
        self.check_logs(os=self.tb.dut1.cli_type, spawn=spawn_debug, mac=self.tb.dut1.mac)
        self.check_event(event="Download Config", mac=self.tb.dut1.mac)
