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
current_directory = os.path.dirname(os.path.abspath(__file__))
print(current_directory)


@mark.testbed_1_node
class onboardDeviceVSP7400UsingCsvTests():


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
            cls.xiq.login.login_user(cls.tb.config.tenant_username,
                                     cls.tb.config.tenant_password,
                                     url=cls.tb.config.test_url,
                                     IRV=True)

            global csv_file_location
            csv_file_location = cls.suiteUdks.create_csv_file(work_dir=current_directory,
                                                              dut_serial=cls.tb.dut1_serial,
                                                              platform=cls.tb.dut1_platform)
            global csv_file_location2
            csv_file_location2 = cls.suiteUdks.create_csv_file(work_dir=current_directory,
                                                               dut_serial=cls.tb.dut1_serial,
                                                               platform=cls.tb.dut1_platform,
                                                               location=cls.tb.dut1_location2)

            cls.udks.setupTeardownUdks.networkElementConnectionManager.connect_to_all_network_elements()

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)


    @classmethod
    def teardown_class(cls):


        if needToDeleteDevice:
            cls.xiq.xflowscommonDevices.delete_device(device_serial=cls.tb.dut1_serial)
        cls.suiteUdks.delete_csv(csv_file_location)
        cls.suiteUdks.delete_csv(csv_file_location2)
        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()
        cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

    # """ Test Cases """
    @mark.development
    @mark.tccs_7651
    def test_onboard_device_using_csv_without_location(self,test_case_skip_check,test_case_started_ended_print):
        '''[Documentation]  Test_Objective: Verify a VSP7400 device can be onboared using a csv file'''
        global needToDeleteDevice

        res = self.xiq.xflowscommonDevices.quick_onboarding_cloud_csv(device_make=self.tb.dut1.os, csv_location=csv_file_location)

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

        device_location = self.suiteUdks.get_value_specific_column(self.xiq, self.tb.dut1_serial, "LOCATION")

        location_to_verify = "Assign Location"
        if device_location != location_to_verify:
            pytest.fail('Current location {} did not match the expected location {} assigned to device {} having serial {}'.format(
                    device_location, location_to_verify, self.tb.dut1_platform, self.tb.dut1_serial))
        else:
            print('Current location {} matched the expected location {} assigned to device {} having serial {}'.format(
                device_location, location_to_verify, self.tb.dut1_platform, self.tb.dut1_serial))

        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1_serial)
        needToDeleteDevice = False

    @mark.development
    @mark.tccs_7651
    def test_onboard_device_using_csv_with_location(self,test_case_skip_check,test_case_started_ended_print):
        '''[Documentation]  Test_Objective: Verify a VSP7400 device can be onboared using a csv file and selecting the location field'''
        global needToDeleteDevice

        res = self.xiq.xflowscommonDevices.quick_onboarding_cloud_csv(device_make=self.tb.dut1.os,
                                                                      location=self.tb.dut1_location1, csv_location=csv_file_location)
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

        location_to_verify = self.suiteUdks.expected_location_in_gui(self.tb.dut1_location1)

        device_location = self.suiteUdks.get_value_specific_column(self.xiq, self.tb.dut1_serial, "LOCATION")

        if location_to_verify not in device_location:
            pytest.fail('Current location {} did not match the expected location {} assigned to device {}'.format(
                device_location, location_to_verify, self.tb.dut1_serial))
        else:
            print('Current location {} matched the expected location {} assigned to device {}'.format(
                device_location, location_to_verify, self.tb.dut1_serial))

        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1_serial)
        needToDeleteDevice = False

    @mark.development
    @mark.tccs_7651
    def test_onboard_device_using_csv_with_location_in_csv(self, test_case_skip_check, test_case_started_ended_print):

        global needToDeleteDevice

        res = self.xiq.xflowscommonDevices.quick_onboarding_cloud_csv(device_make=self.tb.dut1.os,
                                                                      csv_location=csv_file_location2)
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

        location_to_verify = self.suiteUdks.expected_location_in_gui(self.tb.dut1_location2)

        device_location = self.suiteUdks.get_value_specific_column(self.xiq, self.tb.dut1_serial, "LOCATION")

        if location_to_verify not in device_location:
            pytest.fail('Current location {} did not match the expected location {} assigned to device {}'.format(
                device_location, location_to_verify, self.tb.dut1_serial))
        else:
            print('Current location {} matched the expected location {} assigned to device {}'.format(
                device_location, location_to_verify, self.tb.dut1_serial))

        self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1_serial)
        needToDeleteDevice = False
