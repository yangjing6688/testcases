from pytest_testconfig import config, load_yaml
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from pytest import mark
from pytest import fixture
import pytest
import os
import re
import sys
import time
from pprint import pprint
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.XiqLibraryHelper import XiqLibraryHelper


@fixture()
def xiq_helper_test_setup_teardown(request):
    request.instance.executionHelper.testSkipCheck()
    request.instance.init_xiq_libaries_and_login(request.instance.cfg['TENANT_USERNAME'], 
                                                 request.instance.cfg['TENANT_PASSWORD'], 
                                                 url=request.instance.cfg['TEST_URL'])
    def teardown():
        request.instance.deactivate_xiq_libaries_and_logout()
        
    request.addfinalizer(teardown)


@mark.testbed_1_node
class xiqTests():

    # A method to get data from a specific column
    def check_specific_column(self, serial, str):
        value_of_column = ''
        while value_of_column == '':
            time.sleep(5)
            self.xiq.xflowsmanageDevices.refresh_devices_page()
            value_of_column = self.xiq.xflowsmanageDevices.get_device_details(serial,str)
            print('{} column did not update yet, will refresh the page then try again'.format(str))
        print('current {} is : {}'.format(str,value_of_column))
        return value_of_column
    
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

    # A method to check versions of code to determine if the release is >,<,= than the version running on the device
    def compare_version(cls, version_to_compare, base_version):

        base_version = base_version.split(".")
        version_to_compare = version_to_compare.split(".")

        if len(base_version) != len(version_to_compare):
            pytest.fail('compareVersion failed. The length of version to compare is not equal to base version')

        for i, value in enumerate(base_version):
            if int(value) > int(version_to_compare[i]):
                return 1
            elif int(value) < int(version_to_compare[i]):
                return -1
        return 0


    # A method to remove unused software versions on the DUT.
    def remove_unused_versions_of_software(self):
        output = self.devCmd.send_cmd(self.tb.dut1_name, 'show software')
        send_cmd_output = output[0].cmd_obj.return_text
        regex = "[A-Za-z0-9]+[.][0-9]+[.][0-9]+[.][0-9]+[.][A-Za-z0-9]+"
        software_release_list = []
        for line in send_cmd_output.split('\n'):
            line = line.replace("\r", "")
            if re.match(regex, line):
                software_release_list.append(line)
        print("This is a list of software releases {0}".format(software_release_list))
        for software_version in software_release_list:
            if ("Primary" in software_version) or ("Backup" in software_version):
                print("Did not remove '{0}' since it is either the primary of backup release".format(software_version))
            else:
                print("software to remove {0}".format(software_version))
                self.devCmd.send_cmd(self.tb.dut1_name, 'software remove ' + software_version)

    # A method to change the software on the DUT via CLI commands.
    # This is needed for times where XIQ can not change the software on the device
    def downgrade_to_base_software(self, release_name):
        self.devCmd.send_cmd(self.tb.dut1_name, 'enable')
        self.devCmd.send_cmd(self.tb.dut1_name, 'software activate ' + release_name)
        time.sleep(15)
        self.devCmd.send_cmd(self.tb.dut1_name, 'show software')
        self.defaultLibrary.apiLowLevelApis.resetDeviceUtils.reboot_network_element_now_and_wait(self.tb.dut1_name,max_wait=300)
        self.defaultLibrary.apiLowLevelApis.resetDeviceUtils.login_after_reset(self.tb.dut1_name, "rwa", "rwa")
        self.devCmd.send_cmd(self.tb.dut1_name, 'enable')
        self.devCmd.send_cmd(self.tb.dut1_name, 'show software')
        self.devCmd.send_cmd(self.tb.dut1_name, 'software commit')

    # A method to commit the software on the device after performing a device upgrade via XIQ
    # This is needed because XIQ does not do this action
    def software_commit_after_upgrading_via_xiq(self):
        self.devCmd.send_cmd(self.tb.dut1_name, 'enable')
        self.devCmd.send_cmd(self.tb.dut1_name, 'show software')
        self.devCmd.send_cmd(self.tb.dut1_name, 'software commit')
 

    # A method to reinstall the the IQAGENT to the version in the software package
    def iqagent_reinstall(self):
        self.devCmd.send_cmd(self.tb.dut1_name, 'enable')
        self.devCmd.send_cmd(self.tb.dut1_name, 'configure terminal')
        self.devCmd.send_cmd(self.tb.dut1_name, 'application')
        self.devCmd.send_cmd(self.tb.dut1_name, 'no iqagent enable')
        self.devCmd.send_cmd(self.tb.dut1_name, 'dbg enable')
        self.devCmd.send_cmd(self.tb.dut1_name, 'software iqagent reinstall')
        self.devCmd.send_cmd(self.tb.dut1_name, 'iqagent enable')
        time.sleep(30)
        self.devCmd.send_cmd(self.tb.dut1_name, 'exit')


    @classmethod
    def setup_class(self):
        try: 
            self.executionHelper = PytestExecutionHelper()
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            self.tb = PytestConfigHelper(config)
            self.cfg = config
            self.cfg['${OUTPUT DIR}'] = os.getcwd()
            self.cfg['${TEST_NAME}'] = 'SETUP'


            # Create new objects to use in test. Here we will import everything from the default library
            self.defaultLibrary = DefaultLibrary()
            self.udks = self.defaultLibrary.apiUdks
            self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend
            self.init_xiq_libaries_and_login(self,
                                             self.cfg['TENANT_USERNAME'], 
                                             self.cfg['TENANT_PASSWORD'], 
                                             url=self.cfg['TEST_URL'])

            # Clear out the device information
            self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
            self.xiq.xflowscommonDevices.search_device_serial(self.tb.dut1.serial)
            self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
            self.udks.setupTeardownUdks.networkElementConnectionManager.connect_to_all_network_elements()

        except Exception as e:
            self.executionHelper.setSetupFailure(True)
        finally:
            # Clean up the xiq libraries
            self.deactivate_xiq_libaries_and_logout(self)

    @classmethod
    def teardown_class(self):
        self.init_xiq_libaries_and_login(self,
                                         self.cfg['TENANT_USERNAME'],
                                         self.cfg['TENANT_PASSWORD'],
                                         url=self.cfg['TEST_URL'])

        self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
        self.xiq.xflowscommonDevices.search_device_serial(self.tb.dut1.serial)
        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
        self.deactivate_xiq_libaries_and_logout(self)
        
    # Starting OS: 8.2.6.0.GA Agent:0.4.0
    #          OS: 8.2.7.0 SoftwareUpgradeType: Global Starting_Agent:0.4.0 EndingAgent:0.4.0
    #          OS: 8.2.8.0 SoftwareUpgradeType: Global Starting Agent:0.4.0 EndingAgent:0.4.0
    #          OS: 8.3.0.0 SoftwareUpgradeType: Non_Global Starting Agent:0.4.0 EndingAgent:0.4.13
    #          OS: 8.3.1.0 SoftwareUpgradeType: Global Starting Agent:0.4.0 EndingAgent:0.4.13
    #	       OS: 8.4.0.0 SoftwareUpgradeType: Global Starting Agent:0.4.0 EndingAgent:0.4.13 

    # Starting OS: 8.2.7.0.GA Agent:0.4.0
    #          OS: 8.2.8.0 SoftwareUpgradeType: Global Starting Agent:0.4.0 EndingAgent:0.4.0
    #          OS: 8.3.0.0 SoftwareUpgradeType: Non_Global Starting Agent:0.4.0 EndingAgent:0.4.13
    #          OS: 8.3.1.0 SoftwareUpgradeType: Global Starting Agent:0.4.0 EndingAgent:0.4.13
    #          OS: 8.4.0.0 SoftwareUpgradeType: Global Starting Agent:0.4.0 EndingAgent:0.4.13 

    # Starting OS: 8.2.8.0.GA Agent:0.4.0
    #          OS: 8.3.0.0 SoftwareUpgradeType: Non_Global Starting Agent:0.4.0 EndingAgent:0.4.13
    #          OS: 8.3.1.0 SoftwareUpgradeType: Global Starting Agent:0.4.0 EndingAgent:0.4.13
    #          OS: 8.4.0.0 SoftwareUpgradeType: Global Starting Agent:0.4.0 EndingAgent:0.4.13 

    # Starting OS: 8.3.0.0.GA Agent:0.4.13
    #          OS: 8.3.1.0 SoftwareUpgradeType: Global Starting Agent:0.4.13 EndingAgent:0.4.13
    #          OS: 8.4.0.0 SoftwareUpgradeType: Global Starting Agent:0.4.13 EndingAgent:0.4.13 

    # Starting OS: 8.3.1.0.GA Agent:0.4.13
    #          OS: 8.4.0.0 SoftwareUpgradeType: Global Starting Agent:0.4.13 EndingAgent:0.4.13 


    # """ Test Cases """
    @mark.p1
    def test_upgrade_and_check_os_and_IQAgent_8270(self, xiq_helper_test_setup_teardown):

        # Assumption is the current OSversion on switch is 8.2.6.0 and IQAgent 0.4.0
        # Each iteration over the OS_list will cover an upgrade from current OS to OS_list[1] which
        # is 8.2.7.0 and a downgrade back to 8.2.6.0 then the cycle continues
        # iterating over OS_list and so on
        agentUpdated = False
        startingOS = '8.3.0.0'
        startingOSSoftwareUpgradeType = 'Non_Global'
        startingAgent = '0.4.13'
        Software = [{'OS': '8.3.1.0', 'SoftwareUpgradeType': 'Global', 'Agent': '0.4.13'},
                    {'OS': '8.4.0.0', 'SoftwareUpgradeType': 'Global', 'Agent': '0.4.13'},
                    {'OS': '8.4.1.0', 'SoftwareUpgradeType': 'Non_Global', 'Agent': '0.4.13'}]

        OS_list = [i["OS"] for i in Software]
        SoftwareUpgradeType_list = [i["SoftwareUpgradeType"] for i in Software]
        Agent_list = [i["Agent"] for i in Software]

        for i in range(len(OS_list)):
            if self.tb.dut1_platform == '1400' and OS_list[i] == '8.4.0.0':
                print('This release {} is not support on this platform {}'.format(OS_list[i],self.tb.dut1_platform))
            else:
                self.cfg['${TEST_NAME}'] = 'test_Onboard'

                # Verify the state of the XIQ agent is up/ready on the device
                if self.tb.dut1.os == "exos":
                    self.devCmd.send_cmd_verify_output(self.tb.dut1_name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
                elif self.tb.dut1.os == "voss":
                    self.devCmd.send_cmd_verify_output(self.tb.dut1_name, 'show application iqagent', ' True', max_wait=30, interval=10)

                time.sleep(10)
                self.remove_unused_versions_of_software()

                # Onboard the device. If the device can not be onboarded fail and print which device did not onboard
                res = self.xiq.xflowscommonDevices.onboard_device(self.tb.dut1.serial, device_make=self.tb.dut1.os)
                if res != 1:
                    pytest.fail('Could not onboard {}'.format(self.tb.dut1.serial))

                time.sleep(30)
                self.xiq.xflowsmanageDevices.refresh_devices_page()
                time.sleep(10)
                res = self.xiq.xflowscommonDevices.search_device_serial(self.tb.dut1.serial)
                if res != 1:
                    pytest.fail('Could not locate serial {}'.format(self.tb.dut1.serial))

                # Wait until the device is online and check to make the state is 'green'
                self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1.serial)

                res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)

                if res != 'green':
                    pytest.fail('Status not equal to Green: {}'.format(res))

                # Check the current OS on the device and make sure it is the exepected version
                self.xiq.xflowsmanageDevices.column_picker_select('OS Version', 'IQAgent', 'Managed')

                OS_current = self.check_specific_column(self.tb.dut1.serial, str='OS VERSION')

                if OS_current != startingOS:
                    pytest.fail('Current OS used is {} . Expected starting OS to be {}'.format(OS_current, startingOS))
                else:
                    print("Current OS is {} matches expected starting OS {}".format(OS_current, startingOS))

                # Check the current IQAGENT  on the device and make sure it is the exepected version
                iqAgentOnSwitch = self.xiq.xflowsmanageDevices.get_device_details(self.tb.dut1.serial, 'IQAGENT')

                if iqAgentOnSwitch != startingAgent:
                    pytest.fail('Current IQAgent is {} . Expected  starting Agent to be {}'.format(iqAgentOnSwitch, startingAgent))
                else:
                    print("Current IQAgent is {} matches expected starting IQAgent {}".format(iqAgentOnSwitch, startingAgent))


                IQAgent_update = 0

                # If Current OS is lower than 8.3.0.0 or 8.3.1.0, IQ agent will update 0.4.0 to 0.4.10 and need rechecking
                if self.compare_version(startingAgent, Agent_list[i]) >= 1:
                    agentUpdated = True


                # Depending on the platform type the archive format and extension changes.
                # For 5520/5420 .voss, the rest uses .tgz
                # Voss devices require VOSS before platform type
                OS = self.tb.dut1.os
                OS = OS.upper()
                platform = self.tb.dut1_platform
                archive_name = ''

                if platform == '1400' or platform == '4900' or platform == '7400':
                    archive_name += OS
                    archive_name += platform
                    archive_name += '.'
                    archive_name += OS_list[i]
                    if SoftwareUpgradeType_list[i] == 'Global':
                        archive_name += '.tgz (GLOBAL)'
                    else:
                        archive_name += '.tgz'
                else:
                    archive_name += platform
                    archive_name += '.'
                    archive_name += OS_list[i]
                    if SoftwareUpgradeType_list[i] == 'Global':
                        archive_name += '.voss (GLOBAL)'
                    else:
                        archive_name += '.voss'

                print('Archive used for upgrade will be {}:'.format(archive_name))
                upgrade = self.xiq.xflowsmanageDevices.select_version_and_upgrade_device_to_specific_version(self.tb.dut1.serial, archive_name)
                if upgrade != 1:
                    pytest.fail('Upgrade to version {} failed'.format(OS_list[i]))

                # Verify the device goes offline, which will happen during the reboot on the device
                self.xiq.xflowscommonDevices.wait_until_device_offline(self.tb.dut1.serial, retry_duration=5, retry_count=60)

                # Wait until the deive is online and check to make the state is 'green'
                self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1.serial, retry_duration=5, retry_count=60)

                res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
                if res != 'green':
                    pytest.fail('Status not equal to Green: {}'.format(res))

                # Check the current OS on the device and make sure it is the exepected version
                OS_current = self.check_specific_column(self.tb.dut1.serial, str='OS VERSION')

                if OS_current != OS_list[i]:
                    pytest.fail('Current OS used is {} . Expected OS was {}'.format(OS_current, OS_list[i]))
                else:
                    print("Current OS is {} matches expected OS {} after upgrading software".format(OS_current, OS_list[i]))


                # If the agent is going to be updated verify it is updated to the correct version
                if agentUpdated:
                    print('IqAgent requires upgrade. This will be done automatically by the cloud')
                    if(self.tb.dut1_platform == "1400"):
                        time.sleep(40)
                    else:
                        time.sleep(20)
                    self.xiq.xflowsmanageDevices.refresh_devices_page()


                iqAgentOnSwitch = self.xiq.xflowsmanageDevices.get_device_details(self.tb.dut1.serial,'IQAGENT')


                if iqAgentOnSwitch != Agent_list[i] and agentUpdated:
                    pytest.fail('IqAgent version found not equal to {}, instead version {} was present. Update of IQagent failed'.format(Agent_list[i], iqAgentOnSwitch))
                elif iqAgentOnSwitch != Agent_list[i] and agentUpdated == False:
                    pytest.fail('IqAgent version found not equal to {}, instead version {} was present'.format(Agent_list[i], iqAgentOnSwitch))
                else:
                    print("Verified that Iqagent version is {} as expected".format(iqAgentOnSwitch))

                self.software_commit_after_upgrading_via_xiq()

                # The following code is going to reset device to the starting OS and IQAGENT
                print('***Starting downgrade section***')


                if agentUpdated:
                    print('Using CLI to downgrade')
                    self.downgrade_to_base_software(startingOS + ".GA")
                    print('IqAgent requires downgrade. This will require user entering debug mode and enter the commands manually')
                    self.iqagent_reinstall()
                    if(self.tb.dut1_platform == "1400"):
                        print('Allow more time for the device to connect to the cloud')
                        time.sleep(60)
                    self.xiq.xflowsmanageDevices.refresh_devices_page()
                    self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1.serial)
                    self.xiq.xflowsmanageDevices.refresh_devices_page()
                else:
                    print('Using Cloud to downgrade')
                    OS = self.tb.dut1.os
                    OS = OS.upper()
                    platform = self.tb.dut1_platform
                    archive_name = ''

                    if platform == '1400' or platform == '4900' or platform == '7400':
                        archive_name += OS
                        archive_name += platform
                        archive_name += '.'
                        archive_name += startingOS
                        if SoftwareUpgradeType_list[i] == 'Global' and startingOSSoftwareUpgradeType == 'Global':
                            archive_name += '.tgz (GLOBAL)'
                        else:
                            archive_name += '.tgz'
                    else:
                        archive_name += platform
                        archive_name += '.'
                        archive_name += startingOS
                        if SoftwareUpgradeType_list[i] == 'Global' and startingOSSoftwareUpgradeType == 'Global':
                            archive_name += '.voss (GLOBAL)'
                        else:
                            archive_name += '.voss'

                    print('Archive used for downgrade will be {}:'.format(archive_name))
                    downgrade = self.xiq.xflowsmanageDevices.select_version_and_upgrade_device_to_specific_version(self.tb.dut1.serial,archive_name)
                    if downgrade != 1:
                        pytest.fail('Downgrade to version {} failed'.format(startingOS))

                    self.xiq.xflowscommonDevices.wait_until_device_offline(self.tb.dut1.serial)
                    time.sleep(30)
                    self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1.serial)
                    self.software_commit_after_upgrading_via_xiq()
                    self.xiq.xflowsmanageDevices.refresh_devices_page()

                res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
                if res != 'green':
                    pytest.fail('Status not equal to Green: {}'.format(res))

                OS_current = self.check_specific_column(self.tb.dut1.serial, str='OS VERSION')

                if OS_current != startingOS:
                    pytest.fail('Current OS used is {} . Expected OS was {}'.format(OS_current, startingOS))

                iqAgentOnSwitch = self.xiq.xflowsmanageDevices.get_device_details(self.tb.dut1.serial,'IQAGENT')
                if iqAgentOnSwitch != startingAgent and agentUpdated == False:
                    pytest.fail('IqAgent version found not equal to {}, instead version {} was present.'.format(startingAgent, iqAgentOnSwitch))
                if iqAgentOnSwitch != startingAgent and agentUpdated:
                    pytest.fail('IqAgent version found not equal to {}, instead version {} was present. Downgrade of IqAgent failed'.format(startingAgent,
                                                                                                               iqAgentOnSwitch))
                print("Verified that Iqagent version was downgraded to {} as expected ".format(iqAgentOnSwitch))

                # Delete device from the cloud
                self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
        


