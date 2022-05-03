# Author        : Natarajan Periannan
# Description   : XIQ-1396 Support upgrade EXOS stacks (5320,5420,5520,x440g2) without policy assignment
# Test Cases    : TC_XIM_15977, TC_XIM_15978
# Date Updated  : 07-Apr-2022
# Pre-Requests  : First organization should be created in the XIQ prior to start this test script
# Comments      : This test is applicable for exos stack devices(5520/5420/5320/X440G2) only


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
import random
import string
from extauto.common.Utils import Utils
import extauto.xiq.flows.common.ToolTipCapture as tool_tip


# Function to generate random word of 12 characters
def random_word():
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(12))
    return randword


# Global Vars
device_serial_list = []
location = "Chennai_"+random_word()
building = "Templesteps_"+random_word()
floor = "Fourth_"
DUT_LOCATION = ""

"""
# To Run this script in command line from the test case directory:

pytest --tc-file /automation/tests/extreme_automation_tests/Environments/environment.local.chrome.yaml --tc-file /automation/tests/extreme_automation_tests/Environments/topo.test.int1r1.nperiannan.yaml --tc-file /automation/tests/extreme_automation_tests/TestBeds/CHENNAI/Dev/5420_3nodes_stack4_chennai.yaml test_xiq_1396_exos_firmware_upgrade_without_policy.py -v

"""


@mark.testbed_1_node    # Marked all test cases as 1 node
class xiqTests():

    # A method to login into the XIQ instance
    def init_xiq_libaries_and_login(self, username, password, capture_version=False, code="default", url="default", incognito_mode="False"):
        self.xiq = XiqLibrary()
        time.sleep(5)
        res = self.xiq.init_xiq_libaries_and_login(username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
        if res != 1:
            pytest.fail('Could not Login')

    # A method to logout of the XIQ instance
    def deactivate_xiq_libaries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None

    # [Setup] Test class setup
    @classmethod
    def setup_class(cls):
        
        """
        This class is used to login to XIQ and onboard the exos stack device in the testbed.yaml file

        """

        try:
            # Create pytest execution helper
            cls.executionHelper = PytestExecutionHelper()

            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config

            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'

            # Skipping the setup and test case execution in case the platform is not an exos-stack
            if cls.tb.dut1_platform.lower() != 'stack':
                pytest.skip("This platform {} is not supported for this feature!".format(cls.tb.dut1.os))
                
            # Getting the list of Stack nodes serial numbers from the testbed file
            device_serial_list = cls.tb.dut1.serial.split(",")
            dutMac = cls.tb.dut1.mac
            dutName = cls.tb.dut1_name
            iqagentServer = cls.cfg['sw_connection_host']
            vrName = "vr-Mgmt"
            floor = "Fourth_"+str(dutMac)                       # Mac address is appended in floor
            DUT_LOCATION = location+","+building+","+floor
            
            # Suite setup, just login to the xiq client and connect all the netelements
            def suite_setup (cls):
                # Create new objects to use in test. Here we will import everything from the default library
                cls.defaultLibrary = DefaultLibrary()
                cls.udks = cls.defaultLibrary.apiUdks
                cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend
                
                cls.xiq = XiqLibrary()
                cls.xiq.login.login_user(cls.tb.config.tenant_username,
                                         cls.tb.config.tenant_password,
                                         url=cls.tb.config.test_url,
                                         IRV=True)

                # Make connections to all the netlement(s) in testbed.yaml file
                cls.udks.setupTeardownUdks.networkElementConnectionManager.connect_to_all_network_elements()

            # Preparing the mapo add the device into the proper location building and floor
            def createLocation (cls):
                # Delete the netelement-1 device from XIQ if it is already onboarded prior to delete the location buildig floor
                result = cls.xiq.xflowscommonDevices.delete_device(device_mac = dutMac)
                if result != 1:
                    pytest.fail("Could not delete the device with mac {}".format(dutMac))

                # Creating a location building floor. Creating the org prior to create any location information.
                cls.xiq.xflowsmanageLocation.create_first_organization("Extreme", "broadway", "newyork", "Romania")

                # Creating the above mentioned location building and floor
                cls.xiq.xflowsmanageLocation.create_location_building_floor(location, building, floor)
                time.sleep(5)

            # Onboarding EXOS device(s)
            def exosDeviceOnboard (cls):
                # Onboarding the exos stack device dut1 from testbed.yaml file using serial numbers
                result = cls.xiq.xflowsmanageSwitch.onboard_switch( cls.tb.dut1.serial, 
                                                                    device_os = "Switch Engine", 
                                                                    entry_type= "Manual", 
                                                                    location= DUT_LOCATION )
                if result != 1:
                    pytest.fail("Onboard is not successful for all the devices.")
                time.sleep(5) 

            def netelementIqagentConfig (cls):
                # An existing iqagent configs will be removed from device prior to configure the iqagent
                cls.devCmd.send_cmd(dutName, 'configure iqagent server ipaddress none', max_wait=10,interval=2)
                cls.devCmd.send_cmd(dutName, 'configure iqagent server vr none', max_wait=10,interval=2)

                # Verify the state of the XIQ agent is up/ready on the dut1(netelement-1)
                cls.devCmd.send_cmd_verify_output(dutName, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                
                vrConfig = "configure iqagent server vr " + vrName
                # Configuring and enabling iqagent on netlement-1 based on the environment passed to the test script
                cls.devCmd.send_cmd(dutName, 'configure iqagent server ipaddress ' + iqagentServer, max_wait=10,interval=2)
                cls.devCmd.send_cmd(dutName, vrConfig, max_wait=10,interval=2)
                cls.devCmd.send_cmd(dutName, 'enable iqagent', max_wait=10,interval=2)
                               
                # Verify the iqagent status is connected within the time intervel of 60 seconds
                cls.devCmd.send_cmd_verify_output_regex(dutName, 'show iqagent', 'Status*.*CONNECTED TO XIQ', max_wait=180, interval=10)

            # Check for the stack onboarded is proper and and all the nodes are connected and managed
            def checkStackStatusInxiq (cls):
                # Waiting for 60 seconds, stack master to communicate XIQ
                time.sleep(60)

                # Refreshing the XIQ device page before checking the stack status
                cls.xiq.xflowsmanageDevices.refresh_devices_page()
                time.sleep(10)

                # Step-1: # Wait until the stack icon turn to 'blue' it is in 'red'
                result =  cls.xiq.xflowscommonDevices.get_exos_stack_status(device_mac=dutMac)
                max_wait = 300
                time_elapsed = 0
                while (result == "red" or result == -1 ) and max_wait >= 0 :
                    print (f"\nINFO \tTime elaspsed in waiting for the stack formation is {time_elapsed} seconds \n")
                    time.sleep(10)
                    max_wait -= 10
                    time_elapsed += 10
                    result =  cls.xiq.xflowscommonDevices.get_exos_stack_status(device_mac=dutMac)
                    # Once the max_wait time is elapsed the it will be declared as not onboared successfully 
                    if (result == "red" or result == -1 ) and max_wait == 0 :
                        print ("\nFAILED \t Stack not formed properly, please check.\n")
                        pytest.fail('Expected stack icon colour is blue but found {}, stack not formed properly'.format(result))
                        
                # Unselect the columns that are not required for this test case.
                time.sleep(10)
                cls.xiq.xflowscommonDevices.column_picker_unselect("Template",
                                                                   "Managed By",
                                                                   "Cloud Config Groups",
                                                                   "MGMT IP Address",
                                                                   "Model",
                                                                   "Uptime",
                                                                   "Connected Clients",
                                                                   "Location",
                                                                   "Feature License",
                                                                   "Device License",
                                                                   "WiFi0 Channel",
                                                                   "WiFi0 Power",
                                                                   "WiFi1 Channel",
                                                                   "WiFi1 Power",
                                                                   "WiFi2 Channel",
                                                                   "WiFi2 Power",
                                                                   "MGT VLAN",
                                                                   "NTP State" )
                                                                   
                               
                # select the required coloumns from the device table if it is not selected.
                time.sleep(10)
                cls.xiq.xflowscommonDevices.column_picker_select("Device Status",
                                                                 "Host Name",
                                                                 "Network Policy",
                                                                 "MAC Address",
                                                                 "Serial #",
                                                                 "Stack Unit",
                                                                 "Stack Role",
                                                                 "Managed",
                                                                 "Updated On",
                                                                 "IQAgent",
                                                                 "OS Version" )                 
                                
                # Step-2: # Ensure all the stack members are in managed state under the stack master by checking each slot managed status
                time.sleep(10)
                result = cls.xiq.xflowscommonDevices.verify_stack_devices_managed(dutMac, device_serial_list)
                if result != 1:
                   pytest.fail('Not all the slots are in managed state from the list of serials {}'.format(device_serial_list))

            # Check the device status is green based on the mac address to proceed the testcase execution
            def checkDeviceStatusInxiq (cls):
                result = cls.xiq.xflowscommonDevices.get_device_status(device_mac=dutMac)
                if result != 'green':
                    print ("\nFAILED \tDevice is not in online or not connected to XIQ...\n")
                    pytest.fail('Status not equal to Green: {}'.format(result))
                    
                print (f"\nINFO \t Successfully onboarded the '{cls.tb.dut1_platform}' switch with mac '{dutMac}'.\n")
             
            # EXOS Stack device onboarding and verification for the stack is formed properly and managed
            def onboardStack (cls):
                # The following functions are used to onboard the stack device in XIQ and check the Status of the device is managed.
                suite_setup (cls)
                createLocation (cls)
                exosDeviceOnboard (cls)
                netelementIqagentConfig (cls)
                checkStackStatusInxiq (cls)
                checkDeviceStatusInxiq (cls)
            
            # Calling the exos stack onboard function
            onboardStack (cls)
            
        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    # [Tear Down] Setup Class Cleanup
    @classmethod
    def teardown_class(cls):
        """
        This function used to cleanup the setup when the test is completed or the encounter any issues during the execution

        """
        print("\nINFO \t ++++++++++++++++++++++++++++++++++++++ Setup TearDown Process Started... +++++++++++++++++++++++++++++++++++\n")

        # Unconfigure the IQAgent from the device
        cls.devCmd.send_cmd(cls.tb.dut1_name, 'configure iqagent server ipaddress none', max_wait=10,interval=2)
        cls.devCmd.send_cmd(cls.tb.dut1_name, 'configure iqagent server vr none', max_wait=10,interval=2)
        time.sleep(5)

        # Delete the dut1 switch if it is already onboarded in to the XIQ environment
        result = cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
        if result != 1:
            pytest.fail("Could not delete the device with mac {}".format(cls.tb.dut1.mac))

        # This is to delete the stack member node(s) which is not stacked under the stack master
        for serial in device_serial_list:
            result = cls.xiq.xflowscommonDevices.delete_device(device_serial=serial)
            time.sleep(5)
            if result != 1:
                pytest.fail("Could not delete the device with serial {}".format(serial))
                
        # Reseting the column selection back to it's default value.
        cls.xiq.xflowscommonDevices.column_picker_select("MGMT IP Address",
                                                         "Uptime",
                                                         "Connected Clients",
                                                         "Model",
                                                         "Location",
                                                         "Feature License",
                                                         "Device License",
                                                         "WiFi0 Channel",
                                                         "WiFi0 Power",
                                                         "WiFi1 Channel",
                                                         "WiFi1 Power",
                                                         "WiFi2 Channel",
                                                         "WiFi2 Power",
                                                         "MGT VLAN",
                                                         "NTP State" )
        time.sleep(5)

        floor = "Fourth_"+str(cls.tb.dut1.mac)           # Mac address is appended in floor
        # To Delete the location building floor that was created in the setup_class
        cls.xiq.xflowsmanageLocation.delete_location_building_floor(location, building, floor)
        time.sleep(5)
        
        # Logout XIQ and close the browser
        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()



    # """ Test Cases """

    @mark.xim_tcxm_15977
    @mark.p1
    @mark.testbed_1_node
    def test_15977_check_update_option_stack_device(self):
        
        """
        Description:    TCXM-15977       Verify the firmware upgrade option is available when a stack node is onboarded on XIQ (5520/5420/5320/X440G2) prior to assigning the policy.

        """

        self.cfg['${TEST_NAME}'] = 'test_15977_check_update_option_stack_device'
        # self.executionHelper.testSkipCheck()

        # Check the firmware upgrade option is avilable for the stack device and close the image upgrade without perfrm upgrade.
        latest_version = self.xiq.xflowscommonDevices.xiq_upgrade_device_to_latest_version(self.tb.dut1.mac,action="close")
        if latest_version == -1:
            pytest.fail("Either firmware upgrade option is not available or unable to get the latest firmware version!")

        print("\nINFO \t Firmware upgrade option is available for EXOS stack prior to assigning the Network Policy...\n")



    @mark.xim_tcxm_15978
    @mark.p2
    @mark.testbed_1_node
    def test_15978_check_update_function_stack_device(self):

        """
        Description:    TCXM-15978       Verify the firmware upgrade option is available when a stack node is onboarded on XIQ (5520/5420/5320/X440G2) and check for the firmware upgrade functionality prior to assigning the policy.

        """

        self.cfg['${TEST_NAME}'] = 'test_15978_check_update_function_stack_device'
        # self.executionHelper.testSkipCheck()

        # Clearing the device static log
        self.devCmd.send_cmd(self.tb.dut1_name, 'clear log static', max_wait=10,interval=2)

        # Step-2 Check the firmware upgrade option is avilable for the stack device and able to perform the image upgrade.
        latest_version = self.xiq.xflowscommonDevices.xiq_upgrade_device_to_latest_version(self.tb.dut1.mac)
        if latest_version == -1:
            pytest.fail("Either firmware upgrade option is not available or unable to get the latest firmware version!")

        # Check switch log for download image issued by iqagent on the device
        expecedResult = " Download image from hostname*.*"+str(latest_version)
        self.devCmd.send_cmd_verify_output_regex(self.tb.dut1_name, 'show log',expecedResult, max_wait=300, interval=10)
        # Sleeping for 60 seconds to get this firmware upgrade info to reflect in xiq 
        # time.sleep(60)
        
        # Checking for the update column to refect the firmware update status
        result = self.xiq.xflowscommonDevices.get_device_updated_status(device_mac=self.tb.dut1.mac)
        count = 0
        max_wait = 300
        while ("Firmware Updating" not in result):
            time.sleep(10)
            count += 10
            result = self.xiq.xflowscommonDevices.get_device_updated_status(device_mac = self.tb.dut1.mac)
            print (f"\nINFO \t Time elapsed in the update column to reflect the firmware updating is '{count} seconds'\n")
            if ("Device Update Failed" in result) or (count > max_wait):
                self.devCmd.send_cmd_verify_output_regex(self.tb.dut1_name, 'show log',expecedResult, max_wait=30, interval=10)
                pytest.fail("Device Update Failed for the device with mac {}".format(self.tb.dut1.mac))

        # Checking firmware update status for every 10 seconds for upto 1200 seconds
        result = self.xiq.xflowscommonDevices.get_device_updated_status(device_mac=self.tb.dut1.mac)
        count = 0
        max_wait = 1200
        while ("Firmware Updating" in result) or ("Rebooting" in result):
            time.sleep(10)
            count += 10
            result = self.xiq.xflowscommonDevices.get_device_updated_status(device_mac = self.tb.dut1.mac)
            print (f"\nINFO \t Time elapsed in firmware update: '{count} seconds'\n")
            if ("Device Update Failed" in result) or (count > max_wait):
                self.devCmd.send_cmd_verify_output_regex(self.tb.dut1_name, 'show log',expecedResult, max_wait=30, interval=10)
                pytest.fail("Device Update Failed for the device with mac {}".format(self.tb.dut1.mac))
                
        # This is to validate the XIQ latest firmware is installed/present in the device post upgrade
        self.devCmd.send_cmd_verify_output(self.tb.dut1_name, 'show version', latest_version, max_wait=10, interval=2)

