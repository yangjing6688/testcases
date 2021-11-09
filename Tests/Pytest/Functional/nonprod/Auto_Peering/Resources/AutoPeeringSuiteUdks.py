# *** Settings ***
# Documentation   Brief description of where these keywords are used.
# Resource        AllResources.robot

# *** Keywords ***
# #----------------------------------------------------------------------------------------------------------
# #   Setup/Teardown Keywords
# #----------------------------------------------------------------------------------------------------------
# Test Suite Setup
    # Base Test Suite Setup


# Test Suite Cleanup
    # Base Test Suite Cleanup
# #----------------------------------------------------------------------------------------------------------

# Test Case Setup
    # Log  Test Case Setup Placeholder
    
from ExtremeAutomation.Imports.DefaultLibrary import DefaultLibrary

class AutoPeeringSuiteUdks():
    
    def __init__(self, pytestConfigHelper):
        self.pytestConfigHelper = pytestConfigHelper
        self.defaultLibrary = DefaultLibrary()
       
    def Test_Suite_Setup(self):
        self.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Setup()
        
    def Test_Suite_Cleanup(self):
        self.defaultLibrary.apiUdks.setupTeardownUdks.Base_Test_Suite_Cleanup()