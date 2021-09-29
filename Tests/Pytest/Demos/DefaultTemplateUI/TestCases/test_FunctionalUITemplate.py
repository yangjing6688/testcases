from pytest_testconfig import config, load_yaml
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary
from ExtremeAutomation.Imports.pytestConfigHelper import PytestConfigHelper
from pytest import mark
from pytest import fixture
import pytest
import os
import sys
import time
from pprint import pprint
from ExtremeAutomation.Imports.pytestExecutionHelper import PytestExecutionHelper
from ExtremeAutomation.Imports.XiqLibrary import XiqLibrary
from ExtremeAutomation.Imports.XiqLibraryHelper import XiqLibraryHelper
from ..Resources.SuiteUdks import SuiteUdk

@fixture()
def xiq_helper_test_setup_teardown(request):
    request.instance.executionHelper.testSkipCheck()
    request.instance.init_xiq_libaries_and_login(request.instance.cfg['xiq_environment']['username'],
                                                 request.instance.cfg['xiq_environment']['password'],
                                                 url=request.instance.cfg['xiq_environment']['test_url'])
    def teardown():
        request.instance.deactivate_xiq_libaries_and_logout()
        
    request.addfinalizer(teardown)


# To run this demo you will need to supply the following yaml files:
# A Test Bed yaml (--tc-file=TestEnvironments/Rdu/Physical/Exos/rdu_x460g2_pod3_3node.yaml)
# An XIQ Environment yaml (--tc-file=TestEnvironments/Xiq/Base/environment.yaml  
# An XIQ Main Topology yaml --tc-file=TestEnvironments/Xiq/Base/topology.yaml  

@mark.testbed_1_node
class xiqTests():
    
    def init_xiq_libaries_and_login(self, username, password, capture_version=False, code="default", url="default", incognito_mode="False"):
        self.xiq = XiqLibrary()
        time.sleep(5)
        res = self.xiq.init_xiq_libaries_and_login(username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode)
        if res != 1:
            pytest.fail('Could not Login')
            
    def deactivate_xiq_libaries_and_logout(self):
        self.xiq.login.logout_user()
        self.xiq.login.quit_browser()
        self.xiq = None
    
    @classmethod
    def setup_class(cls):
        try: 
            cls.executionHelper = PytestExecutionHelper()
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            cls.tb = PytestConfigHelper(config)
            cls.cfg = config
            cls.cfg['${OUTPUT DIR}'] = os.getcwd()
            cls.cfg['${TEST_NAME}'] = 'SETUP'


            # Create new objects to use in test. Here we will import everything from the default library
            cls.defaultLibrary = DefaultLibrary()
         
            # Log into the xiq
            cls.init_xiq_libaries_and_login(cls,
                                             cls.cfg['xiq_environment']['username'], 
                                             cls.cfg['xiq_environment']['password'], 
                                             url=cls.cfg['xiq_environment']['test_url'])
            
            # Call the setup
            cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
            
        except Exception as e:
            cls.executionHelper.setSetupFailure(True)
        finally:
            # Clean up the xiq libraries
            cls.deactivate_xiq_libaries_and_logout(cls)

    @classmethod
    def teardown_class(cls):
        cls.init_xiq_libaries_and_login(cls,
                                         cls.cfg['xiq_environment']['username'],
                                         cls.cfg['xiq_environment']['password'],
                                         url=cls.cfg['xiq_environment']['test_url'])
        cls.deactivate_xiq_libaries_and_logout(cls)
        cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()
        
    # """ Test Cases """
    @mark.p1
    def test_dosomething(self, xiq_helper_test_setup_teardown):
        self.executionHelper.testSkipCheck()
        print("do something")
        
   
  

