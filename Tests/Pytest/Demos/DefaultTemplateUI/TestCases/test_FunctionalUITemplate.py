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
    request.instance.init_xiq_libaries_and_login(request.instance.cfg['tenant_username'],
                                                 request.instance.cfg['tenant_password'],
                                                 url=request.instance.cfg['test_url'])
    def teardown():
        request.instance.deactivate_xiq_libaries_and_logout()
        
    request.addfinalizer(teardown)


# To run this demo you will need to supply the following yaml files:
# A Test Bed yaml (--tc-file=TestBeds/SALEM/Demo/demo_salem_1_node_exos.yaml)
# An XIQ Environment yaml (--tc-file=Environments/environment.local.chrome.yaml
# An XIQ Main Topology yaml --tc-file=Environments/topo.test.g2r1.yaml

@mark.testbed_1_node
class xiqTests():
    
    def init_xiq_libaries_and_login(self, username, password, capture_version=False, code="default", url="default", incognito_mode="False", **kwargs):
        self.xiq = XiqLibrary()
        time.sleep(5)
        self.xiq.init_xiq_libaries_and_login(username, password, capture_version=capture_version, code=code, url=url, incognito_mode=incognito_mode, **kwargs)
            
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

            # Call the setup
            cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
            
        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        cls.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()
        
    # """ Test Cases """
    @mark.p1
    def test_dosomething(self, xiq_helper_test_setup_teardown):
        """ This is the test case description for test one """
        self.executionHelper.testSkipCheck()
        print("do something")
        
    @mark.p1
    def test_expect_login_fail(self):
        """ This is the test case description for test two """
        # IRV = Internal Results Verification
        self.init_xiq_libaries_and_login("bob", "bob", url=self.tb.config['test_url'], IRV=True, expect_error=True)
        self.xiq.login.quit_browser()
        
   
  

