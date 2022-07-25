# Author :          Zoican Ionut Daniel
# Description :     This script runs the below tests for Delta CLI VLAN add/delete port range commands to individual
#                   commands feature according with XIQ-1027 story.
#                   In some cases delta CLI is created with range commands. Depending on the range width the CLI can
#                   take plus 20 minutes to process for CLI commands handling add/delete VLAN to ports. The purpose of
#                   this story is to convert VLAN add/delete port EXOS range generated delta CLI commands to individual
#                   delta CLI commands. Currently VOSS handles creating commands without range format and EXOS should
#                   follow the same format moving forward.
# Testcases :       TCXM-18696, TCXM-18697, TCXM-18698, TCXM-18699, TCXM-18709, TCXM-18710, TCXM-18712, TCXM-18716,
#                   TCXM-18717
# Comments :        This test is applicable for exos, exos_Stack

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
import string
import random
from pprint import pprint
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.XiqLibraryHelper import XiqLibraryHelper

def random_word(x=12):
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(x))
    return randword


location = "Location_" + random_word()
building = "Building_" + random_word()
floor = "Floor_" + random_word()
network_policy_name = 'Policy_' + random_word()
sw_template_name = 'Template_' + random_word()
trunk_port_type_name = 'Trunk_' + random_word()
vlan_range = '200-300'
vlan_range2 = '400-500'
port_numbers = '1,3,5,10'
port_numbers2 = '6,7,8'

@fixture()
def xiq_teardown_template(request):
    request.instance.executionHelper.testSkipCheck()
    def teardown():
        request.instance.cfg['${TEST_NAME}'] = 'Teardown Template'
        if request.instance.tb.dut1.platform == 'Stack':
            for slot in range(1, len(request.instance.tb.dut1.serial.split(',')) + 1):

                def _check_d360_navigation():
                    return request.instance.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                                                                                           request.instance.tb.dut1.mac)
                request.instance.xiq.Utils.wait_till(_check_d360_navigation, timeout=30, delay=10)

                def _check_port_configuration_navigation():
                    return request.instance.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
                request.instance.xiq.Utils.wait_till(_check_port_configuration_navigation, timeout=30, delay=10)

                def _check_stack_selection():
                    return request.instance.xiq.xflowsmanageDevice360.select_stack_unit(slot)
                request.instance.xiq.Utils.wait_till(_check_stack_selection, timeout=30, delay=10)

                request.instance.xiq.xflowsmanageDevice360.device360_configure_ports_access_vlan_stack(
                                                                                  port_numbers=port_numbers2, slot=slot)
            request.instance.xiq.xflowsmanageDevices.refresh_devices_page()
            # request.instance.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name,
            #                                                                             option="disable",
            #                                                                             device_mac=request.instance.tb.
            #                                                                             dut1.mac)
            # request.instance.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(
            #                                                                                request.instance.tb.dut1.mac)
            def _check_device_update():
                return request.instance.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(
                                                                                       policy_name=network_policy_name,
                                                                                       option="disable",
                                                                                       device_mac=request.instance.tb.dut1.mac)

            request.instance.xiq.Utils.wait_till(_check_device_update, timeout=60, delay=3, msg='Checking the '
                                                                                                'initialization of the '
                                                                                                'update')

            def _check_device_update_status():
                return request.instance.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(request.instance.tb.dut1.mac)

            request.instance.xiq.Utils.wait_till(_check_device_update_status, timeout=300, delay=5, msg='Checking update status')

        else:
            request.instance.xiq.xflowsmanageDevice360.device360_configure_ports_access_vlan(
                                                                                device_mac=request.instance.tb.dut1.mac,
                                                                                port_numbers=port_numbers2,
                                                                                access_vlan_id="1")
            request.instance.xiq.xflowsmanageDevices.refresh_devices_page()
            # request.instance.xiq.xflowsmanageDevices.update_override_configuration_to_device(
            #                                                               device_serial=request.instance.tb.dut1.serial)
            # request.instance.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(
            #                                                                                request.instance.tb.dut1.mac)
            def _check_device_update():
                return request.instance.xiq.xflowsmanageDevices.update_override_configuration_to_device(
                                                                          device_serial=request.instance.tb.dut1.serial)

            request.instance.xiq.Utils.wait_till(_check_device_update, timeout=60, delay=3, msg='Checking the '
                                                                                                'initialization of the '
                                                                                                'update')

            def _check_device_update_status():
                return request.instance.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(
                                                                                           request.instance.tb.dut1.mac)

            request.instance.xiq.Utils.wait_till(_check_device_update_status, timeout=300, delay=5,
                                                 msg='Checking update status')

            request.instance.xiq.xflowsconfigureSwitchTemplate.delete_switch_template_from_policy(network_policy_name,
                                                                                                  sw_template_name)
            request.instance.xiq.xflowsconfigureCommonObjects.delete_switch_template(sw_template_name)

            request.instance.xiq.xflowsconfigureCommonObjects.delete_port_type_profile(trunk_port_type_name)

    request.addfinalizer(teardown)

@mark.testbed_1_node
class XiqTests():

    def init_xiq_libaries_and_login(self, username, password, url="default"):
        self.xiq = XiqLibrary()
        res = self.xiq.login.login_user(username, password,  url=url)
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

    def check_ports_existence(self, ports):
        output = self.devCmd.send_cmd(self.tb.dut1.name, 'show ports vlan ')[0].cmd_obj._return_text
        ports_not_found = []
        flag = 1
        if self.tb.dut1.platform == 'Stack':
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):
                for port in ports.split(','):
                    if str(slot) + ':' + port not in output:
                        flag = -1
                        ports_not_found.append(str(slot) + ':' + port)
                    else:
                        print("Found the port: " + str(slot) + ':' + port)
        else:
            for port in ports.split(','):
                if port + ' ' not in output:
                    flag = -1
                    ports_not_found.append(port)
                else:
                    print("Found the port: " + port)

        if ports_not_found:
            print('The following ports were not found: ')
            for port_not_found in ports_not_found:
                print(port_not_found)

        return flag

    def get_device_template_model_name(self):
        device_system_output = self.devCmd.send_cmd(self.tb.dut1.name, 'show system')[0].cmd_obj._return_text
        system_type_regex = '(System Type:[ ]{2,}.{0,})'
        system_type = self.xiq.Utils.get_regexp_matches(device_system_output, system_type_regex, 1)[0]
        system_type_string = system_type.replace(self.xiq.Utils.get_regexp_matches(system_type,
                                                                                   '(System Type:[ ]{2,})')[0], '')
        if 'SwitchEngine' in system_type_string:
            system_type_string = 'Switch Engine ' + system_type_string
            system_type_string = system_type_string.replace('-SwitchEngine', '')
            system_type_string = system_type_string.replace('\r', '')
        elif 'EXOS' in system_type_string:
            system_type_string = 'Switch Engine ' + system_type_string
            system_type_string = system_type_string.replace('-EXOS', '')
            system_type_string = system_type_string.replace('\r', '')
        else:
            system_type_string = system_type_string.replace(system_type_string[:4], system_type_string[:4] + '-')
            system_type_string = system_type_string.replace('\r', '')
        print('The device template name is: ' + system_type_string)
        return system_type_string

    def check_add_vlan_range_commands_to_individual(self, device_mac, vlan_rng, ports):
        def check_delta_config():
            pass
        delta_configs = self.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta(device_mac)
        if delta_configs == -1:
            pytest.fail('Did not manage to collect the delta configurations.')

        flag = 1
        not_found = []
        if self.tb.dut1.platform == 'Stack':
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):
                for port in ports.split(','):
                    for vlan in range(int(vlan_rng.split('-')[0]), int(vlan_rng.split('-')[1]) + 1):
                        if 'configure vlan ' + str(vlan) + ' add port ' + str(slot) + ':' + str(port) + ' tagged' + \
                                                                                      ' #y' not in delta_configs:
                            not_found.append('configure vlan ' + str(vlan) + ' add port ' + str(slot) + ':' +
                                             str(port) + ' tagged' + ' #y')
                            flag = 0

        else:
            for port in ports.split(','):
                for vlan in range(int(vlan_rng.split('-')[0]), int(vlan_rng.split('-')[1])+1):
                    if 'configure vlan ' + str(vlan) + ' add port ' + str(port) + ' tagged' + ' #y'not in delta_configs:
                        not_found.append('configure vlan ' + str(vlan) + ' add port ' + str(port) + ' tagged' + ' #y')
                        flag = 0
        if not_found:
            print("Did not find the following add port commands:\n")
            for nf in not_found:
                print(nf)
        return flag

    def check_delete_vlan_range_commands_to_individual(self, device_mac, vlan_range, ports):
        delta_configs = self.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta(device_mac)
        if delta_configs == -1:
            pytest.fail('Did not manage to collect the delta configurations.')
        flag = 1
        not_found = []
        if self.tb.dut1.platform == 'Stack':
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):
                for port in ports.split(','):
                    for vlan in range(int(vlan_range.split('-')[0]), int(vlan_range.split('-')[1]) + 1):
                        if 'configure vlan ' + str(vlan) + ' delete port ' + str(slot) + ':' + str(port) not in delta_configs:
                            flag = 0
                            not_found.append('configure vlan ' + str(vlan) + ' delete port ' + str(slot) + ':' +
                                             str(port))
        else:
            for port in ports.split(','):
                for vlan in range(int(vlan_range.split('-')[0]), int(vlan_range.split('-')[1])+1):
                    if 'configure vlan ' + str(vlan) + ' delete port ' + str(port) not in delta_configs:
                        flag = 0
                        not_found.append('configure vlan ' + str(vlan) + ' delete port ' + str(port))
        if not_found:
            print("Did not find the following delete port commands: ")
            for nf in not_found:
                print(nf)

        return flag

    def get_device_vlan_configuration(self, ports):
        configuration_list = []
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        def _check_device_update():
            return self.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name,
                                                                                   option="disable",
                                                                                   device_mac=self.tb.dut1.mac)
        self.xiq.Utils.wait_till(_check_device_update, timeout=60, delay=3, msg='Checking the initialization of the '
                                                                                'update')

        def _check_device_update_status():
            return self.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(self.tb.dut1.mac)
        self.xiq.Utils.wait_till(_check_device_update_status, timeout=300, delay=5, msg='Checking update status')

        output = self.devCmd.send_cmd(self.tb.dut1.name, 'show ports vlan ')[0].cmd_obj._return_text
        if self.tb.dut1.platform == 'Stack':
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):
                for port in ports.split(','):
                    if str(slot) + ':' + port not in output:
                        print("Cannot find the port: " + str(slot) + ':' + port )
                        return -1
                    counter = 0
                    start_index = 0
                    stop_index = 0
                    for letter in output:
                        if counter + 3 == len(output):
                            break
                        if int(port) + 1 > 9:
                            if output[counter] == str(slot) and output[counter + 1] == ':' and output[counter + 2] + \
                                    output[counter + 3] == port:
                                start_index = counter
                            if str(slot) + ':' + str(int(port) + 1) not in output:
                                stop_index = len(output)
                            elif output[counter] == str(slot) and output[counter + 1] == ':' and output[counter + 2] + \
                                    output[counter + 3] == str(int(port) + 1):
                                stop_index = counter
                                configuration_list.append(output[start_index:stop_index])
                                break
                        else:
                            if output[counter] == str(slot) and output[counter + 1] == ':' and \
                                    output[counter + 2] == port:
                                start_index = counter
                            if str(slot) + ':' + str(int(port) + 1) not in output:
                                stop_index = len(output)
                            elif output[counter] == str(slot) and output[counter + 1] == ':' and \
                                    output[counter + 2] == str(int(port) + 1):
                                stop_index = counter
                                configuration_list.append(output[start_index:stop_index])
                                break
                        counter = counter + 1
        else:
            for port in ports.split(','):
                if port not in output:
                    print("Cannot find the port: " + port)
                    return -1
                counter = 0
                start_index = 0
                stop_index = 0
                for letter in output:
                    if counter + 2 == len(output):
                        break
                    if int(port) + 1 > 9:
                        if output[counter] + output[counter + 1] == port and output[counter + 2] == ' ':
                            start_index = counter
                        if str(int(port) + 1) not in output:
                            stop_index = len(output)
                        elif output[counter] + output[counter + 1] == str(int(port) + 1) and output[counter + 2] == ' ':
                            stop_index = counter
                            configuration_list.append(output[start_index:stop_index])
                            break
                    else:
                        if output[counter] == port and output[counter + 1] == ' ':
                            start_index = counter
                        if str(int(port) + 1) not in output:
                            stop_index = len(output)
                        elif output[counter] == str(int(port) + 1) and output[counter + 1] == ' ':
                            stop_index = counter
                            configuration_list.append(output[start_index:stop_index])
                            break
                    counter = counter + 1
        print(configuration_list)
        return configuration_list

    def check_devices_config_after_individual_add_port_push(self, vlan_range, ports):
        configuration_list = self.get_device_vlan_configuration(ports)
        flag = 1
        for configuration in configuration_list:
            vlans_not_found = []
            vlan_list_config = self.xiq.Utils.get_regexp_matches(configuration, "(\d\d\d\d)", 1)
            for vlan in range(int(vlan_range.split('-')[0]), int(vlan_range.split('-')[1]) + 1):

                if vlan < 10:
                    if '000' + str(vlan) not in vlan_list_config:
                        vlans_not_found.append(str(vlan))
                elif vlan >= 10 and vlan < 100:
                    if '00' + str(vlan) not in vlan_list_config:
                        vlans_not_found.append(str(vlan))
                elif vlan >= 100 and vlan < 1000:
                    if '0' + str(vlan) not in vlan_list_config:
                        vlans_not_found.append(str(vlan))
                elif vlan >= 1000:
                    if str(vlan) not in vlan_list_config:
                        vlans_not_found.append(str(vlan))

            if vlans_not_found:
                flag = 0
                print("Vlans not found. The vlan range was: " + vlan_range)
                print('The port is currently configured as follows: ')
                print(configuration)
                print("The following vlans are missing:")
                vlans_not_found_string = ''
                for vlan in vlans_not_found:
                    vlans_not_found_string = vlans_not_found_string + vlan + ', '
                print(vlans_not_found_string[:-1])
                print(3 * '\n')
            else:
                print("The add port commands for this port have been pushed succesfully!")
                print(configuration)
        return flag

    def check_devices_config_after_individual_delete_port_push(self, ports, vlan_range):
        configuration_list = self.get_device_vlan_configuration(ports)
        flag = 1
        for configuration in configuration_list:
            vlans_found = []
            vlan_list_config = self.xiq.Utils.get_regexp_matches(configuration, "(\d\d\d\d)", 1)
            for vlan in range(int(vlan_range.split('-')[0]), int(vlan_range.split('-')[1]) + 1):

                if vlan < 10:
                    if '000' + str(vlan) in vlan_list_config:
                        vlans_found.append(str(vlan))
                elif vlan >= 10 and vlan < 100:
                    if '00' + str(vlan) in vlan_list_config:
                        vlans_found.append(str(vlan))
                elif vlan >= 100 and vlan < 1000:
                    if '0' + str(vlan) in vlan_list_config:
                        vlans_found.append(str(vlan))
                elif vlan >= 1000:
                    if str(vlan) in vlan_list_config:
                        vlans_found.append(str(vlan))

            if vlans_found:
                flag = 0
                print("Vlans found. The vlan range was: " + vlan_range)
                print('The port is currently configured as follows: ')
                print(configuration)
                print("The following vlans are still present:")
                vlans_found_string = ''
                for vlan in vlans_found:
                    vlans_found_string = vlans_found_string + vlan + ', '
                print(vlans_found_string[:-1])
                print(3 * '\n')
            else:
                print("The delete port commands for this port have been pushed succesfully!")
                print("The port is currently configured as follows: ")
                print(configuration)
        return flag

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

            # Check if device is exos. If the device is voss or SR, skip the test
            if cls.tb.dut1.cli_type != 'exos':
                pytest.skip("Device should be exos.")
            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()
            cls.udks = cls.defaultLibrary.apiUdks
            cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend
            cls.devCmdManager = cls.defaultLibrary.deviceNetworkElement.networkElementConnectionManager
            cls.devCmdManager.connect_to_all_network_elements()
            if cls.check_ports_existence(cls, port_numbers) != 1:
                pytest.fail("One or more ports were not found. Choose other ports.")
            if cls.check_ports_existence(cls, port_numbers2) != 1:
                pytest.fail("One or more ports were not found. Choose other ports.")
            cls.init_xiq_libaries_and_login(cls, cls.cfg['tenant_username'], cls.cfg['tenant_password'],
                                            url=cls.cfg['test_url'])
            cls.delete_create_location_organization(cls)
            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            cls.xiq.xflowsglobalsettingsGlobalSetting.change_exos_device_management_settings("disable", "EXOS")
            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
            solo_serial = cls.tb.dut1.serial.split(',')
            for eachdevice in solo_serial:
                cls.xiq.xflowscommonDevices.delete_device(device_mac=eachdevice)
            dut_location = f'{location},{building},{floor}'

            global setup_flag_onboard_fail
            setup_flag_onboard_fail = 1
            cls.devCmd.send_cmd(cls.tb.dut1.name, 'configure iq server ipaddress none')
            cls.devCmd.send_cmd(cls.tb.dut1.name, 'enable iqagent')
            if cls.xiq.xflowsmanageSwitch.onboard_switch(cls.tb.dut1.serial, device_os=cls.tb.dut1.cli_type,
                                                         switch_make=cls.tb.dut1.make, location=dut_location) == 1:
                setup_flag_onboard_fail = 0
            global setup_flag_connect_fail
            setup_flag_connect_fail = 1
            if '5320' in cls.tb.dut1.model:
                cls.xiq.Cli.configure_device_to_connect_to_cloud(cls.tb.dut1.cli_type, cls.tb.dut1.ip,
                                                                 cls.tb.dut1.port, cls.tb.dut1.username,
                                                                 cls.tb.dut1.password, cls.cfg['sw_connection_host'],
                                                                 vr='VR-Default', retry_count=30)
                setup_flag_connect_fail = 0
            else:
                cls.xiq.Cli.configure_device_to_connect_to_cloud(cls.tb.dut1.cli_type, cls.tb.dut1.ip,
                                                                 cls.tb.dut1.port, cls.tb.dut1.username,
                                                                 cls.tb.dut1.password, cls.cfg['sw_connection_host'],
                                                                 vr='VR-Mgmt', retry_count=30)
                setup_flag_connect_fail = 0
            if cls.xiq.xflowscommonDevices.wait_until_device_online(device_mac=cls.tb.dut1.mac, retry_count=30) != 1:
                pytest.fail("Device didn't come online.")
            if cls.tb.dut1.platform == "Stack":
                if cls.xiq.xflowsmanageDevices.get_device_stack_status(device_mac=cls.tb.dut1.mac) != 'blue':
                    pytest.fail("Stack status is disconnected.")
            cls.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(network_policy_name)
            cls.xiq.xflowscommonNavigator.navigate_to_devices()
            cls.xiq.xflowsmanageDevices.assign_network_policy_to_switch_mac(network_policy_name, cls.tb.dut1.mac)
            if cls.tb.dut1.platform == "Stack":
                cls.xiq.xflowscommonDevices.column_picker_select('Template')
                if cls.xiq.xflowsmanageDevices.create_stack_auto_template(device_mac=cls.tb.dut1.mac,
                                                                          name_stack_template=sw_template_name) == 1:
                    cls.xiq.xflowsconfigureSwitchTemplate.save_stack_template()
                else:
                    pytest.fail("Failed to create template for the stack!")

                def _check_device_update():
                    return cls.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(
                        policy_name=network_policy_name, option="disable", device_mac=cls.tb.dut1.mac)

                cls.xiq.Utils.wait_till(_check_device_update, timeout=60, delay=3, msg='Checking the initialization of '
                                                                                       'the update')
                # cls.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name,
                #                                                                option="disable",
                #                                                                device_mac=cls.tb.dut1.mac)
            else:
                def _check_device_update():
                    return cls.xiq.xflowsmanageDevices.update_override_configuration_to_device(
                        device_serial=cls.tb.dut1.serial)

                cls.xiq.Utils.wait_till(_check_device_update, timeout=60, delay=3, msg='Checking the initialization of '
                                                                                       'the update')
                # cls.xiq.xflowsmanageDevices.update_override_configuration_to_device(device_serial=cls.tb.dut1.serial)

            def _check_device_update_status():
                return cls.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(cls.tb.dut1.mac)

            cls.xiq.Utils.wait_till(_check_device_update_status, timeout=300, delay=5, msg='Checking update status')
            #cls.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(cls.tb.dut1.mac)
        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        cls.cfg['${TEST_NAME}'] = 'Teardown'
        if setup_flag_onboard_fail:
            cls.xiq.login.quit_browser()
            pytest.exit("Failed to onboard the device. Exiting...")

        if setup_flag_connect_fail:
            if cls.tb.dut1.platform == "Stack":
                for slot_serial in cls.tb.dut1.serial.split(','):
                    cls.xiq.xflowscommonDevices.delete_device(device_serial=slot_serial)
            else:
                cls.xiq.xflowscommonDevices.delete_device(device_serial=cls.tb.dut1.serial)
            cls.xiq.xflowsmanageLocation.delete_location_building_floor(location, building, floor)
            cls.deactivate_xiq_libaries_and_logout(cls)
            pytest.exit("The device did not connect to the cloud. Exiting...")

        if cls.tb.dut1.platform == 'Stack':
            for slot in range(1, len(cls.tb.dut1.serial.split(',')) + 1):

                def _check_d360_navigation():
                    return cls.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        cls.tb.dut1.mac)
                cls.xiq.Utils.wait_till(_check_d360_navigation, timeout=30, delay=5)

                def _check_port_configuration_navigation():
                    return cls.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
                cls.xiq.Utils.wait_till(_check_port_configuration_navigation, timeout=30, delay=5)

                def _check_stack_selection():
                    return cls.xiq.xflowsmanageDevice360.select_stack_unit(slot)
                cls.xiq.Utils.wait_till(_check_stack_selection, timeout=30, delay=5)

                cls.xiq.xflowsmanageDevice360.device360_configure_ports_access_vlan_stack(port_numbers=port_numbers2,
                                                                                          slot=slot)
            for slot in range(1, len(cls.tb.dut1.serial.split(',')) + 1):

                def _check_d360_navigation():
                    return cls.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        cls.tb.dut1.mac)
                cls.xiq.Utils.wait_till(_check_d360_navigation, timeout=30, delay=5)

                def _check_port_configuration_navigation():
                    return cls.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
                cls.xiq.Utils.wait_till(_check_port_configuration_navigation, timeout=30, delay=5)

                def _check_stack_selection():
                    return cls.xiq.xflowsmanageDevice360.select_stack_unit(slot)
                cls.xiq.Utils.wait_till(_check_stack_selection, timeout=30, delay=5)

                cls.xiq.xflowsmanageDevice360.device360_configure_ports_access_vlan_stack(port_numbers=port_numbers,
                                                                                          slot=slot)
            cls.xiq.xflowsmanageDevices.refresh_devices_page()
            # cls.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name,
            #                                                                option="disable", device_mac=cls.tb.dut1.mac)
            # cls.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(cls.tb.dut1.mac)
            def _check_device_update():
                return cls.xiq.xflowscommonDevices.get_update_devices_reboot_rollback(policy_name=network_policy_name,
                                                                                       option="disable",
                                                                                       device_mac=cls.tb.dut1.mac)

            cls.xiq.Utils.wait_till(_check_device_update, timeout=60, delay=3, msg='Checking the initialization of the '
                                                                                   'update')

            def _check_device_update_status():
                return cls.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(cls.tb.dut1.mac)

            cls.xiq.Utils.wait_till(_check_device_update_status, timeout=300, delay=5, msg='Checking update status')

            cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
            cls.xiq.xflowsconfigureSwitchTemplate.delete_stack_switch_template(network_policy_name, sw_template_name)
            cls.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
            for slot in range(1, len(cls.tb.dut1.serial.split(',')) + 1):
                cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(sw_template_name + '-' + str(slot))

            cls.xiq.xflowsconfigureCommonObjects.delete_port_type_profile(trunk_port_type_name)

        else:
            cls.xiq.xflowsmanageDevice360.device360_configure_ports_access_vlan(device_mac=cls.tb.dut1.mac,
                                                                                port_numbers=port_numbers2,
                                                                                access_vlan_id="1")
            cls.xiq.xflowsmanageDevice360.device360_configure_ports_access_vlan(device_mac=cls.tb.dut1.mac,
                                                                                port_numbers=port_numbers,
                                                                                access_vlan_id="1")
            cls.xiq.xflowsmanageDevices.refresh_devices_page()
            # cls.xiq.xflowsmanageDevices.update_override_configuration_to_device(device_serial=cls.tb.dut1.serial)
            # cls.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(cls.tb.dut1.mac)
            def _check_device_update():
                return cls.xiq.xflowsmanageDevices.update_override_configuration_to_device(device_serial=
                                                                                           cls.tb.dut1.serial)

            cls.xiq.Utils.wait_till(_check_device_update, timeout=60, delay=3,
                                     msg='Checking the initialization of the '
                                         'update')

            def _check_device_update_status():
                return cls.xiq.xflowsmanageDevices.check_device_update_status_by_using_mac(cls.tb.dut1.mac)

            cls.xiq.Utils.wait_till(_check_device_update_status, timeout=300, delay=5, msg='Checking update status')
            cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
            cls.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(network_policy_name)
            cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(sw_template_name)
            cls.xiq.xflowsconfigureCommonObjects.delete_port_type_profile(trunk_port_type_name)



        cls.xiq.xflowsmanageLocation.delete_location_building_floor(location, building, floor)
        cls.deactivate_xiq_libaries_and_logout(cls)

    @mark.tcxm_18709
    @mark.p1
    @mark.testbed_1_node
    def test_check_delta_cli_add_port_range_commands_to_individual_from_template_tcxm_18709(self):
        self.cfg['${TEST_NAME}'] = 'Check delta cli add port range commands to individual from template and ' \
                                   'check device config'
        self.executionHelper.testSkipCheck()
        template_exos = {'name': [trunk_port_type_name, trunk_port_type_name],
                         'description': [None, None],
                         'status': [None, 'on'],
                         'port usage': ['trunk port', 'TRUNK'],
                         'page2 trunkVlanPage': ['next_page', None],
                         'native vlan': ['1', '1'],
                         'allowed vlans': [vlan_range, vlan_range],
                         'page3 transmissionSettings': ["next_page", None],
                         'page4 stp': ["next_page", None],
                         'page5 stormControlSettings': ["next_page", None],
                         'page6 MACLocking': ["next_page", None],
                         'page7 ELRP': ["next_page", None],
                         'page8 pseSettings': ["next_page", None],
                         'page9 summary': ["next_page", None]
                         }
        if self.tb.dut1.platform != "Stack":
            self.xiq.xflowsconfigureSwitchTemplate.add_sw_template(network_policy_name,
                                                                   self.get_device_template_model_name(),
                                                                   sw_template_name)
        try:
            def _check_sw_template_selection():
                return self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
            self.xiq.Utils.wait_till(_check_sw_template_selection, timeout=30, delay=5)
        except:
            pytest.fail(f'Did not find: {sw_template_name} template')
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        self.xiq.xflowsmanageDevice360.create_new_port_type(template_exos, port_numbers.split(',')[0])
        if self.tb.dut1.platform == "Stack":
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):

                def _check_sw_template_selection():
                    return self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                     sw_template_name)
                self.xiq.Utils.wait_till(_check_sw_template_selection, timeout=30, delay=5)

                self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot)
                self.xiq.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                      trunk_port_type_name)
        else:
            def _check_sw_template_selection():
                return self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
            self.xiq.Utils.wait_till(_check_sw_template_selection, timeout=30, delay=5)

            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
            self.xiq.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  trunk_port_type_name)

        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        if self.check_add_vlan_range_commands_to_individual(self.tb.dut1.mac, vlan_range, port_numbers):
            print("Found the individual add port commands!")
            if self.check_devices_config_after_individual_add_port_push(vlan_range, port_numbers):
                print("The add commands that have been pushed are present on the device's config.")
                pass
            else:
                pytest.fail("The delete commands that have been pushed are not present!")
        else:
            pytest.fail("Failed to find the individual add port commands!")

    @mark.tcxm_18710
    @mark.p1
    @mark.testbed_1_node
    def test_check_delta_cli_delete_port_range_commands_to_individual_from_template_tcxm_18710(self):
        self.cfg['${TEST_NAME}'] = 'Check delta cli delete port range commands to individual from template and ' \
                                   'check device config'
        self.executionHelper.testSkipCheck()
        for new_trunk_port in port_numbers2.split(','):
            for port in port_numbers.split(','):
                if int(new_trunk_port) == int(port):
                    pytest.fail("The new trunk ports must be different from the initial ones!")
        def _check_navigation_to_network_policy():
            return self.xiq.xflowscommonNavigator.navigate_to_network_policies_list_view_page()
        self.xiq.Utils.wait_till(_check_navigation_to_network_policy)

        def _check_sw_template_selection():
            return self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
        self.xiq.Utils.wait_till(_check_sw_template_selection, timeout=30, delay=5)

        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        if self.tb.dut1.platform == "Stack":
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot)
                self.xiq.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                      "Access Port")

                def _check_sw_template_selection():
                    return self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name,
                                                                                     sw_template_name)
                self.xiq.Utils.wait_till(_check_sw_template_selection, timeout=30, delay=5)

                self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
                self.xiq.xflowsconfigureSwitchTemplate.sw_template_stack_select_slot(slot=slot)
        else:
            self.xiq.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers,
                                                                                                  "Access Port")

            def _check_sw_template_selection():
                return self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(network_policy_name, sw_template_name)
            self.xiq.Utils.wait_till(_check_sw_template_selection, timeout=30, delay=5)

            self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()

        self.xiq.xflowsconfigureSwitchTemplate.template_assign_ports_to_an_existing_port_type(port_numbers2,
                                                                                              trunk_port_type_name)
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        if self.check_delete_vlan_range_commands_to_individual(self.tb.dut1.mac, vlan_range, port_numbers):
            print("Found the individual delete port commands!")
            if self.check_devices_config_after_individual_delete_port_push(port_numbers, vlan_range):
                print("The delete commands that have been pushed are present on the device's config.")
                pass
            else:
                pytest.fail("The delete commands that have been pushed are not present!")
        else:
            pytest.fail("Failed to find the individual delete port commands!")

    @mark.tcxm_18712
    @mark.p2
    @mark.testbed_1_node
    def test_verify_that_changes_are_present_in_delta_cLI_after_overwr_template_vlan_config_in_d360_tcxm_18712(
                                                                                        self, xiq_teardown_template):
        self.cfg['${TEST_NAME}'] = 'Verify that changes are present in Delta CLI after overwriting the template vlan ' \
                                   'config in d360 config'
        self.executionHelper.testSkipCheck()
        if self.tb.dut1.platform == 'Stack':
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):

                def _check_d360_navigation():
                    return self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        self.tb.dut1.mac)
                self.xiq.Utils.wait_till(_check_d360_navigation, timeout=30, delay=5)

                def _check_port_configuration_navigation():
                    return self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
                self.xiq.Utils.wait_till(_check_port_configuration_navigation, timeout=30, delay=5)

                def _check_stack_selection():
                    return self.xiq.xflowsmanageDevice360.select_stack_unit(slot)
                self.xiq.Utils.wait_till(_check_stack_selection, timeout=30, delay=5)

                self.xiq.xflowsmanageDevice360.device360_configure_ports_trunk_stack(port_numbers=port_numbers2,
                                                                                     trunk_native_vlan="1",
                                                                                     trunk_vlan_id=vlan_range2,
                                                                                     slot=slot)
        else:
            self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(self.tb.dut1.mac)
            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            self.xiq.xflowsmanageDevice360.device360_configure_ports_trunk_vlan(port_numbers=port_numbers2,
                                                                                trunk_native_vlan="1",
                                                                                trunk_vlan_id=vlan_range2)
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        delta_configs = self.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta(self.tb.dut1.mac)
        if delta_configs == -1:
            pytest.fail('Did not manage to collect the delta configurations.')
        if 'delete vlan ' + vlan_range in delta_configs:
            if self.check_add_vlan_range_commands_to_individual(self.tb.dut1.mac, vlan_range2, port_numbers2):
                print("Found the add commands for the second vlan range!")
                pass
            else:
                pytest.fail("Failed to find the individual add port commands!")
        else:
            pytest.fail("Did not find the deletion command for the previous range!")

    @mark.tcxm_18696
    @mark.tcxm_18716
    @mark.p1
    @mark.testbed_1_node
    def test_check_delta_cli_add_port_range_commands_to_individual_tcxm_18696_tcxm_18716(self):
        self.cfg['${TEST_NAME}'] = 'Check Individual Add Port Commands'
        self.executionHelper.testSkipCheck()
        if self.tb.dut1.platform == 'Stack':
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):

                def _check_d360_navigation():
                    return self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        self.tb.dut1.mac)
                self.xiq.Utils.wait_till(_check_d360_navigation, timeout=30, delay=5)

                def _check_port_configuration_navigation():
                    return self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
                self.xiq.Utils.wait_till(_check_port_configuration_navigation, timeout=30, delay=5)

                def _check_stack_selection():
                    return self.xiq.xflowsmanageDevice360.select_stack_unit(slot)
                self.xiq.Utils.wait_till(_check_stack_selection, timeout=30, delay=5)

                self.xiq.xflowsmanageDevice360.device360_configure_ports_trunk_stack(port_numbers=port_numbers,
                                                                                     trunk_native_vlan="1",
                                                                                     trunk_vlan_id=vlan_range,
                                                                                     slot=slot)
        else:
            self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(self.tb.dut1.mac)
            self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
            self.xiq.xflowsmanageDevice360.device360_configure_ports_trunk_vlan(port_numbers=port_numbers,
                                                                                trunk_native_vlan="1",
                                                                                trunk_vlan_id=vlan_range)
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        if self.check_add_vlan_range_commands_to_individual(self.tb.dut1.mac, vlan_range, port_numbers):
            print("Found the commands!")
        else:
            pytest.fail("Failed to find the individual add port commands!")

    @mark.tcxm_18697
    @mark.p2
    @mark.testbed_1_node
    def test_check_device_config_after_add_port_individual_commands_update_tcxm_18697(self):
        self.cfg['${TEST_NAME}'] = 'Check Device Config after updating the device with individual add port commands.'
        self.executionHelper.testSkipCheck()
        if self.check_devices_config_after_individual_add_port_push(vlan_range, port_numbers):
            print("The commands that have been pushed, are present on the device's config.")
            pass
        else:
            pytest.fail("The commands that have been pushed, are not present!")

    @mark.tcxm_18698
    @mark.tcxm_18717
    @mark.p1
    @mark.testbed_1_node
    def test_check_delta_cli_delete_port_range_commands_to_individual_tcxm_18698_tcxm_18717(self):
        self.cfg['${TEST_NAME}'] = 'Check Individual Delete Port Commands'
        self.executionHelper.testSkipCheck()
        new_trunk_port = '6'
        for port in port_numbers.split(','):
            if int(new_trunk_port) == int(port):
                pytest.fail("The new trunk port must be different from the initial ones!")
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        if self.tb.dut1.platform == 'Stack':
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):

                def _check_d360_navigation():
                    return self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        self.tb.dut1.mac)
                self.xiq.Utils.wait_till(_check_d360_navigation, timeout=30, delay=5)

                def _check_port_configuration_navigation():
                    return self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
                self.xiq.Utils.wait_till(_check_port_configuration_navigation, timeout=30, delay=5)

                def _check_stack_selection():
                    return self.xiq.xflowsmanageDevice360.select_stack_unit(slot)
                self.xiq.Utils.wait_till(_check_stack_selection, timeout=30, delay=5)

                self.xiq.xflowsmanageDevice360.device360_configure_ports_trunk_stack(port_numbers=port_numbers2,
                                                                                     trunk_native_vlan="1",
                                                                                     trunk_vlan_id=vlan_range,
                                                                                     slot=slot)
            for slot in range(1, len(self.tb.dut1.serial.split(',')) + 1):
                def _check_d360_navigation():
                    return self.xiq.xflowscommonNavigator.navigate_to_device360_page_with_mac(
                        self.tb.dut1.mac)
                self.xiq.Utils.wait_till(_check_d360_navigation, timeout=30, delay=5)

                def _check_port_configuration_navigation():
                    return self.xiq.xflowsmanageDevice360.device360_navigate_to_port_configuration()
                self.xiq.Utils.wait_till(_check_port_configuration_navigation, timeout=30, delay=5)

                def _check_stack_selection():
                    return self.xiq.xflowsmanageDevice360.select_stack_unit(slot)
                self.xiq.Utils.wait_till(_check_stack_selection, timeout=30, delay=5)

                self.xiq.xflowsmanageDevice360.device360_configure_ports_access_vlan_stack(
                                                                                  port_numbers=port_numbers, slot=slot)
        else:
            self.xiq.xflowsmanageDevice360.device360_configure_port_trunk_vlan(device_mac=self.tb.dut1.mac,
                                                                               port_number=new_trunk_port,
                                                                               trunk_native_vlan="1",
                                                                               trunk_vlan_id=vlan_range,
                                                                               port_type="Trunk Port")

            self.xiq.xflowsmanageDevice360.device360_configure_ports_access_vlan(device_mac=self.tb.dut1.mac,
                                                                                 port_numbers=port_numbers,
                                                                                 access_vlan_id="1")
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        if self.check_delete_vlan_range_commands_to_individual(self.tb.dut1.mac, vlan_range, port_numbers):
            print('The individual delete commands have been found.')
        else:
            pytest.fail("Failed to find the individual delete port commands.")

    @mark.tcxm_18699
    @mark.p2
    @mark.testbed_1_node
    def test_check_device_config_after_delete_port_individual_commands_update_tcxm_18699(self):
        self.cfg['${TEST_NAME}'] = 'Check Device Config after updating the device with individual delete port commands.'
        self.executionHelper.testSkipCheck()
        if self.check_devices_config_after_individual_delete_port_push(port_numbers, vlan_range):
            print('The individual delete commands have been pushed to the device.')
        else:
            pytest.fail("Some or all ports are still configured on trunk.")
