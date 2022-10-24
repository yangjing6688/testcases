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
from extauto.common.CloudDriver import CloudDriver


class xiqBase:

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
            self.utils = Utils()
            self.auto_actions = AutoActions()

            self.xiq = XiqLibrary()
            
            try:
                assert self.xiq.login.login_user(
                    username=self.cfg['tenant_username'],
                    password=self.cfg['tenant_password'],
                    url=self.cfg['test_url'],
                ) == 1

            except Exception as e:
                err_msg = f"Unable to load the XIQ libraries and login!\n{repr(e)}"
                CloudDriver().close_browser()
                print(err_msg)
                pytest.fail(err_msg)

            self.suite_udk = SuiteUdk(self)

        except Exception as err:
            self.utils.print_error(repr(err))
            self.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
