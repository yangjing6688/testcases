*** Settings ***
Resource        ../Resources/AllResources.robot
Suite Setup     Test Suite Setup
Suite Teardown  Test Suite Cleanup
Force Tags      testbed_1_node

# The keywords in Login.py have been moved to the keywords directory.
# If the moved keyword is not working correctly import the original library and remove the keywords/gui/login/KeywordsLogin.py version.
#Library    extauto/xiq/flows/common/Login.py
Library     keywords/gui/login/KeywordsLogin.py

*** Test Cases ***
01 do_something
    [Documentation]     Check the login and logout functionality
    [Tags]      sanity      login
    ${result1}=      Login User      ${tenant_username}     ${tenant_password}   url=${test_url}
    Should Be Equal As Strings      '${result1}'     '1'
    ${result2}=      Logout User
    Should Be Equal As Strings      '${result2}'     '1'
    Quit Browser

02 expect_to_fail
    [Documentation]     Check the login and logout functionality
    [Tags]      sanity      login

    Login User      bob     bob   url=${test_url}  IRV=true  expect_error=true
    Quit Browser

