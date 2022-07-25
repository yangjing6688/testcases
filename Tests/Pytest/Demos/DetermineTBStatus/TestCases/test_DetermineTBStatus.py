import os
from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.XiqLibraryHelper import XiqLibraryHelper
from Tests.Pytest.SystemTest.XIQ.Wired.Resources.SuiteUdks import SuiteUdks


class DetermineTBStatusTests:

    # [Setup]  Test class Setup
    @classmethod
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()

            # Create an instance of the helper class that will read 
            # the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            #
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'

            # Create new objects to use in test. Here we will import 
            # everything from the default library
            #
            cls.defaultLibrary = DefaultLibrary()
            cls.udks   = cls.defaultLibrary.apiUdks

            cls.suiteUdks = SuiteUdks()
            cls.devCmd = cls.defaultLibrary.deviceNetworkElement.networkElementCliSend
            cls.xiq    = XiqLibrary()
            cls.xiq.login.login_user(cls.tb.config.tenant_username,
                                  cls.tb.config.tenant_password,
                                  url=cls.tb.config.test_url,
                                  IRV=True)

        except Exception:
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test class Cleanup
    @classmethod
    def teardown_class(cls):
        cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()
        cls.udks.setupTeardownUdks.Base_Test_Suite_Cleanup()

        cls.xiq.login.logout_user()
        cls.xiq.login.quit_browser()

    def test_01_testConnection_with_switches(self):
        self.executionHelper.testSkipCheck()
        self.udks.setupTeardownUdks.Base_Test_Suite_Setup()

    def test_02_testConnection_with_xiq(self):
        self.executionHelper.testSkipCheck()
