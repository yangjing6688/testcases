*** Settings ***
Force Tags      testbed_1_node
# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library     extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py
Library     extauto/xiq/xapi/globalsettings/XapiGlobalSettings.py
Library     extauto/xiq/xapi/devices/XapiDevices.py
Variables   Environments/${TOPO}
Variables   Environments/${ENV}
Variables   TestBeds/${TESTBED}

*** Test Cases ***
01 login_with_xapi
    [Documentation]     Check the login and logout functionality
    [Tags]      sanity      login

    login user      ${tenant_username}     ${tenant_password}   url=${test_url}  XAPI_ENABLED=true  XAPI_ONLY=true
    Quit Browser



