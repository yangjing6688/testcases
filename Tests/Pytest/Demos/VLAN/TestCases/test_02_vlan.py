from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark
from time import sleep

# VLAN Variables
vlan_a = "800"
vlan_b = "804"
vlan_b_name = "test"


@mark.testbed_1_node
class Vlan01Tests:

    # [Setup]  Test Case Setup
    @classmethod
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()

            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)

            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()

            # Create a shorter version for the UDKs
            cls.udks = cls.defaultLibrary.apiUdks

            # Call the setup
            cls.udks.setupTeardownUdks.Base_Test_Suite_Setup()

        except Exception:
            # Setup has failed, so set the flag
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test Case Cleanup
    @classmethod
    def teardown_class(cls):
        cls.udks.vlanUdks.Remove_VLAN_and_Verify_it_is_Removed(cls.tb.dut1_name, vlan_a)
        cls.udks.setupTeardownUdks.Base_Test_Suite_Cleanup()

    def test_02_01_verify_create_vlan(self):

        self.udks.vlanUdks.Create_VLAN_and_Verify_it_Exists(self.tb.dut1_name, vlan_a)
