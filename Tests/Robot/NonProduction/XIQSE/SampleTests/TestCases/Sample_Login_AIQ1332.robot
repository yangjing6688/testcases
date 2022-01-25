#----------------------------------------------------------------------
# Copyright (C) 2022... 2022 Extreme Networks Inc.
# This software is copyright protected and may not be reproduced in any
# form or fashion without the written consent of Extreme Networks Inc.
#----------------------------------------------------------------------
#
# Author        : Heidi S. White
# Description   : Test Suite for sanity testing of basic XIQ-SE login functionality.
#                 This is qTest TC-894 in the XIQ-SE project.

*** Settings ***
Resource        ../../SampleTests/Resources/AllResources.robot

Force Tags      testbed_0_node


*** Variables ***
${ENV}                  environment.remote.chrome.windows.xiqse1.yaml
${TOPO}                 topo.test.xiqse1.connected.yaml
${TESTBED}              SALEM/Dev/devices-salem-acceptance.yaml

${XIQSE_URL}            ${xiqse.url}
${XIQSE_USER}           ${xiqse.user}
${XIQSE_PASSWORD}       ${xiqse.password}


*** Test Cases ***
Test 1: Confirm Log In with Valid Credentials - Perform Credential Check
    [Documentation]     Confirms successful log in with valid credentials
    [Tags]              xiqse_tc_894    aiq_1332    development    sample    xiqse    login    test1

    Log Into XIQSE and Confirm Success    ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Confirm User Is Logged Into XIQSE

    Log Out of XIQSE and Confirm Success
    [Teardown]  Quit Browser and Confirm Success

Test 2: Confirm Log In with Valid Credentials - Skip Credential Check
    [Documentation]     Confirms successful log in with valid credentials
    [Tags]              xiqse_tc_894    aiq_1332    development    sample    xiqse    login    test2

    Log Into XIQSE and Skip Credential Check    ${XIQSE_USER}  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Confirm User Is Logged Into XIQSE

    Log Out of XIQSE and Confirm Success
    [Teardown]  Quit Browser and Confirm Success

Test 3: Confirm Log In with Invalid User
    [Documentation]     Confirms log in with invalid user fails
    [Tags]              xiqse_tc_894    aiq_1332    development    sample    xiqse    login    test3

    ${result}=  XIQSE Load Page and Log In  BAD_USER  ${XIQSE_PASSWORD}  url=${XIQSE_URL}
    Should Be Equal As Integers             ${result}     -1

    [Teardown]  Quit Browser and Confirm Success

Test 4: Confirm Log In with Invalid Password
    [Documentation]     Confirms log in with invalid password fails
    [Tags]              xiqse_tc_894    aiq_1332    development    sample    xiqse    login    test4

    ${result}=  XIQSE Load Page and Log In  ${XIQSE_USER}  BAD_PASSWORD  url=${XIQSE_URL}
    Should Be Equal As Integers             ${result}     -1

    [Teardown]  Quit Browser and Confirm Success

Test 5: Confirm Log In with Invalid User and Invalid Password
    [Documentation]     Confirms log in with invalid user and invalid password fails
    [Tags]              xiqse_tc_894    aiq_1332    development    sample    xiqse    login    test5

    ${result}=  XIQSE Load Page and Log In  BAD_USER  BAD_PASSWORD  url=${XIQSE_URL}
    Should Be Equal As Integers             ${result}     -1

    [Teardown]  Quit Browser and Confirm Success

Test 6: Confirm Log In with Valid Credentials after Invalid Credentials is Successful
    [Documentation]     Confirms log in with valid credentials works after failing with invalid credentials
    [Tags]              xiqse_tc_894    aiq_1332    development    sample    xiqse    login    test6

    ${invalid_result}=  XIQSE Load Page and Log In  BAD_USER  BAD_PASSWORD  url=${XIQSE_URL}
    Should Be Equal As Integers                     ${invalid_result}     -1

    ${valid_result}=  XIQSE Login User              ${XIQSE_USER}  ${XIQSE_PASSWORD}
    Should Be Equal As Integers                     ${valid_result}     1
    Confirm User Is Logged Into XIQSE

    Log Out of XIQSE and Confirm Success
    [Teardown]  Quit Browser and Confirm Success
