from pytest_testconfig import config
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from pytest import mark
from Tests.Pytest.Functional.nonprod.Auto_Peering.Resources.AutoPeeringSuiteUdks import AutoPeeringSuiteUdks

class AutoPeeringBase:

    # [Setup]  Test class Setup
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
          
            # Setup the test
            cls.autoPeeringSuiteUdks = AutoPeeringSuiteUdks(cls.tb)
            cls.autoPeeringSuiteUdks.Test_Suite_Setup()
            
        except Exception as e:
            cls.executionHelper.setSetupFailure(True)
    
    @classmethod
    def teardown_class(cls):
         cls.autoPeeringSuiteUdks.Test_Suite_Cleanup()
   

