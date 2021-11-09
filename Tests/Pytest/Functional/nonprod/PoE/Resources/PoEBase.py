from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from Tests.Pytest.Functional.nonprod.PoE.Resources.PoESuiteUdks import PoESuiteUdks


class PoEBase:

    @classmethod
    def setup(cls):

        try:
            # create pytest execution helper
            cls.execution_helper = PytestExecutionHelper()

            # create test bed object from the config
            cls.test_bed = PytestConfigHelper(config)

            # load the suite
            cls.udks = PoESuiteUdks(cls.test_bed)

            # import everything from default library
            cls.defaultLibrary = DefaultLibrary()
            cls.udks_default = cls.defaultLibrary.apiUdks

            cls.udks_default.setupTeardownUdks.Base_Test_Suite_Setup()

        except Exception:
            cls.execution_helper.setSetupFailure(True)

    @classmethod
    def teardown(cls):
        cls.udks_default.setupTeardownUdks.Base_Test_Suite_Cleanup()
