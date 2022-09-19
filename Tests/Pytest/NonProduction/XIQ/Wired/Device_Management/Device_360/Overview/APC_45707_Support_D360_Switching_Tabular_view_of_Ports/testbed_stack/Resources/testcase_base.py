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
from ..Resources.SuiteUdks import SuiteUdk


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
        time.sleep(5)
        res = self.xiq.login.login_user(username, password, capture_version=capture_version, code=code,
                                        url=url, incognito_mode=incognito_mode)
        if res != 1:
            pytest.fail('Could not Login')

    def deactivate_xiq_libraries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None

    @classmethod
    def setup_class(self):
        try: 
            self.executionHelper = PytestExecutionHelper()
            self.tb = PytestConfigHelper(config)
            self.cfg = config
            self.cfg['${OUTPUT DIR}'] = os.getcwd()
            self.cfg['${TEST_NAME}'] = 'SETUP'

            self.defaultLibrary = DefaultLibrary()
            self.udks = self.defaultLibrary.apiUdks
            self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend
            self.network_manager = NetworkElementConnectionManager()
            self.init_xiq_libraries_and_login(self,
                                              self.cfg['tenant_username'],
                                              self.cfg['tenant_password'],
                                              url=self.cfg['test_url'])

            self.xiq.xflowsmanageDevices.refresh_devices_page()
            time.sleep(10)
            self.xiq.xflowscommonDevices.column_picker_select("Template",
                                                              "Managed By",
                                                              "MAC Address",
                                                              "Cloud Config Groups",
                                                              "Model",
                                                              "Uptime",
                                                              "Connected Clients",
                                                              "Location",
                                                              "Feature License",
                                                              "Device License",
                                                              "MGT VLAN",
                                                              "Stack Unit",
                                                              "IQAgent",
                                                              "Managed",
                                                              "Stack Role",
                                                              "Serial #",
                                                              "Network Policy",
                                                              "Host Name"
                                                              )  
            self.suite_udk = SuiteUdk(self.cfg, self.xiq, self.devCmd)

        except Exception as e:
            self.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(self):
        self.deactivate_xiq_libraries_and_logout(self)
