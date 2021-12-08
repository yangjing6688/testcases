from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark
from Tests.Pytest.Functional.nonprod.MACsec.Resources.MACsecSuiteUdks import MACsecSuiteUdks

@mark.required_capability('MacsecXflow','MacsecOrHalfDuplex','MacsecEpdm')
class MACsecBase:

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
            cls.suiteUdks = MACsecSuiteUdks(cls.tb)

            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()
          
            #Setup the test
            cls.suiteUdks.Test_Suite_Setup()
            
        except Exception as e:
            cls.executionHelper.setSetupFailure(True)
    
    @classmethod
    def teardown_class(cls):
        cls.suiteUdks.Cleanup_DUT(cls.tb.dut1)
        cls.suiteUdks.Cleanup_DUT(cls.tb.dut2)
   

