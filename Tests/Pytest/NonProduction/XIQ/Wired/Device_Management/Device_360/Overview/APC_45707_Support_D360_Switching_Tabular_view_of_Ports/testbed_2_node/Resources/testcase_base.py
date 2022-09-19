import pytest
import time
import os

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from dataclasses import dataclass
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.Utils import Utils
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from extauto.common.AutoActions import AutoActions
from extauto.xiq.elements.ClientWebElements import ClientWebElements
from extauto.xiq.elements.Device360WebElements import Device360WebElements
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

            if self.tb.node_count < 2:
               pytest.skip(
                   "****This testcase doesn't run on single node testbed, it needs at least two nodes for execution. "
                   "Hence skipping test****")

            self.defaultLibrary = DefaultLibrary()
            self.udks = self.defaultLibrary.apiUdks
            self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend
            self.network_manager = NetworkElementConnectionManager()
            self.init_xiq_libraries_and_login(self,
                                             self.cfg['tenant_username'], 
                                             self.cfg['tenant_password'], 
                                             url=self.cfg['test_url'])
            self.auto_actions = AutoActions()
            self.client_web_elements = ClientWebElements()
            self.device_360_web_elements = Device360WebElements()
            self.suite_udk = SuiteUdk(self)
            
        except Exception as e:
            self.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(self):
        self.deactivate_xiq_libraries_and_logout(self)
