from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark
from ..Resources.SuiteUdks import SuiteUdk

################################################
# Run all tests:
#    pytest --tc-file=<path to test bed yaml>
# Run all P1:
#    pytest -m p1 --tc-file=<path to test bed yaml>
# Run all P1 and P2:
#    pytest -m "p1 or p2" --tc-file=<path to test bed yaml>
#
# Note: There are extra options in the pytest.ini file that will be appended.
#
# The test should produce a report.html file when the run is completed
#

# Mark the class with the test bed configuration that you have chosen:
#
# @mark.testbed_1_node
# @mark.testbed_2_node
# @mark.testbed_3_node
# @mark.testbed_4_node
# @mark.testbed_5_node
#

@mark.testbed_1_node # Marked all test cases as 1 node
class DefaultTests:
    
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
            cls.mySess = cls.defaultLibrary.deviceNetworkElement.networkElementConnectionManager

            # Call the setup
            cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
        except Exception :
            cls.executionHelper.setSetupFailure(True)

    # [Teardown]  Test class Cleanup
    @classmethod
    def teardown_class(cls):
        cls.suiteUdks.doExtraStuff()
        cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()

    # Test Cases:
    # The test case name must be test_[number]_action format. If pytest is going to treat this as a test case the prefix must be test_.
    # Any other utility classes can be written in the ../Resources
    # The marks are defined in the pytest.ini file at the root of this project.
    #
    @mark.p1  # Marked as a P1 test case
    def test_01_do_something(self):
        self.executionHelper.testSkipCheck()
        print("test_01_dosomething")
    @mark.p2  # Marked as a P2 test case
    def test_02_do_something_else(self):
        self.executionHelper.testSkipCheck()
        print("test_02_do_something_else")
        
    @mark.p3  # Marked as a P3 test case
    def test_03_do_extra(self):
        self.executionHelper.testSkipCheck()
        self.suiteUdks.doExtraStuff()
