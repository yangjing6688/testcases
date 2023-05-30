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
from Tests.Pytest.SystemTest.XIQ.Wired.Resources.SuiteUdks import SuiteUdks





@mark.testbed_none
class verifyRdcInfoTests():


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
            cls.suiteUdks = SuiteUdks()
            cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend

            # Create the new object for the XIQ / XIQSE Libraries
            cls.xiq = XiqLibrary()
            cls.xiq.login.login_user(cls.tb.config.tenant_username,
                                     cls.tb.config.tenant_password,
                                     url=cls.tb.config.test_url,
                                     IRV=True)

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)


    @classmethod
    def teardown_class(cls):
        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()



    """ Test Cases """

    @mark.development
    @mark.tccs_7651
    def test_verify_data_center_name(self,test_case_skip_check,test_case_started_ended_print):
        '''[Documentation]  Test_Objective: Verify the correct data center name is displayed using "About ExtremeClod IQ'''
        data_center_name = self.xiq.login.get_data_center_name()
        if data_center_name != self.cfg['data_center_name']:
            pytest.fail(f"FAILED The Data Center Name found is {data_center_name}. "
                        f"Expected Data Center Name was {self.cfg['data_center_name']}")
        else:
            print(f"The Data Center Name found {data_center_name} matches the "
                  f"expected name {self.cfg['data_center_name']}")

    @mark.development
    @mark.tccs_7651
    def test_verify_xiq_version(self,test_case_skip_check,test_case_started_ended_print):
        '''[Documentation]  Test_Objective: Verify the correct Build Version is displayed using "About ExtremeClod IQ'''
        xiq_version = self.xiq.login.get_xiq_version()
        if xiq_version != self.cfg['build_version']:
            pytest.fail(f"FAILED The XIQ version found is {xiq_version}. "
                        f"Expected XIQ version is {self.cfg['build_version']} on RDC {self.cfg['data_center_name']}")
        else:
            print(f"The XIQ Version found {xiq_version} matches the "
                  f"expected XIQ version  {self.cfg['build_version']} on RDC {self.cfg['data_center_name']}")
