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
from Tests.Pytest.SystemTest.XIQ.Wired.Resources.SuiteUdks import SuiteUdks


needToDeleteDevice = False


@mark.testbed_1_node
class rebootTests():


    @classmethod
    def setup_class(cls):
        try:
            cls.executionHelper = PytestExecutionHelper()
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'

            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()
            cls.udks = cls.defaultLibrary.apiUdks
            cls.suiteUdks  = SuiteUdks()
            cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend

            # Create the new object for the XIQ / XIQSE Libraries
            cls.xiq = XiqLibrary()
            spawn_connection = cls.xiq.Cli.open_spawn(cls.tb.dut1_ip, cls.tb.dut1_port, cls.tb.dut1_username,
                                                      cls.tb.dut1_password, cls.tb.dut1_cli_type)
            cls.xiq.Cli.downgrade_iqagent(cls.tb.dut1_cli_type, spawn_connection)
            cls.xiq.Cli.close_spawn(spawn_connection)

            cls.xiq.login.login_user(cls.tb.config.tenant_username,
                                     cls.tb.config.tenant_password,
                                     url=cls.tb.config.test_url,
                                     IRV=True)



            cls.udks.setupTeardownUdks.networkElementConnectionManager.connect_to_all_network_elements()

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)


    @classmethod
    def teardown_class(cls):


        if needToDeleteDevice:
            cls.xiq.xflowscommonDevices.delete_device(device_serial=cls.tb.dut1_serial)
        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()
        cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

    #""" Test Cases """
    @mark.development
    @mark.tccs_7651
    def test_reboot(self, test_case_skip_check, test_case_started_ended_print):

        global needToDeleteDevice

        res = self.xiq.xflowscommonDevices.onboard_device_quick(self.tb.dut1)

        if res != 1:
            pytest.fail(f'Could not onboard device {self.tb.dut1_platform} with serial {self.tb.dut1_serial}')
        else:
            print(f'Device {self.tb.dut1_platform} with serial {self.tb.dut1_serial} has been onboarded')
            needToDeleteDevice = True

        self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1_serial)

        managed_res = self.xiq.xflowscommonDevices.wait_until_device_managed(self.tb.dut1_serial)

        if managed_res == 1:
            print('Status for device with serial number: {} is equal to managed'.format(self.tb.dut1_serial))
        else:
            pytest.fail('Status for serial {} not equal to managed: {}'.format(self.tb.dut1_serial, managed_res))

        res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1_serial)
        if res != 'green':
            pytest.fail('Status for serial {} not equal to Green: {}'.format(self.tb.dut1_serial, res))
        else:
            print('Status for device with serial number: {} is equal to Green'.format(self.tb.dut1_serial))

        self.xiq.xflowscommonDevices.device_reboot(device_serial=self.tb.dut1_serial)

        device_offline_result = self.xiq.xflowscommonDevices.wait_until_device_offline(self.tb.dut1_serial, retry_duration=15,
                                                               retry_count=12)

        if device_offline_result == 1:
            print('Status for device with serial number: {} is offline'.format(self.tb.dut1_serial))
        else:
            pytest.fail('Status for serial {} is not offline: {}'.format(self.tb.dut1_serial, managed_res))


        bootWaitTime = self.suiteUdks.get_boot_wait_time(self.tb.dut1_model,self.tb.dut1_cli_type)
        print("Sleeping for {} seconds to allow device to come back on line".format(bootWaitTime))
        time.sleep(bootWaitTime)
        self.xiq.xflowscommonDevices.wait_until_device_reboots(self.tb.dut1_serial, retry_duration=15, retry_count=12)
        self.xiq.xflowscommonDevices.wait_until_device_online(self.tb.dut1_serial, retry_duration=15, retry_count=12)


        self.xiq.xflowsmanageDevices.column_picker_select('Updated On')

        reboot_message = self.suiteUdks.get_value_specific_column(self.xiq, self.tb.dut1_serial, column='UPDATED')
        regex = "(\d{4})-((0[1-9])|(1[0-2]))-(0[1-9]|[12][0-9]|3[01]) ([0-2]*[0-9]\:[0-6][0-9]\:[0-6][0-9])"
        if re.match(regex, reboot_message):
            print("Device finished rebooting at: {}".format(reboot_message))
        else:
            pytest.fail('Failed to get a timestamp of last reboot. Instead got the following message: {}'.format(
                reboot_message))

        managed_res = self.xiq.xflowscommonDevices.wait_until_device_managed(self.tb.dut1_serial)

        if managed_res == 1:
            print('Status for device with serial number: {} is equal to managed'.format(self.tb.dut1_serial))
        else:
            pytest.fail('Status for serial {} not equal to managed: {}'.format(self.tb.dut1_serial, managed_res))

        res = self.xiq.xflowscommonDevices.get_device_status(device_serial=self.tb.dut1_serial)
        if res != 'green':
            pytest.fail('Status for serial {} not equal to Green: {}'.format(self.tb.dut1_serial, res))
        else:
            print('Status for device with serial number: {} is equal to Green'.format(self.tb.dut1_serial))

        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1_serial)
        needToDeleteDevice = False
