# Author        : Gomathi Janarththanam / Natarajan Periannan
# Description   : APC-34320 Extreme Firmware upgrade /
#                 Verify the firmware upgrade function to the latest version when upgrade even if versions are same option is selected.
# Test Cases    : TCXM-20112,TCXM-20113,TCXM-20114,TCXM-20115,TCXM-20116,TCXM-20117,TCXM-20676
# Total # Cases : 7
# Pre-Requests  : 1. First organization should be created in the XIQ prior to start this test script
#                 2. If the setup is using VR-Default then default vlan port should be used as a mgmt connection
# Comments      : This test is applicable for EXOS Standalone , Stack and VOSS device.
#                 Known EXOS tftp issue EXOS BUG - EXOS-27245 - download url fails over longhaul connection, but rarely


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
def random_word(x=12):
    randword = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(x))
    return randword


# Global Vars
device_serial_list = []
location = "Chennai_" + random_word()
building = "Templesteps_" + random_word()
floor = "Fourth_"
DUT_LOCATION = ""

nw_policy = "SWITCH_POLICY_"+random_word(4)

sw_template_name = "SWITCH_TEMPLATE_"+random_word(4)

defaultColumns=["Template","Host Name","Network Policy","Managed By","Cloud Config Groups","MGMT IP Address","Model","IQAgent","Uptime","Connected Clients", \
                "Location","Feature License","Device License","WiFi0 Channel","WiFi0 Power","WiFi1 Channel","WiFi1 Power", \
                "WiFi2 Channel","WiFi2 Power","MGT VLAN","NTP State"]
columnsToBeSelected =["Template","Host Name","Network Policy","Device Status","MAC Address","Serial #","Managed","Updated On","OS Version","Stack Unit","Stack Role"]


@mark.testbed_1_node  # Marked all test cases as 1 node
class xiqTests():

    # [Setup] Test class setup
    @classmethod
    def setup_class(cls):

        """
        This class is used to login to XIQ and onboard the NOS device from the supplied testbed.yaml file

        """

        try:
            # Create pytest execution helper
            cls.executionHelper = PytestExecutionHelper(defaultAction='fail')

            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config

            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'

            # Getting the list of Stack nodes serial numbers from the testbed file
            global device_serial_list, ip, dutName, sw_model, model_units, floor, dutMac, defaultColumns, columnsToBeSelected
            if cls.tb.dut1_platform.lower() == 'stack':
                 device_serial_list = cls.tb.dut1.serial.split(",")
            else:
                device_serial_list = ["f{cls.tb.dut1.serial}"]

            dutMac = cls.tb.dut1.mac
            dutName = cls.tb.dut1_name
            iqagentServer = cls.cfg['sw_connection_host']
            ip = cls.tb.dut1.ip
            floor = "Fourth_" + str(dutMac)  # Mac address is appended in floor
            DUT_LOCATION = location + "," + building + "," + floor

            if (cls.tb.dut1_platform.lower() == 'stack'):
                model_list = []
                for i in range(1, len(device_serial_list) + 1):
                    var = 'cls.tb.dut1.stack.slot' + str(i) + '.model'
                    model_act = eval(var)
                    if "SwitchEngine" in model_act:
                        mat = re.match('(.*)(Engine)(.*)', model_act)
                        model_md = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_','-')
                        switch_type=re.match('(\d+).*',mat.group(3).split('_')[0]).group(1)
                        sw_model = 'Switch Engine '+switch_type+'-Series-Stack'
                    else:
                        model_act=model_act.replace('10_G4','10G4')
                        m = re.match(r'(X\d+)(G2)(.*)', model_act)
                        model_md = m.group(1) + '-' + m.group(2) + m.group(3).replace('_','-')
                        sw_model = m.group(1) + '-' + m.group(2) + '-Series-Stack'
                    model_list.append(model_md)
                model_units = ','.join(model_list)
            elif "Engine" in cls.tb.dut1.model:
                mat = re.match('(.*)(Engine)(.*)', cls.tb.dut1.model)
                sw_model = mat.group(1) + ' ' + mat.group(2) + ' ' + mat.group(3).replace('_','-')
            elif "G2" in cls.tb.dut1.model:
                model_act = cls.tb.dut1.model.replace('10_G4', '10G4')
                m = re.match(r'(X\d+)(G2)(.*)', model_act)
                sw_model = m.group(1) + '-' + m.group(2) + m.group(3).replace('_','-')
            else:
                sw_model = cls.tb.dut1.model.replace('_','-')

            # Suite setup, just login to the xiq client and connect all the netelements
            def suite_setup(cls):
                # Create new objects to use in test. Here we will import everything from the default library
                cls.defaultLibrary = DefaultLibrary()
                cls.udks = cls.defaultLibrary.apiUdks
                cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend
                cls.xiq = XiqLibrary()
                cls.xiq.login.login_user(cls.tb.config.tenant_username,
                                         cls.tb.config.tenant_password,
                                         url=cls.tb.config.test_url,
                                         IRV=True,quick=True)
                # Make connections to all the netlement(s) in testbed.yaml file
                cls.udks.setupTeardownUdks.networkElementConnectionManager.connect_to_all_network_elements()

            def testbed_cleanup(cls):
                # cleanup iqagent for EXOS
                if cls.tb.dut1_make.upper() == "EXOS":
                    # An existing iqagent configs will be removed from device prior to configuring the iqagent
                    cls.devCmd.send_cmd(dutName, 'disable iqagent', max_wait=10, interval=2, confirmation_phrases='Do you want to continue?', confirmation_args='y')
                    cls.devCmd.send_cmd(dutName, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dutName, 'configure iqagent server vr none', max_wait=10, interval=2)
                    # Verify the state of the XIQ agent is up/ready on the dut1(netelement-1)
                    cls.devCmd.send_cmd_verify_output(dutName, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                # iqagent cleanup for VOSS
                elif cls.tb.dut1_make.upper() == "VOSS":
                    cls.devCmd.send_cmd(dutName, 'configure terminal', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dutName, 'application', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dutName, 'no iqagent enable', max_wait=10, interval=2)

            # To get the virtual router info
            def get_virtual_router(cls, mgmtip):
                global vrName, slot, port,dut_vlan_name
                if cls.tb.dut1_make.upper() == "EXOS":
                    cmd = 'show vlan | grep ' + ip
                    output = cls.devCmd.send_cmd(dutName, cmd, max_wait=10, interval=2)
                    output_text = output[0].cmd_obj.return_text
                    out_txt = output_text.strip()
                    out_lst = out_txt.split()
                    dut_vlan_name = out_lst[0]
                    vrName = out_lst[8]
                    if vrName == "VR-Default":
                        cmd = 'show vlan ' + dut_vlan_name
                        output = cls.devCmd.send_cmd(dutName, cmd, max_wait=10, interval=2)
                        output_text = output[0].cmd_obj.return_text
                        out_lst = output_text.split('\r\n')
                        out_str = ''.join(out_lst)
                        if (cls.tb.dut1_platform.lower() == 'stack'):
                            slot = re.match(r'.*Untag:\s+\*(\d):(\d+)', out_str).group(1)
                            port = re.match(r'.*Untag:\s+\*(\d):(\d+)', out_str).group(2)
                        else:
                            port = re.match(r'.*Untag:\s+\*(\d)', out_str).group(1)
                else:
                    vrName = 'None'

            # Preparing the mapo add the device into the proper location building and floor
            def create_location(cls):
                total_devices = cls.xiq.xflowscommonDevices.get_total_device_count()
                if total_devices > 0:
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
            def onboard_devices(cls):
                # Onboarding the exos/voss and exos stack device from testbed.yaml file defined as dut1 using serial number(s)
                result = cls.xiq.xflowscommonDevices.onboard_device_quick(cls.tb.dut1)
                if result != 1:
                    pytest.fail("Onboard is not successful for all the devices.")
                time.sleep(5)

            def configure_iqagent(cls):
                if cls.tb.dut1_make.upper() == "EXOS":
                    # To get the vrName updated correctly for the given mgmt ipaddress
                    get_virtual_router(cls, cls.tb.dut1.ip)
                    # Configuring and enabling iqagent on netlement-1 based on the environment passed to the test script
                    cls.devCmd.send_cmd(dutName, 'configure iqagent server ipaddress ' + iqagentServer, max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dutName, f'configure iqagent server vr {vrName}', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dutName, 'enable iqagent', max_wait=10, interval=2)
                    # Verify the iqagent status is connected within the time intervel of 300 seconds
                    cls.devCmd.send_cmd_verify_output_regex(dutName, 'show iqagent', 'Status*.*CONNECTED TO XIQ', max_wait=300, interval=10)
                elif cls.tb.dut1_make.upper() == "VOSS":
                    cls.devCmd.send_cmd(dutName, 'iqagent server ' + iqagentServer, max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dutName, 'iqagent enable', max_wait=10, interval=2)
                    cls.devCmd.send_cmd_verify_output(dutName, 'show application iqagent', 'true', max_wait=30, interval=10)
                    cls.devCmd.send_cmd(dutName, 'exit', max_wait=10, interval=2)
                    cls.devCmd.send_cmd(dutName, 'exit', max_wait=10, interval=2)
                else:
                    pytest.fail('Device make \'{}\' is not supportted!'.format(cls.tb.dut1_make))
                time.sleep(10)

            # Check for the stack onboarded is proper and and all the nodes are connected and managed
            def check_device_status_connected(cls):
                # Waiting for 60 seconds, device to communicate XIQ and establise connection
                time.sleep(60)
                # Refreshing the XIQ device page before checking the stack status
                cls.xiq.xflowsmanageDevices.refresh_devices_page()
                time.sleep(2)
                # Unselect the columns that are not required for this test case.
                cls.xiq.xflowscommonDevices.column_picker_unselect(defaultColumns)
                time.sleep(2)
                # select the required coloumns from the device table if it is not selected.
                cls.xiq.xflowscommonDevices.column_picker_select(columnsToBeSelected)
                # Refreshing the XIQ device page before checking the stack status
                cls.xiq.xflowsmanageDevices.refresh_devices_page()
                time.sleep(10)

                # This is specific to the EXOS stack setup onboard validation
                if (cls.tb.dut1_platform.lower() == 'stack'):
                    # Step-1: # Wait until the stack icon turn to 'blue' it is in 'red'
                    result = cls.xiq.xflowscommonDevices.get_stack_status(device_mac=dutMac, ignore_failure=True)
                    max_wait = 300
                    time_elapsed = 0
                    while (result == "red" or result == -1) and max_wait >= 0:
                        print(f"\nINFO \tTime elaspsed in waiting for the stack formation is {time_elapsed} seconds \n")
                        time.sleep(10)
                        max_wait -= 10
                        time_elapsed += 10
                        result = cls.xiq.xflowscommonDevices.get_stack_status(device_mac=dutMac, ignore_failure=True)
                        # Once the max_wait time is elapsed the it will be declared as not onboared successfully
                        if (result == "red" or result == -1) and max_wait == 0:
                            print("\nFAILED \t Stack not formed properly, please check.\n")
                            pytest.fail(
                                'Expected stack icon colour is blue but found {}, stack not formed properly'.format(
                                    result))

                    # Step-2: # Ensure all the stack members are in managed state under the stack master by checking each slot managed status
                    time.sleep(10)
                    result = cls.xiq.xflowscommonDevices.verify_stack_devices_managed(dutMac, device_serial_list)
                    if result != 1:
                        pytest.fail('Not all the slots are in managed state from the list of serials {}'.format(
                            device_serial_list))

                # This code specific to EXOS/VOSS Standalone devices
                else:
                    # Check the device status is online and green based on the mac address to proceed the testcase execution
                    result = cls.xiq.xflowscommonDevices.get_device_status(device_mac=dutMac)
                    if result != 'green':
                        print("\nFAILED \t Device is not in online or not connected to XIQ...\n")
                        pytest.fail('Status not equal to Green: {}'.format(result))

                print(f"\nINFO \t Successfully onboarded the '{cls.tb.dut1_platform}' device make '{cls.tb.dut1_make}'.\n")
                time.sleep(2)

            # Create and Deploy the policy to the respected device.
            def create_and_deploy_policy(cls):
                # create a policy with name SWITCH_POLICY
                res = cls.xiq.xflowsconfigureNetworkPolicy.create_switching_routing_network_policy(nw_policy)
                if res != 1:
                    pytest.fail(f"No policy was created'{nw_policy}'")
                print(f"Network Policy '{nw_policy}' was created successfully")

                # Deploy policy for stack devices.
                if (cls.tb.dut1_platform.lower() == 'stack'):
                    # create switch template with name as SWITCH_TEMPLATE in SWITCH_POLICY for stack device for each slot device model.
                    res = cls.xiq.xflowsconfigureSwitchTemplate.add_5520_sw_stack_template(model_units, nw_policy, sw_model,sw_template_name)
                    if res != 1:
                        pytest.fail(f"No Switch Template '{sw_template_name}' was created in the policy '{nw_policy}'")
                    print(f"Switch Template '{sw_template_name}' was created in the policy '{nw_policy}' successfully")

                    # Deploy SWITCH_POLICY to the DUT1  stack device.
                    res = cls.xiq.xflowsconfigureNetworkPolicy.deploy_stack_network_policy(cls.tb.dut1.mac, nw_policy, sw_template_name)
                    if res == -1:
                        pytest.fail(f"Deploy switch policy '{nw_policy}' was failed")
                    print(f"Switch Policy '{nw_policy}' was deployed successfully on the device")

                #deploy policy for standalone devices.
                else:
                    # create switch template with name as SWITCH_TEMPLATE in SWITCH_POLICY for standalone device with respected device model.
                    res = cls.xiq.xflowsconfigureSwitchTemplate.add_sw_template(nw_policy, sw_model, sw_template_name)
                    if res != 1:
                        pytest.fail(f"No Switch Template '{sw_template_name}' was created in the policy '{nw_policy}'")
                    print(f"Switch Template '{sw_template_name}' was created in the policy '{nw_policy}' successfully")

                    # Deploy SWITCH_POLICY to the DUT1 standalone device.
                    res = cls.xiq.xflowsconfigureNetworkPolicy.deploy_stack_network_policy(cls.tb.dut1.mac, nw_policy, None)
                    if res == -1:
                        pytest.fail(f"Deploy switch policy '{nw_policy}' was failed")
                    print(f"Switch Policy '{nw_policy}' was deployed successfully on the device")

                # Load the Manage --> Devices page to verify Device update status.
                cls.xiq.xflowsmanageLocation.auto_actions.click(cls.xiq.xflowsmanageLocation.ml_insights_plan_web_elements.get_manage_left_pane_click())
                cls.xiq.xflowsmanageLocation.auto_actions.click(cls.xiq.xflowsmanageLocation.ml_insights_plan_web_elements.get_manage_devices_click())

                # Checking for the update column to refect the configuration update status
                result = cls.xiq.xflowscommonDevices.get_device_updated_status(device_mac=cls.tb.dut1.mac)
                count = 0
                max_wait = 100
                while ("Configuration Updating" not in result and result == "" ):
                    time.sleep(10)
                    count += 10
                    result = cls.xiq.xflowscommonDevices.get_device_updated_status(device_mac=cls.tb.dut1.mac)
                    print(
                        f"\nINFO \t Time elapsed in the update column to reflect the configuration updating is '{count} seconds'\n")
                    if ("Device Update Failed" in result) or (count > max_wait):
                        pytest.fail(
                            "Device Update Failed for the device with mac {} while performing deploy policy".format(
                                cls.tb.dut1.mac))

                ##Checking for the device configuration update status every 10 seconds, this loop will continue as long as it is
                ##"Configuration Updating". Incase of "Update Failed" it will comeout and calls the tear down.
                count = 0
                res = cls.xiq.xflowscommonDevices.get_device_updated_status(device_mac=cls.tb.dut1.mac)
                while "Configuration Updating" in res or re.search(r'\d+-\d+-\d+', res):
                    time.sleep(10)
                    count += 10
                    res = cls.xiq.xflowscommonDevices.get_device_updated_status(device_mac=cls.tb.dut1.mac)
                    print(f"\nINFO \t Time elapsed in the configuration update is '{count}' seconds\n")
                    if (re.search(r'(\d+-\d+-\d+)', res)):
                        print('Device Update Passed for the device with mac {}'.format(cls.tb.dut1.mac))
                        break
                    elif ("Device Update Failed" in res) or (count > 1500):
                        pytest.fail(
                            'Device Update Failed for the device with mac {} while performing policy update'.format(
                                cls.tb.dut1.mac))
                        break

            # The following functions are used to onboard the Testing device in XIQ and check the Status of the device is managed.
            suite_setup(cls)
            get_virtual_router(cls, cls.tb.dut1.ip)
            testbed_cleanup(cls)
            create_location(cls)
            onboard_devices(cls)
            configure_iqagent(cls)
            check_device_status_connected(cls)
            create_and_deploy_policy(cls)

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    # [Tear Down] Setup Class Cleanup
    @classmethod
    def teardown_class(cls):

        """ This function used to cleanup the setup when the test is completed or the encounter any issues during the execution """

        print("\nINFO \t ++++++++++++++++++++++++++++++++++++++ Setup TearDown Process Started... +++++++++++++++++++++++++++++++++++\n")

        # Unconfigure the IQAgent from the device
        if cls.tb.dut1_make.upper() == "EXOS":
            # Unconfigure the IQAgent from the device
            cls.devCmd.send_cmd(dutName, 'configure iqagent server ipaddress none', max_wait=10, interval=2)
            cls.devCmd.send_cmd(dutName, 'configure iqagent server vr none', max_wait=10, interval=2)

        elif cls.tb.dut1_make.upper() == "VOSS":
            cls.devCmd.send_cmd(dutName, 'configure terminal', max_wait=10, interval=2)
            cls.devCmd.send_cmd(dutName, 'application', max_wait=10, interval=2)
            cls.devCmd.send_cmd(dutName, 'no iqagent enable', max_wait=10, interval=2)
            cls.devCmd.send_cmd(dutName, 'exit', max_wait=10, interval=2)
            cls.devCmd.send_cmd(dutName, 'exit', max_wait=10, interval=2)

		    #wait for below sleep time for configuration get applied in device.
        time.sleep(5)

        # Reseting the column selection back to it's default value.
        cls.xiq.xflowscommonDevices.column_picker_select(defaultColumns)
        time.sleep(2)

        # Delete the dut1 switch if it is already onboarded in to the XIQ environment
        result = cls.xiq.xflowscommonDevices.delete_device(device_mac=cls.tb.dut1.mac)
        if result != 1:
            pytest.fail("Could not delete the device with mac {}".format(cls.tb.dut1.mac))

        # This is to delete the stack member node(s) which is not stacked under the stack master
        if (cls.tb.dut1_platform.lower() == 'stack'):
            for serial in device_serial_list:
                result = cls.xiq.xflowscommonDevices.delete_device(device_serial=serial)
                time.sleep(5)

        # To Delete the above mentioned location building floor from the XIQ
        cls.xiq.xflowsmanageLocation.delete_location_building_floor(location, building, floor)
        time.sleep(5)

		    #delete the above mention policy file.
        cls.xiq.xflowsconfigureNetworkPolicy.delete_network_policy(nw_policy)
        time.sleep(3)

		    #delete user created switch template from Configure ---> 'Common Objects' for stack device.
        if (cls.tb.dut1_platform.lower() == 'stack'):
            for i in range(1, len(device_serial_list) + 1):
                cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(sw_template_name + "-" + str(i))
        else:
            cls.xiq.xflowsconfigureCommonObjects.delete_switch_template(sw_template_name)

        # Logout XIQ and close the browser
        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()


    # Methods required for the test cases

    # This is used to generate the heading with box
    def boxHeading(self, content):
        """ This method is used to create a boxed label and the text will be in the center of the box """
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
    def preCheck (self,test_case, waitTimer = 60):
        """
        This method used to validate the EXOS Stack status and to clear the logs prior to start the test on EXOS
        """
        testid = test_case.split("_")[1]
        self.boxHeading(f"T.C-{testid} pre-check started...")
        time.sleep(waitTimer)
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
        self.boxHeading(f"T.C-{testid} is failed, colllecting logs...")
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

    @mark.tcxm_20112
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20112_update_to_latest_version_and_check_update_same_version_option (self):
        """
        Description:    TCXM-20112       Verify the firmware upgrade function to the latest version even if versions are the same
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20112_update_to_latest_version_and_check_update_same_version_option'
        self.executionHelper.testSkipCheck()

        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac)
        if result == -1: self.collectLogs(test_case)

    @mark.tcxm_20113
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20113_update_to_latest_version_and_uncheck_the_update_same_version_option (self):
        """
        Description:    TCXM-20113       Verify the firmware upgrade to the latest version without selecting the option perform upgrade even if versions are same.
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20113_update_to_latest_version_and_uncheck_the_update_same_version_option'
        self.executionHelper.testSkipCheck()

        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, forceDownloadImage="false")
        if result == -1: self.collectLogs(test_case)

    @mark.tcxm_20115
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20115_update_to_latest_version_from_specific_and_check_update_same_version (self):
        """
        Description:    TCXM-20115       Verify the firmware upgrade for a specific version and perform upgrade with upgrade even if versions are the same option selected.
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20115_update_to_latest_version_from_specific_and_check_update_same_version'
        self.executionHelper.testSkipCheck()

        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, version="latest", updateTo="Specific")
        if result == -1: self.collectLogs(test_case)

    @mark.tcxm_20116
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20116_update_to_latest_version_from_specific_and_uncheck_update_same_version (self):
        """
        Description:    TCXM-20116       Verify firmware upgrade to a specific firmware version and perform upgrade without upgrade even if versions are same option.
        """

        self.cfg['${TEST_NAME}'] = test_case = 'test_20116_update_to_latest_version_from_specific_and_uncheck_update_same_version'
        self.executionHelper.testSkipCheck()

        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac,version="latest", forceDownloadImage="false", updateTo="Specific")
        if result == -1: self.collectLogs(test_case)

    @mark.tcxm_20114
    @mark.development
    @mark.p1
    @mark.testbed_1_node
    def test_20114_update_to_specific_noncurrent_version_and_uncheck_the_update_same_version (self):
        """
        Description:    TCXM-20114       Verify the firmware upgrade for the specific firmware version and perform upgrade but the versions are not same
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20114_update_to_specific_noncurrent_version_and_uncheck_the_update_same_version'
        self.executionHelper.testSkipCheck()

        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, forceDownloadImage="false", version="noncurrent",updateTo="specific")
        if result == -1: self.collectLogs(test_case)

    @mark.tcxm_20117
    @mark.development
    @mark.p2
    @mark.testbed_1_node
    def test_20117_update_to_latest_version_from_D360_and_check_update_same_version(self):
        """
        Description:    TCXM-20117       Verify the firmware upgrade button is present and can be launching the firmware upgrade window from D360 page.
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20117_update_to_latest_version_from_D360_and_check_update_same_version'
        self.executionHelper.testSkipCheck()

        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, forceDownloadImage="false", updatefromD360Page="true")
        if result == -1: self.collectLogs(test_case)

    @mark.tcxm_20676
    @mark.development
    @mark.p2
    @mark.testbed_1_node
    def test_20676_validating_the_operation_of_close_button_in_update_window (self):
        """
        Description:    TCXM-20676       Verify the close button operation on the firmware update window
        """
        self.cfg['${TEST_NAME}'] = test_case = 'test_20676_validating_the_operation_of_close_button_in_update_window'
        self.executionHelper.testSkipCheck()

        self.preCheck(test_case)
        result = self.xiq.xflowscommonDevices.update_network_device_firmware(device_mac=self.tb.dut1.mac, performUpgrade="false")
        if result == -1: self.collectLogs(test_case)
