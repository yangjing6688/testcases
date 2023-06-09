*** Settings ***
Library      String
Library     common/Mu.py
Library     common/Cli.py
Library     common/Utils.py
Library     common/TestFlow.py

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     xiq/flows/manage/Devices.py
Library     xiq/flows/common/GlobalSearch.py
Library     xiq/flows/configure/CommonObjects.py
Library     xiq/flows/configure/NetworkPolicy.py
Library     xiq/flows/configure/ExpressNetworkPolicies.py
Library     xiq/flows/manage/Location.py
Library     xiq/flows/common/Navigator.py
Library     ExtremeAutomation/Imports/CommonObjectUtils.py
Library     ExtremeAutomation/Keywords/UserDefinedKeywords/NetworkElements/SetupTeardown/SetupTeardownUdks.py

Variables    TestBeds/${TESTBED}
Variables    Environments/${TOPO}
Variables    Environments/${ENV}
Variables    Environments/Config/device_commands.yaml
Variables    Environments/Config/waits.yaml