import pytest
import time
import os

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import NetworkElementConnectionManager
from dataclasses import dataclass
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.Utils import Utils
from Tests.Pytest.NonProduction.XIQ.XIQ_1365.testbed_1_node.Resources.SuiteUdks import SuiteUdk

class xiqBase:

    @pytest.fixture
    def logger(self):
        @dataclass
        class Log:
            info = lambda msg: Utils().print_info(msg)
            warning = lambda msg: Utils().print_warning(msg)
            error = lambda msg: Utils().print_error(msg)
        return Log

    def init_xiq_libraries_and_login(self, username, password, capture_version=False, code="default", url="default",
                                    incognito_mode="False"):
        self.xiq = XiqLibrary()
        time.sleep(4)
        res = self.xiq.login.login_user(
            username=username, password=password, capture_version=capture_version, code=code, url=url,
            incognito_mode=incognito_mode)

        if res != 1:
            pytest.fail('Could not Login')

    def deactivate_xiq_libraries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None

    def close_connection_with_error_handling(self):
        try:
            self.network_manager.device_collection.remove_device(self.tb.dut1.name.name)
            self.network_manager.close_connection_to_network_element(self.tb.dut1.name.name)
        except Exception as exc:
            print(exc)
        else:
            time.sleep(30)

    @classmethod
    def setup_class(self):
        try:
            self.executionHelper = PytestExecutionHelper(defaultAction='fail')
            self.tb = PytestConfigHelper(config)
            self.cfg = config
            self.cfg['${OUTPUT DIR}'] = os.getcwd()
            self.cfg['${TEST_NAME}'] = 'SETUP'

            self.defaultLibrary = DefaultLibrary()
            self.udks = self.defaultLibrary.apiUdks
            self.localsuiteudks = SuiteUdk()
            self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend
            self.network_manager = NetworkElementConnectionManager()
            self.network_manager.connect_to_network_element_name(self.tb.dut1.name)
            self.init_xiq_libraries_and_login(self,
                                             self.cfg['tenant_username'],
                                             self.cfg['tenant_password'],
                                             url=self.cfg['test_url'])

            self.xiq.xflowscommonDevices.delete_device(device_serial=self.tb.dut1.serial)


        except Exception as e:
            self.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(self):
        self.deactivate_xiq_libraries_and_logout(self)
        self.close_connection_with_error_handling(self)
        time.sleep(5)
