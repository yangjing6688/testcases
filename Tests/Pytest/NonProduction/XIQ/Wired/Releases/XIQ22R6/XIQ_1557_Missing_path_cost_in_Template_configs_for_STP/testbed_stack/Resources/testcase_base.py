import pytest
import os

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.AutoActions import AutoActions
from extauto.common.Utils import Utils
from ..Resources.SuiteUdks import SuiteUdk
from extauto.xiq.elements.SwitchTemplateWebElements import SwitchTemplateWebElements
from extauto.xiq.flows.configure.SwitchTemplate import SwitchTemplate


class xiqBase:

    def init_xiq_libraries_and_login(self, username, password, capture_version=False, code="default", url="default",
                                     incognito_mode="False"):
        self.xiq = XiqLibrary()
        try:
            res = self.xiq.login.login_user(username, password, capture_version=capture_version, url=url,
                                            incognito_mode=incognito_mode)
            assert res == 1
        except Exception as e:
            err_msg = f"Unable to load the XIQ libraries and login!\n{repr(e)}"
            print(err_msg)
            pytest.fail(err_msg)

    def deactivate_xiq_libaries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()

    @classmethod
    def setup_class(self):
        try:
            self.executionHelper = PytestExecutionHelper()
            self.tb = PytestConfigHelper(config)
            self.cfg = config
            self.cfg['${OUTPUT DIR}'] = os.getcwd()
            self.cfg['${TEST_NAME}'] = 'SETUP'
            self.cfg['${MAX_CONFIG_PUSH_TIME}'] = 300

            self.defaultLibrary = DefaultLibrary()
            self.udks = self.defaultLibrary.apiUdks
            self.devCmd = self.defaultLibrary.deviceNetworkElement.networkElementCliSend
            self.network_manager = NetworkElementConnectionManager()
            self.init_xiq_libraries_and_login(self,
                                              self.cfg['tenant_username'],
                                              self.cfg['tenant_password'],
                                              url=self.cfg['test_url'])
            self.suite_udk = SuiteUdk(self)
            self.utils = Utils()
            self.auto_actions = AutoActions()
            self.switch_tmpl = SwitchTemplate()
            self.switch_template_web_elements = SwitchTemplateWebElements()

        except Exception as e:
            self.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(self):
        self.deactivate_xiq_libaries_and_logout(self)
