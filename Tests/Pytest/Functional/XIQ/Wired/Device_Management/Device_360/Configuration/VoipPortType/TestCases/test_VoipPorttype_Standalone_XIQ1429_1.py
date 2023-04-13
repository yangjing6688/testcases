# Author        : Siva prasath
# Description   : This script run the below tests for voip story feature according with XIQ-1429 story
# Testcases     : TCXM_19208, TCXM_19433,TCXM_19476,TCXM_19489,TCXM_19491,TCXM_19494,TCXM_19434,TCXM_19507,TCXM_19562,
#                 TCXM_19579,TCXM_19477,TCXM_19490,TCXM_19630,TCXM_19681,TCXM_19688,TCXM_19690,TCXM_19695,TCXM_19697,TCXM_19699,
#                 TCXM_19705,TCXM_19735,TCXM_19736
# Pre-Requests  : First organization should be created in the XIQ prior to start this test script in case of AIO.
#                 In cloud it is not necessary.
# Comments      : This test is applicable for 1 node setup only, the script run for Exos standalone

from pytest_testconfig import config, load_yaml
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from pytest import mark
from pytest import fixture
import pytest
import os
import random,string
import os.path
import re
import sys
from time import sleep
from pprint import pprint
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.XiqLibraryHelper import XiqLibraryHelper
from extauto.common.Utils import Utils
from extauto.common.AutoActions import AutoActions
from ..Resources.SuiteUdks import SuiteUdk
# Function to generate random word of 12 characters
from extauto.common.Screen import Screen

def random_word():
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(5))
    return randword
current_exos_port = 2
# Global Vars
device_serial_list = []
location = "Chennai_"+random_word()
building = "Templesteps_"+random_word()
org = "extreme"+random_word()
floor = "Fourth_"
dut_location = ""
nw_policy = "voippolicy_"+random_word()
sw_template_name = "voip_switch_template_"+random_word()
vr_name ="VR-Mgmt"
local_portType = "testing_"+random_word()

@mark.testbed_1_node
class xiqTests():

    def delete_create_location_organization(self):
        self.xiq.xflowsmanageLocation.create_first_organization("Extreme", "broadway", "newyork", "Romania")
        self.xiq.xflowsmanageLocation.delete_location_building_floor(org, location, building)
        self.xiq.xflowsmanageLocation.create_location_building_floor(org, location, building)

    # A method to logout of the XIQ instance
    def deactivate_xiq_libaries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None
        # To get the virtual router info

    def get_virtual_router(self, dut_name, mgmtip):
        global vr_name
        # Send a command "show vlan" to switch and get the output
        result = self.devCmd.send_cmd(dut_name, 'show vlan', max_wait=10, interval=2)
        # getting the command output from the result object as a string as given below
        output = result[0].cmd_obj.return_text
        # create a regex pattern to match the vlan that contains a testbed mgmt ip to find it's virtual router info
        pattern = f'(\w+)(\s+)(\d+)(\s+)({mgmtip})(\s+)(\/.*)(\s+)(\w+)(\s+/)(.*)(VR-\w+)'
        # match variable contains a Match object.
        match = re.search(pattern, output)
        if match:
            print(f"Mgmt Vlan Name : {match.group(1)}")
            print(f"Vlan ID        : {match.group(3)}")
            print(f"Mgmt Ipaddress : {match.group(5)}")
            print(f"Active Ports   : {match.group(9)}")
            print(f"Total Ports    : {match.group(11)}")
            print(f"Virtual Router : {match.group(12)}")
            # return the vr info only if there is an active port in the mgmt vlan
            if int(match.group(9)) > 0:
                vr_name = match.group(12)
                return match.group(12)
            else:
                print(f"There is no active port in the mgmt vlan {match.group(1)}")
                return -1
        else:
            print("Pattern not found, unable to get the virtual router info!")
            return -1
    def generate_cli_locally(self,configs_list,ports=2,vlan_voice=77,vlan_data=78,voicevlan_alpha="VLAN_0077"):

        configs = ["configure vlan %s add port %s untagged",                    #0
                   "configure vlan %s add port %s tagged",                      #1
                   "configure lldp ports %s advertise vendor-specific med capabilities",#2
                   "configure lldp ports %s advertise system-capabilities",#3
                   "configure lldp ports %s advertise vendor-specific dot1 vlan-name vlan %s",#4
                   "configure lldp ports %s advertise vendor-specific dot1 port-protocol-vlan-id vlan %s",#5
                   "configure lldp ports %s advertise vendor-specific med policy application voice vlan %s dscp 10",#6
                   "configure lldp ports %s advertise vendor-specific med policy application voice-signaling vlan %s dscp 10",#7
                   "configure cdp voip-vlan %s ports %s",#8
                   "configure cdp power-available advertise ports %s", #9
                    ]

        configurationList = []
        for each in configs_list:
            if each == 0:
                configurationList.append((configs[each] % (vlan_data, ports)))
            if each == 1:
                configurationList.append((configs[each] % (vlan_voice, ports)))
            if each in [2,3]:
                configurationList.append((configs[each] % (ports)))
            if each in [4, 5, 6, 7]:
                configurationList.append((configs[each] % (ports, voicevlan_alpha)))
            if each == 8:
                configurationList.append((configs[each] % (voicevlan_alpha,ports)))
            if each == 9:
                configurationList.append((configs[each] % (ports)))

        return configurationList

    def Configure_iqagent(self, os, dut_name, serial):
        if os == "exos":

            self.devCmd.send_cmd_verify_output(dut_name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
            self.devCmd.send_cmd(dut_name, 'disable iqagent', max_wait=10, interval=2,confirmation_phrases='Do you want to continue?',confirmation_args='y')
            self.devCmd.send_cmd(dut_name, 'configure iqagent server ipaddress None', max_wait=10, interval=2)

            self.devCmd.send_cmd(dut_name, 'configure iqagent server ipaddress ' + self.cfg['sw_connection_host'],
                             max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'enable iqagent', max_wait=10, interval=2)
            sleep(10)
        elif os == "voss":

            self.devCmd.send_cmd(dut_name, 'configure terminal', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'application', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'no iqagent enable', max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'iqagent server ' + self.cfg['sw_connection_host'],
                                 max_wait=10, interval=2)
            self.devCmd.send_cmd(dut_name, 'iqagent enable', max_wait=10, interval=2)
            self.devCmd.send_cmd_verify_output(dut_name, 'show application iqagent', 'true', max_wait=30,
                                               interval=10)
            self.devCmd.send_cmd(dut_name, 'exit', max_wait=10, interval=2)
            sleep(10)

        else:
            pytest.fail("No device os found")
        sleep(2)

    @classmethod
    def setup_class(cls):
        try:
            cls.executionHelper = PytestExecutionHelper()

            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config
            cls.screen = Screen()
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'
            cls.defaultLibrary = DefaultLibrary()
            # Create a shorter version for the UDKs
            cls.udks = cls.defaultLibrary.apiUdks
            dut_location = location + "," + building + "," + floor
            if cls.tb.dut1.cli_type == "voss" or cls.tb.dut1_platform.lower() == "stack":
                pytest.skip("This platform {} is not supported for this feature!".format(cls.tb.dut1.cli_type))
            cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend
            cls.xiq = XiqLibrary()
            cls.xiq.login.login_user(cls.tb.config.tenant_username, cls.tb.config.tenant_password, url=cls.tb.config.test_url,
                                     IRV=True)


            cls.utils = Utils()
            cls.auto_actions = AutoActions()
            cls.udks = cls.defaultLibrary.apiUdks
            cls.suite_udk = SuiteUdk(cls)
            dut = cls.suite_udk.get_dut(os="exos")
            assert dut, "Failed to find a dut in tb"
            cls.dut = dut
            # Call the setup
            cls.udks.setupTeardownUdks.networkElementConnectionManager.connect_to_all_network_elements()

            cls.delete_create_location_organization(cls)

            if cls.xiq.xflowscommonDevices.search_device(device_mac=cls.tb.dut1.mac, ignore_failure=True) == 1:
                print(f'Found device using mac-address {cls.tb.dut1.mac}')
                cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
            else:
                for a_serial in cls.tb.dut1_serial.split(","):
                    if cls.xiq.xflowscommonDevices.search_device(device_serial=a_serial, ignore_failure=True) == 1:
                        print(f'Found device using serial-number {a_serial}')
                        cls.xiq.xflowscommonDevices.delete_device(device_serial=a_serial)
                    else:
                        print(f'Did not find device with mac-address {cls.tb.dut1.mac} or serial number(s) {cls.tb.dut1_serial}')

            if cls.tb.dut1.make == "exos":
                cls.get_virtual_router(cls,cls.tb.dut1_name, cls.tb.dut1.ip)
            cls.Configure_iqagent(cls, cls.tb.dut1.cli_type, cls.tb.dut1_name, cls.tb.dut1.serial)
            if cls.tb.dut1.cli_type == "exos":
                res = cls.xiq.xflowsmanageSwitch.onboard_switch(cls.tb.dut1.serial, device_os=cls.tb.dut1.cli_type,
                                                                entry_type="Manual", location=dut_location)

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        if cls.xiq.xflowscommonDevices.search_device(device_mac=cls.tb.dut1.mac, ignore_failure=True) == 1:
            print(f'Found device using mac-address {cls.tb.dut1.mac}')
            cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
        else:
            for a_serial in cls.tb.dut1_serial.split(","):
                if cls.xiq.xflowscommonDevices.search_device(device_serial=a_serial, ignore_failure=True) == 1:
                    print(f'Found device using serial-number {a_serial}')
                    cls.xiq.xflowscommonDevices.delete_device(device_serial=a_serial)
                else:
                    print(f'Did not find device with mac-address {cls.tb.dut1.mac} or serial number(s) {cls.tb.dut1_serial}')
        cls.screen.save_screen_shot()
        cls.xiq.xflowsmanageLocation.delete_location_building_floor(org, location, building)
        cls.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(nw_policy)
        cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(sw_template_name)
        cls.xiq.xflowsconfigureCommonObjects.delete_port_type_profile(local_portType)

        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()

    def inc_port(cls):
        global current_exos_port
        current_exos_port += 1
        return current_exos_port

    @mark.p1
    @mark.testbed_1_node
    @mark.tcxm_19208
    @mark.itsanity
    def test_Create_VOIP_Port_type_at_template_Level(self):
        """Test Objective: Create VOIP Port type at template Level"""
        self.executionHelper.testSkipCheck()

        model_act = []

        if self.tb.dut1_platform.lower() == "stack":
            device_serial_list = self.tb.dut1.serial.split(",")
            for i in range(1, len(device_serial_list)+1):
                slots = 'self.tb.dut1.stack.slot' + str(i) + '.model'
                val= eval(slots)
                model_act.append(val)
        sw_model,model_units = self.xiq.xflowsconfigureSwitchTemplate.generate_template_name(self.tb.dut1_platform.lower(),
                                                                                      self.tb.dut1.serial, self.tb.dut1.model,model_act)
        navigate = self.xiq.xflowscommonNavigator.navigate_to_devices()
        navigation = self.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(nw_policy)
        if navigation !=1:
            pytest.fail("Cannot navigate and create Network policy")

        template_creation = self.xiq.xflowsconfigureSwitchTemplate.add_sw_template(nw_policy, sw_model, sw_template_name, self.tb.dut1.cli_type)
        if template_creation != 1:
            pytest.fail("Cannot create to Network template...")
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        sleep(10)
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(nw_policy, sw_template_name, self.tb.dut1.cli_type)
        sleep(3)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        sleep(10)
        self.xiq.xflowsmanageDevice360.create_voice_port(
                port="2", port_type_name=local_portType, voice_vlan ="77", data_vlan="78", lldp_voice_options_flag=False,
                cdp_voice_options_flag=False)
        sleep(10)
        self.xiq.xflowsconfigureSwitchTemplate.switch_template_save()
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowsmanageDevices.refresh_devices_page()
        # TEMPORARY SLEEP UNTIL XIQ BUG IS FIXED
        sleep(10)
        assign = self.xiq.xflowsmanageDevices.assign_network_policy_to_switch_mac(nw_policy,self.tb.dut1.mac)
        if not assign:
            pytest.fail("testcase has failed")

    @mark.p1
    @mark.testbed_1_node
    @mark.tcxm_19433
    @mark.itsanity
    def test_In_new_port_type_editor_Phone_with_Data_Port_should_present(self):
        """In new port type editor - "Phone with a Data Port" should present"""
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonDevices.revert_device_to_template_but_donot_update(self.tb.dut1.mac)
        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        sleep(5)
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(nw_policy, sw_template_name, self.tb.dut1.cli_type)
        sleep(3)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        sleep(10)
        self.xiq.xflowsmanageDevice360.edit_voice_port_type(port_type_name=local_portType,
                                                                           lldp_voice_options_flag=False,
                                                                           cdp_voice_options_flag=False)
        sleep(2)
        editPorttype = self.xiq.xflowsmanageDevice360.edit_voice_port_type(
                port_type_name=local_portType, lldp_voice_options_flag=True,
                lldp_voice_vlan_dscp=10, lldp_voice_signaling_dscp=10,
                lldp_advertisment_of_med_voice_vlan_flag=True,
                lldp_advertisment_of_med_signaling_vlan_flag=True,
                cdp_voice_options_flag=True)
        if editPorttype !=1:
            pytest.fail("the testcase has failed")
        sleep(5)
        self.xiq.xflowsconfigureSwitchTemplate.switch_template_save()
        self.xiq.xflowscommonNavigator.navigate_to_devices()

    @mark.p1
    @mark.testbed_1_node
    @mark.tcxm_19476
    @mark.itsanity
    def test_verify_template_voice_view_when_lldp_cdp_advertisements_are_disabled(self):
        """Verify Template voice view - when lldp and cdp advertisements are disabled"""
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonDevices.refresh_devices_page()
        sleep(20)
        self.xiq.xflowscommonDevices.refresh_devices_page()
        deltaconfigs = self.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta(self.tb.dut1.mac)
        expectedCli = self.generate_cli_locally([0, 1, 2, 3, 4, 5, 8], 2, 77, 78, "VLAN_0077")
        print(expectedCli)
        for eachcli in expectedCli:
            if eachcli not in deltaconfigs:
                pytest.fail("Expected CLI: %s Not present in Delta"%( eachcli))

    @mark.p1
    @mark.testbed_1_node
    @mark.tcxm_19489
    @mark.itsanity
    def test_verify_template_voice_view_when_lldp_disabled_cdp_advertisements_are_enabled(self):
        """ Verify Template voice view - when lldp advertisement - disabled & cdp advertisements - enabled"""

        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        # sleep(10)
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(nw_policy, sw_template_name, self.tb.dut1.cli_type)
        sleep(3)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        sleep(10)
        self.xiq.xflowsmanageDevice360.edit_voice_port_type(port_type_name=local_portType,
                                                                           lldp_voice_options_flag=False,
                                                                           cdp_voice_options_flag=False)
        sleep(2)
        editPorttype = self.xiq.xflowsmanageDevice360.edit_voice_port_type(
                port_type_name=local_portType, lldp_voice_options_flag=False, cdp_voice_options_flag=True)
        if editPorttype !=1:
            pytest.fail("the testcase has failed")
        sleep(5)

        self.xiq.xflowsconfigureSwitchTemplate.switch_template_save()
        self.xiq.xflowscommonNavigator.navigate_to_devices()

        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonDevices.refresh_devices_page()
        sleep(10)
        self.xiq.xflowscommonDevices.refresh_devices_page()
        deltaconfigs = self.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta(self.tb.dut1.mac)
        expectedCli = self.generate_cli_locally([0, 1, 8, 9], 2, 77, 78, "VLAN_0077")
        print("expected cli ==>>>>", expectedCli)
        for eachcli in expectedCli:
            print("expected cli ==>>>>", eachcli)
            if eachcli not in deltaconfigs:
                pytest.fail("Expected CLI: %s Not present in Delta"%( eachcli))
        self.xiq.xflowscommonNavigator.navigate_to_devices()

    @mark.p1
    @mark.testbed_1_node
    @mark.tcxm_19491
    @mark.itsanity
    def test_verify_template_voice_view_when_lldp_enabled_med_voice_vlan_enabled_cdp_advertisements_are_disabled(self):
        """ Verify Template voice view - when lldp advertisement - enabled and MED  Voice VLAN/DSCP	"""
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        # sleep(10)
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(nw_policy, sw_template_name, self.tb.dut1.cli_type)
        sleep(3)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        sleep(10)
        self.xiq.xflowsmanageDevice360.edit_voice_port_type(port_type_name=local_portType,
                                                                           lldp_voice_options_flag=False,
                                                                           cdp_voice_options_flag=False)
        sleep(2)
        editPorttype = self.xiq.xflowsmanageDevice360.edit_voice_port_type(port_type_name=local_portType,
            lldp_voice_options_flag=True,voice_vlan=77,data_vlan=78, dot1_vlan_id_flag=True, lldp_advertisment_of_med_voice_vlan_flag=True,
            lldp_voice_vlan_dscp=10, cdp_voice_options_flag=False)

        sleep(10)
        editPorttype = self.xiq.xflowsmanageDevice360.edit_voice_port_type(port_type_name=local_portType,
            lldp_voice_options_flag=None, dot1_vlan_id_flag=False, lldp_advertisment_of_med_voice_vlan_flag=None,
            cdp_voice_options_flag=None)
        if editPorttype !=1:
            pytest.fail("the testcase has failed")
        sleep(5)
        self.xiq.xflowsconfigureSwitchTemplate.switch_template_save()
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonDevices.refresh_devices_page()
        sleep(20)
        self.xiq.xflowscommonDevices.refresh_devices_page()
        deltaconfigs = self.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta(self.tb.dut1.mac)

        expectedCli = self.generate_cli_locally([0, 1, 2, 6], 2, 77, 78, "VLAN_0077")
        print("expectedCli==>",expectedCli)

        for eachcli in expectedCli:
            if eachcli not in deltaconfigs:
                print("each cli -->",eachcli)
                pytest.fail("Expected CLI: %s Not present in Delta", eachcli)
            print("Expected CLI %s present in Delta"%(eachcli))
        self.xiq.xflowscommonNavigator.navigate_to_devices()

    @mark.p1
    @mark.testbed_1_node
    @mark.tcxm_19494
    @mark.itsanity
    def test_verify_template_voice_view_when_lldp_disabled_cdp_advertisements_are_enabled_voice_vlan_enabled(self):
        """ Verify Template voice view - cdp advertisements - enabled and Enable CDP advertisement of Voice VLAN"""
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        # sleep(10)
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(nw_policy, sw_template_name, self.tb.dut1.cli_type)
        sleep(3)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        sleep(10)
        #Resetting to disable
        self.xiq.xflowsmanageDevice360.edit_voice_port_type(port_type_name=local_portType, lldp_voice_options_flag=False,
                                                            cdp_voice_options_flag=True)
        sleep(10)
        editPorttype = self.xiq.xflowsmanageDevice360.edit_voice_port_type(
                port_type_name=local_portType, cdp_voice_options_flag=None,cdp_advertisment_of_power_available_flag=False)
        self.screen.save_screen_shot()
        if editPorttype !=1:
            pytest.fail("the testcase has failed")
        sleep(5)

        self.xiq.xflowsconfigureSwitchTemplate.switch_template_save()
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonDevices.refresh_devices_page()
        sleep(20)
        self.xiq.xflowscommonDevices.refresh_devices_page()
        deltaconfigs = self.xiq.xflowsmanageDeviceConfig.get_device_config_audit_delta(self.tb.dut1.mac)

        expectedCli = self.generate_cli_locally([0, 1, 8], 2, 77, 78, "VLAN_0077")
        print(expectedCli)

        for eachcli in expectedCli:
            if eachcli not in deltaconfigs:
                pytest.fail("Expected CLI: %s Not present in Delta", eachcli)

        self.xiq.xflowscommonNavigator.navigate_to_devices()

    @mark.p2
    @mark.testbed_1_node
    @mark.tcxm_19434
    @mark.itsanity
    def test_verify_voice_vlan_and_data_vlan_is_visible_on_selection_phone_with_a_data_port(self):
        """ Check Voice VLAN and Data VLAN can be created"""
        self.xiq.xflowscommonNavigator.navigate_to_devices()
        self.xiq.xflowscommonNavigator.navigate_configure_network_policies()
        # sleep(10)
        self.xiq.xflowsconfigureSwitchTemplate.select_sw_template(nw_policy, sw_template_name, self.tb.dut1.cli_type)
        sleep(3)
        self.xiq.xflowsconfigureSwitchTemplate.go_to_port_configuration()
        sleep(10)
        self.xiq.xflowsmanageDevice360.edit_voice_port_type(port_type_name=local_portType,
                                                                           lldp_voice_options_flag=False,
                                                                           cdp_voice_options_flag=False)
        sleep(2)
        editPorttype = self.xiq.xflowsmanageDevice360.edit_voice_port_type(
                port_type_name=local_portType, data_vlan=30, voice_vlan=40,lldp_voice_options_flag=False,cdp_voice_options_flag=False)

        if editPorttype !=1:
            pytest.fail("the testcase has failed")
        sleep(5)

        self.xiq.xflowsconfigureSwitchTemplate.switch_template_save()
        self.xiq.xflowscommonNavigator.navigate_to_devices()
