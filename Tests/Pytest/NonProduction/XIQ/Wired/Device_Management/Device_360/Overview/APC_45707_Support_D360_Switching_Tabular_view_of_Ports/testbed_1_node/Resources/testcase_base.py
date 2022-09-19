import pytest
import os

from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Keywords.NetworkElementKeywords.NetworkElementConnectionManager import \
    NetworkElementConnectionManager
from dataclasses import dataclass
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from extauto.common.Utils import Utils
from ..Resources.SuiteUdks import SuiteUdk
from common.AutoActions import AutoActions
from extauto.common.CloudDriver import CloudDriver
from extauto.xiq.elements.DeviceCommonElements import DeviceCommonElements


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
            self.auto_actions = AutoActions()
            self.cloud_driver = CloudDriver().cloud_driver

        except Exception as e:
            self.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(self):
        self.deactivate_xiq_libaries_and_logout(self)

    @pytest.fixture
    def setup_lldp(self, onboarded_switch):

        ports = sorted(
            self.suite_udk.get_ports_from_dut(onboarded_switch),
            key=int if onboarded_switch.cli_type.upper() == "EXOS" else (lambda x: int(x.split("/")[1]))
        )
        
        try:
            self.suite_udk.set_lldp(onboarded_switch, ports, action="disable")
            self.suite_udk.bounce_IQAgent(onboarded_switch)
            
            yield
            
        finally:
            self.suite_udk.set_lldp(onboarded_switch, ports, action="enable")
            self.suite_udk.bounce_IQAgent(onboarded_switch)

    @pytest.fixture
    def check_switch_is_onboarded(self, onboarded_switch, logger):
        """ Check that the switch is actually onboarded before starting the testcase 
        """
        devices = DeviceCommonElements().get_device_grid_rows()
        assert devices, "Did not find any onboarded devices in the XIQ"

        self.xiq.xflowscommonDevices.column_picker_select("MAC Address")            
        for row in devices:
            if any(
                [
                    onboarded_switch.mac.upper() in row.text,
                    onboarded_switch.mac.lower() in row.text
                ]
            ):
                logger.info(f"Successfully found device with mac={onboarded_switch.mac}")
                break
        else:
            pytest.fail(f"Did not find device with mac={onboarded_switch.mac}")
