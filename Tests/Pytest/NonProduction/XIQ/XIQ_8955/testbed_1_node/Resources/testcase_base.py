import pytest
import time
import os

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.Utils import Utils
from Tests.Pytest.NonProduction.XIQ.XIQ_8955.testbed_1_node.Resources.SuiteUdks import SuiteUdks


class XIQBase:
    cfg = None
    defaultLibrary = None
    executionHelper = None
    network_manager = None
    tb = None
    utils = None
    xiq = None

    @classmethod
    def setup_class(cls):
        try:
            cls.executionHelper = PytestExecutionHelper(defaultAction='fail')
            cls.tb = PytestConfigHelper(config)
            cls.utils = Utils()
            
            cls.cfg = config
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'

            cls.localSuiteUdks = SuiteUdks()
            cls.defaultLibrary = DefaultLibrary()

            cls.network_manager = NetworkElementConnectionManager()
            cls.network_manager.connect_to_network_element_name(cls.tb.dut1.name)

            cls.xiq = XiqLibrary()
            res = cls.xiq.login.login_user(cls.cfg['tenant_username'], cls.cfg['tenant_password'],
                                           url=cls.cfg['test_url'])
            if res != 1:
                pytest.fail('Could not Login')

            cls.xiq.xflowscommonDevices.delete_device(device_serial=cls.tb.dut1.serial)
        except Exception as exc:
            cls.utils.print_info(exc)
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        try:
            cls.xiq.login.logout_user()
            cls.xiq.login.quit_browser()
            cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()
        except Exception as exc:
            cls.utils.print_info(exc)
        finally:
            time.sleep(5)
