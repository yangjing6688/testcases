# Author        : Natarajan Periannan
# Description   : APC-34320 - Extreme Firmware upgrade
# Test Cases    : TC_XIM_20120, TC_XIM_20121, TC_XIM_20122, TC_XIM_20123, TC_XIM_20124, TC_XIM_20125, TC_XIM_20677
# Total no Cases: 7
# Date Updated  : 16-May-2022
# Pre-Requests  : First organization should be created in the XIQ prior to start this testing. The firmware images like 
#                 Latest and last supported four images should be copied to the test environment prior to start this test.
# Comments      : These test cases are applicable for EXOS, VOSS and EXOS-STACK devices that are supported by XIQ. 
#                 EXOS is having known bug OS-27245 which will often failed to download the image to device, if the device 
#                 and tftp server in different locations. So it is recommented to run these upgrade tests when both Test
#                 Environment and Testbeds are in the same geological location.
#                 EXOS BUG - EXOS-27245 - download url fails over longhaul connection, but rarely

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


# Function to generate random word of 12 characters
def random_word():
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(12))
    return randword


# Global Vars
device_serial_list = []
location = "Chennai_"+random_word()
building = "Templesteps_"+random_word()
floor = "Fourth_"+random_word()
DUT_LOCATION = location+","+building+","+floor
vr_name = "VR-Mgmt"
defaultColumns='"Template","Host Name","Network Policy","Managed By","Cloud Config Groups","MGMT IP Address","Model","IQAgent","Uptime","Connected Clients", \
                "Location","Feature License","Device License","WiFi0 Channel","WiFi0 Power","WiFi1 Channel","WiFi1 Power", \
                "WiFi2 Channel","WiFi2 Power","MGT VLAN","NTP State"'
columnsToBeSelected = '"Device Status","MAC Address","Serial #","Managed","Updated On","OS Version"'

@mark.testbed_1_node    # Marked all test cases as 1 node
class xiqTests():
    # [Setup] Test class setup
    @classmethod
    def setup_class(cls):
        """ This class is used to login to XIQ and onboard the exos stack device in the testbed.yaml file. """
        try:
            # Create pytest execution helper
            cls.executionHelper = PytestExecutionHelper(defaultAction='fail')
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'
            dut_mac = cls.tb.dut1.mac
            dut_name = cls.tb.dut1_name
            iqagentServer = cls.cfg['sw_connection_host']                
                      
            # To identify the testbed platform is a exos-stack to get the serial numbers in the list
            if cls.tb.dut1_platform.lower() == 'stack' :
                # Getting the list of Stack nodes serial numbers from the testbed file
                device_serial_list = cls.tb.dut1.serial.split(",")
                columnsToBeSelected = '"Device Status","MAC Address","Serial #","Managed","Stack Unit","Stack Role","Updated On","OS Version"'

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

            def get_virtual_router (cls, mgmtip):
                global vr_name
                # Send a command "show vlan" to switch and get the output
                result = cls.devCmd.send_cmd(dut_name, 'show vlan', max_wait=10, interval=2)
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
                    if int(match.group(9)) > 0 :
                        vr_name = match.group(12)
                        return match.group(12)
                    else:
                        print (f"There is no active port in the mgmt vlan {match.group(1)}")
                        return -1
                else:
                    print("Pattern not found, unable to get the virtual router info!")
                    return -1

            # Preparing the mapo add the device into the proper location building and floor
            def create_location (cls):
                # Delete the netelement-1 device from XIQ if it is already onboarded prior to delete the location buildig floor
                result = cls.xiq.xflowscommonDevices.delete_device(device_mac = dut_mac)
                if result != 1:
                    pytest.fail("Could not delete the device with mac {}".format(dut_mac))
                # Creating a location building floor. Creating the org prior to create any location information.
                cls.xiq.xflowsmanageLocation.create_first_organization("Extreme", "broadway", "newyork", "Romania")
                # Creating the above mentioned location building and floor
                cls.xiq.xflowsmanageLocation.create_location_building_floor(location, building, floor)
                time.sleep(5)

            # Onboarding EXOS device(s)
            def onboard_devices (cls):
                # Onboarding the exos/voss and exos stack device from testbed.yaml file defined as dut1 using serial number(s)
                result = cls.xiq.xflowsmanageSwitch.onboard_switch( cls.tb.dut1.serial,
                                                                    device_os = cls.tb.dut1.cli_type,
                                                                    location= DUT_LOCATION )
                if result != 1:
                    pytest.fail("Onboard is not successful for all the devices.")
                time.sleep(5)

            def configure_iqagent(cls):
                if cls.tb.dut1_make.upper() == "EXOS":
                    # To get the vr name updated correctly for the given mgmt ipaddress
                    result = get_virtual_router (cls, cls.tb.dut1.ip)
                    if result == -1:
                        pytest.fail("Unable to get the virtual router info for the given mgmt ip {}".format(cls.tb.dut1.ip))
                    # An existing iqagent configs will be removed from device prior to configuring the iqagent
                    cls.devCmd.send_cmd(dut_name, 'clear log static', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dut_name, 'disable iqagent', max_wait=10, interval=2, confirmation_phrases='Do you want to continue?',confirmation_args='y')
                    cls.devCmd.send_cmd(dut_name, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dut_name, 'configure iqagent server vr none', max_wait=10, interval=2)
                    # Verify the state of the XIQ agent is up/ready on the dut1(netelement-1)
                    cls.devCmd.send_cmd_verify_output(dut_name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                    # Configuring and enabling iqagent on netlement-1 based on the environment passed to the test script
                    cls.devCmd.send_cmd(dut_name, 'configure iqagent server ipaddress ' + iqagentServer, max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dut_name, f'configure iqagent server vr {vr_name}', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dut_name, 'enable iqagent', max_wait=10, interval=2)
                    # Verify the iqagent status is connected within the time intervel of 300 seconds
                    cls.devCmd.send_cmd_verify_output_regex(dut_name, 'show iqagent', 'Status*.*CONNECTED TO XIQ', max_wait=300, interval=10)

                elif cls.tb.dut1_make.upper() == "VOSS":
                    # Configuring and enabling iqagent on netlement-1 based on the environment passed to the test script
                    cls.devCmd.send_cmd(dut_name, 'configure terminal', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dut_name, 'application', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dut_name, 'no iqagent enable', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dut_name, 'iqagent server ' + iqagentServer, max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dut_name, 'iqagent enable', max_wait=10, interval=2)
                    # Verify the iqagent status is connected within the time intervel of 300 seconds
                    cls.devCmd.send_cmd_verify_output(dut_name, 'show application iqagent', 'true', max_wait=10, interval=2)
                    cls.devCmd.send_cmd_verify_output(dut_name, 'show application iqagent', ': connected', max_wait=300, interval=10)
                    cls.devCmd.send_cmd(dut_name, 'exit', max_wait=10, interval=2)

                else:
                    pytest.fail('Device make \'{}\' is not supportted!'.format(cls.tb.dut1_make))
                    
                # Waiting for 60 seconds, device to ommunicate XIQ and XIQ to process the data
                time.sleep(60)

            # Check for the stack onboarded is proper and and all the nodes are connected and managed
            def check_device_status_connected(cls):
                # Refreshing the XIQ device page before checking the stack status
                cls.xiq.xflowsmanageDevices.refresh_devices_page()
                time.sleep(10)
                
                # Unselect the columns that are not required for this test case.
                # cls.xiq.xflowscommonDevices.column_picker_unselect(defaultColumns)
                cls.xiq.xflowscommonDevices.column_picker_unselect("Template",
                                                                   "Managed By",
                                                                   "Host Name",
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
                                                                   "NTP State")
                time.sleep(10)
                
                # select the required coloumns from the device table if it is not selected.
                # cls.xiq.xflowscommonDevices.column_picker_select(columnsToBeSelected)
                cls.xiq.xflowscommonDevices.column_picker_select("Device Status",
                                                                 "Network Policy",
                                                                 "MAC Address",
                                                                 "Serial #",
                                                                 "Stack Unit",
                                                                 "Stack Role",
                                                                 "Managed",
                                                                 "Updated On",
                                                                 "IQAgent",
                                                                 "OS Version")
                
                # Refreshing the XIQ device page before checking the stack status
                cls.xiq.xflowsmanageDevices.refresh_devices_page()
                time.sleep(10)
                # This is specific to the EXOS stack setup onboard validation
                if (cls.tb.dut1_platform.lower() == 'stack'):
                    # Step-1: # Wait until the stack icon turn to 'blue' it is in 'red'
                    result =  cls.xiq.xflowscommonDevices.get_exos_stack_status(device_mac=dut_mac)
                    max_wait = 300
                    time_elapsed = 0
                    while (result == "red" or result == -1 ) and max_wait >= 0 :
                        print (f"\nINFO \tTime elaspsed in waiting for the stack formation is {time_elapsed} seconds \n")
                        time.sleep(10)
                        max_wait -= 10
                        time_elapsed += 10
                        result =  cls.xiq.xflowscommonDevices.get_exos_stack_status(device_mac=dut_mac)
                        # Once the max_wait time is elapsed the it will be declared as not onboared successfully
                        if (result == "red" or result == -1 ) and max_wait == 0 :
                            print ("\nFAILED \t Stack not formed properly, please check.\n")
                            pytest.fail('Expected stack icon colour is blue but found {}, stack not formed properly'.format(result))
                    # Step-2: # Ensure all the stack members are in managed state under the stack master by checking each slot managed status
                    time.sleep(10)
                    result = cls.xiq.xflowscommonDevices.verify_stack_devices_managed(dut_mac, device_serial_list)
                    if result != 1:
                       pytest.fail('Not all the slots are in managed state from the list of serials {}'.format(device_serial_list))
                # This code specific to EXOS/VOSS Standalone devices
                else:
                    # Check the device status is online and green based on the mac address to proceed the testcase execution
                    result = cls.xiq.xflowscommonDevices.get_device_status(device_mac=dut_mac)
                    if result != 'green':
                        print ("\nFAILED \t Device is not in online or not connected to XIQ...\n")
                        pytest.fail('Status not equal to Green: {}'.format(result))
                print (f"\nINFO \t Successfully onboarded the '{cls.tb.dut1_platform}' device make '{cls.tb.dut1_make}'.\n")

            # EXOS/VOSS NOS device onboarding and verification
            def onboarding_functions (cls):
                suite_setup (cls)
                create_location (cls)
                onboard_devices (cls)
                configure_iqagent (cls)
                check_device_status_connected (cls)

            # Calling the NOS devices onboarding functions
            onboarding_functions(cls)

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    # [Tear Down] Setup Class Cleanup
    @classmethod
    def teardown_class(cls):
        """
        This function used to cleanup the setup when the test is completed or the encounter any issues during the execution
        """
        print("\nINFO \t ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("INFO \t ++                                     Setup TearDown Process Started                                     ++")
        print("INFO \t ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

        # Unconfigure the IQAgent config from the device
        if cls.tb.dut1_make.upper() == "EXOS":
            cls.devCmd.send_cmd(cls.tb.dut1_name, 'configure iqagent server ipaddress none', max_wait=10,interval=2)
            cls.devCmd.send_cmd(cls.tb.dut1_name, 'configure iqagent server vr none', max_wait=10,interval=2)
        elif cls.tb.dut1_make.upper() == "VOSS":
            cls.devCmd.send_cmd(cls.tb.dut1_name, 'configure terminal', max_wait=10, interval=2)
            cls.devCmd.send_cmd(cls.tb.dut1_name, 'application', max_wait=10, interval=2)
            cls.devCmd.send_cmd(cls.tb.dut1_name, 'no iqagent enable', max_wait=10, interval=2)
            cls.devCmd.send_cmd(cls.tb.dut1_name, 'exit', max_wait=10, interval=2)    
        time.sleep(5)

        # Reseting the column selection back to it's default value.
        cls.xiq.xflowscommonDevices.column_picker_select("MGMT IP Address",
                                                         "Uptime",
                                                         "Host Name",
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
                                                         "NTP State")
        time.sleep(10)

        # Delete the dut1 switch if it is already onboarded in to the XIQ environment
        result = cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
        if result != 1:
            pytest.fail("Could not delete the device with mac {}".format(cls.tb.dut1.mac))

        # This is to delete the stack member node(s) which is not stacked under the stack master
        if (cls.tb.dut1_platform.lower() == 'stack'):
            for serial in device_serial_list:
                result = cls.xiq.xflowscommonDevices.delete_device(device_serial=serial)
                time.sleep(5)
                # if result != 1:
                   # pytest.fail("Could not delete the device with serial {}".format(serial))

        # To Delete the location building floor that was created in the setup_class
        cls.xiq.xflowsmanageLocation.delete_location_building_floor(location, building, floor)
        time.sleep(5)

        # Logout XIQ and close the browser
        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()



    # Methods required for the test cases
    
    # This is used to generate the heading with box
    def boxHeading(self, content):
        """ This method used to create a boxed label and the text will be in the center of the box """
        total_length = 130
        if len(content)%2 != 0: 
            total_length += 1
        freespace = total_length-len(content)
        multiplier = int(freespace/2)
        print("\n\n\t+"+"+"*total_length+"+")
        if len(content) <= 130:
            print("\t+"+" "*multiplier+content+" "*multiplier+"+")
        else:
            print("\t+"+content+"+")
        print("\t+"+"+"*total_length+"+\n\n")


    # This is used to perform the prec condition of the network element 
    def preCheck (self,test_case):
        """
        This method used to validate the EXOS Stack status and to clear the logs prior to start the test on EXOS
        """
        testid = test_case.split("_")[1]
        self.boxHeading(f"T.C-{testid} pre-check started...")
        time.sleep(60)
        if self.tb.dut1_make.upper() == "EXOS":
            self.devCmd.send_cmd(self.tb.dut1_name, 'show version', max_wait=10, interval=2)
            self.devCmd.send_cmd(self.tb.dut1_name, 'show switch', max_wait=10, interval=2)
            self.devCmd.send_cmd(self.tb.dut1_name, 'clear log static', max_wait=10, interval=2)
            if (self.tb.dut1_platform.upper() == 'STACK'):
                slotcount = len (self.tb.dut1.serial.split(','))
                result = self.devCmd.send_cmd(self.tb.dut1_name, f'show switch | grep (Image Booted:)', max_wait=10, interval=2)
                output = result[0].cmd_obj.return_text
                pattern = f'(\s+Image Booted:\s+)(\w+)(\s+)(\w+)(\s+)'
                match = re.search(pattern, output)
                partition = match.group(2)
                if slotcount > 1:
                    self.devCmd.send_cmd_verify_output(self.tb.dut1_name, f'show slot | grep "Operational" | count', f'Total lines: {slotcount}', max_wait=10, interval=2)
                    self.devCmd.send_cmd_verify_output(self.tb.dut1_name, f'show slot detail | grep (Image Booted:\s+)({partition}) | count',  f'Total lines: {slotcount}',max_wait=10, interval=2)
                else:
                    pytest.skip("Either all slots are not in 'Operational' state or Image Booted from different partitions...")      
                self.devCmd.send_cmd(self.tb.dut1_name, 'show version images', max_wait=10, interval=2)
        else:
            self.devCmd.send_cmd(self.tb.dut1_name, 'show sys software | include Version', max_wait=10, interval=2)
            self.devCmd.send_cmd(self.tb.dut1_name, 'clear logging', max_wait=10, interval=2)
        time.sleep(5)


    # This is to collect the logs when a test case is failed.
    def collectLogs (self, test_case):
        """
        This method used to collect the device logs in case of test case failed on EXOS devices
        """
        testid = test_case.split("_")[1]
        self.boxHeading(f"T.C-{testid} is failed, collecting logs...")
        if self.tb.dut1_make.upper() == "EXOS":
            self.devCmd.send_cmd(self.tb.dut1_name, 'show version', max_wait=10, interval=2)
            self.devCmd.send_cmd(self.tb.dut1_name, 'show log', max_wait=10, interval=2)
            self.devCmd.send_cmd(self.tb.dut1_name, 'clear log static', max_wait=10, interval=2)
        else:
            self.devCmd.send_cmd(self.tb.dut1_name, 'show sys software | include Version', max_wait=10, interval=2)
            self.devCmd.send_cmd(self.tb.dut1_name, 'show logging file detail', max_wait=10, interval=2)
            self.devCmd.send_cmd(self.tb.dut1_name, 'clear logging', max_wait=10, interval=2)
        time.sleep(30)
        pytest.fail('{} is failed...'.format(test_case))
        



    # """ Test Cases """ 

    @mark.xim_tcxm_20120
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20120_update_to_latest_version_and_check_update_same_version_option (self):
        """
        Description:    TCXM-20120       Verify the firmware upgrade function to the latest version even if versions are the same
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20120_update_to_latest_version_and_check_update_same_version_option'
        self.executionHelper.testSkipCheck()
        
        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac)
        if result == -1: self.collectLogs(test_case)



    @mark.xim_tcxm_20121
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20121_update_to_latest_version_and_uncheck_the_update_same_version_option (self):
        """
        Description:    TCXM-20121       Verify the firmware upgrade to the latest version without selecting the option perform upgrade even if versions are same.
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20121_update_to_latest_version_and_uncheck_the_update_same_version_option'
        self.executionHelper.testSkipCheck()
        
        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, forceDownloadImage="false")
        if result == -1: self.collectLogs(test_case)



    @mark.xim_tcxm_20123
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20123_update_to_latest_version_from_specific_and_check_update_same_version (self):
        """
        Description:    TCXM-20123       Verify the firmware upgrade for a specific version and perform upgrade with upgrade even if versions are the same option selected.
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20123_update_to_latest_version_from_specific_and_check_update_same_version'
        self.executionHelper.testSkipCheck()
        
        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, version="latest", updateTo="Specific")
        if result == -1: self.collectLogs(test_case)



    @mark.xim_tcxm_20124
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20124_update_to_latest_version_from_specific_and_uncheck_update_same_version (self):
        """
        Description:    TCXM-20124       Verify firmware upgrade to a specific firmware version and perform upgrade without upgrade even if versions are same option.
        """

        self.cfg['${TEST_NAME}'] = test_case = 'test_20124_update_to_latest_version_from_specific_and_uncheck_update_same_version'
        self.executionHelper.testSkipCheck()
        
        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac,version="latest", forceDownloadImage="false", updateTo="Specific")
        if result == -1: self.collectLogs(test_case)



    @mark.xim_tcxm_20122
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20122_update_to_specific_noncurrent_version_and_uncheck_the_update_same_version (self):
        """
        Description:    TCXM-20122       Verify the firmware upgrade for the specific firmware version and perform upgrade but the versions are not same
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20122_update_to_specific_noncurrent_version_and_uncheck_the_update_same_version'
        self.executionHelper.testSkipCheck()
        
        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, forceDownloadImage="false", version="noncurrent",updateTo="specific")
        if result == -1: self.collectLogs(test_case)



    @mark.xim_tcxm_20125
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20125_update_to_latest_version_from_D360_and_check_update_same_version(self):
        """
        Description:    TCXM-20125       Verify the firmware upgrade button is present and can be launching the firmware upgrade window from D360 page.
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20125_update_to_latest_version_from_D360_and_check_update_same_version'
        self.executionHelper.testSkipCheck()
        
        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, forceDownloadImage="false", updatefromD360Page="true")
        if result == -1: self.collectLogs(test_case)
        
        
        
    @mark.xim_tcxm_20677
    @mark.development
    @mark.p2
    @mark.testbed_1_node
    def test_20677_validating_the_operation_of_close_button_in_update_window (self):
        """
        Description:    TCXM-20677       Verify the close button operation on the firmware update window
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20677_validating_the_operation_of_close_button_in_update_window'
        self.executionHelper.testSkipCheck()
        
        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, performUpgrade="false")
        if result == -1: self.collectLogs(test_case)
        
