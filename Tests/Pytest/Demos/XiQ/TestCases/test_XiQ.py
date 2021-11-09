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
def xiq_helper_test_setup_teardown(request):
    request.instance.executionHelper.testSkipCheck()
    request.instance.init_xiq_libaries_and_login(request.instance.cfg['TENANT_USERNAME'], 
                                                 request.instance.cfg['TENANT_PASSWORD'], 
                                                 url=request.instance.cfg['TEST_URL'])
    def teardown():
        request.instance.deactivate_xiq_libaries_and_logout()
        
    request.addfinalizer(teardown)


# To run this demo you will need to supply the following yaml files:
# A Test Bed yaml (--tc-file=TestEnvironments/Rdu/Physical/Exos/rdu_x460g2_pod3_3node.yaml)
# An XIQ Environment yaml (--tc-file=TestEnvironments/Xiq/Base/environment.yaml  
# An XIQ Waits yaml --tc-file=TestEnvironments/Xiq/Base/waits.yaml 
# An XIQ Main Topology yaml --tc-file=TestEnvironments/Xiq/Base/topology.yaml  
# An XIQ Extra Topology yaml --tc-file=TestEnvironments/Xiq/Rdu/topo-1.yaml

@mark.testbed_1_node
class xiqTests():
    
    def init_xiq_libaries_and_login(self, username, password, capture_version=False, code="default", url="default", incognito_mode="False"):
        self.xiq = XiqLibrary()
        time.sleep(5)
        res = self.xiq.init_xiq_libaries_and_login(username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
        if res != 1:
            pytest.fail('Could not Login')
            
    def deactivate_xiq_libaries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None
    
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
            # self.devCmd.send_cmd(self.tb.dut1_name, 'configure iqagent server ipaddress {}'.format(self.cfg['SWITCH_CONNECTION_HOST']))
            # self.devCmd.send_cmd(self.tb.dut1_name, 'configure dns-client add name-server 8.8.8.8 vr vr-mgmt')
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
        
        self.devCmd.send_cmd(self.tb.dut1_name, 'configure dns-client delete name-server 8.8.8.8 vr vr-mgmt')
        self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
        self.xiq.xflowscommonDevices.search_device_serial(self.tb.dut1.serial)
        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
        self.deactivate_xiq_libaries_and_logout(self)
        
    # """ Test Cases """
    @mark.p1
    def test_Onboard(self, xiq_helper_test_setup_teardown): 
        # Checks for Exos switch advanced onboarding on XIQ
        self.cfg['${TEST_NAME}'] = 'test_Onboard'
        self.devCmd.send_cmd_verify_output(self.tb.dut1_name, 'show process iqagent', 'Ready', max_wait=30, interval=10)
        res =  self.xiq.xflowscommonDevices.onboard_device(self.tb.dut1.serial, device_make=self.tb.dut1.os)
      
        if res != 1:
            pytest.fail('Could not onboard {}'.format(self.tb.dut1.serial))

        res = self.xiq.xflowscommonDevices.search_device_serial(self.tb.dut1.serial)
        if res != 1:
            pytest.fail('Could not locate serial {}'.format(self.tb.dut1.serial))

        connhost = self.xiq.xflowsmanageSwitch.capture_xiq_switch_connection_host()
        if connhost == '':
            pytest.fail('Could not locate Switch Connection Host')

        self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1.serial)

        res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
        if res != 'green':
            pytest.fail('Status not equal to Green: {}').format(res)

        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
        
    @mark.skip("Select Device Type is not working")
    def test_AdvanceOnboard(self, xiq_helper_test_setup_teardown):
        #Checks for Exos switch advanced onboarding on XIQ
        self.cfg['${TEST_NAME}'] = 'test_Onboard'
        # self.devCmd.send_cmd_verify_output(self.tb.dut1_name, 'show process iqagent', 'Ready', max_wait=30, interval=10)

        res = self.xiq.xflowsmanageAdvanceOnboarding.advance_onboard_device(self.tb.dut1.serial, device_make=self.tb.dut1.os,
                    dev_location=self.cfg['LOCATION'], create_location=True)
        if res != 1:
            pytest.fail('Could not onboard {}'.format(self.tb.dut1.serial))

        res = self.xiq.xflowscommonDevices.search_device_serial(self.tb.dut1.serial)
        if res != 1:
            pytest.fail('Could not locate serial {}'.format(self.tb.dut1.serial))

        connhost = self.xiq.xflowsmanageSwitch.capture_xiq_switch_connection_host()
        if connhost == '':
            pytest.fail('Could not locate Switch Connection Host')

        self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1.serial)

        res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1.serial)
        if res != 'green':
            pytest.fail('Status not equal to Green: {}').format(res)

        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)
  

