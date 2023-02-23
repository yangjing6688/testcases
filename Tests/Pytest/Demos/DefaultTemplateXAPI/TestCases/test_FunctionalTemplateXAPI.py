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
from extauto.xiq.xapi.globalsettings.XapiGlobalSettings import XapiGlobalSettings

@fixture()
# Test case setup and tear down
def test_case_one_setup_teardown_skip_test(request):
    request.instance.executionHelper.testSkipCheck()
    yield
    # Teardown (after yield)

@fixture()
# Test case setup and tear down
def test_case_one_setup_teardown_print(request):
    print("TEST STARTED")
    yield
    print("TEST END")
# To run this demo you will need to supply the following yaml files:
# A Test Bed yaml (--tc-file=TestBeds/SALEM/Demo/wired/demo_salem_1_node_exos.yaml)
# An XIQ Environment yaml (--tc-file=Environments/environment.local.chrome.yaml
# An XIQ Main Topology yaml --tc-file=Environments/topo.test.g2r1.yaml

@mark.testbed_1_node
class xiqTests():

    @classmethod
    def setup_class(cls):
        try:
            cls.executionHelper = PytestExecutionHelper()
            # Create an instance of the helper class that will read in the test bed yaml file and provide basic methods and variable access.
            # The user can also get to the test bed yaml by using the config dictionary
            config['${OUTPUT DIR}'] = os.getcwd()
            config['${TEST_NAME}'] = 'SETUP'
            cls.tb = PytestConfigHelper(config)

            # Creae the new object for the Switch / Traffic Generator Libraries
            cls.defaultLibrary = DefaultLibrary()

            # Create the new object for the XIQ / XIQSE Libraries
            cls.xiq = XiqLibrary()

            # log into the UI
            cls.xiq.login.login_user(cls.tb.config.tenant_username,
                                          cls.tb.config.tenant_password,
                                          url=cls.tb.config.test_url,
                                          IRV=True, XAPI_ENABLED=True)

        except Exception as e:
            cls.executionHelper.setSetupFailure(True)

    @classmethod
    def teardown_class(cls):
        cls.xiq.login.quit_browser()

    # """ Test Cases """
    @mark.p2
    def test_xapi_call_to_get_viq_information(self, test_case_one_setup_teardown_skip_test):
        """ This is the test case description for test two """

        # get the VIQ Info
        xapiGlobalSettings = XapiGlobalSettings()
        results = xapiGlobalSettings.get_viq_info()
        print(f"get_viq_information: {results}")




