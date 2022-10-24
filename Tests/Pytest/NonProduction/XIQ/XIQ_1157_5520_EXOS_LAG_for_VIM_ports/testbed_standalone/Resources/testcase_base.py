import os
from time import sleep

import pytest
from pytest_testconfig import config

from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from extauto.common.AutoActions import AutoActions
from extauto.xiq.elements.DevicesWebElements import DevicesWebElements
from extauto.xiq.elements.NetworkPolicyWebElements import NetworkPolicyWebElements
from extauto.xiq.elements.SwitchTemplateWebElements import SwitchTemplateWebElements
from extauto.xiq.elements.UserGroupsWebElements import UserGroupsWebElements
from extauto.xiq.flows.configure.SwitchTemplate import SwitchTemplate
from .SuiteUdks import SuiteUdk


class xiqBase:

    def init_xiq_libraries_and_login(self, username, password, capture_version=False, code="default", url="default",
                                     incognito_mode="False"):
        self.xiq = XiqLibrary()
        sleep(5)
        res = self.xiq.login.login_user(username, password, capture_version=capture_version, code=code,
                                        url=url, incognito_mode=incognito_mode, quick=True)
        if res != 1:
            pytest.fail('Could not Login')

    def deactivate_xiq_libraries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None

    @classmethod
    def setup_class(cls):
        try:
            cls.executionHelper = PytestExecutionHelper()
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'

            cls.defaultLibrary = DefaultLibrary()
            cls.switch_template = SwitchTemplate()
            cls.sw_template_web_elements = SwitchTemplateWebElements()
            cls.xeleNetworkPolicyWebElements = NetworkPolicyWebElements()
            cls.auto_actions = AutoActions()
            cls.dev_web_elem = DevicesWebElements()
            cls.user_groups = UserGroupsWebElements()
            cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend
            cls.init_xiq_libraries_and_login(cls,
                                             cls.cfg['tenant_username'],
                                             cls.cfg['tenant_password'],
                                             url=cls.cfg['test_url'])
            cls.network_manager = NetworkElementConnectionManager()
            cls.suite_udk = SuiteUdk(cls)
            cls.auto_actions = AutoActions()
        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        cls.deactivate_xiq_libraries_and_logout(cls)
