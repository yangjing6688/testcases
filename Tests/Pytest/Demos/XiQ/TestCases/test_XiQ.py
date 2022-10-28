from pytest_testconfig import config, load_yaml
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from pytest import mark
from pytest import fixture
import pytest
import os
import sys
import time
from pprint import pprint
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.XiqLibraryHelper import XiqLibraryHelper

@fixture()
def test_case_one_setup_teardown_skip_test(request):
    request.instance.executionHelper.testSkipCheck()
    yield
    # Teardown (after yield)


# To run this demo you will need to supply the following yaml files:
# A Test Bed yaml (--tc-file=TestEnvironments/Rdu/Physical/Exos/rdu_x460g2_pod3_3node.yaml)
# An XIQ Environment yaml (--tc-file=TestEnvironments/Xiq/Base/environment.yaml  
# An XIQ Waits yaml --tc-file=TestEnvironments/Xiq/Base/waits.yaml 
# An XIQ Main Topology yaml --tc-file=TestEnvironments/Xiq/Base/topology.yaml  
# An XIQ Extra Topology yaml --tc-file=TestEnvironments/Xiq/Rdu/topo-1.yaml

@mark.testbed_1_node
class xiqTests():

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
            # Create the new object for the XIQ / XIQSE Libraries
            self.xiq = XiqLibrary()
            self.xiq.login.login_user(self.tb.config.tenant_username,
                                     self.tb.config.tenant_password,
                                     url=self.tb.config.test_url,
                                     IRV=True)

            # Clear out the device information
            self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
            self.xiq.xflowscommonDevices.search_device(device_serial=self.tb.dut1.serial)
            self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
            self.udks.setupTeardownUdks.networkElementConnectionManager.connect_to_all_network_elements()
            # self.devCmd.send_cmd(self.tb.dut1_name, 'configure iqagent server ipaddress {}'.format(self.cfg['SWITCH_CONNECTION_HOST']))
            # self.devCmd.send_cmd(self.tb.dut1_name, 'configure dns-client add name-server 8.8.8.8 vr vr-mgmt')
        except Exception as e:
            self.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(self):
        # self.init_xiq_libaries_and_login(self,
        #                                  self.cfg['TENANT_USERNAME'],
        #                                  self.cfg['TENANT_PASSWORD'],
        #                                  url=self.cfg['TEST_URL'])
        self.devCmd.send_cmd(self.tb.dut1_name, 'configure dns-client delete name-server 8.8.8.8 vr vr-mgmt')
        self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
        self.xiq.xflowscommonDevices.search_device(device_serial=self.tb.dut1.serial)
        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
        self.xiq.login.logout_user(IRV=True)
        self.xiq.login.quit_browser()
        
    # """ Test Cases """
    @mark.p1
    def test_Onboard(self,test_case_one_setup_teardown_skip_test):
        # Checks for Exos switch advanced onboarding on XIQ
        self.cfg['${TEST_NAME}'] = 'test_Onboard'
        self.devCmd.send_cmd_verify_output(self.tb.dut1_name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
        res =  self.xiq.xflowscommonDevices.onboard_device(self.tb.dut1.serial, device_make=self.tb.dut1.os)
      
        if res != 1:
            pytest.fail('Could not onboard {}'.format(self.tb.dut1.serial))

        res = self.xiq.xflowscommonDevices.search_device(device_serial=self.tb.dut1.serial)
        if res != 1:
            pytest.fail('Could not locate serial {}'.format(self.tb.dut1.serial))

        connhost = self.xiq.login.get_switch_connection_host()
        if connhost == '':
            pytest.fail('Could not locate Switch Connection Host')

        self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1.serial)

        res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
        if res != 'green':
            pytest.fail('Status not equal to Green: {}').format(res)

        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
        
    @mark.skip("Select Device Type is not working")
    def test_AdvanceOnboard(self,test_case_one_setup_teardown_skip_test):
        #Checks for Exos switch advanced onboarding on XIQ
        self.cfg['${TEST_NAME}'] = 'test_Onboard'
        # self.devCmd.send_cmd_verify_output(self.tb.dut1_name, 'show process iqagent', 'Ready', max_wait=30, interval=10)

        res = self.xiq.xflowsmanageAdvanceOnboarding.advance_onboard_device(self.tb.dut1.serial, device_make=self.tb.dut1.os,
                    dev_location=self.cfg['LOCATION'], create_location=True)
        if res != 1:
            pytest.fail('Could not onboard {}'.format(self.tb.dut1.serial))

        res = self.xiq.xflowscommonDevices.search_device(device_serial=self.tb.dut1.serial)
        if res != 1:
            pytest.fail('Could not locate serial {}'.format(self.tb.dut1.serial))

        connhost = self.xiq.login.get_switch_connection_host()
        if connhost == '':
            pytest.fail('Could not locate Switch Connection Host')

        self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1.serial)

        res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
        if res != 'green':
            pytest.fail('Status not equal to Green: {}').format(res)

        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
  

