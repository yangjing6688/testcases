from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark

@mark.testbed_1_node # Marked all test cases as 1 node
class DefaultTests:
    
    # [Setup]  Test class Setup
    @classmethod
    def setup_class(cls):
        try:
            # Create the pytest execution helper
            cls.executionHelper = PytestExecutionHelper()
        
        except Exception :
            cls.executionHelper.setSetupFailure(True)


    # Test Cases:
    # The test case name must be test_[number]_action format. If pytest is going to treat this as a test case the prefix must be test_.
    # Any other utility classes can be written in the ../Resources
    # The marks are defined in the pytest.ini file at the root of this project.
    #
    @mark.p1  # Marked as a P1 test case
    def test_01_do_something(self):
        """ This is the test case description for test one """
        self.executionHelper.testSkipCheck()
        print("test_01_dosomething")

    @mark.p2  # Marked as a P2 test case
    def test_02_do_something_else(self):
        """ This is the test case description for test two """
        self.executionHelper.testSkipCheck()
        print("test_02_do_something_else")
        
    @mark.p3  # Marked as a P3 test case
    def test_03_do_extra(self):
        """ This is the test case description for test three """
        self.executionHelper.testSkipCheck()
