from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark
from Tests.Pytest.Demos.DefaultTemplate.Resources.SuiteUdks import SuiteUdk

class DetermineTBStatusTests:

    # [Setup]  Test class Setup
    @classmethod
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()
        
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
          
            # Load up the suite
            cls.suiteUdks = SuiteUdk()

            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()

        except Exception :
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test class Cleanup
    @classmethod
    def teardown_class(cls):
        cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

    def test_01_testConnection_with_switches(self):
        self.executionHelper.testSkipCheck()

        # Call the setup
        self.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()

